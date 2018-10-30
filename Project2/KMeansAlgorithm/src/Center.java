import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map.Entry;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

public class Center {
	private static String centerFilePath = "Output/";
	private static String centerFileName = "part-r-00000";
	private static HashMap<Integer,ArrayList<ArrayList<Float>>> allkind = new HashMap<Integer,ArrayList<ArrayList<Float>>>();
	
	private Parser parser;
	private Configuration conf;
	private int IndexofKind = 1;
	private ArrayList<String> InputPath;
	
	public Center() throws IOException {
		conf = new Configuration();
		parser = new Parser();
	}
	public void setInputPath(ArrayList<String> InputPath) {
		this.InputPath = InputPath;
	}
	public void setOutputFilePath(String path) {
		centerFilePath = path + "/";
	}
	public String getCenterFilePath() {
		return centerFilePath;
	}
	public String getFileName() {
		return centerFileName;
	}
	public static HashMap<Integer,ArrayList<ArrayList<Float>>> getAllKind() {
		return allkind;
	}
	public void writeFile(String dst,HashMap<Integer,ArrayList<Float>> cen) throws IOException {
		Path dstPath = new Path(dst);
		FileSystem fs = dstPath.getFileSystem(conf);
		FSDataOutputStream outStream = fs.create(dstPath);
		Iterator<Entry<Integer,ArrayList<Float>>> iter = cen.entrySet().iterator();
		while(iter.hasNext()) {
			Entry<Integer,ArrayList<Float>> entry = iter.next();
			Integer kind = entry.getKey();
			ArrayList<Float> value = entry.getValue();
			String contents = parser.code(value,true);
			contents = (kind.toString() + "\t") + contents;
			outStream.writeBytes(contents);
		}
		outStream.close();
	}
	public ArrayList<ArrayList<Float>> readAllkindInArrayList() throws IOException{
		ArrayList<ArrayList<Float>> result = new ArrayList<ArrayList<Float>>();
		ArrayList<String> allfiles = new ArrayList<String>();
		for(String path : InputPath) {
			allfiles.addAll(this.getFileList(path));
		}
		FileSystem fs = FileSystem.get(conf);
		for(String filepath : allfiles) {
			String line = null;
			Path file = new Path(filepath);
			FSDataInputStream inStream = fs.open(file);
			BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inStream));
			while((line = bufferedReader.readLine()) != null) {
				ArrayList<Float> data = parser.decode(line);
				result.add(data);
			}
		}
		return result;
	}
	public void readAllKind() throws IOException{
		ArrayList<String> allfiles = new ArrayList<String>();
		for(String path : InputPath) {
			allfiles.addAll(this.getFileList(path));
		}
		FileSystem fs = FileSystem.get(conf);
		for(String filepath : allfiles) {
			String line = null;
			Path file = new Path(filepath);
			FSDataInputStream inStream = fs.open(file);
			BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inStream));
			while((line = bufferedReader.readLine()) != null) {
				ArrayList<Float> data = parser.decode(line);
				Float keyf = data.get(IndexofKind);
				Integer key = keyf.intValue();
				if(allkind.containsKey(key)) {
					allkind.get(key).add(data);
				}
				else {
					ArrayList<ArrayList<Float>> arr = new ArrayList<ArrayList<Float>>();
					arr.add(data);
					allkind.put(key,arr);
				}
			}
		}
	}
	public void InitCenter(ArrayList<Integer> centerSeeds) throws IOException {
		this.readAllKind();
		HashMap<Integer,ArrayList<Float>> seed = new HashMap<Integer,ArrayList<Float>>();
		Iterator<Entry<Integer, ArrayList<ArrayList<Float>>>> iter = allkind.entrySet().iterator();
		int count = 1;
		while(iter.hasNext()) {
			Entry<Integer, ArrayList<ArrayList<Float>>> entry = iter.next();
			ArrayList<ArrayList<Float>> value = entry.getValue();
			for(ArrayList<Float> elem : value) {
				for(Integer s : centerSeeds) {
					if(s.intValue() == (int)Math.ceil(elem.get(0))) {
						ArrayList<Float> data = new ArrayList<Float>();
						for(int i = 2;i != elem.size();++i) {
							data.add(elem.get(i));
						}
						Integer key = new Integer(count);
						seed.put(key,data);
						count++;
					}
				}
			}
		}
		writeFile(centerFilePath+centerFileName,seed);
	}
	public ArrayList<String> getFileList(String srcpath) throws IOException{
		ArrayList<String> files = new ArrayList<String>();
		Path path = new Path(srcpath);
		FileSystem fs = path.getFileSystem(conf);
		if(fs.exists(path)) {
			for(FileStatus status : fs.listStatus(path)) {
				if(status.isFile())
					files.add(status.getPath().toString());
			}
		}
		return files;
	}
	public HashMap<Integer,ArrayList<Float>> getCenter(String path) throws IOException{
		HashMap<Integer, ArrayList<Float>> result = new HashMap<Integer,ArrayList<Float>>();
		String line = null;
		FileSystem fs = FileSystem.get(conf);
		Path file = new Path(path);
		FSDataInputStream inStream = fs.open(file);
		BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inStream));
		while((line = bufferedReader.readLine()) != null) {
			ArrayList<Float> data = parser.decode(line);
			Integer key = data.get(0).intValue();
			data.remove(0);
			result.put(key, data);
		}
		inStream.close();
		bufferedReader.close();
		return result;
	}
}
