
# coding: utf-8

# In[21]:

import numpy as np
from sklearn.decomposition import PCA
import colorsys
import matplotlib.pyplot as plt


# plotting
def pca_visualise(result,dataset) :
    
    RGBcolors = []
    # Compute PCA
    pca=PCA(n_components =2)
    dim_red = pca.fit_transform(dataset)
    
    # Get the list of the clusters
    clusters = []
    for i in range(len(result)) :
        clusters = set(result)
        
    #Compute the colors
    for x in range(len(clusters)) :
        h=(x*1.0/(len(clusters)))
        s=0.6
        v=0.6
        RGBcolors.append(colorsys.hsv_to_rgb (h, s, v))
    col = zip(clusters,RGBcolors)
    
    # Scatter plot   
    for name,color in col:
        plt.scatter(
        dim_red[result==name,0],
        dim_red[result==name,1],
        label=name,
        c=color,
        )
    plt.title('K-Means MapReduce')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.show()
    
# calculating jaccard co-efficients and rand index
def validation(result,labels):
    num = len(result)
    my_mat = np.empty([num,num])
    g_truth = np.empty([num,num])
    m00 = 0
    m01 =0 
    m10=0
    m11 =0
    
    #Build the clustered matrix
    for i in range (num):
        for j in range (num):
            if(result[i] == result[j]):
                my_mat[i][j] = 1
            else:
                my_mat[i][j] = 0
                 
    #Build ground truth matrix             
    for i in range (num) :
        for j in range (num) :
            if(labels[i] == labels[j]) :
                g_truth[i][j] = 1
            else :
                 g_truth[i][j] = 0
              
    #compute jaccard coffecient
    for i in range (num) :
        for j in range (num) :
            if(my_mat[i][j] == 0 and g_truth[i][j]==0) :
                m00+=1
            elif (my_mat[i][j] == 0 and g_truth[i][j]==1):
                m01+=1
            elif (my_mat[i][j] == 1 and g_truth[i][j]==0):
                m10+=1
            else :
                m11+=1
                
    j_coff = float(m11)/(m11+m10+m01)
    randi = float(m11+m00)/(m11+m10+m01+m00)
    
    print("Jaccard-Coffecient: ",j_coff)
    print("RandIndex: ",randi)

result = []
results = []
index = 0
with open('clusters.txt') as inputfile:
    for line in inputfile:
        index_details = []
        each_line = line.strip().split('\t')
        line_data = []
        for value in each_line:
            line_data.append(value)    
        result.append(line_data)

# actual code starts here

# reading the file and loading to the dataset
with open('cho.txt') as inputfile:
    for line in inputfile:
        index_details = []
        each_line = line.strip().split('\t')
        line_data = []
        for value in each_line:
            line_data.append(value)    
        results.append(line_data)
        
# deriving groundtruth and clustering
groundtruth = [i[1] for i in results]
res = [0] * len(results)
k = 1
for list in result:
    for val in list:
        res[int(val) - 1] = k
    k = k + 1

# calling validation function to retrieve jaccard coefficient and rand index
validation(res, groundtruth)

# visualization
pca_visualise(np.asarray(res), np.asarray(results))

