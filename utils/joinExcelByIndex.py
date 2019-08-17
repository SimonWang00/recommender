#!/usr/bin/python3
# __*__ coding: utf-8 __*__

'''
@Author: simonKing
@License: (C) Copyright 2013-2019, Best Wonder Corporation Limited.
@Os：Windows 10 x64
@Contact: bw_wangxiaomeng@whty.com.cn
@Software: PY PyCharm 
@File: joinExcelByIndex.py
@Time: 2019/7/4 10:43
@Desc: define your function
'''

import pandas as pd
from pandas import DataFrame


def concat_excels(xlsx1,xlsx2,index):
    '''
    根据字段名合并表格
    :param xlsx1:输入excel表格1；
    :param xlsx2:输入excel表格2；
    :param index:合并的字段名
    :return:输出合并后的表格
    '''
    if '.xlsx' not in xlsx1:
        raise Exception('输入文件类型有误！')
    if '.xlsx' not in xlsx2:
        raise Exception('输入文件类型有误！')
    data1 = pd.read_excel(xlsx1, sheet_name='Sheet1', dtype={index: str})
    df_obj1 = DataFrame(data1)
    data2 = pd.read_excel(xlsx2, sheet_name='Sheet1', dtype={index: str})
    data2 = data2.drop_duplicates([index])
    df_obj2 = DataFrame(data2)

    excel = pd.merge(df_obj1, df_obj2, on=index,how='outer')
    excel_list = [excel]
    total_excel = pd.concat(excel_list)
    # total_excel = excel_list.set_index('cate_tp').T.to_dict('list')
    total_excel.to_excel('../user_point/tice20190717.xlsx', index=False)
    return

# if __name__ =='__main__':
#     pass
#     index = 'tax_id'
#     xs1 = r'D:\invoice1.xlsx'
#     xs2 = r'D:\invoice2.xlsx'
#     concat_excels(xs1,xs2,index)