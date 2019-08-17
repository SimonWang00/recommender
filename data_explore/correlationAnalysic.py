#!/usr/bin/python3
# __*__ coding: utf-8 __*__

'''
@Author: simonKing
@License: (C) Copyright 2013-2019, Best Wonder Corporation Limited.
@Os：Windows 10 x64
@Contact: bw_wangxiaomeng@whty.com.cn
@Software: PY PyCharm 
@File: correlationAnalysic.py
@Time: 2019/7/12 14:38
@Desc: 关联性推荐
'''
import pandas as pd
import pylab as plt


def corrPer(seris1,seris2,index = None):
    '''
    计算数列间的相关系数
    :param seris1:数列1
    :param seris2:数列2
    :param index:数列名称
    :return:相关系数，1相关，0不相关，-1负相关
    '''
    # 利用Series将列表转换成新的、pandas可处理的数据
    s1 = pd.Series(seris1)
    s2 = pd.Series(seris2)
    # 计算皮尔逊相关系数，round(a, 4)是保留a的前四位小数
    corr_per = round(s1.corr(s2), 4)
    # print('corr_per :', corr_per)
    # 最后画一下两列表散点图，直观感受下，结合相关系数揣摩揣摩
    plt.scatter(seris1, seris2)
    if index:
        plt.xlabel(index[0])
        plt.ylabel(index[1])
    plt.title('corr_per :' + str(corr_per), fontproperties='SimHei')
    plt.show()
    return corr_per


def graAnalysic(seris1, seris2):
    '''
    分析两个数列的相关性
    :param seris1:数列1
    :param seris2:数列2
    :return:-1负相关，0不相干，1正相关
    '''
    x = pd.DataFrame(data=[seris1,seris2])
    # 1、数据均值化处理
    x_mean = x.mean(axis=1)
    for i in range(x.index.size):
        x.iloc[i,:] = x.iloc[i,:]/x_mean[i]
    # 2、提取参考队列和比较队列
    ck=x.iloc[0,:]
    cp=x.iloc[1:,:]
    # 比较队列与参考队列相减
    t=pd.DataFrame()
    for j in range(cp.index.size):
        temp=pd.Series(cp.iloc[j,:] - ck)
        t=t.append(temp,ignore_index=True)
    #求最大差和最小差
    mmax=t.abs().max().max()
    mmin=t.abs().min().min()
    rho=0.5
    #3、求关联系数
    ksi=((mmin + rho*mmax)/(abs(t) + rho*mmax))
    #4、求关联度
    r=ksi.sum(axis=1)/ksi.columns.size
    #5、关联度排序
    result=r.sort_values(ascending=False)
    plt.plot(seris1)
    plt.plot(seris2)
    plt.show()
    return result

# if __name__ == '__main__':
#     pass
    # s1 = [0.4755,0.4299,0.6358,0.7527,0.4228,0.3358]
    # s2 = [0.6591,0.5739,0.5465,0.8993,0.6661,0.4037]
    # result = graAnalysic(s1,s2)