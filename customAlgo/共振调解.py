import numpy as np
from datetime import datetime   
from Signal1_index import indexx
from preprocess_data import ndarray2list0, ndarray2list1
from envlop_xiao import env
import heapq
from mydb.get_mongo import get_db
from preprocess import *
from Signal6_denoise import denoisex
from 去滑雪坡特征 import ski_slope

#曹学勇修补 共振调解
def update_mins_fj_signal_analysis_resonance_cao_fix(data, fs, methods='raw'):
    # db = get_db()
    # 使用numpy进行简单处理，然后只在最后转成列表
    speed = 0
    speed = np.array([float(speed)]) / 60
    speed = np.round(speed, 6)
    # ##############

    # 对原始信号下采样并去均值
    signal = np.array(data)
    signal = (signal - np.mean(signal)).tolist()

    # 执行自定义方法（由 methods 参数指定），得到 Feaa
    blank_dict = {}
    exec(f"blank_dict['out']={methods}(signal, fs)")
    Feaa = blank_dict['out'].tolist()

    # 读取数据库中与共振解调相关的配置
    # permissions_collection = db['permissions']
    # permissions = permissions_collection.find_one({}, {"fmin": 1, "fmax": 1})
    permissions ={}
    fmin = permissions.get("fmin", 200) if permissions else 200
    fmax = permissions.get("fmax", 1000) if permissions else 1000
    # 在共振解调里有2个参数fmin fmax是可以
    # 进行共振解调
    T = denoisex(RawSignal=Feaa, SampleFraquency=fs)
    # Feax, Feay = T.resonancex(fmin, fmax)
    Feax, Feay = T.resonancex()

    result = {}
    # 原信号数据及其横坐标
    result['fea_y'] = Feaa
    length = len(Feaa)
    f_x1 = ndarray2list0(np.arange(length) + 1)
    f_x = [x / fs for x in f_x1]
    f_x=[round(num,6) for num in f_x ]
    result['fea_x'] = f_x

    # 包络谱数据
    # 注意：Feax被转换为整数可能会降低频率精度，如果需要更高精度，可以保留小数部分
    Feax = [int(num) for num in Feax]  # 根据您的需求保留整数
    result['fea_xaxis'] = Feax
    result['peak'] = Feay.tolist()

    # 当前特征频率
    frequencyxxx = round(Feax[np.argmax(Feay)], 6)
    result['frequencyxxx'] = frequencyxxx

    # -------------- 新增：提取频谱中幅值最大的 12 个点 --------------
    largest_12 = heapq.nlargest(12, enumerate(Feay), key=lambda x: x[1])
    indices, values = zip(*largest_12)
    # 根据索引获取对应频率
    positions = [Feax[i] for i in indices]

    # 幅值和位置分别保留小数位数
    formatted_values = [round(val, 6) for val in values]
    formatted_positions = [round(pos, 6) for pos in positions]

    result['formatted_values'] = formatted_values
    result['formatted_positions'] = formatted_positions
    # ---------------------------------------------------------

    # 拼接基本信息 'SE_1_1_2_3'
    result['group'] = str(1)
    result['machine'] = str(1)
    result['component'] = '2'
    result['sensor'] = '3'

    # collection_group = db['group_data']
    # group_name = list(collection_group.find({'groupID': 'GR_' + str(group)}, {'name': 1}))[0]['name']

    # collection_machine = db['machine_data']
    # machine_name = list(collection_machine.find({'machineID': 'MA_' + str(group) + '_' + str(machine)}, {'name': 1}))[0]['name']

    # collection_component = db['component_data']
    # component_name = list(collection_component.find(
    #     {'componentID': 'CO_' + str(group) + '_' + str(machine) + '_' + str(component)},
    #     {'name': 1}
    # ))[0]['name']

    # collection_sensor = db['sensor_data']
    # sensor_name = list(collection_sensor.find(
    #     {'sensorID': 'SE_' + str(group) + '_' + str(machine) + '_' + str(component) + '_' + str(sensor)},
    #     {'name': 1}
    # ))[0]['name']

    # result['group_name'] = group_name
    # result['machine_name'] = machine_name
    # result['component_name'] = component_name
    # result['sensor_name'] = sensor_name
    result['file'] = ""

    # 从 localfilename 中提取时间信息
    # time_add = datetime.strptime(filetime.split('.')[0], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    # result['time_add'] = time_add

    # 将 speed 这个列表返回
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
        # collectionf.find({'sensorID': f'SE_{group}_{machine}_{component}_{sensor}'}, {'faultfre': 1, 'hardware': 1}))
    # if len(fault_fre) > 0:
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
    # fault_fre_values = [round(fault_fre[k], 6) for k in ordered_keys]
    # === 修改部分结束 ===

    result['fault_fre_txt'] = fault_fre_txt
    # result['fault_fre_values'] = fault_fre_values
    #print("result: ", result)

    return result




if __name__ == "__main__":
    sensor_id = 'SE_1_1_2_3'
    time = "20251229180100"
    db = get_db()
    collection = db['pump_waveform_report']
    # 通过sensorId取信号原始数据
    query = {
        # 'sensorId':sesor_id,
        'measureSiteId':int(1077691462944),
        'measureGatherId':int(1077691480608),
        'time':'20260109040100'
    }
    print("query",query)
    document = collection.find_one(query)
    
    document = collection.find_one(query)
    print("数据Data是否为不为空",document is not None)
    # 提取 fs 字段
    fs = document.get('fs')
    data = document.get('datas')
    update_mins_fj_signal_analysis_resonance_cao_fix(data, fs,methods='raw')
