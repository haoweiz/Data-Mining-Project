import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

public class HDFSOperator {
	private Configuration config;
	private FileSystem hdfs;
	public HDFSOperator() throws IOException {
		config = new Configuration();
		hdfs =  FileSystem.get(config);
	}
	
	public void mkdir(String path) throws IllegalArgumentException, IOException {
		hdfs.mkdirs(new Path(path));
	}
	
	public void deleteDir(String path) throws IllegalArgumentException, IOException {
		hdfs.delete(new Path(path),true);
	}
	
	public void deleteFile(String path) throws IllegalArgumentException, IOException {
		hdfs.delete(new Path(path),false);
	}

	public void move(String remoteFilePath, String remoteToFilePath) throws IOException {
		Path srcPath = new Path(remoteFilePath);
		Path dstPath = new Path(remoteToFilePath);
		hdfs.rename(srcPath, dstPath);
	}
}
