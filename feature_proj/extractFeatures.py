#!/usr/bin/python3
# __*__ coding: utf-8 __*__

'''
@Author: simonKing
@License: (C) Copyright 2013-2019, Best Wonder Corporation Limited.
@Os：Windows 10 x64
@Contact: bw_wangxiaomeng@whty.com.cn
@Software: PY PyCharm 
@File: extractFeatures.py
@Time: 2019/6/24 13:57
@Desc: define your function
'''

import pandas as pd
from feature_proj.featureSelector import FeatureSelector

# 用户消费数据保密，不开源
fname = ''
train = pd.read_excel(fname)
index = ["times-wp","je-wp","recently-wp","times-bqt","je-bqt","recently-bqt","times-bft","je-bft","recently-bft",
         "zczb_x","industry_x","ages_x","dayInvoiceNum_x","dayInvoiceJe_x","flag"]

train = train.ix[:, index]

train_labels = train['flag']

labels = []
for label in train_labels:
    if label <3:labels.append(1)
    else:labels.append(label)

train = train.drop(columns = ['flag'])

fs = FeatureSelector(data = train, labels = labels)

# 皮尔逊相关系数  相关系数 0.8-1.0 极强相关 , 0.6-0.8 强相关  ,0.4-0.6 中等程度相关  ,0.2-0.4 弱相关  ,0.0-0.2 极弱相关或无相关
fs.identify_collinear(correlation_threshold=0.9)
correlated_features = fs.ops['collinear']
print(correlated_features[:])
# # 热力图
fs.plot_collinear()
fs.plot_collinear(plot_all=True)

# 查看分类效果
fs.identify_zero_importance(task = 'classification', eval_metric = 'auc', n_iterations = 10, early_stopping = True)
print(fs.data_all.head(10))
zero_importance_features = fs.ops['zero_importance']
print(zero_importance_features[10:15])
# 变量重要性排名
fs.plot_feature_importances(threshold = 0.9, plot_n = 14)

# 累计重要性达到0.99，的特征排名
fs.identify_low_importance(cumulative_importance = 0.99)
low_importance_features = fs.ops['low_importance']
print(low_importance_features[:5])

# 特征删除
# train_no_missing = fs.remove(methods = ['missing'])
# # 删除多个
# fs.identify_all(selection_params = {'missing_threshold': 0.6, 'correlation_threshold': 0.98,'task': 'classification',
#                                     'eval_metric': 'auc','cumulative_importance': 0.99})
# # train_no_missing_zero = fs.remove(methods = ['missing', 'zero_importance'])
# all_to_remove = fs.check_removal()
# all_to_remove[10:25]
# train_removed = fs.remove(methods = 'all')




