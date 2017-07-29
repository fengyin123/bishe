import os
import json
import random
import sys
import time
import numpy as np
import matplotlib.pyplot as plt

def readFile(filename):
    '''
    读文件 转成list
    :param filename:
    :return:
    '''
    data = []
    if not os.path.exists(filename):
        exit("未找到该文件")
    with open(filename,'r') as f:
        readdata = f.readlines()
        for value in readdata:
            line = value.split(',')[1:100]
            line = [float(i) for i in line]
            data.append(line)
    return data

def ED(x,y):
    '''
    #计算欧式距离
    :param x:
    :param y:
    :return:
    '''
    return np.sum(np.square(np.array(x).astype('float64') - np.array(y).astype('float64')))

def dtw(arr_a,arr_b):
    '''
    dtw距离
    :param arr_a:
    :param arr_b:
    :return:
    '''
    la = len(arr_a)
    lb = len(arr_b)
    matrix = [[ED(i,j) for i in arr_a] for j in arr_b]
    distance = [[0 for i in range(la)] for j in range(lb)]
    distance[0][0] = matrix[0][0]
    for i in range(1,la):
        distance[0][i] = distance[0][i-1]+matrix[0][i]
    for j in range(1,lb):
        distance[j][0] = distance[j-1][0]+matrix[j][0]
    for i in range(1,lb):
        for j in range(1,la):
            distance[i][j] = matrix[i][j] + min(distance[i-1][j],distance[i][j-1],distance[i-1][j-1]+matrix[i-1][j-1])
    return(distance[lb-1][la-1])

def initData(data,length):
    '''
    对list中每条时间序列进行拆分打乱
    :param dataList: [时间序列]
    :return:
    '''
    result = {}
    result[length] = []
    count = 0   #key
    for value in data:
        count += 1
        for l in range(len(value)-length+1):
            sequence={}
            sequence["Seq"]=value[l:l+length]
            sequence["Start"] = l
            sequence["End"] = l+length-1
            sequence["OrderNumber"] = count
            result[length].append(sequence)
            random.shuffle(result[length])
    return result

def seekDTW(data,query):
    '''
    利用dtw寻找最相似
    :param timeDict:
    :param k: 寻找与k最相似的序列
    :return:
    '''
    list = []
    min = sys.maxsize
    StartTime = time.time()
    index = {}
    for value in data:
        temp = dtw(value['Seq'],query)
        if temp<min:
            index = value
            min = temp
        list.append(temp)
    index["DTW"] = min
    EndTime = time.time()
    index["Time"] = EndTime-StartTime
    return index

def plotDTWFigure(query, result):
    plt.figure()
    plt.subplot(211)
    plt.plot(query)
    plt.title("Query Time Series")
    plt.subplot(212)
    plt.plot(result)
    plt.title("Most Similar Answer")
    plt.show()

def seekDTWPlot(data,query):
    '''
    利用dtw寻找最相似
    :param timeDict:
    :param k: 寻找与k最相似的序列
    :return:
    '''
    list = []
    min = sys.maxsize
    StartTime = time.time()
    index = {}
    for value in data:
        temp = dtw(value['Seq'],query)
        if temp<min:
            index = value
            min = temp
        list.append(temp)
    print("序列号:%d\t起始位置 %d\t结束位置%d"%(index["OrderNumber"],index["Start"],index["End"]))
    print("DTW距离:",min)
    EndTime = time.time()
    print("所花费时间：",EndTime-StartTime)
    plotDTWFigure(query,index["Seq"])

def make(query):
    length=len(query)
    filename = '/Users/houruijie/bisheruijie/FinishCode/demo/demo/TimeSeries/ECG200/ECG200_TEST'
    if not os.path.exists(filename):
        exit("file not found")
    data = readFile(filename)
    data = initData(data,length)
    return seekDTW(data[length],query)

if __name__ == '__main__':
    pass