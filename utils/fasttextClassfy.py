#!/usr/bin/python3
# __*__ coding: utf-8 __*__

'''
@Author: simonKing
@License: (C) Copyright 2013-2019, Best Wonder Corporation Limited.
@Os：Windows 10 x64
@Contact: bw_wangxiaomeng@whty.com.cn
@Software: PY PyCharm 
@File: fasttextClassfy.py
@Time: 2019/6/25 10:47
@Desc: define your function
'''
import jieba
import random
import jieba.posseg as pseg
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from utils.cutScopebusiness import MysqlOperate
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


# 朴素贝叶斯算法
def nb_model(train, train_label, test, test_label):
    clf_model = MultinomialNB(alpha=0.01)
    clf_model.fit(train, train_label)
    predict_results = clf_model.predict(test)

    count = 0
    predict_list = predict_results.tolist()
    for i, pred in enumerate(predict_list):
        if (pred == test_label[i]):
            count += 1

    print("nb_model_precision_score: " + str(float(count) / len(predict_list)))

# 创建朴素贝叶斯分类模型
def nb_classfy_model(train, train_label,inputs):
    '''
    :param train: 训练语料
    :param train_label: 训练标签
    :param inputs:待预测预料
    :return:预测结果
    '''
    clf_model = MultinomialNB(alpha=0.01)
    clf_model.fit(train, train_label)
    predict_results = clf_model.predict(inputs)
    # print('贝叶斯预测结果：',predict_results)
    predict_results = predict_results[0].split('__label__')[1]
    return predict_results


# K近邻算法
def knn_model(train, train_label, test, test_label):
    knn_model = KNeighborsClassifier(n_neighbors=8)
    knn_model.fit(train, train_label)
    predict_results = knn_model.predict(test)

    count = 0
    predict_list = predict_results.tolist()
    for i, pred in enumerate(predict_list):
        if (pred == test_label[i]):
            count += 1

    print("knn_model_precision_score: " + str(float(count) / len(predict_list)))


# 支持向量机算法
def svm_model(train, train_label, test, test_label):
    svm_clf = SVC(kernel="linear", verbose=False)
    svm_clf.fit(train, train_label)
    predict_results = svm_clf.predict(test)

    count = 0
    predict_list = predict_results.tolist()
    for i, pred in enumerate(predict_list):
        if (pred == test_label[i]):
            count += 1
    print("svm_model_precision_score: " + str(float(count) / len(predict_list)))


# 使用传统方法的文本分类
def text_classification(inputs):
    count = 0
    test_text_list = []
    train_text_list = []
    test_label_list = []
    train_label_list = []
    total_text_list = []
    total_label_list = []
    # 待测
    inputs_text_list = []
    inputs_text_list.append(inputs)

    print("start loading data...")
    finput = open("../data/data_train.txt", encoding='utf-8')
    for line in finput:
        count += 1
        text_array = line.split("\\t", 1)
        if (len(text_array) != 2):
            continue

        # 保存全部样本
        total_text_list.append(text_array[1])
        total_label_list.append(text_array[0])

        # 划分训练集和测试集
        probability = random.random()
        if (probability > 0.1):
            train_text_list.append(text_array[1])
            train_label_list.append(text_array[0])
        else:
            test_text_list.append(text_array[1])
            test_label_list.append(text_array[0])
    finput.close()
    print("load data is finished...")

    print("start building vector model...")
    # 构建词典
    vec_total = CountVectorizer()
    vec_total.fit_transform(total_text_list)

    # 基于构建的词典分别统计训练集/测试集词频, 即每个词出现1次、2次、3次等
    vec_train = CountVectorizer(vocabulary=vec_total.vocabulary_)
    tf_train = vec_train.fit_transform(train_text_list)

    vec_test = CountVectorizer(vocabulary=vec_total.vocabulary_)
    tf_test = vec_test.fit_transform(test_text_list)

    vec_inputs = CountVectorizer(vocabulary=vec_total.vocabulary_)
    tf_inputs = vec_inputs.fit_transform(inputs_text_list)

    # 进一步计算词频-逆文档频率
    tfidftransformer = TfidfTransformer()
    tfidf_train = tfidftransformer.fit(tf_train).transform(tf_train)
    tfidf_test = tfidftransformer.fit(tf_test).transform(tf_test)
    tfidf_inputs = tfidftransformer.fit(tf_inputs).transform(tf_inputs)
    print("building vector model is finished...")

    # 朴素贝叶斯算法
    nb_model(tfidf_train, train_label_list, tfidf_test, test_label_list)
    predict_result = nb_classfy_model(tfidf_train, train_label_list,tfidf_inputs)
    # K近邻算法
    # knn_model(tfidf_train, train_label_list, tfidf_test, test_label_list)
    # 支持向量机算法
    # svm_model(tfidf_train, train_label_list, tfidf_test, test_label_list)
    print("building predict model is finished...")
    return predict_result


industry_dict = ['农林牧渔','制造业','卫生医疗','商务服务','居民服务','建筑产业','房地产业','教育培训','文体娱乐',
                 '电信通讯','科学技术','租赁服务','维修服务','设计服务','运输物流','采矿工业','金融服务','餐饮住宿']


if __name__ == '__main__':
    print("贝叶斯文本分类...")
    stopword = ['、', '；', ', ', '。', '（', '，', '）', '++', '**', '*','[ ',']','【','】','：','国务院','部门','国家'
        ,'：','法律','法规','的','规定','决定','许可','批准','禁止不得','经营应当','审批经','审批',';无需市场主体','经营','机关后','自主',
                '选择','开展','活动','后方','相关','经','可','须','取得','无需市场主体',';','(',' )','有限公司']
    sql = "select enterpriseName,scopeOfBusiness,uniformSocialCreditCode from basic_info"

    # sql = "select * from basic_info"
    datas = MysqlOperate().read_data(sql)
    for data in datas:
        # inputs = '科技企业孵化；投资管理；高新技术开发、技术咨询、技术服务；计算机技术培训；出租办公用房；设计、制作、代理、发布国内各类广告；会议会展服务；企业咨询服务（不含民间借贷中介及证券、期货、保险、金融投资信息咨询）；企业管理服务；企业营销策划；教育咨询服务（依法须经批准的项目，经相关部门批准后方可开展经营活动）'
        inputs = data[1]
        inputs_array_list = []
        names = [w for w,f in pseg.cut(data[0]) if f !='ns' ]
        for word in jieba.lcut(inputs) + names:
            if word not in stopword:
                if len(word) >1:
                    inputs_array_list.append(word)
        inputs = ' '.join(inputs_array_list)
        print('企业名称：%s，输入语料：%s'%(data[0],inputs))
        predict = int(text_classification(inputs)) -1
        labels = industry_dict[predict]
        print('labels:',labels)
        query = "update basic_info set industry = '%s' where uniformSocialCreditCode = '%s'"%(labels,data[2])
        MysqlOperate().update_data(query)
        print("\n----------------------------------------------")