import numpy as np
import sys
from random import randint
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

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
            if round(float(oneline[1])) not in classify:
                classify[round(float(oneline[1]))] = []
            classify[round(float(oneline[1]))].append(data)
            line = file.readline()
    return alldata,classify

def draw(classify,alldata):
    ax = plt.subplot()
    res_len = 0
    for elem in classify:
        res_len = len(classify[elem][0])-2
        break
    attribute = np.zeros(shape=(0,res_len))
    for elem in alldata:
        attribute = np.vstack((attribute,elem[2:len(elem)]))
    pca = PCA(n_components=2)
    result = pca.fit_transform(attribute)
    ax = plt.subplot()
    array = "0123456789ABCDEF"
    for elem in classify:
        length = len(classify[elem])
        x_list = []
        y_list = []
        for data in classify[elem]:
            x_list.append(result[int(data[0]-1)][0])
            y_list.append(result[int(data[0]-1)][1])
        color = "#"
        for i in range(0,6):
            color = color+array[randint(0,len(array)-1)]
        ax.scatter(x_list,y_list,c=color,label=elem,s=20,alpha=1)
    plt.legend(loc='upper left')
    plt.show()

if __name__ == "__main__":
    argv = len(sys.argv)
    if argv != 2:
        print "error"
        exit(1)
    path = sys.argv[1]
    alldata,classify = readfile(path)
    draw(classify,alldata)
