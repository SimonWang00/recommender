#!/usr/bin/python3
# __*__ coding: utf-8 __*__

'''
@Author: simonKing
@License: (C) Copyright 2013-2019, Best Wonder Corporation Limited.
@Os：Windows 10 x64
@Contact: bw_wangxiaomeng@whty.com.cn
@Software: PY PyCharm 
@File: evaluationFunction.py
@Time: 2019/7/11 10:21
@Desc: define your function
'''
'''
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

日均开票次数：
10次及以上 --> 3;
5-10次     --> 2;
0-5次      --> 1;

日均开票金额：
1000及以上  --> 3;
100-1000    --> 2;
100以内     --> 1;
'''


import pandas as pd


def loadExcel(fname,index):
    '''
    从Excel 中导入数据
    :param fname:excel文件名
    :param index:导入的列
    :return:矩阵
    '''
    df = pd.read_excel(fname)
    return df.ix[:, index]

def R_eval(days):
    '''
    最近一次购买，分析最近的购买需求度，越小越好
    :param days:距离2019年7月最近一次购买天数
    :return:1-5
    '''
    if int(days) == -1:return 0
    if abs(days) <90:score = 5
    elif 90<= abs(days) < 180:score = 4
    elif 180<= abs(days) < 360:score = 3
    elif 360<= abs(days) < 720:score = 2
    elif abs(days) >= 720:score = 1
    else:raise  Exception('check days type. ERR')
    return score

def F_eval(times):
    '''
    购买频率打分，频率越高越忠诚，得分越高
    :param times:购买次数
    :return:1-5
    '''
    if abs(times) > 4:score = 5
    elif 3< abs(times) <= 4:score = 4
    elif 2< abs(times) <= 3:score = 3
    elif 1< abs(times) <= 2:score = 2
    elif 0< abs(times) <= 1:score = 1
    elif times ==0:score=0
    else:raise  Exception('check times type. ERR')
    return score

def M_eval(je):
    '''
    消费金额打分，得分越高贡献度越高
    :param je:金额
    :return:1-5
    '''
    if abs(je) >= 2000:score = 5
    elif 900<= abs(je) < 2000: score = 4
    elif 370<= abs(je) < 900:score = 3
    elif 200<= abs(je) < 370:score = 2
    elif 0< abs(je) < 200:score = 1
    elif abs(je) == 0: score = 0
    else:raise  Exception('check je type. ERR')
    return score

def ZB_eval(zczb):
    '''
    注册资本打分
    :param zczb:注册资本
    :return:1-5
    '''
    if abs(zczb) >= 1000:score = 5
    elif 500<= abs(zczb) < 1000:score = 4
    elif 100<= abs(zczb) < 500:score = 3
    elif 50<= abs(zczb) < 100:score = 2
    elif 0< abs(zczb) < 50:score = 1
    else:score = 0
    return score

def AGE_eval(age):
    '''
    公司成立日期打分，成立较短的打高分
    :param age:成立年限
    :return:打分2，1
    '''
    if abs(age) > 2:score = 1
    elif 0< abs(age) <= 2:score = 2
    elif abs(age) == 0: score = 0
    else:raise Exception('check age type. ERR')
    return score

def INDUSTRY_eval(indestry):
    '''
    行业分类打分，为了突出餐饮住宿、制造业，打分
    :param indestry:行业分类
    :return:行业分类打分3，2，1
    '''
    if indestry == '餐饮住宿':score = 3
    elif indestry == '制造业':score = 2
    else:score = 1
    return score

def LOGINS_eval(logins):
    '''
    日均登录次数打分
    :param logins:日均登录次数
    :return:打分1-5
    '''
    if abs(logins) >= 5:score = 5
    elif 4<= abs(logins) < 5:score = 4
    elif 3<= abs(logins) < 4:score = 3
    elif 2<= abs(logins) < 3:score = 2
    elif 0<  abs(logins) < 2:score = 1
    else:score = 0
    return score

