import numpy as np
import numpy.fft as fft
from scipy.fftpack import hilbert, fft, ifft
from sig_frequency import frequencyx
from sig_frequency2 import indexx, env
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


# def update_mins_fj_signal_analysis4_cao_fix(data, fs, methods='raw'):
def trend_analysis(data, fs, methods='raw'):

    # 从文件名中提取转速
    speed = 0
    speed = np.array([float(speed)]) / 60
    speed = np.round(speed, 4)
    ###############

    # 下采样并去均值
    signal = np.array(signal)
    signal = (signal - np.mean(signal)).tolist()

    # 执行自定义方法
    blank_dict = {}
    exec(f"blank_dict['out']={methods}(signal, fs)")
    signal = blank_dict['out'].tolist()

    # 计算波形指标（基于时间）
    index13_interval = 100
    T = indexx(RawSignal=signal, SampleFraquency=fs, Sampleinterval=index13_interval)
    Fea = T.time_domainx()

    # 包络分析
    Feax, Feay = env(signal, fs)

    # 拼接返回结果
    result = {}

    # 1) 时间指标（如均方根、峭度等）
    #    这里的 Fea 是一个二维数组，每一列为一种指标，这里假定 Fea[:,0] 有意义
    if len(Fea) >= 1:
        result['pinpu1'] = Fea[:, 0].tolist()
        length = len(Fea[:, 0])
    else:
        result['pinpu1'] = []
        length = 0

    result['fea_xaxis1'] = ndarray2list0(np.arange(length) + 1)

    # 2) 包络分析结果
    #    Feax, Feay 需要返回给前端
    result['fea_xaxis3'] = Feax.tolist()
    result['pinpu3'] = Feay.tolist()

    # 3) 原始（或处理后）时域波形
    result['pinpu2'] = signal
    length_signal = len(signal)
    f_x1 = ndarray2list0(np.arange(length_signal) + 1)
    # 横坐标单位换算
    f_x = [x / fs for x in f_x1]
    f_x = [round(num, 2) for num in f_x]
    result['fea_xaxis2'] = f_x

    # ----------------- 新增：从包络谱 Feay 中提取最大的 12 个峰值 -----------------
    if len(Feay) == 0:
        # 避免空数据导致报错
        formatted_values = []
        formatted_positions = []
    else:
        largest_n = min(12, len(Feay))
        # 获取最大的 largest_n 个点及其索引
        largest_12 = heapq.nlargest(largest_n, enumerate(Feay), key=lambda x: x[1])
        indices, values = zip(*largest_12)
        # 获取对应的频率位置
        positions = [Feax[i] for i in indices]

        # 幅值和位置分别保留一定小数
        formatted_values = [round(val, 4) for val in values]
        formatted_positions = [round(pos, 2) for pos in positions]

    result['formatted_values'] = formatted_values
    result['formatted_positions'] = formatted_positions
    # ---------------------------------------------------------------------

    # 拼接机器信息
    # result['group'] = str(group)
    # result['machine'] = str(machine)
    # result['component'] = component
    # result['sensor'] = sensor

    # 从数据库查名称
    # collection_group = db['group_data']
    # group_name = list(collection_group.find({'groupID': 'GR_' + str(group)}, {'name': 1}))[0]['name']

    # collection_machine = db['machine_data']
    # machine_name = \
    #     list(collection_machine.find({'machineID': 'MA_' + str(group) + '_' + str(machine)}, {'name': 1}))[0]['name']

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

    # 从 localfilename 提取时间信息
    # time_add = datetime.strptime(file_name.split('.')[0], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    # result['time_add'] = time_add

    # speed 以列表返回
    speed = speed.tolist()
    result['speed'] = speed

    # collectionf = db['sensor_data_2025']
    ###############显示报警结论
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
    # fault_fre_values = [round(fault_fre[k], 2) for k in ordered_keys]
    # === 修改部分结束 ===

    result['fault_fre_txt'] = fault_fre_txt
    # result['fault_fre_values'] = fault_fre_values

    return result
