#!/usr/bin/python3
# __*__ coding: utf-8 __*__

'''
@Author: simonKing
@License: (C) Copyright 2013-2019, Best Wonder Corporation Limited.
@Os：Windows 10 x64
@Contact: bw_wangxiaomeng@whty.com.cn
@Software: PY PyCharm 
@File: cutScopebusiness.py
@Time: 2019/6/25 10:56
@Desc: define your function
'''

'''
行业分类参考：https://blog.csdn.net/chenhuamain/article/details/84579667
农林牧渔 1
制造业 2
卫生医疗 3
商务服务 4
居民服务 5
建筑产业 6
房地产业 7
教育培训 8
文体娱乐 9
电信通讯 10
科学技术 11
租赁服务 12
维修服务 13
设计服务 14
运输物流 15
采矿工业 16
金融服务 17
餐饮住宿 18
'''
import pymysql

class MysqlOperate:
    def __init__(self):
        self.db = pymysql.connect("192.168.5.135", "root", "000000", "platform")
        self.cursor = self.db.cursor()
        pass

    def read_data(self,sql):
        self.cursor.execute(sql)
        # datas = self.cursor.fetchmany(100)
        datas = self.cursor.fetchall()
        # print(datas)
        self.db.close()
        return datas

    def update_data(self,sql):
        self.cursor.execute(sql)
        self.db.commit()
        return
