
import numpy as np
from signal_processing.envlop_xiao import env
import os
from signal_processing.Signal1_index import indexx
from signal_processing.Signal3_timefrequency import *
import config
from mq.fs_table import FSTableService
from mydb.get_mongo import get_db
from signal_processing.preprocess import *


def ndarray2list0(data):
    list0 = []
    for temp in data:
        list0.append(temp.tolist())
    return list0


def ndarray2list1(data):
    list0 = []
    for temp in data:
        list0.append(temp.tolist())
    list1 = []
    for i in list0:
        for j in i:
            list1.append(j)
    return list1


def update_mins_fj_signal_analysis_fft3d(path, group, machine, component, sensor, file, localfilename, methods):
    db = get_db()
    collection = db['vibration_data']
    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)
    file = int(file)
    temp_subsignal = ''
    if file == 2:
        temp_subsignal = '128K加速度波形'
        fs = 2000 * 2.56
        fend = 6410
    elif file == 1:
        temp_subsignal = '256K加速度波形'
        fs = 10000 * 2.56
        fend = 51203
    else:
        temp_subsignal = '16k速度波形'
        fs = 1000 * 2.56
        fend = 51282
    # temp_subsignal = '128K加速度波形'
    folder_path = config.local_data_path + f"/{group}/{machine}/{component}/{sensor}/{temp_subsignal}/"
    nearest_file_name = find_closest_file(folder_path, '_'.join(localfilename.split('_')[:2]))
    signal_path = folder_path + f"/{nearest_file_name}"
    with open(signal_path, 'r+') as f:
        data = f.readlines()[0]
    signal = [eval(i) for i in data.split(',')]
    # 转速信号提取
    percent_index = nearest_file_name.find('%')
    second_dot_index = nearest_file_name[percent_index + 1:].find('.') + percent_index + 1 + 1
    third_dot_index = nearest_file_name.find('.', second_dot_index + 1)
    speed = nearest_file_name[percent_index + 1:third_dot_index]
    speed = np.array([float(speed)]) / 60
    speed = np.round(speed, 4)
    # -------------------------   以下为之前读数据库的模式，需要被替换掉
    # data1 = list(collection.find({'machine': machine,'group':group,'component':component,'sensor':sensor}, {'vib':1,'speed':1}).sort([('datetime', -1)]).limit(1))[0]  # 改动
    # signal=data1.get('vib')
    signal = np.array(signal)
    data = (signal - np.mean(signal)).tolist()

    Fea = np.array(data).flatten()
    # 参数读取
    speed = speed
    fs = int(fs)
    n = len(Fea)
    chunk_size = n // 8  # 计算每段长度
    Fea = Fea[:8 * chunk_size]  # 截断多余数据

    # 使用列表存储结果（推荐方式）
    Feax_list, Feay_list = [], []
    for i in range(8):
        segment = Fea[i * chunk_size: (i + 1) * chunk_size]
        Feax, Feay = timefrequencyx(RawSignal=segment, SampleFraquency=fs).fftxx()
        Feax_list.append(Feax)
        Feay_list.append(Feay)
    #######
    Feaz1 = [1 for _ in range(len(Feay_list[0]) - 1)]
    a = Feay_list[0]
    ddata = []
    y = len(Feaz1)
    for j in range(y):
        temp = [1, j, abs(a[j])]
        ddata.append(temp)

    Feaz2 = [1 for _ in range(len(Feay_list[1]) - 1)]
    a2 = Feay_list[1]
    ddata2 = []
    y2 = len(Feaz2)
    for j in range(y2):
        temp = [2, j, abs(a2[j])]
        ddata2.append(temp)

    Feaz3 = [1 for _ in range(len(Feay_list[2]) - 1)]
    a3 = Feay_list[2]
    ddata3 = []
    y3 = len(Feaz3)
    for j in range(y3):
        temp = [3, j, abs(a3[j])]
        ddata3.append(temp)

    Feaz4 = [1 for _ in range(len(Feay_list[3]) - 1)]
    a4 = Feay_list[3]
    ddata4 = []
    y4 = len(Feaz4)
    for j in range(y4):
        temp = [4, j, abs(a4[j])]
        ddata4.append(temp)

    Feaz5 = [1 for _ in range(len(Feay_list[4]) - 1)]
    a5 = Feay_list[4]
    ddata5 = []
    y5 = len(Feaz5)
    for j in range(y5):
        temp = [5, j, abs(a5[j])]
        ddata5.append(temp)

    Feaz6 = [1 for _ in range(len(Feay_list[5]) - 1)]
    a6 = Feay_list[5]
    ddata6 = []
    y6 = len(Feaz6)
    for j in range(y6):
        temp = [6, j, abs(a6[j])]
        ddata6.append(temp)

    Feaz7 = [1 for _ in range(len(Feay_list[6]) - 1)]
    a7 = Feay_list[6]
    ddata7 = []
    y7 = len(Feaz7)
    for j in range(y7):
        temp = [7, j, abs(a7[j])]
        ddata7.append(temp)

    Feaz8 = [1 for _ in range(len(Feay_list[7]) - 1)]
    a8 = Feay_list[7]
    ddata8 = []
    y8 = len(Feaz8)
    for j in range(y8):
        temp = [8, j, abs(a8[j])]
        ddata8.append(temp)

    result = {}
    result['ddata'] = ddata
    result['ddata2'] = ddata2
    result['ddata3'] = ddata3
    result['ddata4'] = ddata4
    result['ddata5'] = ddata5
    result['ddata6'] = ddata6
    result['ddata7'] = ddata7
    result['ddata8'] = ddata8

    result['group'] = str(group)
    result['machine'] = str(machine)
    result['component'] = component
    result['sensor'] = sensor

    collection_group = db['group_data']
    group_name = list(collection_group.find({'groupID': 'GR_' + str(group)}, {'name': 1}))

    collection_machine = db['machine_data']
    machine_name = list(collection_machine.find({'machineID': 'MA_' + str(group) + '_' + str(machine)}, {'name': 1}))

    collection_component = db['component_data']
    component_name = list(
        collection_component.find({'componentID': 'CO_' + str(group) + '_' + str(machine) + '_' + str(component)},
                                  {'name': 1}))

    collection_sensor = db['sensor_data']
    sensor_name = list(collection_sensor.find(
        {'sensorID': 'SE_' + str(group) + '_' + str(machine) + '_' + str(component) + '_' + str(sensor)}, {'name': 1}))

    group_name = group_name[0]['name']
    machine_name = machine_name[0]['name']
    component_name = component_name[0]['name']
    sensor_name = sensor_name[0]['name']
    result['group_name'] = group_name
    result['machine_name'] = machine_name
    result['component_name'] = component_name
    result['sensor_name'] = sensor_name
    result['file'] = file
    time_add = localfilename[2:14]
    result['time_add'] = time_add
    speed = speed.tolist()
    result['speed'] = speed
    return result