def INVOICES_eval(invoices):
    '''
    日均开票次数打分
    :param invoices:日均开票次数
    :return:打分3，2，1
    '''
    if abs(invoices) >= 10:score = 3
    elif 5<= abs(invoices) < 10:score = 2
    elif 0< abs(invoices) < 5:score = 1
    else:score = 0
    return score

def INVOICEJE_eval(invoiceJe):
    '''
    日均开票金额打分
    :param invoiceJe: 日均开票金额
    :return: 分数 3，2，1
    '''
    if abs(invoiceJe) >= 1000:score = 3
    elif 100<= abs(invoiceJe) < 1000:score = 2
    elif 0< abs(invoiceJe) < 100:score = 1
    else:score = 0
    return score

def computeScore(scoreDic):
    '''
    根据每个用户评级dic 算出对产品的打分
    :param scoreDic:每个用户对商品的评级
    :return:对产品的打分
    '''
    if len(scoreDic) <1:raise Exception('scoreDic is none')
    if scoreDic.get('dayLoginTimes') == None:scoreDic['dayLoginTimes'] = 0
    score = scoreDic['recently'] * 1000 + scoreDic['je'] * 100 + scoreDic['times'] * 100 + \
            scoreDic['zczb'] * 10 + scoreDic['dayInvoiceNum'] * 10 + scoreDic['dayLoginTimes'] * 10 + \
            scoreDic['dayInvoiceJe'] * 10 + scoreDic['ages'] * 10 + scoreDic['industry'] * 1
    return score

def computeTotalScore(scoreDic):
    '''
    根据用户对所有商品的打分
    :param scoreDic:每个用户对所有商品的评级
    :return:对产品的打分
    index = ["times-wp","je-wp","recently-wp","times-bqt","je-bqt","recently-bqt","times-bft","je-bft","recently-bft","dayLoginTimes",
         "zczb","industry","ages","dayInvoiceNum","dayInvoiceJe"]
    '''
    if len(scoreDic) <1:raise Exception('scoreDic is none')
    if scoreDic.get('dayLoginTimes') == None:scoreDic['dayLoginTimes'] = 0
    score_common = scoreDic['registeredCapital'] * 10 + scoreDic['dayCountAvg'] * 30 + scoreDic['loginFrequency'] * 30 + \
            scoreDic['daySumAvg'] * 30 + scoreDic['dateOfEstablishment'] * 10 + scoreDic['industry'] * 10
    if scoreDic['deadline']==5: bft = 200 + (scoreDic['userConsumeTotalAmount'] + scoreDic['userConsumeTotalTimes'])* 50
    else:bft = 0
    if scoreDic['recently_bqt']==5: bqt = 100 + (scoreDic['je_bqt'] + scoreDic['times_bqt'])* 50
    else:bqt = 0
    if scoreDic['deadline_wp']==5: wp = 100 + (scoreDic['je_wp'] + scoreDic['times_wp'])* 50
    else:wp = 0
    score = bft + bqt + wp + score_common
    return score


