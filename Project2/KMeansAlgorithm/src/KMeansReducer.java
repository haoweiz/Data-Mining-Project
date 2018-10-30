import java.io.IOException;
import java.util.ArrayList;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class KMeansReducer extends Reducer<IntWritable,Text,IntWritable,Text> {
	private Parser parser;
	
	public KMeansReducer() throws IOException {
		parser = new Parser();
	}
	public void reduce(IntWritable key,Iterable<Text> values, Context context) throws IOException, InterruptedException {
		ArrayList<Float> sum = new ArrayList<Float>();
		int count = 0;
		for(Text text : values) {
			ArrayList<Float> data = parser.decode(text.toString());
			if(count == 0) {
				for(int i = 2;i != data.size();++i) {
					sum.add(new Float("0.0"));
				}
			}
			for(int i = 2;i != data.size();++i) {
				float val = data.get(i)+sum.get(i-2);
				sum.set(i-2,new Float(val));
			}
			count++;
		}
		for(int i = 0;i != sum.size();++i) {
			float newVal = sum.get(i)/count;
			sum.set(i,newVal);
		}
		String newCenter = parser.code(sum,false);
		context.write(key,new Text(newCenter));
	}
}
