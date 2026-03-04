import numpy as np
import numpy.fft as fft
from scipy.fftpack import hilbert, fft, ifft
from utils.sig_frequency import frequencyx
from utils.preprocess_data import raw, tintegral, cderiv, routliers, ndarray2list0, ndarray2list1




# def update_mins_fj_signal_analysis6_cao_fix(data, fs, methods='raw'):
def spectrum(data, fs, methods='raw'):
    # 转速信号提取
    speed = 0
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
    ######################

    signal = np.array(data)  # 1. 处理成 np.array
    signal = (signal - np.mean(signal)).tolist()  # 减去均值

    # collectionfs=db['sensor_data']
    # fs=list(collectionfs.find({'sensorID':f'SE_{group}_{machine}_{component}_{sensor}','onlineflag':True},
    #                        {'samplingfrequency':1}))[0]
    # fs=fs['samplingfrequency']

    blank_dict = {}
    exec(f"blank_dict['out']={methods}(signal,fs)")
    Feaa = blank_dict['out'].tolist()  # Feaa是预处理过的原始数据 但这里的方式是raw就是不处理

    T = frequencyx(RawSignal=Feaa, SampleFraquency=fs)
    Fea1x, Fea1y = T.fftx()  # # 频率分辨率 频率幅值
    log_y = np.log(Fea1y + 0.0001)  # 频率幅值计算对数

    result = {}
    # 原信号数据
    result['fea_y'] = Feaa
    length = len(Feaa)
    f_x1 = ndarray2list0(np.arange(length) + 1)
    # 可以用下面的代码更简洁
    # f_x1 = list(np.arange(length) + 1)
    f_x = [x / fs for x in f_x1]
    f_x = [round(num, 2) for num in f_x]
    result['fea_x'] = f_x

    Fea1x = np.round(Fea1x, 3)
    Fea1x = Fea1x.tolist()
    # Fea1x=[num for num in Fea1x if num <= fend]
    result['fea_xaxis'] = Fea1x
    LL = len(Fea1x)
    Fea1y = Fea1y[0:LL]
    print("Fea1y.tolist :", Fea1y.tolist())
    result['fftyy'] = Fea1y.tolist()
    result['log_y'] = log_y.tolist()  # 增加对数变换后的数据
    # print("Fea1y.tolist :", Fea1y.tolist())
    ###########################################
    ##############显示报警结论
    # collectionf = db['sensor_data_2025']
    # collectionfre = eval(f'db.indicator_data_{group}_{machine}')
    # fault_txtn = list(collectionfre.find({'sensorID': f'SE_{group}_{machine}_{component}_{sensor}'}, {'faultstr': 1}))
    # fault_txt = fault_txtn[-1] if len(fault_txtn) >= 1 else {}
    # fault_txt = fault_txt.get("faultstr", "")
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
        # collectionf.find({'sensorID': f'SE_{group}_{machine}_{component}_{sensor}'}, {'faultfre': 1, 'hardware': 1}))
    # if len(fault_fre) >= 1:
    #     fault_fre = fault_fre[0]['faultfre']
    # else:
    #     fault_fre = {}
    ######
    # speed3=speed3[0]
    # fault_fre = {key: round(value * speed3, 2) for key, value in fault_fre.items()}
    # print('xxxx',fault_fre)
    ########
    # keys = list(fault_fre.keys())
    # fault_fre_values = list(fault_fre.values())
    # fault_fre_txt = [fault_dict[key] for key in keys if key in fault_dict]
    # fault_fre_values = [round(num, 2) for num in fault_fre_values]
    # fault_fre_values = [x * float(speed)*10 for x in fault_fre_values]
    # fault_fre_values = [round(x, 3) for x in fault_fre_values]
    # 如果 component==2 且 sensor==4，则过滤掉所有以 "HSS" 开头的键
    # if component == 2 and sensor == 4:
        # filtered_keys = [k for k in fault_fre.keys() if not k.startswith("HSS")]
    # else:
        # filtered_keys = list(fault_fre.keys())

    # 自定义顺序，将'fm'放在第一位
    ordered_keys = []
    # 如果存在'fm'键，先添加它
    # if 'fm' in filtered_keys:
    #     ordered_keys.append('fm')
    #     # 添加其他所有键（除了已添加的'fm'）
    #     ordered_keys.extend([k for k in filtered_keys if k != 'fm'])
    # else:
    #     ordered_keys = filtered_keys

    # fault_fre_txt = [fault_dict[k] for k in ordered_keys if k in fault_dict]
    # fault_fre_values = [round(fault_fre[k], 2) for k in ordered_keys]
    # === 修改部分结束 ===

    # result['fault_fre_txt'] = fault_fre_txt
    # result['fault_fre_values'] = fault_fre_values

    # #####################谐波标注
    # fault_txt_list = fault_txt.split('\t')
    # fault_txt_list = [item for item in fault_txt_list if item]  # 所有预警的小部件
    # result['fault_txt_list'] = fault_txt_list
    # ####所有预警的频率
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
    # fre_v = [faultfre_dict.get(key) for key in fault_txt_list]
    # selected_values = {key: fault_fre[key] for key in fre_v if key in fault_fre}
    # selected_values = list(selected_values.values())
    # fault_frev = [round(num, 2) for num in selected_values]

    # ######边频添加
    # print(fault_txt_list,fault_frev)
    # Mdic = dict(zip(fault_txt_list, fault_frev))
    Mdic = {}
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
        # fault_txt_list = [key for key, value in Mdic.items()]
        # fault_txt_list = {}
        # fault_frev = [value for key, value in Mdic.items()]

    # ######
    # for i, value in enumerate(fault_txt_list):
    #     key = f"fault_txt_list_{i + 1}"
    #     result[key] = value

    # for i, value in enumerate(fault_frev):
    #     key = f"fault_frev_{i + 1}"
    #     result[key] = value
    # result['maxnum'] = len(fault_frev)

    # #######################################
    # show_values = [item[1] for item in fault_fre.items()]
    # show_values2 = show_values + [x * 2 for x in show_values]
    # result['maxnum2'] = len(show_values2)
    # result['show_values2'] = show_values2
    # # ###################
    # ##################显示工厂信息
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

    result['file'] = ""

    # time_add = datetime.strptime(file_name.split('.')[0], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    # result['time_add'] = time_add
    speed = speed.tolist()
    result['speed'] = speed
    result['code'] = 200
    result['msg'] = '请求成功'

    # largest_12 = heapq.nlargest(12, enumerate(Fea1y), key=lambda x: x[1])
    # if len(largest_12) >= 1:
    #     indices, values = zip(*largest_12)
    # else:
    #     indices, values = [], []

    # values_positions = [Fea1x[i] for i in indices]
    # largest_12 = [item for sublist in largest_12 for item in sublist]
    # formatted_values = [round(num, 4) for num in largest_12]
    # formatted_positions = [round(num, 2) for num in values_positions]
    # formatted_values = formatted_values[1::2]
    # result['formatted_values'] = formatted_values
    # result['formatted_positions'] = formatted_positions
    return result
