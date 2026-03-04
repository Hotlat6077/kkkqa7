import numpy as np
import math
import heapq  # ---------- 新增：用于提取最大峰值 ----------
from scipy.fftpack import hilbert, fft, ifft

def ndarray2list0(data):
    list0=[]
    for temp in data:
        list0.append(temp.tolist())
    return list0
def ndarray2list1(data):
    list0=[] 
    for temp in data:
        list0.append(temp.tolist())
    list1=[]
    for i in list0:
        for j in i:
            list1.append(j)
    return list1

def get_time_domain_features(data):
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
    # 最小值绝对值，最大值绝对值 比较大小选值最大的
    x_p = max(abs(max_), abs(min_))  # 6.峰值 这段切分的数据里的峰值 peak
    for i in range(len_):
        x_rms += data[0, i] ** 2  # 这段数据的第个元素的平方再求和
        absXbar += abs(data[0, i])  # 绝对值求和 第一个数据的绝对值和
        x_r += math.sqrt(abs(data[0, i]))  # 这段数据的第个元素的绝对值 开根号 再求和
        S += (data[0, i] - mean_[0]) ** 3  # 偏斜度计算的分子部分 # 每个元素数据-均值 的三次方再求和
        K += (data[0, i] - mean_[0]) ** 4  # 峭度计算的分子部分 # 每个元素数据-均值 的四次方再求和
    rms = math.sqrt(x_rms / len_)  # 7.均方根值 # 每个元素的平方和 除以 元素个数 再开根号
    peak = x_p / x_rms  # 11.峰值指标 # 峰值 除以 均方根值 这段数据的第个元素的平方再求和
    pulse = x_p / mean_[0]  # 12.脉冲指标 均值[0] 是因为 mean_ 是个数组 pulse是脉冲的意思
    ske = S / ((len_ - 1) * std_ ** 3)  # 14.偏斜度 偏斜度计算的分子部分/长度-1 乘以 标准差的三次方
    kur = K / ((len_ - 1) * std_ ** 4)  # 15.峭度 峭度计算的分子部分/长度-1 乘以 标准差的四次方
    fea = [rms, peak, kur, pulse, var, ske]  # rms速度有效值 峰值指标 峭度 脉冲指标 方差 偏斜度

    
    return fea


"""
def get_time_domain_features_new(data):
    len_ = int(data.shape)
    mean_ = data.mean(axis=1)  # 1.均值
    var = data.var(axis=1)      # 2.方差
    std_ = data.std(axis=1)      # 3.标准差
    max_ = data.max(axis=1)      # 4.最大值
    min_ = data.min(axis=1)      # 5.最小值
    # 6.峰值
    x_p = np.maximum(np.abs(max_), np.abs(min_))
    # 7.均方根值 - 向量化计算
    x_rms = np.sum(data ** 2, axis=1)
    rms = np.sqrt(x_rms / len_)
    # 修正：原代码中的 x_r 计算有误，应该是绝对平均值
    # 原代码中 x_r 是 sqrt(abs(x)) 的和，但通常峰值因子计算用的是绝对平均值
    absXbar = np.sum(np.abs(data), axis=1)
    margin = x_p / absXbar  # 修正为峰值因子
    # 10.波形指标
    shape_factor = rms / mean_
    # 11.峰值指标 - 修正计算
    peak = x_p / rms
    # 12.脉冲指标
    pulse = x_p / mean_
    # 13.裕度指标
    clearance = x_p / (np.sum(np.sqrt(np.abs(data)), axis=1) / len_)
    # 14.偏斜度 - 向量化计算
    S = np.sum((data - mean_.reshape(-1, 1)) ** 3, axis=1)
    ske = S / ((len_ - 1) * std_ ** 3)
    # 15.峭度 - 向量化计算
    K = np.sum((data - mean_.reshape(-1, 1)) ** 4, axis=1)
    kur = K / ((len_ - 1) * std_ ** 4)
    # 返回特征数组
    fea = [rms[0], peak[0], kur[0], pulse[0], var[0], ske[0]]
    return fea
"""


