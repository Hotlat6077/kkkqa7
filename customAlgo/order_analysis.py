import numpy as np
import heapq

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

def order_analysis(vibration_signal, sampling_frequency, rpm):
    rpm=[float(rpm)]
    rpm=rpm*100
    rps = np.array(rpm)
    t = np.arange(len(vibration_signal)) / sampling_frequency
    rps_interp = np.interp(t, np.linspace(0, t[-1], len(rps)), rps)
    inst_phase = np.cumsum(rps_interp) / sampling_frequency * 2 * np.pi
    resampled_signal = np.interp(np.linspace(0, inst_phase[-1], len(vibration_signal)), inst_phase, vibration_signal)
    freqs = np.fft.fftfreq(len(resampled_signal), d=1 / sampling_frequency)
    fft_values = np.fft.fft(resampled_signal)
    pos_freqs = freqs[:len(freqs) // 2]
    pos_fft_values = np.abs(fft_values[:len(fft_values) // 2])
    return pos_freqs, pos_fft_values

# 阶次分析
def update_mins_fj_signal_analysis_14_cao_fix(data, fs, methods):

    signal = []


    signal = np.array(data)
    signal = (signal - np.mean(signal)).tolist()

    # 转速信号提取
    speed = 0
    speed = np.array([float(speed)]) / 60
    speed = np.round(speed, 4)
    ######################

    blank_dict = {}
    exec(f"blank_dict['out']={methods}(signal,fs)")
    signal = blank_dict['out'].tolist()

    Feax, Feay = order_analysis(signal, fs, speed)

    result = {}
    # # ------谐波标注------

    # 原信号数据
    result['fea_y'] = signal
    length = len(signal)
    f_x1 = ndarray2list0(np.arange(length) + 1)
    f_x = [x / fs for x in f_x1]
    f_x = [round(num, 2) for num in f_x]
    result['fea_x'] = f_x
    # 阶次分析

    # Feax=Feax.astype(int)
    Feax = np.round(Feax, 3)
    Feax = Feax.tolist()
    # Feax=[num for num in Feax if num <= fend]
    result['fea_xaxis'] = Feax
    LL = len(Feax)
    Feay = Feay[0:LL] / 100000
    result['fea_y2'] = Feay.tolist()
    # result['hw'] = str(hw)
    # result['faults'] = fault_type
    # result['group'] = str(group)
    # result['machine'] = str(machine)
    # result['component'] = component
    # result['sensor'] = sensor
    # collectionf = db['sensor_data_2025']
    ##############显示报警结论
    # collectionfre = eval(f'db.indicator_data_{group}_{machine}')
    # fault_txtn = list(collectionfre.find({'sensorID': f'SE_{group}_{machine}_{component}_{sensor}'}, {'faultstr': 1}))
    # fault_txt = fault_txtn[-1] if len(fault_txtn) >= 1 else {}
    fault_txt = fault_txt.get('faultstr',"")
    result['fault_txt'] = fault_txt

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

    if len(fault_fre) >= 1:
        fault_fre = fault_fre[0]['faultfre']
    else:
        fault_fre = {}
    ######
    # speed3=speed3[0]
    # fault_fre = {key: round(value * speed3, 2) for key, value in fault_fre.items()}
    # print('xxxx',fault_fre)
    ########
    # keys = list(fault_fre.keys())
    # fault_fre_values = list(fault_fre.values())
    # fault_fre_txt = [fault_dict[key] for key in keys if key in fault_dict]
    # fault_fre_values = [round(num, 2) for num in fault_fre_values]
    # # fault_fre_values = [x * float(speed) for x in fault_fre_values]
    # # fault_fre_values = [round(x, 3) for x in fault_fre_values]

    # === 修复部分开始 ===
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
    fault_fre_values = [round(fault_fre[k], 2) for k in ordered_keys]
    # === 修改部分结束 ===

    result['fault_fre_txt'] = fault_fre_txt
    result['fault_fre_values'] = fault_fre_values

    ######################谐波标注
    fault_txt_list = fault_txt.split('\t')
    fault_txt_list = [item for item in fault_txt_list if item]  # 所有预警的小部件
    result['fault_txt_list'] = fault_txt_list
    #####所有预警的频率
    faultfre_dict = {
        '内圈报警': 'inner',
        '外圈报警': 'inner',
        '滚动体报警': 'ball',
        '太阳轮报警': 'sun',
        '行星轮报警': 'planet',
        '齿圈报警': 'race',
        '啮合频率报警': 'fm',
        '一级齿圈报警': 'race1',
        '二级齿圈报警': 'race2',
        '保持架报警': 'cage',
        '三级大齿轮报警': 'gear3b',
        '三级小齿轮报警': 'gear3s',
        'HIS高速轴内圈报警': 'HIS_inner',
        'HIS高速轴外圈报警': 'HIS_outer',
        'HIS高速轴滚动体报警': 'HIS_ball',
        'HIS高速轴保持架报警': 'HIS_cage',
        'HSS高速轴内圈报警': 'HSS_inner',
        'HSS高速轴外圈报警': 'HSS_outer',
        'HSS高速轴滚动体报警': 'HSS_ball',
        'HSS高速轴保持架报警': 'HSS_cage',
        'PL1行星轮轴承内圈报警': 'PL1_inner',
        'PL1行星轮轴承外圈报警': 'PL1_outer',
        'PL1行星轮轴承滚动体报警': 'PL1_ball',
        'PL1行星轮轴承保持架报警': 'PL1_cage',
        'PL2行星轮轴承内圈报警': 'PL2_inner',
        'PL2行星轮轴承外圈报警': 'PL2_outer',
        'PL2行星轮轴承滚动体报警': 'PL2_ball',
        'PL2行星轮轴承保持架报警': 'PL2_cage',
    }
    fre_v = [faultfre_dict.get(key) for key in fault_txt_list]
    selected_values = {key: fault_fre[key] for key in fre_v if key in fault_fre}
    selected_values = list(selected_values.values())
    fault_frev = [round(num, 2) for num in selected_values]

    #######边频添加
    # print(fault_txt_list,fault_frev)
    Mdic = dict(zip(fault_txt_list, fault_frev))
    if '啮合频率报警' in Mdic:
        # 获取 '啮合频率报警' 对应的值
        meshing_fault_value = Mdic['啮合频率报警']
        # 获取 '行星轮报警' 和 '太阳轮报警' 对应的值
        planetary_fault_value = Mdic['行星轮报警']
        sun_fault_value = Mdic['太阳轮报警']
        # 计算 '边频1' 和 '边频2'
        sideband1 = meshing_fault_value - 5 * planetary_fault_value
        sideband2 = meshing_fault_value - 5 * sun_fault_value
        sideband3 = meshing_fault_value + 5 * planetary_fault_value
        sideband4 = meshing_fault_value + 5 * sun_fault_value
        # 将 '边频1' 和 '边频2' 添加到字典中
        Mdic['边频1'] = sideband1
        Mdic['边频2'] = sideband2
        Mdic['边频3'] = sideband3
        Mdic['边频4'] = sideband4
        fault_txt_list = [key for key, value in Mdic.items()]
        fault_frev = [value for key, value in Mdic.items()]

    #######
    for i, value in enumerate(fault_txt_list):
        key = f"fault_txt_list_{i + 1}"
        result[key] = value

    for i, value in enumerate(fault_frev):
        key = f"fault_frev_{i + 1}"
        result[key] = value

    result['maxnum'] = len(fault_frev)

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

    group_name = group_name[0]['name']
    machine_name = machine_name[0]['name']
    component_name = component_name[0]['name']
    sensor_name = sensor_name[0]['name']
    result['group_name'] = group_name
    result['machine_name'] = machine_name
    result['component_name'] = component_name
    result['sensor_name'] = sensor_name
    result['file'] = ""
    # time_add = datetime.strptime(file_name.split('.')[0], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    # result['time_add'] = time_add
    speed = speed.tolist()
    result['speed'] = speed

    largest_12 = heapq.nlargest(12, enumerate(Feay), key=lambda x: x[1])
    if len(largest_12) >= 1:
        indices, values = zip(*largest_12)
    else:
        indices, values = [], []

    values_positions = [Feax[i] for i in indices]
    largest_12 = [item for sublist in largest_12 for item in sublist]
    formatted_values = [round(num, 4) for num in largest_12]
    formatted_positions = [round(num, 2) for num in values_positions]
    formatted_values = formatted_values[1::2]
    result['formatted_values'] = formatted_values
    result['formatted_positions'] = formatted_positions

    return result
