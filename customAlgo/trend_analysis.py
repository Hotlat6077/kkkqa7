import numpy as np
import numpy.fft as fft
import heapq
from scipy.fftpack import hilbert, fft, ifft
from sig_frequency2 import indexx


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


def env(data):
    data = data[1:10000]
    fs = 1000  # 采样频率
    fmin = 200  # 选取频率范围：最小
    fmax = 1000  # 选取频率范围：最大
    n = 1 # 选择分析列数
    m = len(data)
    f = np.arange(0, m) * fs / m  # 频域波形很坐标 ：频率
    f_half = f[0:int(np.round(m / 2))]  # 取一半
    fmin_number = int(np.round(fmin * m / fs))  # 获取点数
    fmax_number = int(np.round(fmax * m / fs))
    y_new = [0 * i for i in range(m)]  # 快速创建一个元素为0的列表
    y = np.array(data[:,n - 1])
    y_fft = fft(y)  # fft
    y_new[fmin_number:fmax_number] = y_fft[fmin_number:fmax_number]  # 替换元素
    y_new[m - fmax_number:m - fmin_number] = y_fft[m - fmax_number:m - fmin_number]  # 替换元素
    y_ifft = ifft(y_new).real  # 逆变换并取复数的实部
    H = np.abs(hilbert(y_ifft) - np.mean(y_ifft))  # 包络
    HP = np.abs(fft(H - np.mean(H))) * 2 / m
    HP_half = HP[0:int(np.round(m / 2))]  # 取一半
    return f_half, HP_half


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


def custom_trend_analysis(data, fs, methods='raw',index13_interval=100):
    # 转速信号提取
    result = {}
    speed = 0
    speed = np.array([float(speed)]) / 60
    speed = np.round(speed, 4)
    # 
    signal = np.array(data)  # 1.列表转为数组
    signal = (signal - np.mean(signal)).tolist()  # 2.将成numpy数组转换列表 这里这个numpy数据的列表怎么没有用到呢
    blank_dict = {}  # 3.创建一个空字典
    exec(f"blank_dict['out']={methods}(signal,fs)")
    Feaa = blank_dict['out'].tolist()  # feaa 就是上面的methods执行得到的结果 vib 字典输出为数组numpy转化成别的数组
    # 计算波形指标（基于时间）
    Fea = []
    for i in range(int(len(Feaa) / index13_interval)):
        signal_temp = Feaa[i * index13_interval:i * index13_interval + index13_interval]
        signal_temp = np.reshape(signal_temp, [1, index13_interval])
        temp = get_time_domain_features(signal_temp)
        Fea.append(temp)

    # 包络分析
    Feax, Feay = env(signal, fs)
    
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
    # result['fea_xaxis2'] = f_x

    
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

    return result

    