# 包络谱
def env(data):
    data = data[1:10000]
    fs = 1000  # 采样频率
    fmin = 200  # 选取频率范围：最小
    fmax = 1000  # 选取频率范围：最大
    n = 1 # 选择分析列数
    m = len(data)
    f = np.arange(0, m) * fs / m  # 频域波形横坐标 ：频率
    f_half = f[0:int(np.round(m / 2))]  # 取一半 
    fmin_number = int(np.round(fmin * m / fs))  # 获取最小值点数
    fmax_number = int(np.round(fmax * m / fs))  # 获取最大值点数

    y_new = [0 * i for i in range(m)]  # 快速创建一个元素为0的列表
    y = np.array(data[:,n - 1])
    y_fft = fft(y)  # fft
    y_new[fmin_number:fmax_number] = y_fft[fmin_number:fmax_number]  # 替换元素
    y_new[m - fmax_number:m - fmin_number] = y_fft[m - fmax_number:m - fmin_number]  # 替换元素
    # 逆变换并取复数的实部
    y_ifft = ifft(y_new).real  # 逆变换并取复数的实部 ifft 是逆傅里叶变换
    H = np.abs(hilbert(y_ifft) - np.mean(y_ifft))  # 包络 hilbert是希尔伯特变换
    HP = np.abs(fft(H - np.mean(H))) * 2 / m  # fft变换后取绝对值 并归一化
    HP_half = HP[0:int(np.round(m / 2))]  # 取一半

    return f_half, HP_half


# 趋势图
def trend_chart(data, fs, methods='raw', window_size=256, overlap=128):
    # 这段暂时没有用到
    speed = 0
    speed = np.array([float(speed)]) / 60
    speed = np.round(speed, 4)
    # ##############
    # 下采样并去均值  实现了：信号中心化 
    signal = np.array(data)  # 1.
    # 下采样并去均值  实现了：信号中心化 
    signal = (signal - np.mean(signal)).tolist()  # .2.
    # 执行自定义方法
    blank_dict = {}
    exec(f"blank_dict['out']={methods}(signal, fs)")  # 3.
    signal = blank_dict['out'].tolist()  # 转List
    # 计算波形指标（基于时间）
    index13_interval = 100 # 每个区间的点数  
    Fea = []
    # 每次切分这段信号的100个点 分隔信号长度 一共可以分为多少段这样的信号
    for i in range(int(len(signal) / index13_interval)):
        # 对信号进行切片提取
        signal_temp = signal[i * index13_interval:i * index13_interval + index13_interval]
        # 重塑为一维数组 shape[1,100] 信号转成 shape[1,100]
        signal_temp = np.reshape(signal_temp, [1, index13_interval])
        # 计算时间域特征 函数代码在上面 get_time_domain_features
        temp = get_time_domain_features(signal_temp)  # 时域特征提取
        Fea.append(temp)  # 每段信号的特征加入Fea列表

    Fea = np.array(Fea) # 转为数组方便后续处理
    # 拼接返回结果
    # 2) 包络分析结果
    # 包络分析 包络是包络和下面的不一样
    Feax, Feay = env(signal, fs)  # Feay是什么值 包络谱的幅值
    result = {}
    # 时间指标（如均方根、峭度等）
    # 这里的 Fea 是一个二维数组，每一列为一种指标，这里假定 Fea[:,0] 有意义
    if len(Fea) >= 1:
        result['pinpu1'] = Fea[:, 0].tolist()  # 第一列数据
        length = len(Fea[:, 0])  # 第一列数据的长度
    else:
        result['pinpu1'] = []  # 空列表
        length = 0  # 长度为0
    # x轴
    result['fea_xaxis1'] = ndarray2list0(np.arange(length) + 1)

    # Feax, Feay 需要返回给前端
    result['fea_xaxis3'] = Feax.tolist()
    result['pinpu3'] = Feay.tolist()  # 频谱3
    # 3) 原始（或处理后）时域波形
    result['pinpu2'] = signal  # 频谱2
    length_signal = len(signal)  # 信号长度
    f_x1 = ndarray2list0(np.arange(length_signal) + 1) #   横坐标点数
    # 横坐标单位换算 为 秒
    f_x = [x / fs for x in f_x1] # 横坐标单位换算 为 秒
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

if __name__ == "__main__":
    trend_chart([], 1000, methods='rms')