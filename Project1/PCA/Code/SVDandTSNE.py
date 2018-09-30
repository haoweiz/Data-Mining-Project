from numpy import *
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
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

def draw(result):
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


def SVD():
    svd = TruncatedSVD(n_components=k)
    result = svd.fit_transform(data)
    draw(result)

def tSNE():
    X_embedded = TSNE(n_components=2).fit_transform(data)
    draw(result)

if __name__ == "__main__":
    SVD()
    tSNE()
