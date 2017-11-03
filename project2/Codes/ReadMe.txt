Instructionns to run the k-means.py :
1) Place the input file which contains the dataset in the same folder as k-means.py
2) Open k-means.py code in the Syder IDE
3) In Line number 219 of the code, assign the name of the input file to the variable inputfile
             Ex : inputfile = "cho.txt"
4) In Line number 222 of the code, assign the variable "k" , its value.
             Ex: k=5
5) In Line number 231 of the code, specify the data point numbers to the variable "dp". They serve as initial centroids.
             Ex:  dp= [5,25,32,100,125]
6) In the Ipython console, on running the code , it outputs the scatter plot, jaccard cofficient and rand index.



Instructions to run hierarchical.py (Hierarchical Agglomerative clustering):
1. To run hierarchical agglomerative clustering, please include the following files in the directory where code is run:
a. cho.txt - sample dataset1 or
b. iyer.txt - sample dataset2 or
c. any new dataset files that you might want to use
d. hierarchical

2. Please specify the filename you want to use in line 110 for running this algorithm in the code

3. Please set some default k value in line 138 to get those number of centroids

4. All the outputs will be printed to the console. They are not written into any files.

5. The output will be jaccard coefficient, rand index and the correspoding graphs.

Note: This code is built on python 3.6 and might show some unexpected behavior when run on earlier versions.




Instructionns to run the DBScan.py :
1) Place the input file which contains the dataset in the same folder as k-means.py
2) Open DBScan.py code in the Syder IDE
3) In Line number 257 of the code, assign the name of the input file to the variable inputfile
             Ex : inputfile = "iyer.txt"
4) In Line number 263 of the code, assign the variable "esp" , its value.
             Ex: esp=0.5
5) In Line number 264 of the code, assignt the variable "Minpts" its value
             Ex:  Minpts = 4
6) In the Ipython console, on running the code , it outputs the scatter plot, jaccard cofficient and rand index.



Instructions to run KMeans.java and mapreduce.py (for mapreduce kmeans):

1. To run k-means mapreduce algorithm, please include the following files in the directory where code is run:
	a. cho.txt - sample dataset1
	b. iyer.txt - sample dataset2
	c. any new dataset files that you might want to use

2. Take a hadoop cluster(linux) and run the following commands to generate and run the jar file.
	a. start-hadoop.sh
	b. hadoop com.sun.tools.javac.Main KMeans.java
	c. cf kmeans.jar KMeans*.class . This creates the jar file. Please place the "centroids.txt" file with initial centroids in the same directory as the jar
	d. hadoop jar kmeans.jar KMeans <Input file location> <Output file location> <Max_No_Iterations> >log.txt
	<Input file location> will be the location where the input you want to run should be stored. in hdfs
	<Output file location> will be the location where the output will be stored in hdfs.
	<Max_No_Iterations> will be the maximum number of iterations that you want to run incase convergence delays.

3. After the desired number of iterations, once the task is done, please copy the 'clusters.txt' file into the directory where this README.txt is present.

4. Please open mapreduce.py file and specify the name of the dataset you've used for generating the clusters. Run this file

4. The output will be jaccard coefficient, rand index and the correspoding graphs.

Note: This code is built on python 3.6 and Java 6 and might show some unexpected behavior when run on earlier versions.