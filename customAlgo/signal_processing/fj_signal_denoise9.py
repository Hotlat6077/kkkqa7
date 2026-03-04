
import numpy as np
from signal_processing.envlop_xiao import env
from signal_processing.Signal1_index import indexx
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
def update_mins_fj_signal_denoise9(path,group,machine,component,sensor):
    db = get_db()
    collection=db['vibration_data']
    group=int(group)
    machine=int(machine)
    component=int(component)
    sensor=int(sensor)
    data1 = list(collection.find({'machine': machine,'group':group,'component':component,'sensor':sensor}, {'vib':1,'speed':1}).sort([('datetime', -1)]).limit(1))[0]  # 改动
    signal=data1.get('vib')

    fs=1000
    T = indexx(RawSignal=signal, SampleFraquency=fs)
    Feay = T.ET()
    result= {}
    result['yy1']=signal
    length=len(Feay)
    result['xx1']=ndarray2list0(np.arange(length)+1)
    # # 剔除后数据
    result['xx2'] =  ndarray2list0(np.arange(length) + 1)
    result['yy2'] = (Feay).tolist()


    result['group'] = str(group)
    result['machine'] = str(machine)
    result['component'] = component
    result['sensor'] = sensor
    return result


def update_mins_zhaji3_export(path,sensor,machine):
    db = get_db()
    collection = db['vibration_data']
    machine = 'F1'
    sensor = 'Gearbox01'
    date3 = list(collection.find({'machine': machine}, {'dt': 1}))[0].get('dt')
    signal = list(collection.find({'machine': machine}, {sensor: 1}))[0].get(sensor)

    Fea = signal
    Feax, Feay = env(Fea)
    Feax = Feax[0:5000]
    Feay = Feay[0:5000]

    data = np.array(signal)
    str_data = data.astype(str)
    date = str(date3)
    file_date = date[0:4] + date[5:7] + date[8:10] + date[11:13] + date[14:16] + date[17:19]
    filename = f"中广核山东招远张星风电场_33_齿轮箱_低速轴径向_25600Hz_加速度_{file_date}.txt"
    desktop = config.desk_path
    full_path = os.path.join(desktop, filename)
    with open(full_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(str_data))

    filename2 = f"中广核山东招远张星风电场_33_齿轮箱_低速轴径向_25600Hz_包络谱_{file_date}.txt"
    full_path2 = os.path.join(desktop, filename2)
    str_datax = Feax.astype(str)
    str_datay = Feay.astype(str)
    with open(full_path2, 'w', encoding='utf-8') as file:
        for x, y in zip(str_datax, str_datay):
            file.write(f"{x}\t{y}\n")

    return {'message':'导出成功!'}





