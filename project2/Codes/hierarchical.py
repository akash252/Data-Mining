
# coding: utf-8

# In[111]:

import numpy as np
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
import scipy.spatial.distance as dist
from sklearn.decomposition import PCA
import colorsys
import matplotlib.pyplot as plt
import math

# distance matrix
def distanceMatrix(dataset) :
        #Calculate Distance Matrix
    samples = dataset.shape[0]
    distMat = np.empty([samples,samples])
    for i in range(samples) :
        for j in range(samples) :
                distMat[i][j] = dist.euclidean(dataset[i],dataset[j])
    return distMat

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
    plt.title('HIERARCHICAL')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.show()
    
# actual code starts here
results = []
clusterDets = []
groundtruth = []
index = 0
with open('cho.txt') as inputfile:
    for line in inputfile:
        index_details = []
        each_line = line.strip().split('\t')
        line_data = []
        groundtruth.append(each_line[1])
        for i in range(2, len(each_line)):
            line_data.append(float(each_line[i]))    
        results.append(line_data)
        index_details.append(index)
        clusterDets.append(index_details)
        index = index + 1

# distance matrix:
distMatrix = squareform(pdist(np.array(results), 'euclidean'))
# distMatrix = []
# for i in range(0, len(results)):
#     distRow = []
#     for j in range(0, len(results)):
#         dist = 0.0
#         for k in range(0, len(results[0])):
#             dist = dist + (results[i][k] - results[j][k])**2
#         dist = math.sqrt(dist)
#         distRow.append(dist)
#     distMatrix.append(distRow)
        
# distMatrix = distanceMatrix(np.asarray(results))

k = 5
result = []
total = len(distMatrix)
mapper = [False] * total
centroids = {}
total = total - k
while total > 0:
    min = float('Inf')
    first = 0
    second = 0
    for i in range (0,len(clusterDets)):
       if not mapper[i]:
           entry1 = clusterDets[i]
           for j in range(i+1,len(clusterDets)):         
               if not mapper[j]:
                   entry2 = clusterDets[j]
                   localmin = float('Inf')
                   for k in range(0, len(entry1)):
                       for l in range(0,len(entry2)):
                            if(localmin > distMatrix[entry1[k]][entry2[l]]):
                                localmin = distMatrix[entry1[k]][entry2[l]]
                   if(localmin<min):
                       first = i
                       second = j
                       min = localmin 
    clusterDets.append((clusterDets[first] + clusterDets[second]))
    mapper[first] = True
    mapper[second] = True
    mapper.append(False)
    total = total - 1
for i in range(0,len(clusterDets)):
    if not mapper[i]:
        try:
            result.append(clusterDets[i])
        except KeyError:
            pass

        
# deriving groundtruth and clustering
res = [0] * len(results)
k = 1
for list in result:
    for val in list:
        res[val] = k
    k = k + 1

# calling validation function to retrieve jaccard coefficient and rand index
validation(res, groundtruth)

# visualization
pca_visualise(np.asarray(res), np.asarray(results))

