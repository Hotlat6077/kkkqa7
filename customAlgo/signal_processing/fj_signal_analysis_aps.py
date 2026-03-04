
import numpy as np
import heapq  # 新增：用于提取最大幅值
from signal_processing.envlop_xiao import env
import os
from signal_processing.Signal2_frequency import frequencyx

from mq.fs_table import FSTableService
from mydb.get_mongo import get_db
from signal_processing.preprocess import *
import config
from frequency_test import theory_frequencies

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


def update_mins_fj_signal_analysis_aps(path, group, machine, component, sensor, file, localfilename, methods):
    db = get_db()
    collection = db['vibration_data']

    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)
    file = int(file)

    # 根据 file 值确定文件夹名称与采样频率
    if file == 2:
        temp_subsignal = '128K加速度波形'
        fs=2000*2.56
        fend=6410
    elif file == 1:
        temp_subsignal = '256K加速度波形'
        fs=10000*2.56
        fend=51203
    else:
        temp_subsignal = '16k速度波形'
        fs=1000*2.56
        fend=51282

    folder_path = config.local_data_path + f"/{group}/{machine}/{component}/{sensor}/{temp_subsignal}/"
    # 根据 localfilename 找到最近匹配文件
    nearest_file_name = find_closest_file(folder_path, '_'.join(localfilename.split('_')[:2]))
    signal_path = folder_path + f"/{nearest_file_name}"

    # 读取本地文件，得到振动信号
    with open(signal_path, 'r+') as f:
        data = f.readlines()[0]
    signal = [eval(i) for i in data.split(',')]

    # 从文件名中提取转速信息
    percent_index = nearest_file_name.find('%')
    if percent_index == -1:
        raise ValueError("文件名中未找到 '%' 符号，无法提取转速信息。")
    second_dot_index = nearest_file_name.find('.', percent_index + 1)
    if second_dot_index == -1:
        raise ValueError("文件名中未找到第二个 '.' 符号，无法提取转速信息。")
    third_dot_index = nearest_file_name.find('.', second_dot_index + 1)
    if third_dot_index == -1:
        raise ValueError("文件名中未找到第三个 '.' 符号，无法提取转速信息。")
    speed_str = nearest_file_name[percent_index + 1:third_dot_index]

    # 使用 numpy 进行简单处理，然后只在最后转成列表
    try:
        speed_array = np.array([float(speed_str)]) / 60
    except ValueError:
        raise ValueError(f"无法将提取的转速 '{speed_str}' 转换为浮点数。")
    speed_array = np.round(speed_array, 4)
    speed_list = speed_array.tolist()  # 最后一次性转为 Python 列表
    speed=speed_array
    ###############
    # files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    # file_pathn = [os.path.join(folder_path, f) for f in files]
    # latest_file_path = max(file_pathn, key=os.path.getmtime)
    # latest_file_name = os.path.basename(latest_file_path)
    # percent_pos = latest_file_name.find("%")
    # txt_pos = latest_file_name.find("txt")
    # speed2= latest_file_name[percent_pos + 1:txt_pos-1]
    # speed2 = float(speed2)
    # speed2 = np.array([speed2])/60
    # # speed2 = np.round(speed2, 4)
    # collectionspeed=db['sensor_data_2025']
    # fault_speedn = list(collectionspeed.find({'sensorID': f'SE_{group}_{machine}_{component}_{sensor}'}, {'hardpara': 1}))
    # fault_speedn=fault_speedn[0]['hardpara']
    # speed_nzero=fault_speedn['输入转速']
    # speed_nzero=np.array(speed_nzero)/60
    # speed_nzero = np.round([speed_nzero], 4)
    # # print('xxx',speed_nzero,speed2)
    # if speed2[0]==0:
    #     speed3=speed/speed_nzero
    # else:
    #     speed3=speed/speed2
    ######################

    # 对原始信号下采样并去均值
    signal = np.array(signal)
    signal = (signal - np.mean(signal)).tolist()

    # 执行自定义方法（由 methods 参数指定），得到 Feaa
    blank_dict = {}
    try:
        exec(f"blank_dict['out']={methods}(signal, fs)")
    except Exception as e:
        raise RuntimeError(f"执行方法 '{methods}' 时出错: {e}")
    Feaa = blank_dict['out'].tolist()

    # 进行自功率谱分析
    T = frequencyx(RawSignal=Feaa, SampleFraquency=fs)
    Feax, Feay = T.aps()

    result = {}
    # 原信号数据及其横坐标
    result['fea_y'] = Feaa
    length = len(Feaa)
    f_x1 = ndarray2list0(np.arange(length) + 1)
    f_x = [x / fs for x in f_x1]
    f_x=[round(num,2) for num in f_x ]
    result['fea_x'] = f_x

    # 自功率谱分析数据
    Feax = [int(num) for num in Feax]  # 根据您的需求保留整数
    result['fea_xaxis'] = Feax
    result['peak'] = Feay.tolist()

    # 当前特征频率
    if len(Feay) == 0:
        frequencyxxx = None
    else:
        frequencyxxx = round(Feax[np.argmax(Feay)], 2)
    result['frequencyxxx'] = frequencyxxx

    # -------------- 新增：提取频谱中幅值最大的 12 个点 --------------
    if len(Feay) < 12:
        largest_n = len(Feay)
    else:
        largest_n = 12
    largest_12 = heapq.nlargest(largest_n, enumerate(Feay), key=lambda x: x[1])
    if largest_n == 0:
        formatted_values = []
        formatted_positions = []
    else:
        indices, values = zip(*largest_12)
        # 根据索引获取对应频率
        positions = [Feax[i] for i in indices]

        # 幅值和位置分别保留小数位数
        formatted_values = [round(val, 4) for val in values]
        formatted_positions = [round(pos, 2) for pos in positions]

    result['formatted_values'] = formatted_values
    result['formatted_positions'] = formatted_positions
    # ---------------------------------------------------------

    # 拼接基本信息
    result['group'] = str(group)
    result['machine'] = str(machine)
    result['component'] = component
    result['sensor'] = sensor

    collection_group = db['group_data']
    group_doc = collection_group.find_one({'groupID': f'GR_{group}'}, {'name': 1})
    if not group_doc:
        raise ValueError(f"未找到 groupID: GR_{group} 的文档。")
    group_name = group_doc['name']

    collection_machine = db['machine_data']
    machine_doc = collection_machine.find_one({'machineID': f'MA_{group}_{machine}'}, {'name': 1})
    if not machine_doc:
        raise ValueError(f"未找到 machineID: MA_{group}_{machine} 的文档。")
    machine_name = machine_doc['name']

    collection_component = db['component_data']
    component_doc = collection_component.find_one(
        {'componentID': f'CO_{group}_{machine}_{component}'},
        {'name': 1}
    )
    if not component_doc:
        raise ValueError(f"未找到 componentID: CO_{group}_{machine}_{component} 的文档。")
    component_name = component_doc['name']

    collection_sensor = db['sensor_data']
    sensor_doc = collection_sensor.find_one(
        {'sensorID': f'SE_{group}_{machine}_{component}_{sensor}'},
        {'name': 1}
    )
    if not sensor_doc:
        raise ValueError(f"未找到 sensorID: SE_{group}_{machine}_{component}_{sensor} 的文档。")
    sensor_name = sensor_doc['name']

    result['group_name'] = group_name
    result['machine_name'] = machine_name
    result['component_name'] = component_name
    result['sensor_name'] = sensor_name
    result['file'] = file

    # 从 localfilename 中提取时间信息
    if len(localfilename) < 14:
        raise ValueError("localfilename 长度不足，无法提取时间信息。")
    time_add = localfilename[2:14]
    result['time_add'] = time_add

    # 将 speed 这个列表返回
    result['speed'] = speed_list

    collectionf = db['sensor_data_2025']
    ###############显示报警结论
    collectionfre = eval(f'db.indicator_data_{group}_{machine}')
    fault_txtn = list(collectionfre.find({'sensorID': f'SE_{group}_{machine}_{component}_{sensor}'}, {'faultstr': 1}))
    fault_txt = fault_txtn[-1] if len(fault_txtn) >= 1 else {}
    fault_txt = fault_txt.get('faultstr',"")
    result['fault_txt'] = fault_txt

    ##########0422
    frexx=str(theory_frequencies(group,machine,component,sensor,speed))
    frexxx=frexx.replace("{", "").replace("}", "")
    frexxxx =frexxx.replace("'", " ")
    result['xxxx']=frexxxx
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
    fault_fre = list(
        collectionf.find({'sensorID': f'SE_{group}_{machine}_{component}_{sensor}'}, {'faultfre': 1, 'hardware': 1}))
    fault_fre = fault_fre[0]['faultfre']
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
    if component == 2 and sensor == 4:
        filtered_keys = [k for k in fault_fre.keys() if not k.startswith("HSS")]
    else:
        filtered_keys = list(fault_fre.keys())

    # 自定义顺序，将'fm'放在第一位
    ordered_keys = []
    # 如果存在'fm'键，先添加它
    if 'fm' in filtered_keys:
        ordered_keys.append('fm')
        # 添加其他所有键（除了已添加的'fm'）
        ordered_keys.extend([k for k in filtered_keys if k != 'fm'])
    else:
        ordered_keys = filtered_keys

    fault_fre_txt = [fault_dict[k] for k in ordered_keys if k in fault_dict]
    fault_fre_values = [round(fault_fre[k], 2) for k in ordered_keys]

    # === 修改部分结束 ===

    result['fault_fre_txt'] = fault_fre_txt
    result['fault_fre_values'] = fault_fre_values


    return result




