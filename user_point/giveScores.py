#!/usr/bin/python3
# __*__ coding: utf-8 __*__

'''
@Author: simonKing
@License: (C) Copyright 2013-2019, Best Wonder Corporation Limited.
@Os：Windows 10 x64
@Contact: bw_wangxiaomeng@whty.com.cn
@Software: PY PyCharm 
@File: giveScores.py
@Time: 2019/7/3 9:24
@Desc: define your function
'''

'''
###############################################################
* 算法设计目的：根据用户使用数据，对百旺和百赋通打分，0~5
* 算法流程：1、数据清洗；2、数据编码码；3、K-means生成得分
* 算法输入：用户在百赋通使用数据，用户在百旺的消费数据
* 算法输出：分别算出每个用户对百赋通和百旺的打分
###############################################################

R,到期时间，得分越高，最高5分，最低1分
90天内购买；5
90-180天未购买；4
180-360天未购买；3
360-720；2
720以上；1


F,交易频率越高，得分越高，最高5分，最低1分
[1,24] ,平均1.1
1 -->1分；
2 -->2分；
3 -->3分；
4 -->4分；
5以上 -->5分；

M,交易金额越高，得分越高，最高5分，最低1分，平均金额374
大于2000  --> 5;
900~2000  --> 4;
370~900   --> 3;
200~370   --> 2;
0~200     --> 1;

注册资本：
大于1000万 -->  5;
500-1000万 -->  4;
100-500万  -->  3;
50-100万   -->  2;
50万以内，未知 -->1;

成立日期：
两年内 -->  2;
两年后 -->  1;

行业分类：
餐饮住宿 -->  3;
制造业   -->  2;
其它     -->  1;

日均登录次数：
5次及以上 --> 5;
4次     --> 4;
3次     --> 3;
2次     --> 2;
0,1次   --> 1;

日均登录次数：
10次及以上 --> 3;
5-10次     --> 2;
0-5次      --> 1;

日均开票金额：
1000及以上  --> 3;
100-1000    --> 2;
100以内     --> 1;

'''

import numpy as np
import openpyxl
import pandas as pd
from sklearn.cluster import KMeans,MiniBatchKMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D




def loadData(fname,splitchar='\t'):
    '''
    导入数据
    :param fname:文件名
    :param splitchar:字符间的分割符合
    :return:输入向量
    '''
    f = open(fname)
    X = [[float(v.split(splitchar)[0].strip()), float(v.split(splitchar)[1].strip()),float(v.split(splitchar)[2].strip())] for v in f]
    # X = [[float(v.split(splitchar)[0].strip()), float(v.split(splitchar)[1].strip()), float(v.split(splitchar)[2].strip()), float(v.split(splitchar)[3].strip())
    #          , float(v.split(splitchar)[4].strip()), float(v.split(splitchar)[5].strip()), float(v.split(splitchar)[6].strip()), float(v.split(splitchar)[7].strip())] for v in f]
    X = np.array(X)
    return X

def loadExcel(fname,index):
    '''
    从Excel 中导入数据
    :param fname:excel文件名
    :param index:导入的列
    :return:矩阵
    '''
    df = pd.read_excel(fname)
    X = df.ix[:, index]
    # print(X)
    # print(type(X))
    Input_X = np.array(X)
    return Input_X

def insertExcel(fname,col,data):
    wb = openpyxl.load_workbook(fname)
    ws = wb.worksheets[0]
    # ws.insert_cols(col)
    for index,row in enumerate(ws.rows):
        if index ==0:
            row[col+1].value = '评分'
        else:
            # ws.rows 比data多出了1行,header
            row[col+1].value = data.tolist()[index-1]
    wb.save('./new.xlsx')

def Kderiv(Input,n=2):
    '''
    求离散数列的2阶导数
    :param Input:输入离散数列
    :param n:n阶导数
    :return:二阶导数
    '''
    fun = np.poly1d(Input)
    fun_1 = np.poly1d.deriv(fun)
    fun_2 = np.poly1d.deriv(fun_1)
    return fun_2

