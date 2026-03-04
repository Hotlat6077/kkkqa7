import math
import numpy as np


def get_time_domain_features(data):
    """
    data为一维振动信号
    """
    absXbar = 0
    x_r = 0
    S = 0
    K = 0
    k = 0
    x_rms = 0
    fea = []
    # print(data.shape)
    len_ = int(data.shape[1])
    mean_ = data.mean(axis=1)  # 1.均值
    # var_ = data.var(axis=1)  # 2.方差
    std_ = data.std(axis=1)  # 3.标准差
    max_ = data.max(axis=1)  # 4.最大值
    min_ = data.min(axis=1)  # 5.最小值/
    x_p = max(abs(max_), abs(min_))  # 6.峰值
    for i in range(len_):
        x_rms += data[0, i] ** 2
        # absXbar += abs(data[0, i])
        # x_r += math.sqrt(abs(data[0, i]))
        # S += (data[0, i] - mean_[0]) ** 3
        K += (data[0, i] - mean_[0]) ** 4
    x_rms = math.sqrt(x_rms / len_)  # 7.均方根值
    # absXbar = absXbar / len_  # 8.绝对平均值
    # x_r = (x_r / len_) ** 2  # 9.方根幅值
    # W = x_rms / mean_[0]  # 10.波形指标
    # C = x_p / x_rms  # 11.峰值指标
    # I = x_p / mean_[0]  # 12.脉冲指标
    # L = x_p / x_r  # 13.裕度指标
    # S = S / ((len_ - 1) * std_ ** 3)  # 14.偏斜度
    K = K / ((len_ - 1) * std_ ** 4)  # 15.峭度
    # fea = [mean_[0],absXbar,var_[0],std_[0],x_r,x_rms,x_p,max_[0],min_[0],W,C,I,L,S,K]
    # fea = [x_rms,x_p,x_r,I,S,K]
    # print('mean',type(mean_),mean_)
    # print('x_p',type(x_p),mean_)
    # print('K',type(K),mean_)
    fea = [mean_[0], x_p[0], K[0], x_rms]
    return fea


def time_domain(signal):
    Fea = []
    for i in range(int(len(signal) / 100)):
        signal_temp = signal[i * 100:i * 100 + 100]
        signal_temp = np.reshape(signal_temp, [1, 100])
        temp = get_time_domain_features(signal_temp)
        Fea.append(temp)
    return np.array(Fea)


def time_domain_liu(signal, interval):
    Fea = []
    for i in range(int(len(signal) / interval)):
        signal_temp = signal[i * interval:i * interval + interval]
        signal_temp = np.reshape(signal_temp, [1, interval])
        temp = get_time_domain_features(signal_temp)
        Fea.append(temp)
    return np.array(Fea)
