import numpy as np
from signal_processing.envlop_xiao import env
from signal_processing.Signal2_frequency import frequencyx
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
def update_mins_fj_signal_denoise4(path,group,machine,component,sensor):
    db = get_db()
    collection=db['vibration_data']
    group=int(group)
    machine=int(machine)
    component=int(component)
    sensor=int(sensor)
    data1 = list(collection.find({'machine': machine,'group':group,'component':component,'sensor':sensor}, {'vib':1,'speed':1}).sort([('datetime', -1)]).limit(1))[0]  # 改动
    signal=data1.get('vib')

    fs=1000
    T = frequencyx(RawSignal=signal, SampleFraquency=fs)
    Feal, Feam, Feah= T.hmlfrequencyx( )
    result= {}
    result['yy1']=Feal.tolist()
    length=len(Feal)
    result['xx1']=ndarray2list0(np.arange(length)+1)
    # # 频谱数据
    Fea1x, Fea1y = frequencyx(RawSignal=Feal, SampleFraquency=fs).fftx()
    Fea2x, Fea2y = frequencyx(RawSignal=Feam, SampleFraquency=fs).fftx()
    Fea3x, Fea3y = frequencyx(RawSignal=Feah, SampleFraquency=fs).fftx()

    # 原信号数据
    result['fea_y'] = signal
    length = len(signal)
    result['fea_x'] = ndarray2list0(np.arange(length)+1)

    result['xx2'] = (Fea1x).tolist()
    result['yy2'] = (Fea1y).tolist()

    result['group'] = str(group)
    result['machine'] = str(machine)
    result['component'] = component
    result['sensor'] = sensor
    return result






