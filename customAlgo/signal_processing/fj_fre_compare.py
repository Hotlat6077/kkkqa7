import numpy as np

from mq.fs_table import FSTableService
from signal_processing.order_ana import *
from signal_processing.Signal2_frequency import frequencyx
import config
import os

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


def update_mins_fj_fre_compare1(group1, machine1, component1, sensor1, localfilename, NN):
    db = get_db()
    # collection=db['vibration_data']

    group1 = int(group1)
    machine1 = int(machine1)
    component1 = int(component1)
    sensor1 = int(sensor1)

    ######################
    temp_subsignal = '256K加速度波形'
    # signal_dir = config.local_data_path + f'/{group1}/{machine1}/{component1}/{sensor1}/{temp_subsignal}'
    # files = os.listdir(signal_dir)
    # if files:
    #     first_file_path = os.path.join(signal_dir, files[int(NN)])
    #     with open(first_file_path, 'r') as f:
    #         data = f.readlines()[0]
    #     signal1 = [float(i) for i in data.split(',')]
    # else:
    #     print("目录为空，没有文件。")
    folder_path = config.local_data_path + f"/{group1}/{machine1}/{component1}/{sensor1}/{temp_subsignal}/"
    print('xxx', folder_path)
    nearest_file_name = find_closest_file(folder_path, '_'.join(localfilename.split('_')[:3]))
    signal_path = folder_path + f"/{nearest_file_name}"
    with open(signal_path, 'r+') as f:
        data = f.readlines()[0]
    signal1 = [eval(i) for i in data.split(',')]

    signal1 = signal1[:]
    signal1 = np.array(signal1)
    signal1 = (signal1 - np.mean(signal1)).tolist()
    fs = 10000 * 2.56
    fend = 10000
    T = frequencyx(RawSignal=signal1, SampleFraquency=fs)
    Feax, Feay = T.envelopex()
    Feaox, Feaoy = T.fftx()

    Feax = np.round(Feax, 1)
    Feax = Feax.tolist()
    Feax = [num for num in Feax if num <= fend]
    Feaox = np.round(Feaox, 1)
    Feaox = Feaox.tolist()
    Feaox = [num for num in Feaox if num <= fend]

    result = {}
    # 原信号数据1
    result['fea_y'] = signal1
    length = len(signal1)
    result['fea_x'] = ndarray2list0(np.arange(length) + 1)

    result['env'] = (Feay).tolist()
    # Feax=Feax.astype(int)
    result['fea_xaxis'] = Feax

    result['or1'] = (Feaoy).tolist()
    # Feaox=Feaox.astype(int)
    result['orx1'] = Feaox

    result['group1'] = group1
    result['machine1'] = machine1
    result['component1'] = component1
    result['sensor1'] = sensor1

    collection_group1 = db['group_data']
    group_name1 = list(collection_group1.find({'groupID': 'GR_' + str(group1)}, {'name': 1}))

    collection_machine1 = db['machine_data']
    machine_name1 = list(
        collection_machine1.find({'machineID': 'MA_' + str(group1) + '_' + str(machine1)}, {'name': 1}))

    collection_component1 = db['component_data']
    component_name1 = list(
        collection_component1.find({'componentID': 'CO_' + str(group1) + '_' + str(machine1) + '_' + str(component1)},
                                   {'name': 1}))

    collection_sensor1 = db['sensor_data']
    sensor_name1 = list(collection_sensor1.find(
        {'sensorID': 'SE_' + str(group1) + '_' + str(machine1) + '_' + str(component1) + '_' + str(sensor1)},
        {'name': 1}))

    group_name1 = group_name1[0]['name']
    machine_name1 = machine_name1[0]['name']
    component_name1 = component_name1[0]['name']
    sensor_name1 = sensor_name1[0]['name']
    result['group_name1'] = group_name1
    result['machine_name1'] = machine_name1
    result['component_name1'] = component_name1
    result['sensor_name1'] = sensor_name1

    return result


