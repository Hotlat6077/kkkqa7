import heapq


import numpy as np
# from envlop_xiao import env
# import os
from Signal10_gearbox import gearboxx
from Signal2_frequency import frequencyx
# import config
# from mq.fs_table import FSTableService
from mydb.get_mongo import get_db
from preprocess import *
# from frequency_test import theory_frequencies



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



# 曹学勇修补 对应 最小熵反褶积
# def update_mins_fj_signal_analysis_MED_cao_fix(group, machine, component, sensor, methods, file_name):
def _to_scalar(x):
    """将可能为数组/列表的输入转为 Python 标量，避免 'only 0-dimensional arrays can be converted to Python scalars'"""
    if x is None:
        raise ValueError("输入不能为 None")
    arr = np.asarray(x)
    if arr.size == 0:
        raise ValueError("输入不能为空")
    return float(arr.ravel()[0])


def update_mins_fj_signal_analysis_MED_cao_fix(data, fs, methods='raw'):
    fs = _to_scalar(fs)
    # db = get_db()
    # group = int(group)
    # machine = int(machine)
    # component = int(component)
    # sensor = int(sensor)

    # fs = FSTableService.get_fs2(group, machine, component, sensor, file_name, db)
    # folder_path = config.local_data_path + f"/{group}/{machine}/{component}/{sensor}/"
    # signal = []
    # with open(f"{folder_path}/{file_name}", 'r+') as f:
    #     data = f.readlines()[0]
    #     signal.extend(list(map(float, data.split(','))))

    # 转速信号提取
    speed = 0
    speed = np.array([float(speed)]) / 60
    speed = np.round(speed, 4)
    ###############

    signal = np.array(data)
    signal = (signal - np.mean(signal)).tolist()
    blank_dict = {}
    exec(f"blank_dict['out']={methods}(signal,fs)")
    Feaa = blank_dict['out'].tolist()

    # permissions_collection = db['permissions']
    # permissions = permissions_collection.find_one({}, {"filterSize": 1, "termIter": 1, "termDelta": 1})
    permissions = {}
    filterSize = permissions.get("filterSize", 5) if permissions else 50
    termIter = permissions.get("termIter", 1) if permissions else 1
    termDelta = permissions.get("termDelta", 1) if permissions else 1
    T = gearboxx(RawSignal=Feaa, SampleFraquency=fs)
    Feax, Feay = T.medx(filterSize=filterSize, termIter=termIter, termDelta=termDelta)

    result = {}
    result['y1'] = signal
    length = len(signal)
    # result['x1'] = (np.arange(length) + 1).tolist()
    f_x1 = (np.arange(length) + 1).tolist()
    f_x = [x / fs for x in f_x1]
    f_x = [round(_to_scalar(num), 2) for num in f_x]
    result['x1'] = f_x

    # med数据
    result['y2'] = ndarray2list1(Feax)
    # print(result['yyy1'])
    length2 = len(ndarray2list1(Feax))
    # result['fea_xaxis2'] = ndarray2list0(np.arange(length2) + 1)
    f_x2 = ndarray2list0(np.arange(length) + 1)
    f_x2 = [x * 1000 / (fs / 4) for x in f_x2]
    result['fea_xaxis2'] = f_x2

    Z = frequencyx(RawSignal=Feax, SampleFraquency=fs)
    Feax2, Feay2 = Z.fftx()
    # 频谱
    # Feax2=Feax2.astype(int)
    Feax2 = np.round(Feax2, 3)
    result['fea_xaxis3'] = (Feax2).tolist()
    result['y3'] = (Feay2).tolist()

    # ------------------ 新增：提取频谱中幅值最大的 12 个点 ------------------
    largest_12 = heapq.nlargest(12, enumerate(Feay2), key=lambda x: x[1])
    if len(largest_12) >= 1:
        indices, values = zip(*largest_12)
    else:
        indices, values = [], []
    # 根据索引获取对应频率（确保为标量，避免多维数组导致 float() 报错）
    positions = [_to_scalar(Feax2[i]) for i in indices]
    values_scalar = [_to_scalar(v) for v in values]

    # 幅值和位置分别保留小数位数（用 np.round 避免 numpy 类型与 Python round 不兼容）
    formatted_values = [round(v, 4) for v in values_scalar]
    formatted_positions = [round(p, 2) for p in positions]

    result['formatted_values'] = formatted_values
    result['formatted_positions'] = formatted_positions
    # ---------------------------------------------------------

    # result['group'] = str(group)
    # result['machine'] = str(machine)
    # result['component'] = component
    # result['sensor'] = sensor

    # collection_group = db['group_data']
    # group_name = list(collection_group.find({'groupID': 'GR_' + str(group)}, {'name': 1}))

    # collection_machine = db['machine_data']
    # machine_name = list(collection_machine.find({'machineID': 'MA_' + str(group) + '_' + str(machine)}, {'name': 1}))

    # collection_component = db['component_data']
    # component_name = list(
    #     collection_component.find({'componentID': 'CO_' + str(group) + '_' + str(machine) + '_' + str(component)},
    #                               {'name': 1}))

    # collection_sensor = db['sensor_data']
    # sensor_name = list(collection_sensor.find(
    #     {'sensorID': 'SE_' + str(group) + '_' + str(machine) + '_' + str(component) + '_' + str(sensor)}, {'name': 1}))

    # group_name = group_name[0]['name']
    # machine_name = machine_name[0]['name']
    # component_name = component_name[0]['name']
    # sensor_name = sensor_name[0]['name']
    # result['group_name'] = group_name
    # result['machine_name'] = machine_name
    # result['component_name'] = component_name
    # result['sensor_name'] = sensor_name
    # result['file'] = ""
    # time_add = datetime.strptime(file_name.split('.')[0], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    # result['time_add'] = time_add
    speed = speed.tolist()
    result['speed'] = speed

    # collectionf = db['sensor_data_2025']
    ###############显示报警结论
    # collectionfre = eval(f'db.indicator_data_{group}_{machine}')
    # fault_txtn = list(collectionfre.find({'sensorID': f'SE_{group}_{machine}_{component}_{sensor}'}, {'faultstr': 1}))
    # fault_txt = fault_txtn[-1] if len(fault_txtn) >= 1 else {}
    # fault_txt = fault_txt.get('faultstr',"")
    # result['fault_txt'] = fault_txt

    ##########0422
    # frexx = str(theory_frequencies(group, machine, component, sensor, speed))
    # frexxx = frexx.replace("{", "").replace("}", "")
    # frexxxx = frexxx.replace("'", " ")
    # result['xxxx'] = frexxxx
    ############显示理论报警频率
    fault_dict = {
        'inner': '内圈报警频率：',
        'outer': '外圈报警频率：',
        'ball': '滚动体报警频率：',
        'sun': '太阳轮报警频率：',
        'planet': '行星轮报警频率：',
        'race': '齿圈报警频率：',
        'fm': '啮合频率报警频率：',
        'race1': '一级齿圈报警频率：',
        'race2': '二级齿圈报警频率：',
        'cage': '保持架报警频率：',
        'gear3b': '三级大齿轮报警频率：',
        'gear3s': '三级小齿轮报警频率：',
        'HIS_inner': 'HIS高速轴内圈报警频率：',
        'HIS_outer': 'HIS高速轴外圈报警频率：',
        'HIS_ball': 'HIS高速轴滚动体报警频率：',
        'HIS_cage': 'HIS高速轴保持架报警频率：',
        'HSS_inner': 'HSS高速轴内圈报警频率：',
        'HSS_outer': 'HSS高速轴外圈报警频率：',
        'HSS_ball': 'HSS高速轴滚动体报警频率：',
        'HSS_cage': 'HSS高速轴保持架报警频率：',
        'PL1_inner': 'PL1行星轮轴承内圈报警频率：',
        'PL1_outer': 'PL1行星轮轴承外圈报警频率：',
        'PL1_ball': 'PL1行星轮轴承滚动体报警频率：',
        'PL1_cage': 'PL1行星轮轴承保持架报警频率：',
        'PL2_inner': 'PL2行星轮轴承内圈报警频率：',
        'PL2_outer': 'PL2行星轮轴承外圈报警频率：',
        'PL2_ball': 'PL2行星轮轴承滚动体报警频率：',
        'PL2_cage': 'PL2行星轮轴承保持架报警频率：',
    }
    # fault_fre = list(
    #     collectionf.find({'sensorID': f'SE_{group}_{machine}_{component}_{sensor}'}, {'faultfre': 1, 'hardware': 1}))
    # if len(fault_fre) >= 1:
    #     fault_fre = fault_fre[0]['faultfre']
    # else:
    #     fault_fre = {}
    ######
    # speed3=speed3[0]
    # fault_fre = {key: round(value * speed3, 2) for key, value in fault_fre.items()}
    # print('xxxx',fault_fre)
    ########
    # parts = nearest_file_name.split('_')
    # N_time = parts[1].split('%')[0]
    # dtn = datetime.strptime(N_time, "%Y%m%d%H%M%S")
    # N_time2 = dtn.strftime("%Y-%m-%d %H:%M:%S")
    # N_time2 = datetime.strptime(N_time2, '%Y-%m-%d %H:%M:%S')

    # keys = list(fault_fre.keys())
    # fault_fre_values = list(fault_fre.values())
    # fault_fre_txt = [fault_dict[key] for key in keys if key in fault_dict]
    # fault_fre_values = [round(num, 2) for num in fault_fre_values]

    # fault_fre_values = [x * float(speed) for x in fault_fre_values]
    # fault_fre_values = [round(x, 3) for x in fault_fre_values]

    # === 修改部分开始 ===
    # 如果 component==2 且 sensor==4，则过滤掉所有以 "HSS" 开头的键
    # if component == 2 and sensor == 4:
    #     filtered_keys = [k for k in fault_fre.keys() if not k.startswith("HSS")]
    # else:
    #     filtered_keys = list(fault_fre.keys())

    # 自定义顺序，将'fm'放在第一位
    ordered_keys = []
    # 如果存在'fm'键，先添加它
    # if 'fm' in filtered_keys:
    #     ordered_keys.append('fm')
    #     # 添加其他所有键（除了已添加的'fm'）
    #     ordered_keys.extend([k for k in filtered_keys if k != 'fm'])
    # else:
    #     ordered_keys = filtered_keys

    fault_fre_txt = [fault_dict[k] for k in ordered_keys if k in fault_dict]
    # fault_fre_values = [round(fault_fre[k], 5) for k in ordered_keys]
    # === 修改部分结束 ===
    # === 修改部分结束 ===

    result['fault_fre_txt'] = fault_fre_txt
    # result['fault_fre_values'] = fault_fre_values
    print("result", result)
    return result


if __name__ == '__main__':
    from mydb.get_mongo import get_db
    db = get_db()
    # collection = db['pump_waveform_report']
    collection = db['pump_acc_test1']
    # 通过sensorId取信号原始数据
    query = {
        # 'sensorId':sesor_id,
         "reportTime":"20260202180139",
         "thingsModel": "wave_1_0_12",
         "serialNum":"3030191700"
    }
    print("query",query)
    document = collection.find_one(query)
    # 提取 fs 字段
    fs = document.get('fs')
    data = document.get('datas')
    res = update_mins_fj_signal_analysis_MED_cao_fix(data, fs, methods='raw')