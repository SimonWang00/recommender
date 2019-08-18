#!/usr/bin/python3
# __*__ coding: utf-8 __*__

'''
@Author: simonKing
@License: (C) Copyright 2013-2019, Best Wonder Corporation Limited.
@Os：Windows 10 x64
@Contact: bw_wangxiaomeng@whty.com.cn
@Software: PY PyCharm 
@File: setting.py
@Time: 2019/8/18 11:21
@Desc: 项目配置文件
'''

# mysql config
server = '127.0.0.1'
port = 3306
user = 'root'
password = '000000'
dbName = 'dcm'

# 准备待预测数据
Tname = "./data/DataRaw.xlsx"
# 准备模型数据
Mname = "./data/DataModel.xlsx"
# header
index = ["times_wp","je_wp","deadline_wp","times_bqt","je_bqt","recently_bqt","userConsumeTotalTimes","userConsumeTotalAmount","deadline","loginFrequency",
         "registeredCapital","industry","dateOfEstablishment","dayCountAvg","daySumAvg"]

# 排名数据
Rfname = "./data/注册资本Ranks"

# 输出名单
Output = './data/'

# 定时执行的时间设置，如每月1号，早上5点执行
exeTime = '01 05'