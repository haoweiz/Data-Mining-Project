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

def getDistance(alldata,cluster1,cluster2):
    minDistance = float('inf')
    for elem1 in cluster1:
        for elem2 in cluster2:
            distance = 0.0
            for index in range(2,len(alldata[0])):
                distance = distance+(alldata[elem1][index]-alldata[elem2][index])**2
            minDistance = min(minDistance,distance)
    return minDistance

def getMergeIndex(alldata,dismat,index2cluster):
    first = -1
    second = -1
    minDistance = float('inf')
    length = len(dismat)
    for i in range(0,length-1):
        for j in range(i+1,length):
            cluster1 = index2cluster[i]
            cluster2 = index2cluster[j]
            distance = getDistance(alldata,cluster1,cluster2)
            if distance < minDistance:
                first = i
                second = j
                minDistance = distance
    return first,second

def Merge(index1,index2,dismat,index2cluster,alldata):
    number = len(dismat)
    newdismat = np.zeros(shape=(number-1,number-1))
    newindex2cluster = index2cluster
    minIndex = min(index1,index2)
    maxIndex = max(index1,index2)
    for elem in index2cluster[maxIndex]:
        newindex2cluster[minIndex].add(elem)
    for i in range(maxIndex,len(index2cluster)-1):
        newindex2cluster[i] = index2cluster[i+1]
    newindex2cluster.pop()
    for i in range(0,number-2):
        for j in range(i+1,number-1):
            newdismat[i][j] = getDistance(alldata,newindex2cluster[i],newindex2cluster[j])
            newdismat[j][i] = newdismat[i][j]
    return newdismat,newindex2cluster

def init(alldata):
    datalength = len(alldata[0])
    number = len(alldata)
    dismat = np.zeros(shape=(number,number))
    index2cluster = []
    for i in range(0,number):
        for j in range(i,number):
            value = 0.0
            for index in range(2,datalength):
                value = value+(alldata[i][index]-alldata[j][index])**2
            dismat[i][j] = value
            dismat[j][i] = value
    for i in range(0,number):
        cluster = set()
        cluster.add(i)
        index2cluster.append(cluster)
    return dismat,index2cluster

def draw(index2cluster,alldata):
    attribute_len = len(alldata[0])-2
    attribute = np.zeros(shape=(0,attribute_len))
    for elem in alldata:
        attribute = np.vstack((attribute,elem[2:len(elem)]))
    pca = PCA(n_components=2)
    result = pca.fit_transform(attribute)
    ax = plt.subplot()
    array = "0123456789ABCDEF"
    index = 0
    for elem in index2cluster:
        x_list = []
        y_list = []
        for data in elem:
            x_list.append(result[data][0])
            y_list.append(result[data][1])
        color = "#"
        for i in range(0,6):
            color = color+array[randint(0,len(array)-1)]
        ax.scatter(x_list,y_list,c=color,label=index,s=20,alpha=1)
        index = index+1
    plt.legend(loc='upper left')
    plt.show()

def accuracy(alldata,classify,index2cluster):
    id2kind = dict()
    total = len(alldata)*len(alldata)
    correct = 0
    for elem in classify:
        for data in classify[elem]:
            id2kind[int(data[0])-1] = elem
    newid2kind = dict()
    for i in range(0,len(index2cluster)):
        for elem in index2cluster[i]:
            newid2kind[elem] = i
    for elem1 in range(0,len(alldata)):
        for elem2 in range(0,len(alldata)):
            if id2kind[elem1]==id2kind[elem2] and newid2kind[elem1]==newid2kind[elem2]:
                correct = correct+1
            elif id2kind[elem1]!=id2kind[elem2] and newid2kind[elem1]!=newid2kind[elem2]:
                correct = correct+1
    return float(correct)/float(total)

def Hierachial(filename):
    alldata,classify = readfile(filename)
    dismat,index2cluster = init(alldata)
    while len(dismat)>len(classify):
        first,second = getMergeIndex(alldata,dismat,index2cluster)
        dismat,index2cluster = Merge(first,second,dismat,index2cluster,alldata)
    draw(index2cluster,alldata)
    print accuracy(alldata,classify,index2cluster)

if __name__ == "__main__":
    Hierachial("cho.txt")
