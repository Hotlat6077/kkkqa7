# 10.高中低频分析
from datetime import datetime
import os

# preprocessing数据预处理方式

# 4. 低通滤波
def hmlfrequencyx1(vib, fs):
    from scipy.signal import butter, lfilter
    fs = fs  # 采样频率
    n = len(vib)  # 点数
    # 设置滤波器参数
    # order = 10
    #
    lowcut = 150  # 低频
    highcut = 300  # 高频
    # 0615
    # lowcut = 2000  # 低频
    # highcut = 4000  # 高频

    # 低通滤波后的低频时域信号
    nyq = 0.5 * fs
    normal_lowcut = lowcut / nyq
    order = 5
    b1, a1 = butter(order, normal_lowcut, btype='low', analog=False)
    y1 = lfilter(b1, a1, vib)
    # 带通滤波后的中频时域信号
    nyq = 0.5 * fs  # 奈奎斯特频率为采样频率的一半
    low = lowcut / nyq
    high = highcut / nyq
    order = 2
    b2, a2 = butter(order, [low, high], btype='band', analog=False)
    y2 = lfilter(b2, a2, vib)
    # 高通滤波后的高频时域信号
    nyq = 0.5 * fs
    normal_highcut = highcut / nyq
    order = 5
    b3, a3 = butter(order, normal_highcut, btype='high', analog=False)
    y3 = lfilter(b3, a3, vib)
    return y1

# 高通滤波
def hmlfrequencyx2(vib, fs):
    from scipy.signal import butter, lfilter
    fs = fs  # 采样频率
    n = len(vib)  # 点数
    # 设置滤波器参数
    # order = 10
    #
    lowcut = 150  # 低频
    highcut = 300  # 高频
    # 0615
    # lowcut = 2000  # 低频
    # highcut = 4000  # 高频

    # 低通滤波后的低频时域信号
    nyq = 0.5 * fs
    normal_lowcut = lowcut / nyq
    order = 5
    b1, a1 = butter(order, normal_lowcut, btype='low', analog=False)
    y1 = lfilter(b1, a1, vib)
    # 带通滤波后的中频时域信号
    nyq = 0.5 * fs  # 奈奎斯特频率为采样频率的一半
    low = lowcut / nyq
    high = highcut / nyq
    order = 2
    b2, a2 = butter(order, [low, high], btype='band', analog=False)
    y2 = lfilter(b2, a2, vib)
    # 高通滤波后的高频时域信号
    nyq = 0.5 * fs
    normal_highcut = highcut / nyq
    order = 5
    b3, a3 = butter(order, normal_highcut, btype='high', analog=False)
    y3 = lfilter(b3, a3, vib)
    return y2

# 带通滤波
def hmlfrequencyx3(vib, fs):
    from scipy.signal import butter, lfilter
    fs = fs  # 采样频率
    n = len(vib)  # 点数
    # 设置滤波器参数
    # order = 10
    #
    lowcut = 150  # 低频
    highcut = 300  # 高频
    # 0615
    # lowcut = 2000  # 低频
    # highcut = 4000  # 高频

    # 低通滤波后的低频时域信号
    nyq = 0.5 * fs
    normal_lowcut = lowcut / nyq
    order = 5
    b1, a1 = butter(order, normal_lowcut, btype='low', analog=False)
    y1 = lfilter(b1, a1, vib)
    # 带通滤波后的中频时域信号
    nyq = 0.5 * fs  # 奈奎斯特频率为采样频率的一半
    low = lowcut / nyq
    high = highcut / nyq
    order = 2
    b2, a2 = butter(order, [low, high], btype='band', analog=False)
    y2 = lfilter(b2, a2, vib)
    # 高通滤波后的高频时域信号
    nyq = 0.5 * fs
    normal_highcut = highcut / nyq
    order = 5
    b3, a3 = butter(order, normal_highcut, btype='high', analog=False)
    y3 = lfilter(b3, a3, vib)
    return y3


# 3.带阻滤波 2024年6月8号####################
def BRF(vib, fs):
    # lowcut=50
    # highcut=100
    # N=8
    # import numpy as np
    # import scipy.signal as signal
    # fs = fs  # 采样频率
    # len_ = len(vib)
    # df = 1 / fs
    # t = np.linspace(0.0, len_ * df, len_)
    # x =  vib   # 原始信号
    # # 确定带阻滤波器的参数
    # lowcut = float(lowcut) # 阻带的下截止频率
    # highcut = float(highcut)  # 阻带的上截止频率
    # # 设计带阻滤波器
    # nyq = 0.5 * fs
    # low = lowcut / nyq
    # high = highcut / nyq
    # b, a = signal.butter(int(N), [low, high], btype='bandstop')
    # # 应用滤波器到时域信号
    # filtered_signal = signal.lfilter(b, a, x)
    # return filtered_signal
    from scipy.signal import butter, lfilter
    fs = fs  # 采样频率
    n = len(vib)  # 点数
    lowcut = 300  # 低频
    highcut = 800  # 高频
    nyq = 0.5 * fs
    normal_lowcut = lowcut / nyq
    order = 5
    b1, a1 = butter(order, normal_lowcut, btype='low', analog=False)
    y1 = lfilter(b1, a1, vib)
    # 高通滤波后的高频时域信号
    nyq = 0.5 * fs
    normal_highcut = highcut / nyq
    order = 5
    b3, a3 = butter(order, normal_highcut, btype='high', analog=False)
    y3 = lfilter(b3, a3, vib)
    y2 = (y1 + y3) / 2
    return y2


