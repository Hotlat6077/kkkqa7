from scipy.fftpack import fft, fftshift, ifft
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from scipy import signal
from scipy.fftpack import hilbert, fft, ifft
# 包络谱


def env2(data):

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
    y = np.array(data[n - 1])
    y_fft = fft(data)  # fft
    y_new[fmin_number:fmax_number] = y_fft[fmin_number:fmax_number]  # 替换元素
    y_new[m - fmax_number:m - fmin_number] = y_fft[m - fmax_number:m - fmin_number]  # 替换元素
    y_ifft = ifft(y_new).real  # 逆变换并取复数的实部
    H = np.abs(hilbert(y_ifft) - np.mean(y_ifft))  # 包络
    HP = np.abs(fft(H - np.mean(H))) * 2 / m
    HP_half = HP[0:int(np.round(m / 2))]  # 取一半
    return f_half, HP_half