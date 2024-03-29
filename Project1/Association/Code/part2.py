import numpy as np
from numpy import *

label = []
data = []
support = 0.5
confidence = 0.7
all_frequent_itemset = []
with open("associationruletestdata.txt") as file:
    line = file.readline()
    while line:
        oneline = line.split('\t')
        row = []
        for i in range(0,len(oneline)-1):
            if oneline[i][0]=='U':
                row.append("G"+str(i+1)+"_UP")
            else:
                row.append("G"+str(i+1)+"_DOWN")
        data.append(row)
        label.append(oneline[-1][:-2])
        line = file.readline()

def apriori():
    total_frequent_itemsets = 0
    item_set = dict()
    rows = len(data)
    cols = len(data[0])
    for i in range(0,rows):
        for j in range(0,cols):
            key = frozenset([data[i][j]])
            if key in item_set:
                item_set[key] = item_set[key]+1
            else:
                item_set[key] = 1
    for item in item_set.keys():
        if item_set[item] < rows*support:
            del(item_set[item])
    total_frequent_itemsets = total_frequent_itemsets+len(item_set)
    print "number of length-1 frequent itemsets:"+str(len(item_set))
    all_frequent_itemset.append(item_set)

    k = 2
    while len(item_set)!=0:
        new_item_set = dict()
        new_item_set_key = item_set.keys()
        new_frequency_set = set()
        for i in range(0,len(new_item_set_key)-1):
            for j in range(i+1,len(new_item_set_key)):
                combination = set()
                for elem in new_item_set_key[i]:
                    combination.add(elem)
                for elem in new_item_set_key[j]:
                    combination.add(elem)
                if(len(combination) == k):
                    new_frequency_set.add(frozenset(combination))
        for elem_new_frequency_set in new_frequency_set:
            for row in range(0,rows):
                count = 0
                for elem in elem_new_frequency_set:
                    index = -1
                    if(elem[2] == '_'):
                        index = int(elem[1:2])
                    elif(elem[3] == '_'):
                        index = int(elem[1:3])
                    else:
                        index = int(elem[1:4])
                    if(data[row][index-1]==elem):
                        count = count+1
                if count==k:
                    if elem_new_frequency_set in new_item_set:
                        new_item_set[elem_new_frequency_set] = new_item_set[elem_new_frequency_set]+1
                    else:
                        new_item_set[elem_new_frequency_set] = 1
        for item in new_item_set.keys():
            if new_item_set[item] < rows*support:
                del(new_item_set[item])
        total_frequent_itemsets = total_frequent_itemsets+len(new_item_set)
        if(len(new_item_set)==0):
            break
        print "number of length-"+str(k)+" frequent itemsets:"+str(len(new_item_set))
        all_frequent_itemset.append(new_item_set)
        item_set = new_item_set
        k = k+1
    print "number of all lengths frequent itemsets:"+str(total_frequent_itemsets)