def update_mins_fj_fre_compare2(group2, machine2, component2, sensor2, localfilename, NN):
    db = get_db()
    # collection=db['vibration_data']
    fs = 10000 * 2.56
    fend = 10000
    # print(localfilename)

    group2 = int(group2)
    machine2 = int(machine2)
    component2 = int(component2)
    sensor2 = int(sensor2)

    ######################
    temp_subsignal = '256K加速度波形'
    folder_path = config.local_data_path + f"/{group2}/{machine2}/{component2}/{sensor2}/{temp_subsignal}/"
    print('xxx', folder_path)
    nearest_file_name = find_closest_file(folder_path, '_'.join(localfilename.split('_')[:3]))
    signal_path = folder_path + f"/{nearest_file_name}"
    with open(signal_path, 'r+') as f:
        data = f.readlines()[0]
    signal2 = [eval(i) for i in data.split(',')]
    signal2 = signal2[:]
    signal2 = np.array(signal2)
    signal2 = (signal2 - np.mean(signal2)).tolist()
    T = frequencyx(RawSignal=signal2, SampleFraquency=fs)
    Feax2, Feay2 = T.envelopex()
    Feaox2, Feaoy2 = T.fftx()

    Feax2 = np.round(Feax2, 1)
    Feax2 = Feax2.tolist()
    Feax2 = [num for num in Feax2 if num <= fend]
    Feaox2 = np.round(Feaox2, 1)
    Feaox2 = Feaox2.tolist()
    Feaox2 = [num for num in Feaox2 if num <= fend]

    result = {}

    Feax2 = np.round(Feax2, 1)
    Feax2 = Feax2.tolist()
    Feax2 = [num for num in Feax2 if num <= fend]
    Feaox2 = np.round(Feaox2, 1)
    Feaox2 = Feaox2.tolist()
    Feaox2 = [num for num in Feaox2 if num <= fend]
    # 原信号数据2
    result['fea_y2'] = signal2
    length2 = len(signal2)
    result['fea_x2'] = ndarray2list0(np.arange(length2) + 1)

    result['env2'] = (Feay2).tolist()
    # Feax2=Feax2.astype(int)
    result['fea_xaxis2'] = Feax2

    result['or2'] = (Feaoy2).tolist()
    # Feaox2=Feaox2.astype(int)
    result['orx2'] = Feaox2

    result['group2'] = group2
    result['machine2'] = machine2
    result['component2'] = component2
    result['sensor2'] = sensor2

    collection_group2 = db['group_data']
    group_name2 = list(collection_group2.find({'groupID': 'GR_' + str(group2)}, {'name': 1}))

    collection_machine2 = db['machine_data']
    machine_name2 = list(
        collection_machine2.find({'machineID': 'MA_' + str(group2) + '_' + str(machine2)}, {'name': 1}))

    collection_component2 = db['component_data']
    component_name2 = list(
        collection_component2.find({'componentID': 'CO_' + str(group2) + '_' + str(machine2) + '_' + str(component2)},
                                   {'name': 1}))

    collection_sensor2 = db['sensor_data']
    sensor_name2 = list(collection_sensor2.find(
        {'sensorID': 'SE_' + str(group2) + '_' + str(machine2) + '_' + str(component2) + '_' + str(sensor2)},
        {'name': 1}))

    group_name2 = group_name2[0]['name']
    machine_name2 = machine_name2[0]['name']
    component_name2 = component_name2[0]['name']
    sensor_name2 = sensor_name2[0]['name']
    result['group_name2'] = group_name2
    result['machine_name2'] = machine_name2
    result['component_name2'] = component_name2
    result['sensor_name2'] = sensor_name2

    return result


def update_mins_fj_fre_compare3(group1, machine1, component1, sensor1, localfilename):
    db = get_db()
    group1 = int(group1)
    machine1 = int(machine1)
    component1 = int(component1)
    sensor1 = int(sensor1)
    # print('xxx',group1,machine1,component1,sensor1,localfilename)

    ######################
    temp_subsignal = '256K加速度波形'

    folder_path = config.local_data_path + f"/{group1}/{machine1}/{component1}/{sensor1}/{temp_subsignal}/"

    nearest_file_name = find_closest_file(folder_path, '_'.join(localfilename.split('_')[:3]))
    signal_path = folder_path + f"/{nearest_file_name}"
    with open(signal_path, 'r+') as f:
        data = f.readlines()[0]
    signal1 = [eval(i) for i in data.split(',')]

    signal1 = signal1[:]
    signal1 = np.array(signal1)
    signal1 = (signal1 - np.mean(signal1)).tolist()

    fs = 10000 * 2.56
    fend = 10000
    T = frequencyx(RawSignal=signal1, SampleFraquency=fs)
    Feax, Feay = T.envelopex()
    Feaox, Feaoy = T.fftx()

    Feax = np.round(Feax, 1)
    Feax = Feax.tolist()
    Feax = [num for num in Feax if num <= fend]
    Feaox = np.round(Feaox, 1)
    Feaox = Feaox.tolist()
    Feaox = [num for num in Feaox if num <= fend]

    result = {}
    # 原信号数据1
    result['fea_y'] = signal1

    length = len(signal1)
    result['fea_x'] = ndarray2list0(np.arange(length) + 1)

    result['env'] = (Feay).tolist()
    # Feax=Feax.astype(int)
    result['fea_xaxis'] = Feax

    result['or1'] = (Feaoy).tolist()
    # Feaox=Feaox.astype(int)
    result['orx1'] = Feaox

    result['group1'] = group1
    result['machine1'] = machine1
    result['component1'] = component1
    result['sensor1'] = sensor1

    collection_group1 = db['group_data']
    group_name1 = list(collection_group1.find({'groupID': 'GR_' + str(group1)}, {'name': 1}))

    collection_machine1 = db['machine_data']
    machine_name1 = list(
        collection_machine1.find({'machineID': 'MA_' + str(group1) + '_' + str(machine1)}, {'name': 1}))

    collection_component1 = db['component_data']
    component_name1 = list(
        collection_component1.find({'componentID': 'CO_' + str(group1) + '_' + str(machine1) + '_' + str(component1)},
                                   {'name': 1}))

    collection_sensor1 = db['sensor_data']
    sensor_name1 = list(collection_sensor1.find(
        {'sensorID': 'SE_' + str(group1) + '_' + str(machine1) + '_' + str(component1) + '_' + str(sensor1)},
        {'name': 1}))

    group_name1 = group_name1[0]['name']
    machine_name1 = machine_name1[0]['name']
    component_name1 = component_name1[0]['name']
    sensor_name1 = sensor_name1[0]['name']
    result['group_name'] = group_name1
    result['machine_name'] = machine_name1
    result['component_name'] = component_name1
    result['sensor_name'] = sensor_name1

    time_add = localfilename[2:14]
    print(time_add)
    result['time_add'] = time_add

    return result


