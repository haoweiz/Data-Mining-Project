import java.util.ArrayList;
import java.util.StringTokenizer;

public class Parser {
	public Parser() {
		
	}
	public String code(ArrayList<Float> data,boolean wrap) {
		String result = "";
		for(int i = 0;i != data.size();++i) {
			result = result + data.get(i).toString() + "\t";
		}
		StringBuilder strBuilder = new StringBuilder(result);
		if(wrap) {
			strBuilder.setCharAt(result.length()-1,'\n');
			return strBuilder.toString();
		}
		return result.substring(0, result.length()-1);
		
	}
	public ArrayList<Float> decode(String str){
		ArrayList<Float> result = new ArrayList<Float>();
		StringTokenizer st = new StringTokenizer(str);
		while(st.hasMoreTokens()) {
			String value = st.nextToken();
			result.add(Float.valueOf(value));
		}
		return result;
	}
}
