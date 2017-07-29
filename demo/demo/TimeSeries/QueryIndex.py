import numpy as np
import json
import time
import matplotlib.pyplot as plt
import sys
'''

'''
def ED(x,y):
    '''
    :param x:
    :param y:
    :return: 欧式距离
    '''
    return np.sum(np.square(np.array(x) - np.array(y)))

def ED_Average(x,y,length):
    '''
    :param x:
    :param y:
    :param length:
    :return: 除以n返回平均ED
    '''
    return np.sum(np.square(np.array(x) - np.array(y)))/length

def DTW(arr_a, arr_b):
    '''
    动态时间规整距离
    :param arr_a:
    :param arr_b:
    :return:
    '''
    la = len(arr_a)
    lb = len(arr_b)
    matrix = [[ED(i, j) for i in arr_a] for j in arr_b]
    distance = [[0 for i in range(la)] for j in range(lb)]
    distance[0][0] = matrix[0][0]
    for i in range(1, la):
        distance[0][i] = distance[0][i - 1] + matrix[0][i]
    for j in range(1, lb):
        distance[j][0] = distance[j - 1][0] + matrix[j][0]
    for i in range(1, lb):
        for j in range(1, la):
            distance[i][j] = matrix[i][j] + min(distance[i - 1][j], distance[i][j - 1],
                                                distance[i - 1][j - 1] + matrix[i - 1][j - 1])
    return (distance[lb - 1][la - 1])

def DTW_Average(x,y,length):
    '''
    除以n返回平均DTW
    :param x:
    :param y:
    :param length:
    :return:
    '''
    return DTW(x,y)/length

def seekMinGroup(QueryData,Data):
    '''
    查询最小的序列代表
    :param QueryData:
    :param Data:
    :return:
    '''
    length = str(len(QueryData))
    minGroup = sys.maxsize
    for key in Data:
        temp = DTW(QueryData,Data[key]["Rep"])
        if temp<minGroup:
            minGroup = temp
            result = key
    return result

def seekMinElementFromGroup(QueryData,Data,key):
    '''
    从代表序列所在相似组寻找最相似序列
    :param QueryData:
    :param Data:
    :param key:
    :return:
    '''
    length = str(len(QueryData))
    list = []
    result = None
    min = sys.maxsize
    for value in Data[key]["Group"]:
        tempdtw = DTW(QueryData, value["Seq"])
        if min > tempdtw:
            result = value
            min = tempdtw
        list.append(tempdtw)
    result["DTW"] = min
    return result

def plotDTWFigure(val1,val2):
    plt.figure()
    plt.subplot(211)
    plt.plot(val1)
    plt.title("Query Time Series")
    plt.subplot(212)
    plt.plot(val2)
    plt.title("Most Similar Answer")
    plt.show()

def make(query):
    length = len(query)
    filename = "/Users/houruijie/bisheruijie/FinishCode/demo/demo/TimeSeries/ECG/"+str(length)+".json"
    Data = json.load(open(filename, "r"))
    startTime = time.time()
    result = seekMinElementFromGroup(query, Data, seekMinGroup(query, Data))
    endTime = time.time()
    result["Time"] = endTime-startTime
    return result

if __name__ == '__main__':
    pass