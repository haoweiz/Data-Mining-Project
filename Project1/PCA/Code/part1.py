import numpy as np
import matplotlib.pyplot as plt
from numpy import *
from random import randint

k = 2
data = []
label = []
file_name = "pca_a.txt"
with open(file_name) as file:
    line = file.readline()
    while line:
        oneline = line.split('\t')
        row = []
        for i in range(0,len(oneline)-1):
            row.append(float(oneline[i]))
        data.append(row)
        label.append(oneline[-1][0:-1])
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
myhashmap = dict()
for i in range(len(result)):
    if label[i] in myhashmap:
        myhashmap[label[i]].append(result[i])
    else:
        myhashmap[label[i]] = []
        myhashmap[label[i]].append(result[i])

for i in range(len(result)):
    print result[i],label[i]
ax = plt.subplot()
array = "0123456789ABCDEF"
for key in myhashmap.keys():
    value = myhashmap[key]
    x_list = []
    y_list = []
    for coordinate in value:
        x_list.append(coordinate[0])
        y_list.append(coordinate[1])
    color = "#"
    for i in range(0,6):
        color = color+array[randint(0,len(array)-1)]
    ax.scatter(x_list,y_list,c=color,label=key,s=20,alpha=0.5)
plt.legend(loc='upper right')
plt.show()