def evaluationTotal(row,index):
    '''
    对输入的用户特征进行评价
    :param row:用户特征数据
    :param index:选择的列数
    :return:打分
    '''
    scoreDic = {}
    if len(row) != len(index):
        raise Exception('table header is incorrect')
    for i in index:
        if i == 'registeredCapital':
            zczb = int(row[i])
            score = ZB_eval(zczb)
            scoreDic['registeredCapital'] = score
        elif i =='industry':
            industry = row[i]
            score = INDUSTRY_eval(industry)
            scoreDic['industry'] = score
        elif i =='je':
            je = float(row[i])
            score = M_eval(je)
            scoreDic['je'] = score
        elif i =='times':
            times = int(row[i])
            score = F_eval(times)
            scoreDic['times'] = score
        elif i =='dayLoginTimes':
            dayLoginTimes = float(row[i])
            score = LOGINS_eval(dayLoginTimes)
            scoreDic['dayLoginTimes'] = score
        elif i =='dayInvoiceNum':
            dayInvoiceNum = float(row[i])
            score = INVOICES_eval(dayInvoiceNum)
            scoreDic['dayInvoiceNum'] = score
        elif i =='dayInvoiceJe':
            dayInvoiceJe = row[i]
            score = INVOICEJE_eval(dayInvoiceJe)
            scoreDic['dayInvoiceJe'] = score
        elif i =='ages':
            ages = float(row[i])
            score = AGE_eval(ages)
            scoreDic['ages'] = score
        elif i =='recently':
            recently = float(row[i])
            score = R_eval(recently)
            scoreDic['recently'] = score
    # print(scoreDic)
    SCORE = computeScore(scoreDic)
    return SCORE,scoreDic

def evaluationTotalProduct(row,index):
    '''
        对输入的用户所有特征进行评价
        :param row:用户特征数据
        :param index:选择的列数
        :return:打分
        '''
    scoreDic = {}
    scoreArr = []
    if len(row) != len(index):
        raise Exception('table header is incorrect')
    for i in index:
        if i == 'registeredCapital':
            try:
                zczb = float(row[i])
            except:
                zczb = 0
            score = ZB_eval(zczb)
            scoreDic['registeredCapital'] = score
        elif i == 'industry':
            industry = row[i]
            score = INDUSTRY_eval(industry)
            scoreDic['industry'] = score
        elif i == 'je_wp':
            je = float(row[i])
            score = M_eval(je)
            scoreDic['je_wp'] = score
        elif i == 'userConsumeTotalAmount':
            je = float(row[i])
            score = M_eval(je)
            scoreDic['userConsumeTotalAmount'] = score
        elif i == 'je_bqt':
            je = float(row[i])
            score = M_eval(je)
            scoreDic['je_bqt'] = score
        elif i == 'times_wp':
            times = int(row[i])
            score = F_eval(times)
            scoreDic['times_wp'] = score
        elif i == 'userConsumeTotalTimes':
            times = int(row[i])
            score = F_eval(times)
            scoreDic['userConsumeTotalTimes'] = score
        elif i == 'times_bqt':
            times = int(row[i])
            score = F_eval(times)
            scoreDic['times_bqt'] = score
        elif i == 'loginFrequency':
            dayLoginTimes = float(row[i])
            score = LOGINS_eval(dayLoginTimes)
            scoreDic['loginFrequency'] = score
        elif i == 'dayCountAvg':
            dayInvoiceNum = float(row[i])
            score = INVOICES_eval(dayInvoiceNum)
            scoreDic['dayCountAvg'] = score
        elif i == 'daySumAvg':
            dayInvoiceJe = row[i]
            score = INVOICEJE_eval(dayInvoiceJe)
            scoreDic['daySumAvg'] = score
        elif i == 'dateOfEstablishment':
            ages = float(row[i])
            score = AGE_eval(ages)
            scoreDic['dateOfEstablishment'] = score
        elif i == 'deadline_wp':
            recently = float(row[i])
            score = R_eval(recently)
            scoreDic['deadline_wp'] = score
        elif i == 'deadline':
            recently = float(row[i])
            score = R_eval(recently)
            scoreDic['deadline'] = score
        elif i == 'recently_bqt':
            recently = float(row[i])
            score = R_eval(recently)
            scoreDic['recently_bqt'] = score
        else:raise Exception('please check index is exist! err:',row)
        scoreArr.append(score)
    # print(scoreDic)
    return scoreArr