import numpy as np


def raw(vib, fs):
    vib = np.array(vib)
    fs = fs
    return vib

# 1.积分
def tintegral(vib, fs):  # 积分
    from scipy import integrate
    fs = fs
    len_ = len(vib)
    df = 1 / fs
    t = np.linspace(0.0, len_ * df, len_)
    sig = vib
    sig_vel = []
    for i in range(len(sig) - 1):
        if i == 0:
            sig_vel.append(integrate.simpson(sig[i:i + 2], t[i:i + 2]))
        else:
            sig_vel.append(sig_vel[-1] + integrate.simpson(sig[i:i + 2], t[i:i + 2]))
    sig_vel = sig_vel - np.mean(sig_vel)
    return sig_vel

# 信号微积分
def cderiv(vib, fs):
    fs = fs
    len_ = len(vib)
    df = 1 / fs
    y = vib
    x = np.linspace(0.0, len_ * df, len_)

    diff_x = []  # 用来存储x列表中的两数之差
    for i, j in zip(x[0::], x[1::]):
        diff_x.append(j - i)
    diff_y = []  # 用来存储y列表中的两数之差
    for i, j in zip(y[0::], y[1::]):
        diff_y.append(j - i)
    slopes = []  # 用来存储斜率
    for i in range(len(diff_y)):
        slopes.append(diff_y[i] / diff_x[i])
    deriv = []  # 用来存储一阶导数
    for i, j in zip(slopes[0::], slopes[1::]):
        deriv.append((0.5 * (i + j)))  # 根据离散点导数的定义，计算并存储结果
    deriv.insert(0, slopes[0])  # (左)端点的导数即为与其最近点的斜率
    deriv.append(slopes[-1])  # (右)端点的导数即为与其最近点的斜率
    deriv = np.array(deriv) / 10000
    return deriv

# 剔除异常点
def routliers(vib, fs):
    method = "iqr",
    threshold = 0.1,
    window_size = 50
    signal = vib
    signal = np.array(signal)
    q1 = np.percentile(signal, 25)
    q3 = np.percentile(signal, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    filtered_signal = signal[(signal > lower_bound) & (signal < upper_bound)]
    return filtered_signal

# 消除线性趋势
def ETT(vib, fs):
    import numpy as np
    from scipy.signal import detrend
    signal = vib
    fs = fs
    len_ = len(vib)
    df = 1 / fs
    time = np.linspace(0.0, df * len_, len_)
    linear_detrended_signal = detrend(signal)
    # 消除二次趋势
    return linear_detrended_signal

# 消除二次趋势
def ET2T(vib, fs):
    degree = 2
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.linear_model import LinearRegression
    fs = fs
    len_ = len(vib)
    df = 1 / fs
    t = np.linspace(0.0, len_ * df, len_)
    sig = np.array(vib)
    sig = sig.reshape(-1, 1)
    t = t.reshape(-1, 1)
    # 构造多项式回归模型
    poly_reg = Pipeline([
        ('poly', PolynomialFeatures(degree=degree)),
        ('lin_reg', LinearRegression(fit_intercept=False))])
    # 训练多项式回归模型（即求待定系数）
    poly_reg.fit(t, sig)
    # 去除趋势项
    sig_predict = poly_reg.predict(t)
    sig_res = sig - sig_predict
    # 输出趋势项待定系数
    model = poly_reg.named_steps['lin_reg']
    sig_res = sig_res.flatten()
    # 返回去趋势项结果
    return sig_res


def find_closest_file(folder_path, new_str):
    # 提取new_str中的time部分
    print(f'################Raw_{new_str}')
    new_time_str = new_str.split('_')[1].split('%')[0]
    # 将新的时间字符串转换为datetime对象
    new_time = datetime.strptime(new_time_str, '%Y%m%d%H%M%S')

    # 初始化最小时间差和最接近的文件名
    min_diff = float('inf')
    closest_file = None

    # 遍历文件夹中的所有文件
    for filename in [i for i in os.listdir(folder_path) if '%' in i and len(i.split('%')[0][2:]) == 14]:
        # 提取文件名中的时间字符串
        file_time_str = filename.split('_')[1].split('%')[0]
        # 尝试将文件名中的时间字符串转换为datetime对象
        # try:
        file_time = datetime.strptime(file_time_str, '%Y%m%d%H%M%S')
        # 计算时间差
        diff = abs((new_time - file_time).total_seconds())
        # 如果当前文件的时间差小于已知的最小时间差，则更新最小时间差和最接近的文件名
        if diff < min_diff:
            min_diff = diff
            closest_file = filename
        # except ValueError:
        # 如果文件名中的时间字符串格式不正确，则跳过该文件
        # continue
    print(closest_file)
    return closest_file