def EmCalcu(data,labels,k):
    '''
    计算群体购买百赋通的数学期望
    :param data:原始数据
    :param labels:标签
    :param k:K均值
    :return:
    '''
    bestBuy = []
    for i in range(k):
        buy = 0
        nbuy = 0
        for j in range(len(labels)):
            if i == labels[j]:
                if data[j][-1] > 0:
                    buy = buy + 1
                elif data[j][-1] ==0:
                    nbuy = nbuy + 1
                else:
                    raise Exception('label not right')
        idx = labels.tolist().index(i)
        buyTimes = buy+ nbuy
        buyRate = buy/buyTimes
        print('K is %s, label is %s , buyRate is %s ,buyTime is %s'%(k,i,buyRate,buyTimes))
        print('example point:',data[idx])
        print("***"*30)


def choiceK(data):
    '''
    手肘法：采用MiniBatch方式寻找最佳的K值
    :param data:输入的数据集
    :return:最佳的K值
    '''
    data = [row for row in data if row[1] > 0]
    raw_data = [row[:6] for row in data]
    sse = []
    for k in range(1, 11):
        # estimator = KMeans(n_clusters=k)
        estimator = MiniBatchKMeans(init='k-means++', n_clusters=k, batch_size=100000, n_init=10, max_no_improvement=10, verbose=0)
        estimator.fit(raw_data)
        labels = estimator.labels_
        EmCalcu(data,labels,k)
        sse.append(estimator.inertia_)
        # data2 = []
        # for d in data.tolist():
        #     if d not in data2:
        #         data2.append(d)
        # data2 = np.array(data2)
        # 显示每个Kmeans聚类效果
        # label_pred = estimator.labels_
        # centroids = estimator.cluster_centers_
        # plotKmeans(data, k, centroids, label_pred).subplot(330+k)
    X = range(1, 11)
    plt.xlabel('K')
    plt.ylabel('SSE')
    plt.title("choice best k value")
    plt.plot(X, sse, 'o-')
    plt.savefig('./shouzhou.png')
    plt.show()
    return

def KmeansModel(data,k):
    '''
    # 构造聚类器
    :param data: 输入训练集
    :param k:聚类的K值
    :return:聚类模型
    '''
    estimator = KMeans(n_clusters=k)
    estimator.fit(data)
    return estimator

def KmeansPredict(clf,Input):
    '''
    Kmeans进行预测
    :param clf:Kmeans分类器
    :param Input:输入待测数据
    :return:分类标签
    '''
    labels = clf.predict(Input)
    return labels

def plotKmeans(dataSet,k,centroids,label_pred):
    '''
    用于绘制Kmeans聚类效果
    :param dataSet:输入数据集
    :param k:聚类的K值
    :param centroids:聚类的质心
    :param label_pred:预测的标签
    :return:
    '''
    mark = [ '^r', '+b', 'sg', 'x', '<r', 'pr','or', 'ob', 'og', 'ok']
    numSamples = len(dataSet)
    # 画出所有样例点 属于同一分类的绘制同样的颜色
    for i in range(numSamples):
        plt.plot(dataSet[i][0], dataSet[i][1], mark[label_pred[i]])
    mark = ['^r', '+b', 'sg', 'x','<r', 'pr', 'or', 'ob', 'og', 'ok']
    # 画出质点，用特殊图型
    for i in range(k):
        plt.plot(centroids[i][0], centroids[i][1], mark[i], markersize=8, label="label %s"%str(i))
    plt.title('Kmeans classfy result')
    plt.legend()
    # plt.savefig('./KmeansClassfyResult.png')
    plt.show()
    return plt

