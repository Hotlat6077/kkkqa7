import numpy as np
import numpy.fft as fft

# 实现对包络算法的数据处理过程
# 要用到地数据处理过程 fs参数：采样频率
def raw(vib, fs):
    vib = np.array(vib)
    fs = fs
    return vib


def ndarray2list0(data):
    list0 = []
    for temp in data:
        list0.append(temp.tolist())
    return list0


def get_time_domain_features(data):
    import math
    absXbar = 0
    x_r = 0
    S = 0
    K = 0
    x_rms = 0
    len_ = int(data.shape[1])
    mean_ = data.mean(axis=1)  # 1.均值
    var = data.var(axis=1)  # 2.方差
    std_ = data.std(axis=1)  # 3.标准差
    max_ = data.max(axis=1)  # 4.最大值
    min_ = data.min(axis=1)  # 5.最小值/
    x_p = max(abs(max_), abs(min_))  # 6.峰值
    for i in range(len_):
        x_rms += data[0, i] ** 2
        absXbar += abs(data[0, i])
        x_r += math.sqrt(abs(data[0, i]))
        S += (data[0, i] - mean_[0]) ** 3
        K += (data[0, i] - mean_[0]) ** 4
    rms = math.sqrt(x_rms / len_)  # 7.均方根值
    peak = x_p / x_rms  # 11.峰值指标
    pulse = x_p / mean_[0]  # 12.脉冲指标
    ske = S / ((len_ - 1) * std_ ** 3)  # 14.偏斜度
    kur = K / ((len_ - 1) * std_ ** 4)  # 15.峭度
    fea = [rms, peak, kur, pulse, var, ske]
    return fea

def custom_rms_velocity(data, fs, methods='raw'):
    # 转速信号提取
    result = {}
    speed = 0
    speed = np.array([float(speed)]) / 60
    speed = np.round(speed, 4)
    # 
    signal = np.array(data)
    signal = (signal - np.mean(signal)).tolist()
    # 
    # fs = 25600
    blank_dict={}
    exec(f"blank_dict['out']={methods}(signal,fs)")
    Feaa=blank_dict['out'].tolist()

    index13_interval=100
    time = np.arange(0, len(Feaa)/fs, 1/fs)  # 时间数组，0到10秒
    velocity = cumulative_trapezoid(Feaa, time, initial=0)
    Fea = []
    for i in range(int(len(velocity) / index13_interval)):
        signal_temp = velocity[i * index13_interval:i * index13_interval + index13_interval]
        signal_temp = np.reshape(signal_temp, [1, index13_interval])
        temp = get_time_domain_features(signal_temp)
        Fea.append(temp)

    result= {}
    # 原信号数据
    result['fea_y'] = Feaa
    length = len(Feaa)
    f_x1=ndarray2list0(np.arange(length)+1)
    f_x=[x / fs for x in f_x1]
    f_x=[round(num,2) for num in f_x ]
    result['fea_x'] = f_x
    if len(Fea) >= 1:
        result['rms']=Fea[:,0].tolist()
        length2 = len(Fea[:,0])
    else:
        result['rms'] = []
        length2 = 0

    result['fea_xaxis']=ndarray2list0(np.arange(length2)+1)

    return Feaa, f_x, Fea[:,0].tolist(), ndarray2list0(np.arange(length2)+1)

