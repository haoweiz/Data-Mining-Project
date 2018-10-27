import numpy as np
from sklearn.decomposition import PCA


def readfile(filename):
    alldata = []
    with open(filename) as file:
        line = file.readline()
        while line:
            oneline = line.split('\t')
            data = []
            for i in range(2,len(oneline)):
                data.append(float(oneline[i]))
            alldata.append(data)
            line = file.readline()
    return alldata


pca = PCA(n_components=2)
data = readfile("cho.txt")
result = pca.fit_transform(data)


def swap(mylist):
    mylist[0] = 1

mylist = [0,0,0,0,0]
swap(mylist)
print mylist
