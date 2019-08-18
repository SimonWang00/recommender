#!/usr/bin/python3
# __*__ coding: utf-8 __*__

'''
@Author: simonKing
@License: (C) Copyright 2013-2019, Best Wonder Corporation Limited.
@Os：Windows 10 x64
@Contact: bw_wangxiaomeng@whty.com.cn
@Software: PY PyCharm 
@File: recommender.py
@Time: 2019/7/16 15:37
@Desc: define your function
'''
import time
import pymysql
import datetime
import pandas as pd
from user_point.evaluationFunction import evaluationTotalProduct,computeTotalScore
from user_recom.DecisionTree import Dtcmodel
from setting import *


def loadData(sql):
    '''
    从mysql中导入数据，
    :param sql:
    :return:DataFrame
    '''
    conn = pymysql.connect(host=server,port=port,user=user,password=password,db=dbName,charset='utf8')
    result = pd.read_sql_query(sql=sql,con=conn)
    return result

def getColumns():
    '''
    接入生产环境的用户数据
    :return:
    '''
    sql = "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = 'dcm' AND TABLE_NAME = 'basic_info_all' LIMIT 10000;"
    conn = pymysql.connect(host=server,port=port,user=user,password=password,db=dbName,charset='utf8').cursor()
    conn.execute(sql)
    columns = conn.fetchall()
    conn.close()
    columns = [row[0] for row in columns]
    return columns

def bftDeadtimeCalcu(deadtime):
    '''
    计算到期的天数
    :param deadtime:到期时间
    :return:天
    '''
    if deadtime == None:return -1
    recently = str(deadtime)
    if recently.strip() == '0' or recently.strip() == None:
        return -1
    try:
        d1 = datetime.datetime.strptime(recently, '%Y-%m-%d')
    except:
        d1 = datetime.datetime.strptime(recently, '%Y/%m/%d')
    nwt = datetime.datetime.now()
    days = (d1 - nwt).days
    if days <0: days=720
    return days

def deadtimeCalcu(recently):
    '''
    根据最近一次购买时间，算出到期时间
    :param recently:最近一次购买日期
    :return:还有多久到期
    '''
    if recently ==None:return -1
    recently = str(recently)
    if recently.strip() == '0' or recently.strip() == None:return -1
    try:
        d1 = datetime.datetime.strptime(recently, '%Y-%m-%d')
    except:
        d1 = datetime.datetime.strptime(recently, '%Y/%m/%d')
    delta = datetime.timedelta(days=365)
    deadtime = d1 + delta
    nwt = datetime.datetime.now()
    days = (deadtime - nwt).days
    if days <0: days=720
    return days

def agesCalcu(age):
    '''
    计算到目前为止，成立的日期
    :param establish:成立日期
    :return:成立了多少年
    '''
    if age ==None:return 3
    age = str(age)
    if age.strip() =="未知" or age == '0':
        return 3
    try:
        d1 = datetime.datetime.strptime(age, '%Y-%m-%d')
    except:
        d1 = datetime.datetime.strptime(age, '%Y/%m/%d')
    nwt = datetime.datetime.now()
    years = round((nwt - d1).days/365,2)
    return years

def rankCalcu(zczb):
    '''
    计算注册资本排名
    :param zczb:输入注册资本
    :return:排名
    '''
    if zczb ==0 or zczb =="未知" or zczb =="0" or zczb ==None:return '未知'
    fname = Rfname
    f = open(fname,'r').readlines()
    zczbArr = pd.Series(f)

    zczbArr = [int(eval(zb.strip())) for zb in zczbArr]
    try:
        rank = zczbArr.index(int(eval(zczb))) + 1
    except:
        rank = '未知'
    return rank

def scoreArrCalcu(data):
    '''
    计算推荐得分
    :param data:用户评级
    :return:所有得分
    '''
    scoreArr = [computeTotalScore(dict(zip(index,data.iloc[i]))) for i in range(len(data))]
    return scoreArr

def scoreCalcu(row):
    '''
    计算单个用户的得分
    :param row: 用户等级
    :return: 得分
    '''
    score = computeTotalScore(dict(zip(index,row)))
    return score


def exeTiming(func):
    '''
    设置装饰器，定时执行
    :param func:方法
    :return:
    '''
    def wrapper():
        t1 = time.time()
        nwt = datetime.datetime.now().strftime('%d %H')
        # 每月1号 5点执行
        if nwt == exeTime:
            func()
            print('recommend sucess !')
            time.sleep(60*60*24)
        else:
            time.sleep(60*30)
        t2 = time.time()
        print(t2-t1)
    return wrapper

def outputXls(data):
    '''
    输出结果，如果用户应该推荐，就写入excel中
    :param data:用户数据
    :return:
    '''
    OutputFile = Output + 'recommendList' + datetime.datetime.now().strftime('%Y%m%d') + '.xls'
    df = pd.DataFrame(data=data)
    try:
        # 生产环境导表头
        columns = getColumns()
    except:
        # 测试环境用index
        columns = index
    columns.append("Rank")
    columns.append("score")
    df.columns = columns
    df.to_excel(OutputFile)


@exeTiming
def recommend():
    '''
    推荐主方法
    :return:输出名单
    '''
    # 测试数据预处理
    test_data = pd.read_excel(Tname)
    data = test_data.ix[:,index]
    # 缺失填充0
    data = data.fillna(0)
    ages = [agesCalcu(y) for y in data['dateOfEstablishment']]
    recently_wp = [bftDeadtimeCalcu(x) for x in data['deadline_wp']]
    recently_bft = [bftDeadtimeCalcu(x) for x in data['deadline']]
    recently_bqt = [deadtimeCalcu(x) for x in data['recently_bqt']]
    data['dateOfEstablishment'] = ages
    data['deadline_wp'] = recently_wp
    data['deadline'] = recently_bft
    data['recently_bqt'] = recently_bqt
    data_raw = []
    # print('raw_data：',data)
    # print(len(data))
    # # 给输入数据评级
    for i in range(len(data)):
        row = data.iloc[i]
        test_X = evaluationTotalProduct(row,index)
        data_raw.append(test_X)
    RecommendList = []
    # # 加载模型，推荐预测
    y_predict = Dtcmodel(Mname,index,data_raw).tolist()
    for j,label in enumerate(y_predict):
        if label ==3:
            row = data_raw[j]
            score = scoreCalcu(row)
            info = test_data.iloc[j].tolist()
            rank = rankCalcu(test_data.iloc[j]['registeredCapital'])
            info.append(rank)
            info.append(score)
            RecommendList.append(info)
            print("推荐意愿打分：",score)
    # 输出结果
    if len(RecommendList) > 0:
        print("注意！生成了推荐名单")
        outputXls(RecommendList)
    else:
        print("没有产生推荐名单")

if __name__ =='__main__':
    while True:
        recommend()