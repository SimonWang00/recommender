#!/usr/bin/python3
# __*__ coding: utf-8 __*__

'''
@Author: simonKing
@License: (C) Copyright 2013-2019, Best Wonder Corporation Limited.
@Os：Windows 10 x64
@Contact: bw_wangxiaomeng@whty.com.cn
@Software: PY PyCharm 
@File: DecisionTree.py
@Time: 2019/7/16 9:36
@Desc: define your function
'''
import os
import pydotplus
import pandas as pd
from IPython.display import Image
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn import tree


def Dtcmodel(fname,index,X_test):
    df = pd.read_excel(fname)
    data = df.ix[:, index]
    flag = df.ix[:, ['flag', ]]
    # flag_names = ['low', 'medium', 'high']
    dtc = DecisionTreeClassifier()
    dtc.fit(data, flag)
    y_predict = dtc.predict(X_test)
    return y_predict

# # 1.导入数据
# index = ["times-wp","je-wp","recently-wp","times-bqt","je-bqt","recently-bqt","times-bft","je-bft","recently-bft","dayLoginTimes",
#          "zczb","industry","ages","dayInvoiceNum","dayInvoiceJe"]
# #
# fname = r'D:\baiwang\21.数据运营\recommender\DataModel.xlsx'
# df = pd.read_excel(fname)
# data = df.ix[:, index]
# flag = df.ix[:,['flag',]]
# flag_names=['low','medium','high']
#
# # 2.将数据拆分为训练集和测试集
# X_train,X_test,y_train,y_test = train_test_split(data,flag,test_size=0.2,random_state=33)
#
# # 3.使用决策树对测试数据进行类别预测
# dtc = DecisionTreeClassifier()
# dtc.fit(X_train,y_train)
# print(X_test)
# y_predict = dtc.predict(X_test)
#
# # # 4.获取结果报告
# print ('Accracy:',dtc.score(X_test,y_test))
# print (classification_report(y_predict,y_test,target_names=flag_names))
# #
# # # 5.将生成的决策树保存
# with open("jueceshu.dot", 'w') as f:
#     f = tree.export_graphviz(dtc, out_file = f)
#
# # # 6.可视化输出为图片
# os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
# dot_tree = tree.export_graphviz(dtc,out_file=None,feature_names=index,class_names=flag_names,filled=True, rounded=True,special_characters=True)
# graph = pydotplus.graph_from_dot_data(dot_tree)
# img = Image(graph.create_png())
# graph.write_png("shuchu.png")