
import numpy as np
from data_all_liu import get_thr
import datetime
import os
import config
from mydb.get_mongo import get_db


def ndarray2list0(data):
    list0=[]
    for temp in data:
        list0.append(temp.tolist())
    return list0
def ndarray2list1(data):
    list0=[]
    for temp in data:
        list0.append(temp.tolist())
    list1=[]
    for i in list0:
        for j in i:
            list1.append(j)
    return list1
def histor_pri(query_order,machine,sensor):
    signal1=[]
    signal2=[]
    signal3=[]
    signal4=[]
    signal5=[]
    signal6=[]
    signal7=[]
    signal8=[]
    db = get_db()
    collection2=db['indicator_data'] ## 改成后台自动算
    start_time = query_order.get("start_time")
    end_time = query_order.get("end_time")
    if start_time and end_time:
        start_time_format = str(start_time)
        end_time_format = str(end_time)
        result = {'fea_xaxis': []}

        result_list1 = list(collection2.find({"$and": [{"date": {"$gte": start_time_format,"$lte": end_time_format}},
                                                       {'machine': int(machine),'sensor': int(sensor)}]},
                                                       {'acc': 1,'resonate': 1,'date':1,'peak': 1,'acc_2': 1,'resonate_2': 1,'peak_2': 1,'kur':1,'kur_2':1}))
        for i in range(0,len(result_list1)):
            signal1.append(result_list1[i].get('acc'))
            signal2.append(result_list1[i].get('resonate'))
            signal3.append(result_list1[i].get('acc_2'))
            signal4.append(result_list1[i].get('resonate_2'))
            signal5.append(result_list1[i].get('peak'))
            signal6.append(result_list1[i].get('peak_2'))
            signal7.append(result_list1[i].get('kur'))
            signal8.append(result_list1[i].get('kur_2'))
            result['fea_xaxis'].append(result_list1[i].get(('date')))

    signal1 = [item for sublist in signal1 for item in sublist]
    signal2 = [item for sublist in signal2 for item in sublist]
    signal3 = [item for sublist in signal3 for item in sublist]
    signal4 = [item for sublist in signal4 for item in sublist]
    signal5 = [item for sublist in signal5 for item in sublist]
    signal6 = [item for sublist in signal6 for item in sublist]
    signal7 = [item for sublist in signal7 for item in sublist]
    signal8 = [item for sublist in signal8 for item in sublist]


    result['trend1'] = signal1
    result['trend2'] = signal2
    result['trend3'] = signal3
    result['trend4'] = signal4
    result['trend5'] = signal5
    result['trend6'] = signal6
    result['trend7'] = signal7
    result['trend8'] = signal8

    return result