# 曹学勇修补 对应标签页 频域对比页面
def update_mins_fj_fre_compare3_fix(group1, machine1, component1, sensor1, file_name):
    db = get_db()
    group1 = int(group1)
    machine1 = int(machine1)
    component1 = int(component1)
    sensor1 = int(sensor1)
    ######################

    folder_path = config.local_data_path + f"/{group1}/{machine1}/{component1}/{sensor1}"
    signal1 = []
    # 检查文件是否存在
    if not os.path.exists(folder_path + "/" + file_name):
        print("当前没有的文件", folder_path + "/" + file_name)
        return {}

    with open(f"{folder_path}/{file_name}", 'r+') as f:
        data = f.readlines()[0]
        signal1.extend(list(map(float, data.split(','))))

    signal1 = np.array(signal1)  # 1.
    signal1 = (signal1 - np.mean(signal1)).tolist()  # 2.

    fs = FSTableService.get_fs2(group1, machine1, component1, sensor1, file_name, db)  # 3.
    fend = 10000
    T = frequencyx(RawSignal=signal1, SampleFraquency=fs)  # 4. 获取频谱
    Feax, Feay = T.envelopex()  # 5.
    Feaox, Feaoy = T.fftx()  # 6.

    Feax = np.round(Feax, 1)  # 7.
    Feax = Feax.tolist()  # 8.
    # Feax = [num for num in Feax if num <= fend]
    Feaox = np.round(Feaox, 1)  # 9.
    Feaox = Feaox.tolist()  # 10.
    # Feaox = [num for num in Feaox if num <= fend]

    result = {}
    # 原信号数据1
    result['fea_y'] = signal1  # 11.y

    length = len(signal1)  #
    result['fea_x'] = ndarray2list0(np.arange(length) + 1)  # 12.x

    result['env'] = (Feay).tolist()  # 13.
    # Feax=Feax.astype(int)
    result['fea_xaxis'] = Feax  # 14.

    result['or1'] = (Feaoy).tolist()  # 15.
    # Feaox=Feaox.astype(int)
    result['orx1'] = Feaox  # 16.

    result['group1'] = group1
    result['machine1'] = machine1
    result['component1'] = component1
    result['sensor1'] = sensor1

    collection_group1 = db['group_data']
    group_name1 = list(collection_group1.find({'groupID': 'GR_' + str(group1)}, {'name': 1}))

    collection_machine1 = db['machine_data']
    machine_name1 = list(
        collection_machine1.find({'machineID': 'MA_' + str(group1) + '_' + str(machine1)}, {'name': 1}))

    collection_component1 = db['component_data']
    component_name1 = list(
        collection_component1.find(
            {'componentID': 'CO_' + str(group1) + '_' + str(machine1) + '_' + str(component1)},
            {'name': 1}))

    collection_sensor1 = db['sensor_data']
    sensor_name1 = list(collection_sensor1.find(
        {'sensorID': 'SE_' + str(group1) + '_' + str(machine1) + '_' + str(component1) + '_' + str(sensor1)},
        {'name': 1}))

    group_name1 = group_name1[0]['name']
    machine_name1 = machine_name1[0]['name']
    component_name1 = component_name1[0]['name']
    sensor_name1 = sensor_name1[0]['name']
    result['group_name'] = group_name1
    result['machine_name'] = machine_name1
    result['component_name'] = component_name1
    result['sensor_name'] = sensor_name1

    time_add = datetime.strptime(file_name.split('.')[0], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    result['time_add'] = time_add

    return result
