import numpy as np
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
            if int(oneline[1]) not in classify:
                classify[int(oneline[1])] = []
            classify[int(oneline[1])].append(data)
            line = file.readline()
    return alldata,classify

def getCenterSeed(classify):
    center = dict()
    for item in classify:
        elem_num = len(classify[item])
        randomdata = classify[item][randint(0,elem_num-1)]
        center[item] = randomdata[2:len(randomdata)]
    return center


def reclassify(center,alldata):
    newclassify = dict()
    for data in alldata:
        minSSE = float('inf')
        label = -1
        for kind in center:
            SSE = 0
            for j in range(2,len(data)):
                SSE = SSE+(data[j]-center[kind][j-2])**2
            if SSE<minSSE:
                minSSE = SSE
                label = kind
        if label not in newclassify:
            newclassify[label] = []
        newclassify[label].append(data)
    return newclassify

def calculatecenter(newclassify):
    center = dict()
    for item in newclassify:
        means = np.mean(newclassify[item],axis=0)
        center[item] = means[2:len(means)]
    return center

def KMeans(filename):
    alldata,classify = readfile(filename)
    id2kind = dict()
    for elem in classify:
        for data in classify[elem]:
            id2kind[data[0]] = elem
    newclassify = classify
    center = getCenterSeed(classify)
    oldaccuracy = -1
    while True:
        newclassify = reclassify(center,alldata)
        center = calculatecenter(newclassify)
        newaccuracy = accuracy(id2kind,newclassify,alldata)
        if newaccuracy == oldaccuracy:
            print newaccuracy
            draw(newclassify,alldata)
            break
        oldaccuracy = newaccuracy

def draw(newclassify,alldata):
    ax = plt.subplot()
    res_len = 0
    for elem in newclassify:
        res_len = len(newclassify[elem][0])-2
        break
    attribute = np.zeros(shape=(0,res_len))
    for elem in alldata:
        attribute = np.vstack((attribute,elem[2:len(elem)]))
    pca = PCA(n_components=2)
    result = pca.fit_transform(attribute)
    ax = plt.subplot()
    array = "0123456789ABCDEF"
    for elem in newclassify:
        length = len(newclassify[elem])
        x_list = []
        y_list = []
        for data in newclassify[elem]:
            x_list.append(result[int(data[0]-1)][0])
            y_list.append(result[int(data[0]-1)][1])
        color = "#"
        for i in range(0,6):
            color = color+array[randint(0,len(array)-1)]
        ax.scatter(x_list,y_list,c=color,label=elem,s=20,alpha=1)
    plt.legend(loc='upper left')
    plt.show()

def accuracy(id2kind,newclassify,alldata):
    newid2kind = dict()
    for elem in newclassify:
        for data in newclassify[elem]:
            newid2kind[data[0]] = elem
    total = (len(newid2kind)-1)*len(newid2kind)/2
    correct = 0
    for i in range(0,len(alldata)-1):
        for j in range(i+1,len(alldata)):
            if id2kind[int(alldata[i][0])]==id2kind[int(alldata[j][0])] and newid2kind[int(alldata[i][0])]==newid2kind[int(alldata[j][0])]:
                correct += 1
            elif id2kind[int(alldata[i][0])]!=id2kind[int(alldata[j][0])] and newid2kind[int(alldata[i][0])]!=newid2kind[int(alldata[j][0])]:
                correct += 1
    return float(correct)/float(total)

if __name__ == "__main__":
    KMeans("cho.txt")
