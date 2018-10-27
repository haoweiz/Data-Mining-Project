import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map.Entry;
import java.util.Random;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

public class Center {
	private Parser parser;
	private Configuration conf;
	private String centerFilePath = null;
	private String centerFileName = "part-r-00000";
	private int IndexofKind = 1;
	private ArrayList<String> InputPath;
	private HashMap<Integer,ArrayList<ArrayList<Float>>> allkind;
	
	public Center(String output) throws IOException {
		centerFilePath = output+"/";
		allkind = new HashMap<Integer,ArrayList<ArrayList<Float>>>();
		conf = new Configuration();
		parser = new Parser();
	}
	public void setInputPath(ArrayList<String> InputPath) {
		this.InputPath = InputPath;
	}
	public String getCenterFilePath() {
		return centerFilePath;
	}
	public String getFileName() {
		return centerFileName;
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
	public void InitCenter() throws IOException {
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
		HashMap<Integer,ArrayList<Float>> seed = new HashMap<Integer,ArrayList<Float>>();
		Iterator<Entry<Integer, ArrayList<ArrayList<Float>>>> iter = allkind.entrySet().iterator();
		while(iter.hasNext()) {
			Entry<Integer, ArrayList<ArrayList<Float>>> entry = iter.next();
			Integer key = entry.getKey();
			ArrayList<ArrayList<Float>> value = entry.getValue();
			Random random = new Random();
			int index = random.nextInt(value.size());
			ArrayList<Float> data = value.get(index);
			data.remove(0);
			data.remove(0);
			seed.put(key,data);
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
		//String path = this.getCenterFilePath()+this.getFileName();
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