# if __name__ == '__main__':
#     # 准备数据
#     fname = r'D:\baiwang\21.数据运营\recommender\user_point\评价\方案2\bft_origin2.xlsx'
#     # 百赋通
#     index = ['tax_id','zczb','industry','je','times','dayLoginTimes','dayInvoiceNum','dayInvoiceJe','ages','recently']
#     # 百企通,旺票
#     # index = ['tax_id','zczb','industry','times','je','recently','ages','dayInvoiceNum','dayInvoiceJe']
#     # index = ['tax_id','zczb','industry','times','je','recently','ages','dayInvoiceNum','dayInvoiceJe']
#     data_origin = loadExcel(fname,index)
#
#     # 写入Excel
#     writer = pd.ExcelWriter('./bftClassfy.xlsx')
#     scoreArr = []
#     TaxidArr = []
#     zczbArr = []
#     industryArr = []
#     timesArr = []
#     dayLoginTimesArr = []
#     jeArr = []
#     recentlyArr = []
#     agesArr = []
#     dayInvoiceNumArr = []
#     dayInvoiceJeArr = []
#     # 逐行遍历
#     for i in range(len(data_origin)):
#         row = data_origin.iloc[i]
#         score,scoreDic = evaluationTotal(row, index)
#         TaxidArr.append(row['tax_id'])
#         scoreArr.append(score)
#         zczbArr.append(scoreDic.get('zczb'))
#         industryArr.append(scoreDic.get('industry'))
#         timesArr.append(scoreDic.get('times'))
#         jeArr.append(scoreDic.get('je'))
#         recentlyArr.append(scoreDic.get('recently'))
#         dayLoginTimesArr.append(scoreDic.get('dayLoginTimes'))
#         agesArr.append(scoreDic.get('ages'))
#         dayInvoiceNumArr.append(scoreDic.get('dayInvoiceNum'))
#         dayInvoiceJeArr.append(scoreDic.get('dayInvoiceJe'))
#         print(row['tax_id'],'score is:',score,'socreDict is:',scoreDic)
#     pd_taxid = pd.DataFrame({'tax_id': TaxidArr})
#     pd_score = pd.DataFrame({'score': scoreArr})
#     pd_zczb = pd.DataFrame({'zczb': zczbArr})
#     pd_industry = pd.DataFrame({'industry': industryArr})
#     pd_times = pd.DataFrame({'times': timesArr})
#     pd_je = pd.DataFrame({'je': jeArr})
#     pd_recently = pd.DataFrame({'recently': recentlyArr})
#     pd_dayLoginTimes = pd.DataFrame({'dayLoginTimes': dayLoginTimesArr})
#     pd_ages = pd.DataFrame({'ages': agesArr})
#     pd_dayInvoiceNum = pd.DataFrame({'dayInvoiceNum': dayInvoiceNumArr})
#     pd_dayInvoiceJe = pd.DataFrame({'dayInvoiceJe': dayInvoiceJeArr})
#     pd_taxid.to_excel(writer, sheet_name='Sheet1', startcol=0, index=False)
#     pd_score.to_excel(writer, sheet_name='Sheet1', startcol=1, index=False)
#     pd_zczb.to_excel(writer, sheet_name='Sheet1', startcol=2, index=False)
#     pd_industry.to_excel(writer, sheet_name='Sheet1', startcol=3, index=False)
#     pd_times.to_excel(writer, sheet_name='Sheet1', startcol=4, index=False)
#     pd_je.to_excel(writer, sheet_name='Sheet1', startcol=5, index=False)
#     pd_recently.to_excel(writer, sheet_name='Sheet1', startcol=6, index=False)
#     pd_dayLoginTimes.to_excel(writer, sheet_name='Sheet1', startcol=10, index=False)
#     pd_ages.to_excel(writer, sheet_name='Sheet1', startcol=7, index=False)
#     pd_dayInvoiceNum.to_excel(writer, sheet_name='Sheet1', startcol=8, index=False)
#     pd_dayInvoiceJe.to_excel(writer, sheet_name='Sheet1', startcol=9, index=False)
#     # 不加会报错
#     writer.save()