def template1(str1,str2,item_list):
    result = set()
    if str1=="RULE":
        if str2=="ANY":
            item_set = set()
            for elem in item_list:
                item_set.add(elem)
            start = len(item_set)-1
            if start==0:
                start = 1
            for i in range(start,len(all_frequent_itemset)):
                frequent_itemset = all_frequent_itemset[i]
                for elem_frequent_itemset in frequent_itemset.keys():
                    flag = 1
                    for elem in item_set:
                        if elem not in elem_frequent_itemset:
                            flag = 0
                            break
                    if flag==0: continue
                    subsets = [[]]
                    for itemset in elem_frequent_itemset:
                        subsets += [i+[itemset] for i in subsets]
                    for subset in subsets:
                        if len(subset)==0 or len(subset)==len(elem_frequent_itemset):
                            continue
                        tempset = set()
                        for elem in subset:
                            tempset.add(elem)
                        if frequent_itemset[elem_frequent_itemset]>=all_frequent_itemset[len(tempset)-1][frozenset(tempset)]*confidence:
                            output = str(frozenset(tempset))+"->"+str(elem_frequent_itemset-frozenset(tempset))
                            result.add(output)

        elif str2=="NONE":
            item_set = set()
            for elem in item_list:
                item_set.add(elem)
            for i in range(1,len(all_frequent_itemset)):
                frequent_itemset = all_frequent_itemset[i]
                for elem_frequent_itemset in frequent_itemset.keys():
                    flag = 1
                    for elem in item_set:
                        if elem in elem_frequent_itemset:
                            flag = 0
                            break
                    if flag==0: continue
                    subsets = [[]]
                    for itemset in elem_frequent_itemset:
                        subsets += [i+[itemset] for i in subsets]
                    for subset in subsets:
                        if len(subset)==0 or len(subset)==len(elem_frequent_itemset):
                            continue
                        tempset = set()
                        for elem in subset:
                            tempset.add(elem)
                        if frequent_itemset[elem_frequent_itemset]>=all_frequent_itemset[len(tempset)-1][frozenset(tempset)]*confidence:
                            output = str(frozenset(tempset))+"->"+str(elem_frequent_itemset-frozenset(tempset))
                            result.add(output)
        else:
            itemnum = int(str2)
            item_set = set()
            for elem in item_list:
                item_set.add(elem)
            for i in range(1,len(all_frequent_itemset)):
                frequent_itemset = all_frequent_itemset[i]
                for elem_frequent_itemset in frequent_itemset.keys():
                    if len(item_set&elem_frequent_itemset) != itemnum:
                        continue
                    subsets = [[]]
                    for itemset in elem_frequent_itemset:
                        subsets += [i+[itemset] for i in subsets]
                    for subset in subsets:
                        if len(subset)==0 or len(subset)==len(elem_frequent_itemset):
                            continue
                        tempset = set()
                        for elem in subset:
                            tempset.add(elem)
                        if frequent_itemset[elem_frequent_itemset]>=all_frequent_itemset[len(tempset)-1][frozenset(tempset)]*confidence:
                            output = str(frozenset(tempset))+"->"+str(elem_frequent_itemset-frozenset(tempset))
                            result.add(output)
    elif str1=="HEAD":
        if str2=="ANY":
            item_set = set()
            for elem in item_list:
                item_set.add(elem)
            start = len(item_set)-1
            if start==0:
                start = 1
            for i in range(start,len(all_frequent_itemset)):
                frequent_itemset = all_frequent_itemset[i]
                for elem_frequent_itemset in frequent_itemset.keys():
                    flag = 1
                    for elem in item_set:
                        if elem not in elem_frequent_itemset:
                            flag = 0
                            break
                    if flag==0: continue
                    subsets = [[]]
                    for itemset in elem_frequent_itemset:
                        subsets += [i+[itemset] for i in subsets]
                    for subset in subsets:
                        if len(subset)==0 or len(subset)==len(elem_frequent_itemset):
                            continue
                        tempset = set()
                        for elem in subset:
                            tempset.add(elem)
                        if len(tempset&item_set)!=len(item_set):
                            continue
                        if frequent_itemset[elem_frequent_itemset]>=all_frequent_itemset[len(tempset)-1][frozenset(tempset)]*confidence:
                            output = str(frozenset(tempset))+"->"+str(elem_frequent_itemset-frozenset(tempset))
                            result.add(output)
        elif str2=="NONE":
            item_set = set()
            for elem in item_list:
                item_set.add(elem)
            for i in range(1,len(all_frequent_itemset)):
                frequent_itemset = all_frequent_itemset[i]
                for elem_frequent_itemset in frequent_itemset.keys():
                    subsets = [[]]
                    for itemset in elem_frequent_itemset:
                        subsets += [i+[itemset] for i in subsets]
                    for subset in subsets:
                        if len(subset)==0 or len(subset)==len(elem_frequent_itemset):
                            continue
                        tempset = set()
                        for elem in subset:
                            tempset.add(elem)
                        if len(tempset&item_set)!=0:
                            continue
                        if frequent_itemset[elem_frequent_itemset]>=all_frequent_itemset[len(tempset)-1][frozenset(tempset)]*confidence:
                            output = str(frozenset(tempset))+"->"+str(elem_frequent_itemset-frozenset(tempset))
                            result.add(output)
        else:
            itemnum = int(str2)
            item_set = set()
            for elem in item_list:
                item_set.add(elem)
            for i in range(1,len(all_frequent_itemset)):
                frequent_itemset = all_frequent_itemset[i]
                for elem_frequent_itemset in frequent_itemset.keys():
                    subsets = [[]]
                    for itemset in elem_frequent_itemset:
                        subsets += [i+[itemset] for i in subsets]
                    for subset in subsets:
                        if len(subset)==0 or len(subset)==len(elem_frequent_itemset):
                            continue
                        tempset = set()
                        for elem in subset:
                            tempset.add(elem)
                        if len(tempset&item_set)!=itemnum:
                            continue
                        if frequent_itemset[elem_frequent_itemset]>=all_frequent_itemset[len(tempset)-1][frozenset(tempset)]*confidence:
                            output = str(frozenset(tempset))+"->"+str(elem_frequent_itemset-frozenset(tempset))
                            result.add(output)
    elif str1=="BODY":
        if str2=="ANY":
            item_set = set()
            for elem in item_list:
                item_set.add(elem)
            start = len(item_set)-1
            if start==0:
                start = 1
            for i in range(start,len(all_frequent_itemset)):
                frequent_itemset = all_frequent_itemset[i]
                for elem_frequent_itemset in frequent_itemset.keys():
                    flag = 1
                    for elem in item_set:
                        if elem not in elem_frequent_itemset:
                            flag = 0
                            break
                    if flag==0: continue
                    subsets = [[]]
                    for itemset in elem_frequent_itemset:
                        subsets += [i+[itemset] for i in subsets]
                    for subset in subsets:
                        if len(subset)==0 or len(subset)==len(elem_frequent_itemset):
                            continue
                        tempset = set()
                        for elem in subset:
                            tempset.add(elem)
                        if len((elem_frequent_itemset-frozenset(tempset))&item_set)!=len(item_set):
                            continue
                        if frequent_itemset[elem_frequent_itemset]>=all_frequent_itemset[len(tempset)-1][frozenset(tempset)]*confidence:
                            output = str(frozenset(tempset))+"->"+str(elem_frequent_itemset-frozenset(tempset))
                            result.add(output)
        elif str2=="NONE":
            item_set = set()
            for elem in item_list:
                item_set.add(elem)
            for i in range(1,len(all_frequent_itemset)):
                frequent_itemset = all_frequent_itemset[i]
                for elem_frequent_itemset in frequent_itemset.keys():
                    subsets = [[]]
                    for itemset in elem_frequent_itemset:
                        subsets += [i+[itemset] for i in subsets]
                    for subset in subsets:
                        if len(subset)==0 or len(subset)==len(elem_frequent_itemset):
                            continue
                        tempset = set()
                        for elem in subset:
                            tempset.add(elem)
                        if len((elem_frequent_itemset-frozenset(tempset))&item_set)!=0:
                            continue
                        if frequent_itemset[elem_frequent_itemset]>=all_frequent_itemset[len(tempset)-1][frozenset(tempset)]*confidence:
                            output = str(frozenset(tempset))+"->"+str(elem_frequent_itemset-frozenset(tempset))
                            result.add(output)
        else:
            itemnum = int(str2)
            item_set = set()
            for elem in item_list:
                item_set.add(elem)
            for i in range(1,len(all_frequent_itemset)):
                frequent_itemset = all_frequent_itemset[i]
                for elem_frequent_itemset in frequent_itemset.keys():
                    subsets = [[]]
                    for itemset in elem_frequent_itemset:
                        subsets += [i+[itemset] for i in subsets]
                    for subset in subsets:
                        if len(subset)==0 or len(subset)==len(elem_frequent_itemset):
                            continue
                        tempset = set()
                        for elem in subset:
                            tempset.add(elem)
                        if len((elem_frequent_itemset-frozenset(tempset))&item_set)!=itemnum:
                            continue
                        if frequent_itemset[elem_frequent_itemset]>=all_frequent_itemset[len(tempset)-1][frozenset(tempset)]*confidence:
                            output = str(frozenset(tempset))+"->"+str(elem_frequent_itemset-frozenset(tempset))
                            result.add(output)
    else:
        print "parameter1 error!"
    return result,len(result)

