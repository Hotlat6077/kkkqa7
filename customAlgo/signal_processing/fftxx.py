import numpy.fft as fft
import numpy as np

def fftxx(data):
    fs = 12800  # 采样频率
    Sampling_points = len(data)  # 采样点数，fft后的点数就是这个数
    df = 1 / fs  # 采样间隔时间
    y = data[:]
    y = list(map(float, y))
    y = np.array(y)
    f_values = np.linspace(0.0, fs/2.0, Sampling_points//2)
    fft_values_ = fft.fft(y)
    fft_values = 2.0/Sampling_points * np.abs(fft_values_[0:Sampling_points//2])
    return f_values, fft_values