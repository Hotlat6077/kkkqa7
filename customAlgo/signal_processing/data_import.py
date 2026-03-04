import numpy as np

from signal_processing.Signal2_frequency import frequencyx

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
# 数据实时显示的def
def update_mins_data_import(path,group,machine,component,sensor,start_datatime,end_datatime):
    db = get_db()
    collection=db['vibration_data_import']
    group=int(group)
    machine=int(machine)
    component=str(component)
    sensor=str(sensor)
    start_datatime=str(start_datatime)
    end_datatime=str(end_datatime)
    data1 = list(collection.find({'machine': machine,'group':group,'component':component,'sensor':sensor}).sort([('datetime', -1)]).limit(1))[0]  # 改动
    signal= data1.get('vib')
    data = signal
    # 参数读取
    fs = int(data1.get('samplingfrequency'))
    Feax, Feay = frequencyx(RawSignal=data, SampleFraquency=fs).fftx()

    result= {}
    result['shiyu']=data
    length=len(data)
    result['fea_xaxis']=ndarray2list0(np.arange(length)+1)
    result['xxx'] = (Feax).tolist()
    result['yyy'] = (Feay).tolist()
    result['group'] = str(group)
    result['machine'] = str(machine)
    result['component'] = component
    result['sensor'] = sensor
    result['start_datatime'] = start_datatime
    result['end_datatime'] = end_datatime
    return result