def template2(str1,size):
    result = set()
    if str1=="RULE":
        for i in range(size-1,len(all_frequent_itemset)):
            frequent_itemset = all_frequent_itemset[i]
            for elem_frequent_itemset in frequent_itemset.keys():
                subsets = [[]]
                for itemset in elem_frequent_itemset:
                    subsets += [i+[itemset] for i in subsets]
                for subset in subsets:
                    if len(subset)==0 or len(subset)==len(elem_frequent_itemset):
                        continue
                    tempset = set()
                    for elem in subset:
                        tempset.add(elem)
                    if frequent_itemset[elem_frequent_itemset]>=all_frequent_itemset[len(tempset)-1][frozenset(tempset)]*confidence:
                            output = str(frozenset(tempset))+"->"+str(elem_frequent_itemset-frozenset(tempset))
                            result.add(output)
    elif str1=="HEAD":
        for i in range(size-1,len(all_frequent_itemset)):
            frequent_itemset = all_frequent_itemset[i]
            for elem_frequent_itemset in frequent_itemset.keys():
                subsets = [[]]
                for itemset in elem_frequent_itemset:
                    subsets += [i+[itemset] for i in subsets]
                for subset in subsets:
                    if len(subset)==0 or len(subset)==len(elem_frequent_itemset):
                        continue
                    tempset = set()
                    for elem in subset:
                        tempset.add(elem)
                    if len(tempset)<size:
                        continue
                    if frequent_itemset[elem_frequent_itemset]>=all_frequent_itemset[len(tempset)-1][frozenset(tempset)]*confidence:
                            output = str(frozenset(tempset))+"->"+str(elem_frequent_itemset-frozenset(tempset))
                            result.add(output)
    elif str1=="BODY":
        for i in range(size-1,len(all_frequent_itemset)):
            frequent_itemset = all_frequent_itemset[i]
            for elem_frequent_itemset in frequent_itemset.keys():
                subsets = [[]]
                for itemset in elem_frequent_itemset:
                    subsets += [i+[itemset] for i in subsets]
                for subset in subsets:
                    if len(subset)==0 or len(subset)==len(elem_frequent_itemset):
                        continue
                    tempset = set()
                    for elem in subset:
                        tempset.add(elem)
                    if len(elem_frequent_itemset)-len(tempset)<size:
                        continue
                    if frequent_itemset[elem_frequent_itemset]>=all_frequent_itemset[len(tempset)-1][frozenset(tempset)]*confidence:
                            output = str(frozenset(tempset))+"->"+str(elem_frequent_itemset-frozenset(tempset))
                            result.add(output)
    else:
        print "parameter1 error!"
    return result,len(result)

