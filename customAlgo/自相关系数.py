import numpy as np
from envlop_xiao import env
import os
from Signal1_index import indexx
from Signal2_frequency import frequencyx
from 去滑雪坡特征 import ski_slope
# from mq.fs_table import FSTableService
from mydb.get_mongo import get_db
from preprocess  import *

# 相关系数
def update_mins_fj_signal_analysis_acf_cao_fix(data, fs, filetime='20251229180100', methods='raw'):
    # db = get_db()
    # group = int(group)
    # machine = int(machine)
    # component = int(component)
    # sensor = int(sensor)

    signal = []


    # 转速信号提取
    speed = 0
    speed = np.array([float(speed)])/60
    speed = np.round(speed, 5)
    # -------------------------   以下为之前读数据库的模式，需要被替换掉
    # data1 = list(collection.find({'machine': machine,'group':group,'component':component,'sensor':sensor}, {'vib':1,'speed':1}).sort([('datetime', -1)]).limit(1))[0]  # 改动
    # signal=data1.get('vib')
    signal=np.array(data)
    signal=(signal-np.mean(signal)).tolist()
    # fs = 25600
    blank_dict={}
    exec(f"blank_dict['out']={methods}(signal,fs)")
    Feaa=blank_dict['out'].tolist()


    T = indexx(RawSignal=Feaa, SampleFraquency=fs)
    Feax, Feay = T.sig_corr()

    result = {}
    # 原信号数据
    result['fea_y'] = Feaa
    length = len(Feaa)
    f_x1=ndarray2list0(np.arange(length)+1)
    f_x=[x / fs for x in f_x1]
    # f_x=[round(num,2) for num in f_x ]
    f_x=[round(num,5) for num in f_x ]
    result['fea_x'] = f_x
    # 自相关分析数据
    result['peak'] = (Feay).tolist()
    result['fea_xaxis'] = (Feax).tolist()

    # result['group'] = str(group)
    # result['machine'] = str(machine)
    # result['component'] = component
    # result['sensor'] = sensor


    # collection_group=db['group_data']
    # group_name = list(collection_group.find({'groupID': 'GR_' + str(group)}, {'name': 1}))

    # collection_machine=db['machine_data']
    # machine_name = list(collection_machine.find({'machineID': 'MA_'+ str(group) + '_' + str(machine)}, {'name': 1}))

    # collection_component=db['component_data']
    # component_name = list(collection_component.find({'componentID': 'CO_' + str(group)+ '_'+str(machine)+'_'+str(component)}, {'name': 1}))

    # collection_sensor=db['sensor_data']
    # sensor_name = list(collection_sensor.find({'sensorID': 'SE_' + str(group)+ '_'+str(machine)+'_'+str(component)+'_'+str(sensor)}, {'name': 1}))

    # group_name = group_name[0]['name']
    # machine_name = machine_name[0]['name']
    # component_name = component_name[0]['name']
    # sensor_name = sensor_name[0]['name']
    # result['group_name']=group_name
    # result['machine_name']=machine_name
    # result['component_name']=component_name
    # result['sensor_name']=sensor_name
    result['file']=""
    time_add = datetime.strptime(filetime.split('.')[0], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    result['time_add']=time_add
    speed=speed.tolist()
    result['speed']=speed
    #print("result: ", result)
    return result

if __name__ == '__main__':
    from mydb.get_mongo import get_db
    db = get_db()
    collection = db['pump_waveform_report']
    query = {
    'sensorId': 'SE_1_1_2_3',
    'time': '20251229180100'
    }
    document = collection.find_one(query)
    # 提取 fs 字段
    fs = document.get('fs')
    data = document.get('datas')
    update_mins_fj_signal_analysis_acf_cao_fix(data, fs, filetime='20251229180100', methods='raw')