# 曹学勇修补
def update_mins_fj_signal_analysis_fft3d_cao_fix(group, machine, component, sensor, methods, file_name):
    db = get_db()
    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)
    fs = FSTableService.get_fs2(group, machine, component, sensor, file_name, db)
    folder_path = config.local_data_path + f"/{group}/{machine}/{component}/{sensor}/"
    signal = []
    with open(f"{folder_path}/{file_name}", 'r+') as f:
        data = f.readlines()[0]
        signal.extend(list(map(float, data.split(','))))

    # 转速信号提取
    speed = 0
    speed = np.array([float(speed)]) / 60
    speed = np.round(speed, 4)
    # -------------------------   以下为之前读数据库的模式，需要被替换掉
    # data1 = list(collection.find({'machine': machine,'group':group,'component':component,'sensor':sensor}, {'vib':1,'speed':1}).sort([('datetime', -1)]).limit(1))[0]  # 改动
    # signal=data1.get('vib')
    signal = np.array(signal)
    data = (signal - np.mean(signal)).tolist()

    Fea = np.array(data).flatten()
    # 参数读取
    speed = speed
    fs = int(fs)
    n = len(Fea)
    chunk_size = n // 8  # 计算每段长度
    Fea = Fea[:8 * chunk_size]  # 截断多余数据

    # 使用列表存储结果（推荐方式）
    Feax_list, Feay_list = [], []
    for i in range(8):
        #这个没有数据的情况
        segment = Fea[i * chunk_size: (i + 1) * chunk_size]
        if len(segment) >= 1:
            Feax, Feay = timefrequencyx(RawSignal=segment, SampleFraquency=fs).fftxx()
            Feax_list.append(Feax)
            Feay_list.append(Feay)
        else:
            Feax_list.append([])
            Feay_list.append([])
    #######
    Feaz1 = [1 for _ in range(len(Feay_list[0]) - 1)]
    a = Feay_list[0]
    ddata = []
    y = len(Feaz1)
    for j in range(y):
        temp = [1, j, abs(a[j])]
        ddata.append(temp)

    Feaz2 = [1 for _ in range(len(Feay_list[1]) - 1)]
    a2 = Feay_list[1]
    ddata2 = []
    y2 = len(Feaz2)
    for j in range(y2):
        temp = [2, j, abs(a2[j])]
        ddata2.append(temp)

    Feaz3 = [1 for _ in range(len(Feay_list[2]) - 1)]
    a3 = Feay_list[2]
    ddata3 = []
    y3 = len(Feaz3)
    for j in range(y3):
        temp = [3, j, abs(a3[j])]
        ddata3.append(temp)

    Feaz4 = [1 for _ in range(len(Feay_list[3]) - 1)]
    a4 = Feay_list[3]
    ddata4 = []
    y4 = len(Feaz4)
    for j in range(y4):
        temp = [4, j, abs(a4[j])]
        ddata4.append(temp)

    Feaz5 = [1 for _ in range(len(Feay_list[4]) - 1)]
    a5 = Feay_list[4]
    ddata5 = []
    y5 = len(Feaz5)
    for j in range(y5):
        temp = [5, j, abs(a5[j])]
        ddata5.append(temp)

    Feaz6 = [1 for _ in range(len(Feay_list[5]) - 1)]
    a6 = Feay_list[5]
    ddata6 = []
    y6 = len(Feaz6)
    for j in range(y6):
        temp = [6, j, abs(a6[j])]
        ddata6.append(temp)

    Feaz7 = [1 for _ in range(len(Feay_list[6]) - 1)]
    a7 = Feay_list[6]
    ddata7 = []
    y7 = len(Feaz7)
    for j in range(y7):
        temp = [7, j, abs(a7[j])]
        ddata7.append(temp)

    Feaz8 = [1 for _ in range(len(Feay_list[7]) - 1)]
    a8 = Feay_list[7]
    ddata8 = []
    y8 = len(Feaz8)
    for j in range(y8):
        temp = [8, j, abs(a8[j])]
        ddata8.append(temp)

    result = {}
    result['ddata'] = ddata
    result['ddata2'] = ddata2
    result['ddata3'] = ddata3
    result['ddata4'] = ddata4
    result['ddata5'] = ddata5
    result['ddata6'] = ddata6
    result['ddata7'] = ddata7
    result['ddata8'] = ddata8

    result['group'] = str(group)
    result['machine'] = str(machine)
    result['component'] = component
    result['sensor'] = sensor

    collection_group = db['group_data']
    group_name = list(collection_group.find({'groupID': 'GR_' + str(group)}, {'name': 1}))

    collection_machine = db['machine_data']
    machine_name = list(collection_machine.find({'machineID': 'MA_' + str(group) + '_' + str(machine)}, {'name': 1}))

    collection_component = db['component_data']
    component_name = list(
        collection_component.find({'componentID': 'CO_' + str(group) + '_' + str(machine) + '_' + str(component)},
                                  {'name': 1}))

    collection_sensor = db['sensor_data']
    sensor_name = list(collection_sensor.find(
        {'sensorID': 'SE_' + str(group) + '_' + str(machine) + '_' + str(component) + '_' + str(sensor)}, {'name': 1}))

    group_name = group_name[0]['name']
    machine_name = machine_name[0]['name']
    component_name = component_name[0]['name']
    sensor_name = sensor_name[0]['name']
    result['group_name'] = group_name
    result['machine_name'] = machine_name
    result['component_name'] = component_name
    result['sensor_name'] = sensor_name
    result['file'] = ""
    time_add = datetime.strptime(file_name.split('.')[0], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    result['time_add'] = time_add
    speed = speed.tolist()
    result['speed'] = speed
    return result
