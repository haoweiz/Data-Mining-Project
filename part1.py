import numpy as np
from numpy import *

k = 2
data = []
label = []
with open("pca_a.txt") as file:
    line = file.readline()
    while line:
        oneline = line.split('\t')
        row = []
        for i in range(0,len(oneline)-1):
            row.append(float(oneline[i]))
        data.append(row)
        label.append(oneline[-1])
        line = file.readline()
mean = np.mean(data,axis=0)
for i in range(len(data)):
    data[i] = data[i]-mean
data = np.transpose(np.array(data))
data_cov = np.cov(data)
eigenvalue,eigenvectors = np.linalg.eig(data_cov)

index_max = np.argsort(-eigenvalue)[:k]
np.sort(index_max)
neweigenvector = eigenvectors[:,index_max]
result = np.dot(data.T,neweigenvector)
for i in range(len(result)):
    print result[i],label[i]
