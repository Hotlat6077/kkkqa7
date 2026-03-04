import numpy as np
import heapq
from Signal2_frequency3 import denoisex,frequencyx


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

def wavelet_thresholding(data, fs , methods='raw',wavelet='',threshold='',level=1):
    # 转速信号提取
    speed =0
    speed = np.array([float(speed)])/60
    speed = np.round(speed, 4)

    signal=np.array(data)
    signal=(signal-np.mean(signal)).tolist()
    blank_dict={}
    exec(f"blank_dict['out']={methods}(signal,fs)")
    Feaa=blank_dict['out'].tolist()


    # permissions_collection = db['permissions']
    # permissions = permissions_collection.find_one({}, {"wavelet": 1, "threshold": 1, "level": 1})
    # wavelet = permissions.get("wavelet", "sym8") if permissions else "sym8"
    # threshold = permissions.get("threshold", "fixed") if permissions else "fixed"
    # level = permissions.get("level", 1) if permissions else 1
    T = denoisex(RawSignal=Feaa, SampleFraquency=fs)
    Feax = T.waveletdx(wavelet=wavelet, threshold=threshold, level=level)

    result = {}
    result['y1'] = signal
    length = len(signal)
    f_x1=ndarray2list0(np.arange(length)+1)
    f_x=[x / fs for x in f_x1]
    f_x=[round(num,2) for num in f_x ]
    result['x1'] = f_x

    Fea2x, Fea2y = frequencyx(RawSignal=Feax, SampleFraquency=fs).envelopex()

    Fea2x=np.round(Fea2x,3)
    result['fea_xaxis3'] = (Fea2x).tolist()
    result['y3'] = (Fea2y).tolist()


    result['y2'] =(Feax).tolist()
    length = len(result['y2'])

    f_x2=(np.arange(length)+1).tolist()
    f_x2=[x / fs for x in f_x2]
    result['fea_xaxis2'] = f_x2

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

    group_name = group_name[0]['name']
    machine_name = machine_name[0]['name']
    component_name = component_name[0]['name']
    sensor_name = sensor_name[0]['name']
    result['group_name']=group_name
    result['machine_name']=machine_name
    result['component_name']=component_name
    result['sensor_name']=sensor_name
    result['file']=""

    # time_add = datetime.strptime(file_name.split('.')[0], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    # result['time_add']=time_add
    speed=speed.tolist()
    result['speed']=speed


    # -------------- 新增：提取最大 12 个幅值及对应的频率位置 --------------
    largest_12 = heapq.nlargest(12, enumerate(Fea2y), key=lambda x: x[1])
    if len(largest_12) >=1:
        indices, values = zip(*largest_12)
    else:
        indices, values = [], []

    # 根据索引获取对应频率
    positions = [Fea2x[i] for i in indices]

    # 幅值与频率分别保留一定小数位
    formatted_values = [round(val, 4) for val in values]
    formatted_positions = [round(pos, 2) for pos in positions]

    # 放入返回结果
    result['formatted_values'] = formatted_values
    result['formatted_positions'] = formatted_positions

    # 拼接返回信息：群组、机组、部件、传感器、时间等
    # collection_group = db['group_data']
    # group_name = list(collection_group.find({'groupID': 'GR_' + str(group)}, {'name': 1}))[0]['name']

    # collection_machine = db['machine_data']
    # machine_name = list(collection_machine.find({'machineID': 'MA_' + str(group) + '_' + str(machine)}, {'name': 1}))[0]['name']

    # collection_component = db['component_data']
    # component_name = list(collection_component.find(
    #     {'componentID': 'CO_' + str(group) + '_' + str(machine) + '_' + str(component)},
    #     {'name': 1}))[0]['name']

    # collection_sensor = db['sensor_data']
    # sensor_name = list(collection_sensor.find(
    #     {'sensorID': 'SE_' + str(group) + '_' + str(machine) + '_' + str(component) + '_' + str(sensor)},
    #     {'name': 1}))[0]['name']

    # result['group'] = str(group)
    # result['machine'] = str(machine)
    # result['component'] = component
    # result['sensor'] = sensor
    result['group_name'] = group_name
    result['machine_name'] = machine_name
    result['component_name'] = component_name
    result['sensor_name'] = sensor_name
    result['file'] = ""

    # 从 localfilename 中提取时间信息
    # time_add = datetime.strptime(file_name.split('.')[0], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    # result['time_add'] = time_add
    result['speed'] = speed


    # -------------- 新增：提取最大 12 个幅值及对应的频率位置 --------------
    largest_12 = heapq.nlargest(12, enumerate(Fea2y), key=lambda x: x[1])
    if len(largest_12) >=1:
        indices, values = zip(*largest_12)
    else:
        indices, values = [], []

    # 根据索引获取对应频率
    positions = [Fea2x[i] for i in indices]

    # 幅值与频率分别保留一定小数位
    formatted_values = [round(val, 4) for val in values]
    formatted_positions = [round(pos, 2) for pos in positions]

    # 放入返回结果
    result['formatted_values'] = formatted_values
    result['formatted_positions'] = formatted_positions

    # 拼接返回信息：群组、机组、部件、传感器、时间等
    # collection_group = db['group_data']
    # group_name = list(collection_group.find({'groupID': 'GR_' + str(group)}, {'name': 1}))[0]['name']

    # collection_machine = db['machine_data']
    # machine_name = list(collection_machine.find({'machineID': 'MA_' + str(group) + '_' + str(machine)}, {'name': 1}))[0]['name']

    # collection_component = db['component_data']
    # component_name = list(collection_component.find(
    #     {'componentID': 'CO_' + str(group) + '_' + str(machine) + '_' + str(component)},
    #     {'name': 1}))[0]['name']

    # collection_sensor = db['sensor_data']
    # sensor_name = list(collection_sensor.find(
    #     {'sensorID': 'SE_' + str(group) + '_' + str(machine) + '_' + str(component) + '_' + str(sensor)},
    #     {'name': 1}))[0]['name']

    # result['group'] = str(group)
    # result['machine'] = str(machine)
    # result['component'] = component
    # result['sensor'] = sensor
    result['group_name'] = group_name
    result['machine_name'] = machine_name
    result['component_name'] = component_name
    result['sensor_name'] = sensor_name
    result['file'] = ""

    # 从 localfilename 中提取时间信息
    # time_add = datetime.strptime(file_name.split('.')[0], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    # result['time_add'] = time_add
    # result['speed'] = speed

    # collectionf = db['sensor_data_2025']
    # ##############显示报警结论
    # collectionfre = eval(f'db.indicator_data_{group}_{machine}')
    # fault_txtn = list(collectionfre.find({'sensorID': f'SE_{group}_{machine}_{component}_{sensor}'}, {'faultstr': 1}))
    # fault_txt = fault_txtn[-1] if len(fault_txtn) >= 1 else {}
    fault_txt = fault_txt.get('faultstr',"")
    result['fault_txt'] = fault_txt

    ##########0422
    # frexx=str(theory_frequencies(group,machine,component,sensor,speed))
    # frexxx=frexx.replace("{", "").replace("}", "")
    # frexxxx =frexxx.replace("'", " ")
    # result['xxxx']=frexxxx
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
    # if len(fault_fre) >=1:
    #     fault_fre = fault_fre[0]['faultfre']
    # else:
        # fault_fre = {}
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
    # fault_fre_values = [round(fault_fre[k], 2) for k in ordered_keys]
    # === 修改部分结束 ===

    result['fault_fre_txt'] = fault_fre_txt
    # result['fault_fre_values'] = fault_fre_values


    return result
