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

def getCenterSeed(classify,alldata,centerSeedId):
    center = dict()
    if len(centerSeedId)!=0:
        for i in range(0,len(centerSeedId)):
            data = alldata[centerSeedId[i]-1]
            center[i+1] = data[2:len(data)]
        return center
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

def KMeans(filename,iternum,centerSeedId):
    alldata,classify = readfile(filename)
    id2kind = dict()
    for elem in classify:
        for data in classify[elem]:
            id2kind[data[0]] = elem
    newclassify = classify
    center = getCenterSeed(classify,alldata,centerSeedId)
    oldaccuracy = -1
    count = 1
    while True:
        newclassify = reclassify(center,alldata)
        center = calculatecenter(newclassify)
        newaccuracy = accuracy(id2kind,newclassify,alldata)
        if iternum==count or newaccuracy == oldaccuracy:
            print newaccuracy
            draw(newclassify,alldata)
            break
        oldaccuracy = newaccuracy
        count += 1

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
            newid2kind[int(data[0])] = elem
    total = len(alldata)*len(alldata)
    intid2kind = dict()
    for elem in id2kind:
        intid2kind[int(elem)]=id2kind[elem]
    correct = 0
    for i in range(0,len(alldata)):
        for j in range(0,len(alldata)):
            if intid2kind[i+1]==intid2kind[j+1] and newid2kind[i+1]==newid2kind[j+1]:
                correct += 1
            elif intid2kind[i+1]!=intid2kind[j+1] and newid2kind[i+1]!=newid2kind[j+1]:
                correct += 1
    return float(correct)/float(total)

if __name__ == "__main__":
    KMeans("demo.txt",10,[3,5,9])
