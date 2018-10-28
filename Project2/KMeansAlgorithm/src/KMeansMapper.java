import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class KMeansMapper extends Mapper<Object,Text,IntWritable,Text>{
	private Parser parser;
	private Map<Integer,ArrayList<Float>> center;
	
	public KMeansMapper() throws IOException {
		parser = new Parser();
		Center c = new Center();
		String centerPath = c.getCenterFilePath()+c.getFileName();
		center = c.getCenter(centerPath);
	}
	
	public void map(Object key,Text value,Context context) throws IOException, InterruptedException {
		ArrayList<Float> data = parser.decode(value.toString());
		Iterator<Entry<Integer, ArrayList<Float>>> iter = center.entrySet().iterator();
		float distance = Float.MAX_VALUE;
		int kind = -1;
		while(iter.hasNext()) {
			float dist = 0;
			Entry<Integer, ArrayList<Float>> entry = (Map.Entry<Integer, ArrayList<Float>>)iter.next();
			int centerkind = (int) entry.getKey();
			ArrayList<Float> centerdata = (ArrayList<Float>) entry.getValue();
			for(int i = 2;i != data.size();++i) {
				float t = data.get(i).floatValue()-centerdata.get(i-2).floatValue();
				dist += t*t;
			}
			if(dist < distance) {
				distance = dist;
				kind = centerkind;
			}
		}
		IntWritable resKey = new IntWritable(kind);
		Text resVal = new Text(value);
		context.write(resKey,resVal);
	}
}
