import numpy as np
import numpy.fft as fft
from scipy.fftpack import hilbert, fft, ifft

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

def custom_envolpe(data, fs, methods='raw'):
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
    #  
    fmin = 200  # 选取频率范围：最小
    fmax = 1000  # 选取频率范围：最大
    n = 1  # 选择分析列数
    m = len(Feaa)  # 采样点数 未处理信号的长度 信号的点数
    f = np.arange(0, m) * fs / m  # 频域波形很坐标 ：频率
    f_half = f[0:int(np.round(m / 2))]  # 取一半
    fmin_number = int(np.round(fmin * m / fs))  # 获取点数
    fmax_number = int(np.round(fmax * m / fs))
    y_new = [0 * i for i in range(m)]  # 快速创建一个元素为0的列表
    y = np.array(Feaa)
    y_fft = fft(y)  # fft
    y_new[fmin_number:fmax_number] = y_fft[fmin_number:fmax_number]  # 替换元素
    y_new[m - fmax_number:m - fmin_number] = y_fft[m - fmax_number:m - fmin_number]  # 替换元素
    y_ifft = ifft(y_new).real  # 逆变换并取复数的实部
    H = np.abs(hilbert(y_ifft) - np.mean(y_ifft))  # 包络
    HP = np.abs(fft(H - np.mean(H))) * 2 / m  # 计算包络的频谱
    HP_half = HP[0:int(np.round(m / 2))]  #  计算包络单边频谱
    # return f_half, HP_half
    result = {}
    # 原信号数据
    result['fea_y'] = H.tolist()  # 6. H是T.envelopex()方法返回的
    length = len(H)  # H的长度 信号的长度
    f_x1 = ndarray2list0(np.arange(length) + 1)  # 7. 先转Numpy 再转数组长度 H的长度转numpy数组 转列表
    f_x = [x / fs for x in f_x1]  # 8.长度/fs 长度/FS是什么意思啊
    f_x = [round(num, 2) for num in f_x]  # 9. f_x 是上面的f_x变成 2位小数 后装到列表里
    result['fea_x'] = f_x  # 10.fea_x可能是x轴

    result['peak'] = HP_half.tolist()  # 10.peak是峰值 表示包络的峰值么

    Feax = np.round(Feax, 3)  # 11.这里是取3位小数

    # Feax=Feax.astype(int)
    Feax = Feax.tolist()  # 12.装到列表里
    # Fea11x=[num for num in Feax if num <= fend]
    result['fea_xaxis'] = Feax  # 13.表示x轴的坐标
    return Feax, f_x, HP_half
