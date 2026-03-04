from __future__ import annotations
import heapq
import config
from frequency_test import theory_frequencies
from mq.fs_table import FSTableService
from mydb.get_mongo import get_db
from signal_processing.Signal2_frequency import frequencyx
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


def update_mins_fj_signal_analysis_HE(path, group, machine, component, sensor, file, localfilename, methods):
    db = get_db()
    collection = db['vibration_data']
    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)
    file = int(file)

    temp_subsignal = ''  # 加速度波形
    if file == 2:
        temp_subsignal = '128K加速度波形'
        fs = 2000 * 2.56
        fend = 2000
    elif file == 1:
        temp_subsignal = '256K加速度波形'
        fs = 10000 * 2.56
        fend = 10000
    else:
        temp_subsignal = '16k速度波形'
        fs = 1000 * 2.56
        fend = 1000
    # temp_subsignal = '128K加速度波形'
    folder_path = config.local_data_path + f"/{group}/{machine}/{component}/{sensor}/{temp_subsignal}/"
    nearest_file_name = find_closest_file(folder_path, '_'.join(localfilename.split('_')[:3]))
    signal_path = folder_path + f"/{nearest_file_name}"

    with open(signal_path, 'r+') as f:
        data = f.readlines()[0]
    signal = [eval(i) for i in data.split(',')]

    percent_index = nearest_file_name.find('%')
    second_dot_index = nearest_file_name[percent_index + 1:].find('.') + percent_index + 1 + 1
    third_dot_index = nearest_file_name.find('.', second_dot_index + 1)
    speed = nearest_file_name[percent_index + 1:third_dot_index]  #
    speed = np.array([float(speed)]) / 60
    speed = np.round(speed, 4)
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
    # print('xxxx',speed,speed2,speed3)
    ######################

    # 不会对数据进行抽取，而是保留了完整的原始采样点
    signal = np.array(signal)
    signal = (signal - np.mean(signal)).tolist()
    blank_dict = {}
    exec(f"blank_dict['out']={methods}(signal,fs)")
    Feaa = blank_dict['out'].tolist()

    T = frequencyx(RawSignal=Feaa, SampleFraquency=fs)
    Feax, Feay = T.envelopex()  # 包络的频谱 包络的单边频谱peak
    H = T.envelopexx()
    result = {}
    # 原信号数据
    result['fea_y'] = H.tolist()
    length = len(H)
    f_x1 = ndarray2list0(np.arange(length) + 1)
    f_x = [x / fs for x in f_x1]  # 长度/fs
    f_x = [round(num, 2) for num in f_x]  # fx 取小数点2位
    result['fea_x'] = f_x  # 频率

    result['peak'] = Feay.tolist()

    Feax = np.round(Feax, 3)

    # Feax=Feax.astype(int)
    Feax = Feax.tolist()
    Fea11x = [num for num in Feax if num <= fend]
    result['fea_xaxis'] = Fea11x

    result['group'] = str(group)
    result['machine'] = str(machine)
    result['component'] = component
    result['sensor'] = sensor
    collectionf = db['sensor_data_2025']
    # #############显示报警结论
    collectionfre = eval(f'db.indicator_data_{group}_{machine}')
    fault_txtn = list(collectionfre.find({'sensorID': f'SE_{group}_{machine}_{component}_{sensor}'}, {'faultstr': 1}))
    fault_txt = fault_txtn[-1]
    fault_txt = fault_txt.get('faultstr', "")
    result['fault_txt'] = fault_txt
    # #########0422
    frexx = str(theory_frequencies(group, machine, component, sensor, speed))
    frexxx = frexx.replace("{", "").replace("}", "")
    frexxxx = frexxx.replace("'", " ")
    result['xxxx'] = frexxxx
    # ###########显示理论报警频率
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
    # print('xxxx',fault_fre)
    # #####
    # speed3=speed3[0]
    # fault_fre = {key: round(value * speed3, 2) for key, value in fault_fre.items()}

    # #######
    # parts = nearest_file_name.split('_')
    # N_time = parts[1].split('%')[0]
    # dtn = datetime.strptime(N_time, "%Y%m%d%H%M%S")
    # N_time2 = dtn.strftime("%Y-%m-%d %H:%M:%S")
    # N_time2 = datetime.strptime(N_time2, '%Y-%m-%d %H:%M:%S')

    # keys = list(fault_fre.keys())
    # fault_fre_values = list(fault_fre.values())
    # fault_fre_txt = [fault_dict[key] for key in keys if key in fault_dict]
    # fault_fre_values=[round(num, 2) for num in fault_fre_values]

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
    # === 修改部分结束 ===

    result['fault_fre_txt'] = fault_fre_txt
    result['fault_fre_values'] = fault_fre_values

    # #####################谐波标注
    fault_txt_list = fault_txt.split('\t')
    fault_txt_list = [item for item in fault_txt_list if item]  # 所有预警的小部件
    result['fault_txt_list'] = fault_txt_list
    # ####所有预警的频率
    faultfre_dict = {
        '内圈报警': 'inner',
        '外圈报警': 'outer',
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

    # ######边频添加
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

    # ######
    for i, value in enumerate(fault_txt_list):
        key = f"fault_txt_list_{i + 1}"
        result[key] = value

    for i, value in enumerate(fault_frev):
        key = f"fault_frev_{i + 1}"
        result[key] = value
    result['maxnum'] = len(fault_frev)

    # #######################################
    show_values = [item[1] for item in fault_fre.items()]
    show_values2 = show_values + [x * 2 for x in show_values]
    result['maxnum2'] = len(show_values2)
    result['show_values2'] = show_values2
    # print(show_values2)
    # #########################################

    # print(result['fault_txt_list_4'],result['fault_txt_list_5'],result['fault_txt_list_6'],result['fault_txt_list_7'])

    # 直方图
    middata = list(fault_fre.items())[:4]
    middata = [value for key, value in middata]
    result['middata'] = middata
    # print(middata)

    # ##################################################### 显示工厂信息
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

    result['speed'] = speed.tolist()

    largest_12 = heapq.nlargest(12, enumerate(Feay), key=lambda x: x[1])
    indices, values = zip(*largest_12)
    values_positions = [Feax[i] for i in indices]
    largest_12 = [item for sublist in largest_12 for item in sublist]
    formatted_values = [round(num, 4) for num in largest_12]
    formatted_positions = [round(num, 2) for num in values_positions]
    formatted_values = formatted_values[1::2]
    result['formatted_values'] = formatted_values
    result['formatted_positions'] = formatted_positions

    return result


#  包络图 更新方法 曹学勇修补对应故障诊断页面
def update_mins_fj_signal_analysis_HE_cao_fix(group, machine, component, sensor, methods, file_name):
    db = get_db()
    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)
    # 这里直接从数据库获取了fs 这里就是传感器参数 就是一个数字
    fs = FSTableService.get_fs2(group, machine, component, sensor, file_name, db)
    # 这里是拿到传感器数据  现在是以文件的形式保存的
    folder_path = config.local_data_path + f"/{group}/{machine}/{component}/{sensor}/"
    signal = []
    # 读取数据 
    with open(f"{folder_path}/{file_name}", 'r+') as f:
        data = f.readlines()[0]
        signal.extend(list(map(float, data.split(','))))
    # 对速度进行处理 这里都是0的话 做什么处理
    speed = 0
    speed = np.array([float(speed)]) / 60
    speed = np.round(speed, 4)

    # 不会对数据进行抽取，而是保留了完整的原始采样点 yij wq im e p tkh wgk wq klj shn b
    # http://222.242.225.73:6100/fj_signal_analysis_HE_data?group_type=GR_1&machine_type=MA_1_1&component_type=CO_1_1_1&
    # sensor_type=SE_1_1_1_1&localfilename=2025-12-07+00%3A07&method_type=raw&real_data=
    signal = np.array(signal)  # 1.列表转为数组
    signal = (signal - np.mean(signal)).tolist()  # 2.将成numpy数组转换列表 这里这个numpy数据的列表怎么没有用到呢
    blank_dict = {}  # 3.创建一个空字典
    exec(f"blank_dict['out']={methods}(signal,fs)")
    """
    这里是执行了raw这个方法 方法的参数是signal fs得到的是vib
    def raw(vib, fs):
        vib = np.array(vib)
        fs = fs
        return vib
    """
    Feaa = blank_dict['out'].tolist()  # feaa 就是上面的methods执行得到的结果 vib 字典输出为数组numpy转化成别的数组
    # 这里是实例化 了这个frequency 出现次数；频繁；频率
    T = frequencyx(RawSignal=Feaa, SampleFraquency=fs)  # 3.这是一个频率的类里面有很多处理数据的方法
    Feax, Feay = T.envelopex()  # 4.包络谱分析方法在frequencyx里
    # H = T.envelopexx() # 5. 这个envelopexx方法在frequencyx没找到是打错字了么
    H = T.envelopex()  # 5. 这个envelopex方法在frequencyx没找到是打错字了么
    result = {}
    # 原信号数据
    result['fea_y'] = H.tolist()  # 6. H是T.envelopex()方法返回的
    length = len(H)  # H的长度 信号的长度
    f_x1 = ndarray2list0(np.arange(length) + 1)  # 7. 先转Numpy 再转数组长度 H的长度转numpy数组 转列表
    f_x = [x / fs for x in f_x1]  # 8.长度/fs 长度/FS是什么意思啊
    f_x = [round(num, 2) for num in f_x]  # 9. f_x 是上面的f_x变成 2位小数 后装到列表里
    result['fea_x'] = f_x  # 10.fea_x可能是x轴

    result['peak'] = Feay.tolist()  # 10.peak是峰值 表示包络的峰值么

    Feax = np.round(Feax, 3)  # 11.这里是取3位小数

    # Feax=Feax.astype(int)
    Feax = Feax.tolist()  # 12.装到列表里
    # Fea11x=[num for num in Feax if num <= fend]
    result['fea_xaxis'] = Feax  # 13.表示x轴的坐标

    result['group'] = str(group)  # 定义组名 可能就是表示工厂名
    result['machine'] = str(machine)  # 表示设备名
    result['component'] = component  # 表示组件名
    result['sensor'] = sensor  # 表示传感器名
    collectionf = db['sensor_data_2025']  # 数据库的表名 应该是
    # #############显示报警结论
    collectionfre = eval(f'db.indicator_data_{group}_{machine}')  # eval是用字串的形式 运行这个代码 获取数据库
    # 相刑兢 果然
    # fault  故障 断层 缺点 错误
    fault_txtn = list(
        collectionfre.find({'sensorID': f'SE_{group}_{machine}_{component}_{sensor}'}, {'faultstr': 1}))  # 获取数据库指定数据
    if len(fault_txtn) == 0:  # 没有数据
        fault_txt = {}
    else:
        fault_txt = fault_txtn[-1]  # 取最后一个元素 这里为什么是取最后一个元素呢

    fault_txt = fault_txt.get('faultstr', "")  # 15. 取faultstr fault 故障字段的值 如果没有，则返回空字符串
    result['fault_txt'] = fault_txt  # 16.存入字典
    # ######### 0 22不相宜 这一步在干什么 要理解好 不要搞模糊了
    frexx = str(theory_frequencies(group, machine, component, sensor, speed))  # 16. 这里的速度是取的假的么 为什么speed写的是0
    frexxx = frexx.replace("{", "").replace("}", "")
    frexxxx = frexxx.replace("'", " ")
    result['xxxx'] = frexxxx  # 这里的xxxx也是一个字典
    # ########### 显示理论报警频率 这些是用在什么地方的？ 缺陷字典
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
    fault_fre = list(  # 工厂 设备 组件 传感器 获取数据库指定数据
        collectionf.find({'sensorID': f'SE_{group}_{machine}_{component}_{sensor}'}, {'faultfre': 1, 'hardware': 1}))
    if len(fault_fre) >= 1 and 'faultfre' in fault_fre[0]:  # 长度大于 且faultfre在里面
        fault_fre = fault_fre[0]['faultfre']  # 就是获取faultfre字段的值
    else:
        fault_fre = {}
    # print('xxxx',fault_fre)
    # #####
    # speed3=speed3[0]
    # fault_fre = {key: round(value * speed3, 2) for key, value in fault_fre.items()}

    # #######
    # parts = nearest_file_name.split('_')
    # N_time = parts[1].split('%')[0]
    # dtn = datetime.strptime(N_time, "%Y%m%d%H%M%S")
    # N_time2 = dtn.strftime("%Y-%m-%d %H:%M:%S")
    # N_time2 = datetime.strptime(N_time2, '%Y-%m-%d %H:%M:%S')

    # keys = list(fault_fre.keys())
    # fault_fre_values = list(fault_fre.values())
    # fault_fre_txt = [fault_dict[key] for key in keys if key in fault_dict]
    # fault_fre_values=[round(num, 2) for num in fault_fre_values]

    # fault_fre_values = [x * float(speed) for x in fault_fre_values]
    # fault_fre_values = [round(x, 3) for x in fault_fre_values]

    # === 修改部分开始 ===  过滤掉的key是什么意思
    # 如果 component==2 且 sensor==4，则过滤掉所有以 "HSS" 开头的键
    if component == 2 and sensor == 4:  # 设备=2 传感器为4 则过滤掉所有以 "HSS" 开头的键
        filtered_keys = [k for k in fault_fre.keys() if not k.startswith("HSS")]
    else:
        filtered_keys = list(fault_fre.keys())

    # 自定义顺序，将'fm'放在第一位 无非就是存一些键值对 排序的key 顺序
    ordered_keys = []
    # 如果存在'fm'键，先添加它的数据
    if 'fm' in filtered_keys:
        ordered_keys.append('fm')
        # 添加其他所有键（除了已添加的'fm'）因为fm的key之前添加过了
        ordered_keys.extend([k for k in filtered_keys if k != 'fm'])
    else:
        ordered_keys = filtered_keys  # 没有就按原来的顺序添加

    fault_fre_txt = [fault_dict[k] for k in ordered_keys if k in fault_dict]  #
    fault_fre_values = [round(fault_fre[k], 2) for k in ordered_keys]  #
    # === 修改部分结束 ===

    result['fault_fre_txt'] = fault_fre_txt  # 把这个ordered_keys添加到字典中
    result['fault_fre_values'] = fault_fre_values  # 把fault_fre_values添加到字典中

    # #####################谐波标注
    fault_txt_list = fault_txt.split('\t')
    fault_txt_list = [item for item in fault_txt_list if item]  # 如果有item 所有预警的小部件
    result['fault_txt_list'] = fault_txt_list
    # ####所有预警的频率
    faultfre_dict = {
        '内圈报警': 'inner',
        '外圈报警': 'outer',
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
    fault_frev = [round(num, 2) for num in selected_values]  # 获取fault_fre_values 2位小数点

    # ###### 边频添加
    # print(fault_txt_list,fault_frev)
    # 这段代码 dict(zip(fault_txt_list, fault_frev)) 是一个常用的 Python 技巧，用于将两个列表组合成字典
    Mdic = dict(zip(fault_txt_list, fault_frev))  # 创建字典
    if '啮合频率报警' in Mdic:
        # 获取 '啮合频率报警' 对应的值
        meshing_fault_value = Mdic['啮合频率报警']
        # 获取 '行星轮报警' 和 '太阳轮报警' 对应的值
        planetary_fault_value = Mdic['行星轮报警']
        sun_fault_value = Mdic['太阳轮报警']
        # 计算 '边频1' 和 '边频2'
        sideband1 = meshing_fault_value - 5 * planetary_fault_value  # 行星轮报警 -
        sideband2 = meshing_fault_value - 5 * sun_fault_value  # 太阳轮报警 -
        sideband3 = meshing_fault_value + 5 * planetary_fault_value  # 行星轮报警 +
        sideband4 = meshing_fault_value + 5 * sun_fault_value  # 太阳轮报警 +
        # 将 '边频1' 和 '边频2' 添加到字典中 4组边频数据 添加到字典中
        Mdic['边频1'] = sideband1
        Mdic['边频2'] = sideband2
        Mdic['边频3'] = sideband3
        Mdic['边频4'] = sideband4
        fault_txt_list = [key for key, value in Mdic.items()]  # 拆出key
        fault_frev = [value for key, value in Mdic.items()]  # 拆出value

    # ###### wq sk c rhf z yi kmq cf wq r rcy i
    for i, value in enumerate(fault_txt_list):  # 枚举列表
        key = f"fault_txt_list_{i + 1}"  # 这里只是给key命名
        result[key] = value  # 给对应的key添加值

    for i, value in enumerate(fault_frev):  # 枚举列表
        key = f"fault_frev_{i + 1}"  # 这里只是给key命名
        result[key] = value  # 给对应的key添加值
    result['maxnum'] = len(fault_frev)

    # #######################################
    show_values = [item[1] for item in fault_fre.items()]  # 把字典中所有值都取出来
    show_values2 = show_values + [x * 2 for x in show_values]  # 列表推导式 再2个列表相加
    result['maxnum2'] = len(show_values2)
    result['show_values2'] = show_values2
    # print(show_values2)
    # #########################################

    # print(result['fault_txt_list_4'],result['fault_txt_list_5'],result['fault_txt_list_6'],result['fault_txt_list_7'])

    # 直方图
    middata = list(fault_fre.items())[:4]  # 只取前面的4个数
    middata = [value for key, value in middata]  # 获取value
    result['middata'] = middata
    # print(middata)

    # ##################################################### 显示工厂信息 有db的地方就是在写数据库了
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

    # time_add=localfilename[2:14] 这里只是添加一些时间吧
    time_add = datetime.strptime(file_name.split('.')[0], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    result['time_add'] = time_add

    result['speed'] = speed.tolist()

    largest_12 = heapq.nlargest(12, enumerate(Feay), key=lambda x: x[1])
    # 没有数据的情况
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
