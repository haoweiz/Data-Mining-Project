import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

public class Main {
	private static String outputFileName = "part-r-00000";
	public Main() throws IOException {
		
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
	      center.InitCenter();
	      String outputPath = otherArgs[otherArgs.length-1];
	      HashMap<Integer,ArrayList<Float>> oldCenter = null;
	      HashMap<Integer,ArrayList<Float>> newCenter = center.getCenter(center.getCenterFilePath()+center.getFileName());

    	  String centerFileName = otherArgs[otherArgs.length-1]+"/"+outputFileName;
    	  String dstPath = ".";
	      HDFSOperator hdfsoperator = new HDFSOperator();
	      while(!newCenter.equals(oldCenter)) {
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
	      }
	      System.exit(0);
	}

}
