import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt


class filter():

    # 使用巴特沃斯高通滤波器
    def butter_highpass(self, highcut, fs, order=5):
        nyq = 0.5 * fs
        normal_highcut = highcut / nyq
        b1, a1 = butter(order, normal_highcut, btype='high', analog=False)
        return b1, a1

    # 定义高通滤波
    def butter_highpass_filter(self, data, highcut, fs, order=5):
        b1, a1 = self.butter_highpass(highcut, fs, order=order)
        y = lfilter(b1, a1, data)
        return y  # Filter requirements.

    # 使用巴特沃斯带通滤波器
    def butter_bandpass(self, lowcut, highcut, fs, order=2):
        nyq = 0.5 * fs  # 奈奎斯特频率为采样频率的一半
        low = lowcut / nyq
        high = highcut / nyq
        b2, a2 = butter(order, [low, high], btype='band', analog=False)
        return b2, a2

    # 定义带通滤波
    def butter_bandpass_filter(self, data, lowcut, highcut, fs, order=2):
        b2, a2 = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = lfilter(b2, a2, data)   # 使用IIR或FIR滤波器沿一维过滤数据,b为分子系数向量,a为分母系数向量,data为数据
        return y  # y为滤波器输出

    # 使用巴特沃斯低通滤波器
    def butter_lowpass(self, lowcut, fs, order=5):
        nyq = 0.5 * fs
        normal_lowcut = lowcut / nyq
        b3, a3 = butter(order, normal_lowcut, btype='low', analog=False)
        return b3, a3

    # 定义低通滤波
    def butter_lowpass_filter(self, data, lowcut, fs, order=5):
        b3, a3 = self.butter_lowpass(lowcut, fs, order=order)
        y = lfilter(b3, a3, data)
        return y  # Filter requirements.



