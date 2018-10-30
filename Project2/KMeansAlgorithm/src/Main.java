import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map.Entry;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

public class Main {
	private static String outputFileName = "part-r-00000";
	private static String reclassifyFileName = "Reclassify.txt";
	private static int initseed[] = {3,5,9};
	private static int iteration = 10;
	public Main() throws IOException {
		
	}
	
	public static void runScript(String reclassifyFilePath) throws IOException {
		Runtime.getRuntime().exec("python Draw.py "+reclassifyFilePath);
	}
	// Generate Center File
	public static void main(String[] args) throws IllegalArgumentException, IOException, ClassNotFoundException, InterruptedException {
	      Configuration conf = new Configuration();
	      String[] otherArgs = (new GenericOptionsParser(conf, args)).getRemainingArgs();
	      if(otherArgs.length < 2) {
	          System.err.println("Usage: KMeans <in> <out>");
	          System.exit(2);
	      }
	      
	      ArrayList<String> InputPath = new ArrayList<String>();
	      for(int i = 0; i < otherArgs.length - 1; ++i) {
	          InputPath.add(otherArgs[i]);
	      }
	      Center center = new Center();
	      center.setOutputFilePath(otherArgs[otherArgs.length-1]);
	      center.setInputPath(InputPath);
	      ArrayList<Integer> centerSeeds = new ArrayList<Integer>();
	      for(int elem : initseed) {
	    	  centerSeeds.add(elem);
	      }
	      center.InitCenter(centerSeeds);
	      String outputPath = otherArgs[otherArgs.length-1];
	      HashMap<Integer,ArrayList<Float>> oldCenter = null;
	      HashMap<Integer,ArrayList<Float>> newCenter = center.getCenter(center.getCenterFilePath()+center.getFileName());

    	  String centerFileName = otherArgs[otherArgs.length-1]+"/"+outputFileName;
    	  String dstPath = ".";
	      HDFSOperator hdfsoperator = new HDFSOperator();
	      int count = 0;
	      while(count != iteration && !newCenter.equals(oldCenter)) {
	    	  oldCenter = newCenter;
	    	  hdfsoperator.move(centerFileName, dstPath);
	    	  hdfsoperator.deleteDir(otherArgs[otherArgs.length-1]);
	    	  center.setOutputFilePath(dstPath);
	    	  
		      Job job = Job.getInstance(conf, "KMeans");
		      job.setJarByClass(Main.class);
		      job.setMapperClass(KMeansMapper.class);
		      job.setReducerClass(KMeansReducer.class);
		      job.setOutputKeyClass(IntWritable.class);
		      job.setOutputValueClass(Text.class);
		      
		      for(int i = 0; i < otherArgs.length - 1; ++i) {
		          FileInputFormat.addInputPath(job, new Path(otherArgs[i]));
		      }
		      FileOutputFormat.setOutputPath(job, new Path(outputPath));
	    	  job.waitForCompletion(true);
	    	  
	    	  newCenter = center.getCenter(centerFileName);
	    	  hdfsoperator.deleteFile(dstPath+"/"+outputFileName);
	    	  count++;
	      }
	      
	      Parser parser = new Parser();
	      ArrayList<ArrayList<Float>> alldata = center.readAllkindInArrayList();
	      Path reclassifyPath = new Path(otherArgs[otherArgs.length-1]+"/"+reclassifyFileName);
	      FileSystem fs = reclassifyPath.getFileSystem(conf);
		  FSDataOutputStream outStream = fs.create(reclassifyPath);
		  for(int i = 0;i != alldata.size();++i) {
			  Iterator<Entry<Integer,ArrayList<Float>>> iter = newCenter.entrySet().iterator();
    		  float distance = Float.MAX_VALUE;
	    	  int kind = -1;
	    	  while(iter.hasNext()) {
	    		  Entry<Integer,ArrayList<Float>> entry = iter.next();
	    		  int key = entry.getKey();
	    		  ArrayList<Float> center_elem = entry.getValue();
	    		  ArrayList<Float> data_elem = alldata.get(i);
	    		  float dist = 0;
	    		  for(int t = 0;t != center_elem.size();++t) {
	    			  dist += (center_elem.get(t)-data_elem.get(t+2))*(center_elem.get(t)-data_elem.get(t+2));
	    		  }
	    		  if(dist < distance) {
	    			  distance = dist;
	    			  kind = key;
	    		  }
	    	  }
	    	  alldata.get(i).set(1, (float) kind);
	    	  String oneline = parser.code(alldata.get(i), true);
	    	  outStream.writeBytes(oneline);
		  }
	      outStream.close();
	      runScript(otherArgs[otherArgs.length-1]+"/"+reclassifyFileName);
	      System.exit(0);
	}

}
