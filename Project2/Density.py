import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from random import randint

def readfile(filename):
    classify = dict()
    alldata = []
    with open(filename) as file:
        line = file.readline()
        while line:
            oneline = line.split('\t')
            data = []
            for i in range(0,len(oneline)):
                data.append(float(oneline[i]))
            alldata.append(data)
            if int(oneline[1]) not in classify:
                classify[int(oneline[1])] = []
            classify[int(oneline[1])].append(data)
            line = file.readline()
    return alldata,classify

def regionQuery(alldata,Point,eps,visited):
    NeighborPts = set()
    for i in range(0,len(alldata)):
        distance = 0.0
        for index in range(2,len(alldata[0])):
            distance = distance+(alldata[i][index]-Point[index])**2
        if distance**0.5<=eps:
            NeighborPts.add(i)
    return NeighborPts

def expandCluster(PointIndex,NeighborPts,clusters,eps,MinPts,visited,alldata,newid2kind):
    cluster = set()
    cluster.add(PointIndex)
    flag = True
    oldNeighborPtsLen = len(NeighborPts)
    while flag==True:
        for point in NeighborPts:
            if visited[point] == True:
                continue
            visited[point] = True
            newNeighborPts = regionQuery(alldata,alldata[point],eps,visited)
            if len(newNeighborPts)>=MinPts:
                NeighborPts = newNeighborPts|NeighborPts
            if point not in newid2kind:
                cluster.add(point)
                newid2kind[point] = len(clusters)
        newNeighborPtsLen = len(NeighborPts)
        if oldNeighborPtsLen==newNeighborPtsLen:
            flag = False
        else:
            oldNeighborPtsLen = newNeighborPtsLen
    clusters.append(cluster)

def draw(alldata,clusters):
    attribute_len = len(alldata[0])-2
    attribute = np.zeros(shape=(0,attribute_len))
    for elem in alldata:
        attribute = np.vstack((attribute,elem[2:len(elem)]))
    pca = PCA(n_components=2)
    result = pca.fit_transform(attribute)
    ax = plt.subplot()
    array = "0123456789ABCDEF"
    index = 0
    for i in range(0,len(clusters)):
        x_list = []
        y_list = []
        for data in clusters[i]:
            x_list.append(result[data][0])
            y_list.append(result[data][1])
        color = "#"
        for i in range(0,6):
            color = color+array[randint(0,len(array)-1)]
        if index==0:
            ax.scatter(x_list,y_list,c=color,label="noise",s=20,alpha=1)
        else:
            ax.scatter(x_list,y_list,c=color,label=index,s=20,alpha=1)
        index = index+1
    plt.legend(loc='upper left')
    plt.show()

def accuracy(alldata,classify,newid2kind):
    id2kind = dict()
    for elem in classify:
        for data in classify[elem]:
            id2kind[int(data[0])-1] = elem
    total = len(alldata)*len(alldata)
    correct = 0
    for i in range(0,len(alldata)):
        for j in range(0,len(alldata)):
            if id2kind[i]==id2kind[j] and newid2kind[i]==newid2kind[j]:
                correct += 1
            elif id2kind[i]!=id2kind[j] and newid2kind[i]!=newid2kind[j]:
                correct += 1
    return float(correct)/float(total)

def DBSCAN(alldata,eps,MinPts,visited,newid2kind):
    noise = set()
    clusters = []
    clusters.append(noise)
    for i in range(0,len(alldata)):
        if visited[i]==True:
            continue
        visited[i] = True
        NeighborPts = regionQuery(alldata,alldata[i],eps,visited)
        if len(NeighborPts)>=MinPts:
            newid2kind[i] = len(clusters)
            expandCluster(i,NeighborPts,clusters,eps,MinPts,visited,alldata,newid2kind)
        else:
            newid2kind[i] = 0
            clusters[0].add(i)
    return clusters

def Density(filename,MinPts,eps):
    alldata,classify = readfile(filename)
    visited = [False for n in range(len(alldata))]
    newid2kind = dict()
    clusters = DBSCAN(alldata,eps,MinPts,visited,newid2kind)
    print accuracy(alldata,classify,newid2kind)
    draw(alldata,clusters)

if __name__ == "__main__":
    Density("demo.txt",3,1)
