import numpy as np
from signal_processing.envlop_xiao import env
import os
from signal_processing.Signal1_index import indexx
import config
from mq.fs_table import FSTableService
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
def update_mins_fj_signal_denoise2(path,group,machine,component,sensor):
    db = get_db()
    collection=db['vibration_data']
    group=int(group)
    machine=int(machine)
    component=int(component)
    sensor=int(sensor)
    data1 = list(collection.find({'machine': machine,'group':group,'component':component,'sensor':sensor}, {'vib':1,'speed':1}).sort([('datetime', -1)]).limit(1))[0]  # 改动
    signal=data1.get('vib')

    Fea=signal
    fs = FSTableService.get_fs2(group, machine, component, sensor, "", db)
    T = indexx(RawSignal=Fea, SampleFraquency=fs)
    t, Feay = T.time_domain_integral()
    t2, Feay2 = T.time_domain_integral2()

    result= {}
    # 原信号数据
    result['fea_y'] = Fea
    length = len(Fea)
    result['fea_x'] = ndarray2list0(np.arange(length)+1)
    # 一次积分
    result['xxx1'] = ndarray2list0(np.arange(length)+1)#(t).tolist()
    result['yyy1'] = (Feay).tolist()
    # 二次积分
    result['xxx2'] = ndarray2list0(np.arange(length)+1)#(t).tolist()
    result['yyy2'] = (Feay2).tolist()



    result['group'] = str(group)
    result['machine'] = str(machine)
    result['component'] = component
    result['sensor'] = sensor
    return result








