
import numpy as np
from signal_processing.envlop_xiao import env
import os
from signal_processing.Signal2_frequency import frequencyx
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


def update_mins_fj_signal_analysis7(path, group, machine, component, sensor, file, localfilename, methods):
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

    temp_subsignal = '128K加速度波形'
    folder_path = config.local_data_path + f"/{group}/{machine}/{component}/{sensor}/{temp_subsignal}/"
    print("111111111111111111")
    print(config.local_data_path)
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
    signal = (signal - np.mean(signal)).tolist()
    # fs = 25600
    blank_dict = {}
    exec(f"blank_dict['out']={methods}(signal,fs)")
    Feaa = blank_dict['out'].tolist()

    T = frequencyx(RawSignal=Feaa, SampleFraquency=fs)
    Fea1y = T.cepstrumx()

    result = {}
    # 原信号数据
    result['fea_y'] = Feaa
    length = len(Feaa)
    f_x1 = ndarray2list0(np.arange(length) + 1)
    f_x = [x / fs for x in f_x1]
    f_x = [round(num, 2) for num in f_x]
    result['fea_x'] = f_x

    result['cyy'] = Fea1y.tolist()
    length2 = len(Fea1y)
    # result['fea_xaxis'] = ndarray2list0(np.arange(length2)+1)
    f_x2 = ndarray2list0(np.arange(length2) + 1)
    f_x2 = [x * 1000 / (fs / 4) for x in f_x2]
    result['fea_xaxis'] = f_x2

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


# 曹学用修补
def update_mins_fj_signal_analysis7_cao_fix(group, machine, component, sensor, methods, file_name):
    db = get_db()
    fs = FSTableService.get_fs2(group, machine, component, sensor, file_name, db)
    folder_path = config.local_data_path + f"/{group}/{machine}/{component}/{sensor}/"
    signal = []
    with open(f"{folder_path}/{file_name}", 'r+') as f:
        data = f.readlines()[0]
        signal.extend(list(map(float, data.split(','))))

    signal = np.array(signal)
    signal = (signal - np.mean(signal)).tolist()
    blank_dict = {}
    exec(f"blank_dict['out']={methods}(signal,fs)")
    Feaa = blank_dict['out'].tolist()

    T = frequencyx(RawSignal=Feaa, SampleFraquency=fs)
    Fea1y = T.cepstrumx()

    result = {}
    # 原信号数据
    result['fea_y'] = Feaa
    length = len(Feaa)
    f_x1 = ndarray2list0(np.arange(length) + 1)
    f_x = [x / fs for x in f_x1]
    f_x = [round(num, 2) for num in f_x]
    result['fea_x'] = f_x

    result['cyy'] = Fea1y.tolist()
    length2 = len(Fea1y)
    # result['fea_xaxis'] = ndarray2list0(np.arange(length2)+1)
    f_x2 = ndarray2list0(np.arange(length2) + 1)
    f_x2 = [x * 1000 / (fs / 4) for x in f_x2]
    result['fea_xaxis'] = f_x2

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
    result['file'] = ""  # file
    # time_add=localfilename[2:14]
    time_add = datetime.strptime(file_name.split('.')[0], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    result['time_add'] = time_add
    # speed=speed.tolist()
    speed = 0
    result['speed'] = speed
    return result