def plot_3Dfigure(data_mat, labels,):

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax3d = Axes3D(fig)
    l = []
    for label in labels:
        if label == 1:
            l.append(1)
        elif label == 2:
            l.append(2)
        elif label == 3:
            l.append(3)
        elif label == 0:
            l.append(0)
        elif label == 4:
            l.append(4)
        else:
            print('ERR:', label)
    labels = l
    y1 = [i for i in range(len(labels)) if labels[i] ==1.0]
    y2 = [i for i in range(len(labels)) if labels[i] ==2.0]
    y3 = [i for i in range(len(labels)) if labels[i] ==3.0]
    y4 = [i for i in range(len(labels)) if labels[i] ==4.0]
    y5 = [i for i in range(len(labels)) if labels[i] ==0.0]
    x1 = [data_mat[i] for i in y1]
    x2 = [data_mat[i] for i in y2]
    x3 = [data_mat[i] for i in y3]
    x4 = [data_mat[i] for i in y4]
    x5 = [data_mat[i] for i in y5]
    x1,x2,x3,x4,x5 = np.array(x1, dtype='float'),np.array(x2, dtype='float'),np.array(x3, dtype='float'),np.array(x4, dtype='float'),np.array(x5, dtype='float')
    # y1,y2,y3,y4,y5 = np.array(y1),np.array(y2),np.array(y3),np.array(y4),np.array(y5)
    ax3d.scatter(x1[:, 2], x1[:, 1], x1[:, 0],marker='.', color='r', s=20, label='一般发展用户')
    ax3d.scatter(x2[:, 2], x2[:, 1], x2[:, 0],marker='.', color='g', s=20, label='重要挽留用户')
    ax3d.scatter(x3[:, 2], x3[:, 1], x3[:, 0],marker='.', color='b', s=20, label='重要发展用户')
    ax3d.scatter(x4[:, 2], x4[:, 1], x4[:, 0],marker='.', color='m', s=20, label='重要保持用户')
    ax3d.scatter(x5[:, 2], x5[:, 1], x5[:, 0],marker='.', color='c', s=20, label='非常重要保持用户')
    # ax3d.legend(loc='best')  # 设置 图例所在的位置 使用推荐位置
    plt.rcParams['axes.unicode_minus'] = True
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title('Kmeans用户评价模型')
    ax3d.set_xlabel('距离最近一次购买时间（单位：天）')
    ax3d.set_zlabel('累计购买金额（单位：元）')
    ax3d.set_ylabel('累计购买次数')
    # plt.savefig('svm_user_is_value.png')
    plt.show()


# 百赋通,k=4;百企通, k=3;  旺票,k=4

# fname = r'D:\baiwang\21.数据运营\recommender\utils\bqt_rfm.xlsx'
# index = ['在百企通总消费次数','在百企通总消费金额','百企通最新度']
# testdata = loadExcel(fname,index)
#
# data = loadData(r'D:\baiwang\21.数据运营\recommender\data\百企通评价模型.txt')
# K = 3
# estimator = KmeansModel(data,K)
# test_label = estimator.predict(testdata)
# print(test_label)
# insertExcel(fname,2,test_label)
index = ["recently-bqt","je-bqt","times-bqt","dayInvoiceNum","industry","zczb","je-bft",]
data = loadExcel(r'D:\baiwang\21.数据运营\Recommend\data\DataModel.xlsx',index=index)
# testdata = loadData(r'D:\baiwang\21.数据运营\recommender\data\testdata.txt')
# step1 选择最佳聚类K
choiceK(data)
# K = 4
# # # step2 创建Kmeans 聚类器
# estimator = KmeansModel(data,K)
# # #
# # # # 获取聚类标签
# label_pred = estimator.labels_

# # # label_pred = estimator.predict(data)
# test_label = estimator.predict(testdata)
# print(test_label)


# 聚类结果统计
# labe0 = [v for v in label_pred.tolist() if v==0]
# print(len(labe0),labe0)
# labe1 = [v for v in label_pred.tolist() if v==1]
# print(len(labe1),labe1)
# labe2 = [v for v in label_pred.tolist() if v==2]
# print(len(labe2),labe2)
# labe3 = [v for v in label_pred.tolist() if v==3]
# print(len(labe3),labe3)


# # 获取聚类中心
# centroids = estimator.cluster_centers_
#加载PCA算法，设置降维后主成分数目为2
# pca=PCA(n_components=2)
# reduced_data=pca.fit_transform(data)
# reduced_centroids = pca.fit_transform(centroids)
# 获取聚类准则的总和
# inertia = estimator.inertia_
# step3 可视化聚类效果
# plotKmeans(reduced_data,K,reduced_centroids,label_pred)
# plot_3Dfigure(data,label_pred)
# # step4 预测
# Test_X = np.array([['1788','6'],])
# predict = KmeansPredict(estimator,Test_X)
# print(predict)