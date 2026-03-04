import numpy as np
from scipy.signal import butter, filtfilt


# 这里传的数据是预处理完后的加速度有效值
def ski_slope(process_data,fs):
    acc = process_data  # 原始振动信号
    #fs = fs
    # 加了处理轴的代码/2.56 features of the ski slope
    fend = fs/2.56
    # 转为 numpy 数组
    a = np.asarray(acc, dtype=float)
    # 2. 0–1000 Hz滤波
    # 同济代码 
    # lowcut = 0.0
    # highcut = 1000
    # 同济代码
    lowcut = 10.0      # 低频截止
    highcut = 1000.0   # 高频截止
    order = 4
    nyquist = fs / 2.0  # 奈奎斯特频率
    low = lowcut / nyquist
    high = highcut / nyquist
    # order = 4
    #wn = highcut / (fs / 2)
    # 同济代码
    #b, c = butter(order, wn, btype='low')
    b, c = butter(order, [low, high], btype='band')
    a_filt = filtfilt(b, c, a)
    # 3. 时域积分得到速度信号
    # 先去掉这段代码看看
    a_filt = a_filt - np.mean(a_filt)

    return a_filt