def template3(*args):
    rule = args[0]
    if rule[1:3]=="or":
        if rule[0] =="1" and rule[-1]=="1":
            result1,num1 = template1(args[1],args[2],args[3])
            result2,num2 = template1(args[4],args[5],args[6])
            result = result1|result2
            return result,len(result)
        elif rule[0] =="1" and rule[-1]=="2":
            result1,num1 = template1(args[1],args[2],args[3])
            result2,num2 = template2(args[4],args[5])
            result = result1|result2
            return result,len(result)
        elif rule[0] == "2" and rule[-1]=="1":
            result1,num1 = template2(args[1],args[2])
            result2,num2 = template1(args[3],args[4],args[5])
            result = result1|result2
            return result,len(result)
        else:
            result1,num1 = template2(args[1],args[2])
            result2,num2 = template2(args[3],args[4])
            result = result1|result2
            return result,len(result)
    elif rule[1:4]=="and":
        if rule[0] =="1" and rule[-1]=="1":
            result1,num1 = template1(args[1],args[2],args[3])
            result2,num2 = template1(args[4],args[5],args[6])
            result = result1&result2
            return result,len(result)
        elif rule[0] =="1" and rule[-1]=="2":
            result1,num1 = template1(args[1],args[2],args[3])
            result2,num2 = template2(args[4],args[5])
            result = result1&result2
            return result,len(result) 
        elif rule[0] == "2" and rule[-1]=="1":
            result1,num1 = template2(args[1],args[2])
            result2,num2 = template1(args[3],args[4],args[5])
            result = result1&result2
            return result,len(result)
        else:
            result1,num1 = template2(args[1],args[2])
            result2,num2 = template2(args[3],args[4])
            result = result1&result2
            return result,len(result)
    else:
        print "parameter1 error!"

if __name__ == "__main__":
    apriori()
    result11,cnt = template1("RULE","ANY",["G59_UP"]);print cnt
    result12,cnt = template1("RULE","NONE",["G59_UP"]);print cnt
    result13,cnt = template1("RULE","1",["G59_UP","G10_DOWN"]);print cnt
    result14,cnt = template1("HEAD","ANY",["G59_UP"]);print cnt
    result15,cnt = template1("HEAD","NONE",["G59_UP"]);print cnt
    result16,cnt = template1("HEAD","1",["G59_UP","G10_DOWN"]);print cnt
    result17,cnt = template1("BODY","ANY",["G59_UP"]);print cnt
    result18,cnt = template1("BODY","NONE",["G59_UP"]);print cnt
    result19,cnt = template1("BODY","1",["G59_UP","G10_DOWN"]);print cnt

    result21,cnt = template2("RULE",3);print cnt
    result22,cnt = template2("HEAD",2);print cnt
    result23,cnt = template2("BODY",1);print cnt

    result31,cnt = template3("1or1","HEAD","ANY",["G10_DOWN"],"BODY","1", ["G59_UP"]);print cnt
    result32,cnt = template3("1and1","HEAD","ANY",["G10_DOWN"],"BODY","1",["G59_UP"]);print cnt
    result33,cnt = template3("1or2","HEAD","ANY",["G10_DOWN"],"BODY",2);print cnt
    result34,cnt = template3("1and2","HEAD","ANY",["G10_DOWN"],"BODY",2);print cnt
    result35,cnt = template3("2or2","HEAD",1,"BODY",2);print cnt
    result36,cnt = template3("2and2","HEAD",1,"BODY",2);print cnt