def update_mins_fj_signal_analysis_aps_cao_fix(group, machine, component, sensor, methods, file_name):
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

    # 从文件名中提取转速信息
    speed = 0
    speed = np.array([float(speed)]) / 60
    speed = np.round(speed, 4)
    # ##############
    # 数据 时间 FS 数据ID(设备编号 测点编号) 类型 raw
    # 对原始信号下采样并去均值
    signal = np.array(signal)
    signal = (signal - np.mean(signal)).tolist()

    # 执行自定义方法（由 methods 参数指定），得到 Feaa
    blank_dict = {}
    try:
        exec(f"blank_dict['out']={methods}(signal, fs)")
    except Exception as e:
        raise RuntimeError(f"执行方法 '{methods}' 时出错: {e}")
    Feaa = blank_dict['out'].tolist()

    # 进行自功率谱分析
    T = frequencyx(RawSignal=Feaa, SampleFraquency=fs)
    Feax, Feay = T.aps()

    result = {}
    # 原信号数据及其横坐标
    result['fea_y'] = Feaa
    length = len(Feaa)
    f_x1 = ndarray2list0(np.arange(length) + 1)
    f_x = [x / fs for x in f_x1]
    f_x=[round(num,2) for num in f_x ]
    result['fea_x'] = f_x

    # 自功率谱分析数据
    Feax = [int(num) for num in Feax]  # 根据您的需求保留整数
    result['fea_xaxis'] = Feax
    result['peak'] = Feay.tolist()

    # 当前特征频率
    if len(Feay) == 0:
        frequencyxxx = None
    else:
        frequencyxxx = round(Feax[np.argmax(Feay)], 2)
    result['frequencyxxx'] = frequencyxxx

    # -------------- 新增：提取频谱中幅值最大的 12 个点 --------------
    if len(Feay) < 12:
        largest_n = len(Feay)
    else:
        largest_n = 12
    largest_12 = heapq.nlargest(largest_n, enumerate(Feay), key=lambda x: x[1])
    if largest_n == 0:
        formatted_values = []
        formatted_positions = []
    else:
        indices, values = zip(*largest_12)
        # 根据索引获取对应频率
        positions = [Feax[i] for i in indices]

        # 幅值和位置分别保留小数位数
        formatted_values = [round(val, 4) for val in values]
        formatted_positions = [round(pos, 2) for pos in positions]

    result['formatted_values'] = formatted_values
    result['formatted_positions'] = formatted_positions
    # ---------------------------------------------------------

    # 拼接基本信息
    result['group'] = str(group)
    result['machine'] = str(machine)
    result['component'] = component
    result['sensor'] = sensor

    collection_group = db['group_data']
    group_doc = collection_group.find_one({'groupID': f'GR_{group}'}, {'name': 1})
    if not group_doc:
        raise ValueError(f"未找到 groupID: GR_{group} 的文档。")
    group_name = group_doc['name']

    collection_machine = db['machine_data']
    machine_doc = collection_machine.find_one({'machineID': f'MA_{group}_{machine}'}, {'name': 1})
    if not machine_doc:
        raise ValueError(f"未找到 machineID: MA_{group}_{machine} 的文档。")
    machine_name = machine_doc['name']

    collection_component = db['component_data']
    component_doc = collection_component.find_one(
        {'componentID': f'CO_{group}_{machine}_{component}'},
        {'name': 1}
    )
    if not component_doc:
        raise ValueError(f"未找到 componentID: CO_{group}_{machine}_{component} 的文档。")
    component_name = component_doc['name']

    collection_sensor = db['sensor_data']
    sensor_doc = collection_sensor.find_one(
        {'sensorID': f'SE_{group}_{machine}_{component}_{sensor}'},
        {'name': 1}
    )
    if not sensor_doc:
        raise ValueError(f"未找到 sensorID: SE_{group}_{machine}_{component}_{sensor} 的文档。")
    sensor_name = sensor_doc['name']

    result['group_name'] = group_name
    result['machine_name'] = machine_name
    result['component_name'] = component_name
    result['sensor_name'] = sensor_name
    result['file'] = ""

    time_add = datetime.strptime(file_name.split('.')[0], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    result['time_add'] = time_add

    # 将 speed 这个列表返回
    speed = speed.tolist()
    result['speed'] = speed

    collectionf = db['sensor_data_2025']
    ###############显示报警结论
    collectionfre = eval(f'db.indicator_data_{group}_{machine}')
    fault_txtn = list(collectionfre.find({'sensorID': f'SE_{group}_{machine}_{component}_{sensor}'}, {'faultstr': 1}))
    fault_txt = fault_txtn[-1] if len(fault_txtn) >= 1 else {}
    fault_txt = fault_txt.get('faultstr',"")
    result['fault_txt'] = fault_txt

    ##########0422
    frexx=str(theory_frequencies(group,machine,component,sensor,speed))
    frexxx=frexx.replace("{", "").replace("}", "")
    frexxxx =frexxx.replace("'", " ")
    result['xxxx']=frexxxx
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
    fault_fre = list(
        collectionf.find({'sensorID': f'SE_{group}_{machine}_{component}_{sensor}'}, {'faultfre': 1, 'hardware': 1}))
    if len(fault_fre) >= 1:
        fault_fre = fault_fre[0]['faultfre']
    else:
        fault_fre = {}
    ######

    # === 修改部分开始 ===
    # 如果 component==2 且 sensor==4，则过滤掉所有以 "HSS" 开头的键
    if component == 2 and sensor == 4:
        filtered_keys = [k for k in fault_fre.keys() if not k.startswith("HSS")]
    else:
        filtered_keys = list(fault_fre.keys())

    # 自定义顺序，将'fm'放在第一位
    ordered_keys = []
    # 如果存在'fm'键，先添加它
    if 'fm' in filtered_keys:
        ordered_keys.append('fm')
        # 添加其他所有键（除了已添加的'fm'）
        ordered_keys.extend([k for k in filtered_keys if k != 'fm'])
    else:
        ordered_keys = filtered_keys

    fault_fre_txt = [fault_dict[k] for k in ordered_keys if k in fault_dict]
    fault_fre_values = [round(fault_fre[k], 2) for k in ordered_keys]

    # === 修改部分结束 ===

    result['fault_fre_txt'] = fault_fre_txt
    result['fault_fre_values'] = fault_fre_values


    return result
