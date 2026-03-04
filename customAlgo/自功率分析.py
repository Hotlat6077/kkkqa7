
import numpy as np
import heapq  # 新增：用于提取最大幅值
from envlop_xiao import env
import os
from Signal2_frequency import frequencyx

# from mq.fs_table import FSTableService
from mydb.get_mongo import get_db
from preprocess import *
# import config
from frequency_test import theory_frequencies
import matplotlib.pyplot as plt
from 去滑雪坡特征 import ski_slope


def update_mins_fj_signal_analysis_aps_cao_fix(data, fs, filetime='20251229180100', methods='raw'):
    # 从文件名中提取转速信息
    speed = 0
    speed = np.array([float(speed)]) / 60
    speed = np.round(speed, 5)
    # ##############
    # 数据 时间 FS 数据ID(设备编号 测点编号) 类型 raw
    # 对原始信号下采样并去均值
    signal = np.array(data)
    signal = (signal - np.mean(signal)).tolist()

    # 执行自定义方法（由 methods 参数指定），得到 Feaa
    blank_dict = {}
    try:
        exec(f"blank_dict['out']={methods}(signal, fs)")
    except Exception as e:
        raise RuntimeError(f"执行方法 '{methods}' 时出错: {e}")
    Feaa = blank_dict['out'].tolist()

    # 进行自功率谱分析（frequencyx 内部需数组型输入，list 无 .shape 会报错）
    T = frequencyx(RawSignal=np.asarray(Feaa), SampleFraquency=fs)
    Feax, Feay = T.aps()

    result = {}
    # 原信号数据及其横坐标
    result['fea_y'] = Feaa
    length = len(Feaa)
    f_x1 = ndarray2list0(np.arange(length) + 1)
    f_x = [x / fs for x in f_x1]
    f_x=[round(num, 5) for num in f_x ]
    result['fea_x'] = f_x

    # 自功率谱分析数据
    Feax = [int(num) for num in Feax]  # 根据您的需求保留整数
    result['fea_xaxis'] = Feax
    result['peak'] = Feay.tolist()

    # 当前特征频率
    if len(Feay) == 0:
        frequencyxxx = None
    else:
        frequencyxxx = round(Feax[np.argmax(Feay)], 5)
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
        formatted_values = [round(val, 5) for val in values]
        formatted_positions = [round(pos, 5) for pos in positions]

    result['formatted_values'] = formatted_values
    result['formatted_positions'] = formatted_positions
    # ---------------------------------------------------------

    # 拼接基本信息
    # result['group'] = str(group)
    # result['machine'] = str(machine)
    # result['component'] = component
    # result['sensor'] = sensor

    # collection_group = db['group_data']
    # group_doc = collection_group.find_one({'groupID': f'GR_{group}'}, {'name': 1})
    # if not group_doc:
    #     raise ValueError(f"未找到 groupID: GR_{group} 的文档。")
    # group_name = group_doc['name']

    # collection_machine = db['machine_data']
    # machine_doc = collection_machine.find_one({'machineID': f'MA_{group}_{machine}'}, {'name': 1})
    # if not machine_doc:
    #     raise ValueError(f"未找到 machineID: MA_{group}_{machine} 的文档。")
    # machine_name = machine_doc['name']

    # collection_component = db['component_data']
    # component_doc = collection_component.find_one(
    #     {'componentID': f'CO_{group}_{machine}_{component}'},
    #     {'name': 1}
    # )
    # if not component_doc:
    #     raise ValueError(f"未找到 componentID: CO_{group}_{machine}_{component} 的文档。")
    # component_name = component_doc['name']

    # collection_sensor = db['sensor_data']
    # sensor_doc = collection_sensor.find_one(
    #     {'sensorID': f'SE_{group}_{machine}_{component}_{sensor}'},
    #     {'name': 1}
    # )
    # if not sensor_doc:
    #     raise ValueError(f"未找到 sensorID: SE_{group}_{machine}_{component}_{sensor} 的文档。")
    # sensor_name = sensor_doc['name']

    # result['group_name'] = group_name
    # result['machine_name'] = machine_name
    # result['component_name'] = component_name
    # result['sensor_name'] = sensor_name
    result['file'] = ""

    time_add = datetime.strptime(filetime.split('.')[0], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    result['time_add'] = time_add

    # 将 speed 这个列表返回
    speed = speed.tolist()
    result['speed'] = speed

    # collectionf = db['sensor_data_2025']
    fault_txt ={}
    ###############显示报警结论
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
    # if len(fault_fre) >= 1:
    #     fault_fre = fault_fre[0]['faultfre']
    # else:
    #     fault_fre = {}
    ######

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


if __name__ == '__main__':
    from mydb.get_mongo import get_db
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
    # 提取 fs 字段
    fs = document.get('fs')
    data = document.get('datas')
    res = update_mins_fj_signal_analysis_aps_cao_fix(data, fs, filetime='20251229180100', methods='raw')
    print("res :", res)
    # # 绘制上下两张波形图
    # plt.figure(figsize=(10, 8))
    
    # # 上图：原始信号波形
    # plt.subplot(2, 1, 1)
    # plt.plot(res['fea_x'], res['fea_y'])
    # plt.title('原始信号波形')
    # plt.xlabel('时间 (s)')
    # plt.ylabel('幅值')
    # plt.grid(True)
    
    # # 下图：自功率谱
    # plt.subplot(2, 1, 2)
    # plt.plot(res['fea_xaxis'], res['peak'])
    # plt.title('自功率谱')
    # plt.xlabel('频率 (Hz)')
    # plt.ylabel('功率')
    # plt.grid(True)
    
    # plt.tight_layout()
    # plt.show()
    
    # # x轴为result['fea_xaxis'] 
    # # y轴为result['fea_y']
    # from draw import plot_waveform
    # plot_waveform(res,'fea_xaxis','peak')