from itertools import combinations, permutations
import time
import numpy as np
import pandas as pd

#20181020_暴力法_correct

data = []
support = 0.3
confidence_num = 0.9
pop = []
setNum = 1
cal_itemset = [] #放所有符合support的itemset
num_itemset = [] #記錄每階段留下的itemset有幾個
dictionary = {}
confidence = []
datasize = 100
itt = []
itt_len=0

df = pd.read_csv('dataset.csv')
data = []
for i in df.values:
    tmp = []
    for j in range(len(i)):
        if i[j] != '?':
            tmp.append(j+1)
    data.append(tmp)

#計算confidence
def cal_confidence(itemset,setNum):
    for i in range(len(itemset)):
        b = []
        for j in range(int((len(itemset[i]))/2)):
            b.append(list(combinations(itemset[i][0:len(itemset[i])-1], j + 1)))
        length = 0
        if len(b) < 2:
            length = len(b)
        else:
            length = len(b) - 1
        for k in range(length):
            for l in range(len(b[k])):
                temp = list(set(itemset[i][0:setNum]).difference(set(list(b[k][l]))))
                temp.sort()
                x = dictionary[tuple(b[k][l])]
                y = dictionary[tuple(temp)]
                total = dictionary[tuple(itemset[i][0:setNum])]
                if x != 0 and (total/x)>confidence_num:
                    confidence.append([tuple(b[k][l]),tuple(temp),total/x])
                if y != 0 and (total/y>confidence_num):
                    confidence.append([tuple(temp),tuple(b[k][l]),total/y])

# 刪除小於support
def pop_itemset(itemset, support, setNum):
    pop = []
    for l in range(len(itemset)):
        if int(itemset[l][setNum]) < int(len(data)*support):
            pop.append(l)   #不符合的紀錄，先存下來再pop掉
        else:
            temp = tuple(itemset[l][0:setNum])
            dictionary.update({temp:itemset[l][setNum]})
    if len(pop) != 0 and len(pop) != 1:
        pop.reverse()
    for m in range(len(pop)):
        itemset.pop(pop[m])
    itt.append(itemset)
    return itemset

# 產生新的itemset
def generate_itemset(setNum, itemset):
    for i in range(len(itemset)): #拿掉cnt
        itemset[i].pop()

    a = list(combinations(itemset, 2))
    b = []

    for i in range(len(a)):
        sort_element = sorted(list(set(a[i][0])|(set(a[i][1]))))
        b.append(sort_element)
    tu = set(tuple(l) for l in b)
    c = [list(t) for t in tu]
    temp = []
    for i in range(len(c)):
        if (len(c[i]) == setNum):
            temp.append(c[i])
    return temp


# 暴力法
itemset = []
start = time.time()

# 產生第一個itemset
for i in range(len(data)):
    for j in range(len(data[i])):
        check = 0
        if len(itemset) == 0:
            temp = [data[i][j], 1]
            itemset.append(temp)
        else:
            for k in range(len(itemset)):
                if itemset[k][0] == data[i][j]:
                    itemset[k][1] = itemset[k][1] + 1
                    check = 1
            if check == 0:
                temp = [data[i][j], 1]
                itemset.append(temp)

while 1:
    itemset = pop_itemset(itemset, support, setNum)
    if setNum != 1:
        cal_confidence(itemset,setNum)

    setNum = setNum + 1

    if len(itemset) <= 1:
        print("success")
        break

    temp = []
    temp = generate_itemset(setNum, itemset)

    itemset = []
    itemset = temp

    for i in range(len(itemset)):  # 新計數
        itemset[i].append(0)

    for i in range(len(data)):
        for j in range(len(itemset)):
            temp = []
            temp = list(set(data[i]) & set(itemset[j][:setNum]))
            if set(itemset[j][:setNum]) == set(temp):
                itemset[j][setNum] = itemset[j][setNum] + 1
end = time.time()
tu = set(tuple(l) for l in confidence)
c = [list(t) for t in tu]

for i in range(len(itt)):
    for j in range(len(itt[i])):
            itt_len+=1
print("Time Taken is:")
print(end-start)
print("All frequent itemsets:")
print(itt_len)
print(itt)