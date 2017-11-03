import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.StringTokenizer;
import java.util.TreeMap;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class KMeans {
	static Map<Integer, String> oldResult = new HashMap<Integer, String>();
	static Map<Integer, ArrayList<Double>> centroids = new TreeMap<Integer, ArrayList<Double>>();
	static boolean flag;
	static Map<Integer, ArrayList<Integer>> clusters = new HashMap<Integer, ArrayList<Integer>>();
	public static class KMeansMapper extends Mapper<Object, Text, IntWritable, Text>{

		private int nearestCentroid(List<Double> dimensions){
			Set<Integer> centroidkeys = centroids.keySet();
			double minDist = Double.MAX_VALUE;
			int minIndex = -1;
			for(int a : centroidkeys){
				List<Double> centrDims = centroids.get(a);
				double distance = 0;
				for(int i = 2 ; i < centrDims.size(); i++){
					distance += Math.pow(centrDims.get(i) - dimensions.get(i), 2);
				}
				distance = Math.sqrt(distance);
				if(distance < minDist){
					minDist = distance;
					minIndex = a;
				}
			}
			return minIndex;
		}

		public void map(Object key, Text value, Context context
				) throws IOException, InterruptedException {
			StringTokenizer tokenizer = new StringTokenizer(value.toString());
			List<Double> dimensions = new ArrayList<Double>();
			while(tokenizer.hasMoreTokens()){
				dimensions.add(Double.parseDouble(tokenizer.nextToken()));
			}
			int centroidIndex = nearestCentroid(dimensions);
			context.write(new IntWritable(centroidIndex), value);
			
		}
	}

	public static class KMeansReducer extends Reducer<IntWritable, Text, IntWritable, Iterable<Text>> {
		int cluster = 1;
		public void reduce(IntWritable key, Iterable<Text> values,
				Context context
				) throws IOException, InterruptedException {
			Map<Integer, Double> dimensions = new TreeMap<Integer, Double>();
			int total = 0;
			for (Text value : values) {
				StringTokenizer tokenizer = new StringTokenizer(value.toString());				
				int i = 0;
				while(tokenizer.hasMoreTokens()){
					String index = tokenizer.nextToken();
					if(i == 0){
						if(clusters.containsKey(cluster)){
							List<Integer> newList = clusters.get(cluster);
							newList.add(Integer.parseInt(index));
							clusters.put(cluster, new ArrayList<Integer>(newList));
						}
						else{
							List<Integer> newList = new ArrayList<Integer>();
							newList.add(Integer.parseInt(index));
							clusters.put(cluster, new ArrayList<Integer>(newList));
						}
					}
					if(dimensions.containsKey(i)){
						dimensions.put(i, dimensions.get(i) + Double.parseDouble(index));
					}
					else{
						dimensions.put(i, Double.parseDouble(index));
					}
					i++;
				}
				total++;			
			}
			StringBuilder position = new StringBuilder();
			for(double val : dimensions.values()){
				position.append(val/total);
				position.append("\t");
			}
			String value = position.toString().trim();
			PrintWriter out = null;
			try{
				out = new PrintWriter(new BufferedWriter(new FileWriter("./centroids.txt", true)));
				out.println(value);
			}
			catch(Exception e){
				
			}
			finally{
				out.close();
			}
			cluster++;
			context.write(key, values);
		}
	}
	
	 public static void main(String[] args) throws Exception {
		 long startTime = System.currentTimeMillis();
		 int iterations = 0;
		 int maxIterations = Integer.parseInt(args[2]);
		 while(true){
			 	int k = 0;
				String filename = "./centroids.txt";
				int count = 0;
				BufferedReader br = new BufferedReader(new FileReader(filename));
				String line = null;
				int counter = 0;
				while ((line = br.readLine()) != null) {
					k++;
					for(String value : oldResult.values()){
						if(line.trim().equals(value.trim())){
							counter++;
						}
					}
					StringTokenizer tokenizer = new StringTokenizer(line);
					List<Double> dimensions = new ArrayList<Double>();
					while(tokenizer.hasMoreTokens()){
						dimensions.add(Double.parseDouble(tokenizer.nextToken()));
					}
					oldResult.put(count, line);
					centroids.put(count++, new ArrayList<Double>(dimensions));
				}
				if(counter == k || maxIterations == iterations){
					clusterSaver();
					break;
				}
				else{
					clusters.clear();
				}
				br.close();
				PrintWriter out = null;
				try{
					out = new PrintWriter(new BufferedWriter(new FileWriter("./centroids.txt", false)));
					out.print("");
				}
				finally{
					out.close();
				}
				 Configuration conf = new Configuration();
				 Job job = Job.getInstance(conf, "KMeans");
				 job.setJarByClass(KMeans.class);
				 job.setMapperClass(KMeansMapper.class);
			//		    job.setCombinerClass(KMeansReducer.class);
				 job.setReducerClass(KMeansReducer.class);
				 job.setMapOutputKeyClass(IntWritable.class);
				 job.setMapOutputValueClass(Text.class);
				 job.setOutputKeyClass(IntWritable.class);
				 job.setOutputValueClass(Iterable.class);
				 FileInputFormat.addInputPath(job, new Path(args[0]));
				 FileOutputFormat.setOutputPath(job, new Path(args[1] +"_" + String.valueOf(iterations++)));
				 System.out.println("Iteration: " +iterations);
				 job.waitForCompletion(true);
			}
		 long endTime = System.currentTimeMillis();
		 System.out.println("Time taken: " + (endTime - startTime) + "ms");
	 }

	private static void clusterSaver() {
		PrintWriter out = null;
		try{
			out = new PrintWriter(new BufferedWriter(new FileWriter("./clusters.txt", true)));
			for(int key: clusters.keySet()){
				List<Integer> list = clusters.get(key);
				StringBuilder sb = new StringBuilder();
				for(int i : list){
					sb.append(i);
					sb.append("\t");
				}
				out.println(sb.toString().trim());
			}		
		}
		catch(Exception e){
//			System.out.println("Exception");
		}
		finally{
			out.close();
		}		
	}
}
