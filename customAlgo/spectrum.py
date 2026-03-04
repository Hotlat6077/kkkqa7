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

def custom_spectrum(data, fs, methods='raw'):
    # 转速信号提取
    #fs=fs*0.78125
    result = {}
    speed = 0
    speed = np.array([float(speed)]) / 60
    speed = np.round(speed, 4)
    # 
    signal = np.array(data)
    signal = (signal - np.mean(signal)).tolist()
    # 
    blank_dict = {}
    exec(f"blank_dict['out']={methods}(signal,fs)")
    Feaa = blank_dict['out'].tolist()
    #
    Sampling_points = len(Feaa)  # 采样点数，fft后的点数就是这个数
    df = 1 / fs  # 采样间隔时间
    y = Feaa[:]
    y = list(map(float, y))
    y = np.array(y)
    f_values = np.linspace(0.0, fs / 2.0, Sampling_points // 2)
    fft_values_ = fft.fft(y)
    fft_values = 2.0 / Sampling_points * np.abs(fft_values_[0:Sampling_points // 2])
    log_y = np.log(fft_values + 0.0001)  # 计算对数
    # 原信号数据
    result['fea_y'] = Feaa
    length = len(Feaa)
    f_x1 = ndarray2list0(np.arange(length) + 1)
    f_x = [x / fs for x in f_x1]
    f_x = [round(num, 2) for num in f_x]
    result['fea_x'] = f_x
    # thj im if yu j wq r i j wb r j wb r i j wq r 
    # ce thg dn wftc su bb yi j wftc su bb im e udtx r 
    # rnuf vb r je gd gip j rg gd knx wq sk c fu vfbrhf z g su r e udvv 
    Fea1x = np.round(Fea1x, 3)
    Fea1x = Fea1x.tolist()
    # Fea1x=[num for num in Fea1x if num <= fend]
    result['fea_xaxis'] = Fea1x
    LL = len(Fea1x)
    Fea1y = Fea1y[0:LL]
    result['fftyy'] = Fea1y.tolist()
    result['log_y'] = log_y.tolist()  # 增加对数变换后的数据
    return Fea1y, log_y
