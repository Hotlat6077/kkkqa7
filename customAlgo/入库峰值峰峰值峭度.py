import numpy as np
from 去滑雪坡特征 import ski_slope

# 曹学勇修补 加速度有效值
# 接收waveID
# def update_mins_fj_signal_analysis3_cao_fix(data, fs , methods='raw', index13_interval = 100):
def update_mins_fj_signal_analysis3_cao_fix(wave_id, filetiem, data):
    # 转速信号提取
    speed = 0
    speed = np.array([float(speed)]) / 60
    speed = np.round(speed, 4)
    # print(localfilename)
    # -------------------------   以下为之前读数据库的模式，需要被替换掉
    # data1 = list(collection.find({'machine': machine,'group':group,'component':component,'sensor':sensor}, {'vib':1,'speed':1}).sort([('datetime', -1)]).limit(1))[0]  # 改动
    # signal=data1.get('vib')
    signal = np.array(data)
    # signal = (signal - np.mean(signal)).tolist()
    # 不tolist 就是数组信号 
    signal = (signal - np.mean(signal)) # 不处理signal就是加速度
    # 加速度有效值 
    acc_rms = np.sqrt(np.mean(signal ** 2))
    # 计算加速度均值
    # acc_mean = np.mean(signal)
    signal_mean = np.mean(signal)
    signal_std = np.std(signal)
    acc_kurtosis = np.mean((signal - signal_mean) ** 4) / (signal_std ** 4) if signal_std != 0 else 0
    # 加速度直接计算最大值 最小值
    max_acc = float(np.max(signal))  # 加速度峰值
    min_acc= float(np.min(signal))
    peak_acc = max(abs(max_acc), abs(min_acc))  # 6.峰值
    # 加速度峰峰值
    peak2peak = max_acc - min_acc

    print("peak_acc: ", peak_acc, "peak2peak: ", peak2peak, "加速度峭度: ", acc_kurtosis)

    # fs = 25600
    # 速度峰值 
    # blank_dict = {}
    # 加速度积分得到速度
    # exec(f"blank_dict['out']=tintegral(signal,fs)")
    # Feaa = blank_dict['out'].tolist()

    # 梯形积分 加速度积分到速度 如果不对就用上面的
    dt = 1.0 / float(fs)
    velocity = np.cumsum(signal) * dt
    # 速度有效值
    velocity_rms = np.sqrt(np.mean(velocity ** 2))
    # 加速度积分后为速度 要去滑雪坡特征
    velocity_ski = ski_slope(velocity, fs)
    # 计算速度均值
    velocity_std = np.std(velocity)
    velocity_mean = np.mean(velocity)
    # 计算 加速度  的峭度
    velocity_kurtosis = np.mean((velocity - velocity_mean)**4) / (velocity_std**4) if velocity_std != 0 else 0
    np.sum((velocity - velocity_mean) ** 4)
    # 速度峰峰值
    max_v = float(np.max(velocity_ski))
    min_v = float(np.min(velocity_ski))
    peak_vel = max(abs(max_v), abs(min_v))
    peak2peak_v = (max_v - min_v)*1000 # 转为 mm/s
    print("velocity peak_acc:", peak_vel, "peak2peak_v:", peak2peak_v,"峭度:", velocity_kurtosis)
    # 
    result = [
    {"id":"acc_1_0_11","value":acc_rms,"name":"加速度有效值","ts":"波形时间","remark":""},
    {"id":"acc_1_0_11","value":velocity_rms,"name":"速度有效值","ts":"波形时间","remark":""},
	{"id":"speed_1_0_11","value":peak_acc,"name":"加速度峰值","ts":"波形时间","remark":""},
	{"id":"peak_1_0_11","value":peak_vel,"name":"速度峰值","ts":"波形时间","remark":""},
    {"id":"p2p_1_0_11","value":peak2peak,"name":"加速度峰峰值","ts":"波形时间","remark":""},
    {"id":"p2p_1_0_11","value":peak2peak_v,"name":"速度峰峰值","ts":"波形时间","remark":""},
    {"id":"kur_1_0_11","value":acc_kurtosis,"name":"加速度峭度","ts":"波形时间","remark":""},
	{"id":"kur_1_0_11","value":velocity_kurtosis,"name":"速度峭度","ts":"波形时间","remark":""}
    ]

    # Fea = T.time_domainx()

    # result = {}
    # # 原信号数据
    # result['fea_y'] = Feaa
    # length = len(Feaa)
    # f_x1 = ndarray2list0(np.arange(length) + 1)
    # f_x = [x / fs for x in f_x1]
    # result['fea_x'] = f_x
    # if len(Fea) >= 1:
    #     result['rms'] = Fea[:, 0].tolist()
    #     result['peak'] = Fea[:, 1].tolist()
    #     length = len(Fea[:, 0])
    # else:
    #     result['rms'] = []
    #     result['peak'] = []
    #     length = 0

    # wave_1_0_11   波形ID 换成其他类型的名称
    # result['fea_xaxis'] = ndarray2list0(np.arange(length) + 1)

if __name__ == '__main__':
    from mydb.get_mongo import get_db
    db = get_db()
    collection = db['pump_waveform_report']
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
    res = update_mins_fj_signal_analysis3_cao_fix(data, fs, methods='raw')
    from draw2plot import plot_waveform_dual
    # plot_waveform_dual(res, 'fea_x', 'fea_y','fea_xaxis', 'peak',top_label= 'Fea',bottom_label='peak')