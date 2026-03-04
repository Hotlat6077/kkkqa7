# 一、时域指标分析的算法放这里
import numpy as np

from scipy.fftpack import hilbert, fft, ifft
# 包络谱

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


class indexx():
    def __init__(self, RawSignal=None, SampleFraquency=None, Sampleinterval=None, RawSignal2=None):
        self.RawSignal = RawSignal
        self.SampleFraquency = SampleFraquency
        self.Sampleinterval = Sampleinterval
        self.RawSignal2 = RawSignal2

    # 可以根据算法用到的参数进行添加，我这里添加了Sampleinterval，
    # 1.时域六个指标算法
    def time_domainx(self):
        Fea = []
        for i in range(int(len(self.RawSignal) / self.Sampleinterval)):
            signal_temp = self.RawSignal[i * self.Sampleinterval:i * self.Sampleinterval + self.Sampleinterval]
            signal_temp = np.reshape(signal_temp, [1, self.Sampleinterval])
            temp = get_time_domain_features(signal_temp)
            print('tempTpey :', type(temp))
            Fea.append(temp)
        print('Fea length :', len(Fea))
        print('FeaType :', type(Fea))
        print(Fea[0])
        print(np.array(Fea).shape)
        return np.array(Fea)

    # 一次积分
    def time_domain_integral(self):  # 一次积分
        import numpy as np
        from scipy import integrate
        fs = self.SampleFraquency
        len_ = len(self.RawSignal)
        df = 1 / fs
        t = np.linspace(0.0, len_ * df, len_)
        sig = self.RawSignal
        sig_vel = []
        for i in range(len(sig) - 1):
            if i == 0:
                sig_vel.append(integrate.simpson(sig[i:i + 2], t[i:i + 2]))
            else:
                sig_vel.append(sig_vel[-1] + integrate.simpson(sig[i:i + 2], t[i:i + 2]))
        sig_vel = sig_vel - np.mean(sig_vel)
        return t, sig_vel

    # 二次积分
    def time_domain_integral2(self):
        import numpy as np
        from scipy import integrate
        fs = self.SampleFraquency
        len_ = len(self.RawSignal)
        df = 1 / fs
        t = np.linspace(0.0, len_ * df, len_)
        sig = self.RawSignal
        sig_vel = []
        for i in range(len(sig) - 1):
            if i == 0:
                sig_vel.append(integrate.simpson(sig[i:i + 2], t[i:i + 2]))
            else:
                sig_vel.append(sig_vel[-1] + integrate.simpson(sig[i:i + 2], t[i:i + 2]))
        sig_vel = sig_vel - np.mean(sig_vel)
        sig_vel2 = []
        for i in range(len(sig_vel) - 1):
            if i == 0:
                sig_vel2.append(integrate.simpson(sig_vel[i:i + 2], t[i:i + 2]))
            else:
                sig_vel2.append(sig_vel2[-1] + integrate.simpson(sig_vel[i:i + 2], t[i:i + 2]))
        sig_vel2 = sig_vel2 - np.mean(sig_vel2)
        return t, sig_vel2

    # 一次微分
    def cal_deriv(self):
        fs = self.SampleFraquency
        len_ = len(self.RawSignal)
        df = 1 / fs
        y = self.RawSignal
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

        return x, deriv

        # 二次微分

    def cal_deriv2(self):
        fs = self.SampleFraquency
        len_ = len(self.RawSignal)
        df = 1 / fs
        y = self.RawSignal
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
        y = deriv
        x = np.linspace(0.0, len_ * df, len_)
        diff_x1 = []  # 用来存储x列表中的两数之差
        for i, j in zip(x[0::], x[1::]):
            diff_x1.append(j - i)
        diff_y1 = []  # 用来存储y列表中的两数之差
        for i, j in zip(y[0::], y[1::]):
            diff_y1.append(j - i)
        slopes1 = []  # 用来存储斜率
        for i in range(len(diff_y1)):
            slopes1.append(diff_y1[i] / diff_x1[i])
        deriv1 = []  # 用来存储一阶导数
        for i, j in zip(slopes1[0::], slopes1[1::]):
            deriv1.append((0.5 * (i + j)))  # 根据离散点导数的定义，计算并存储结果
        deriv1.insert(0, slopes1[0])  # (左)端点的导数即为与其最近点的斜率
        deriv1.append(slopes1[-1])  # (右)端点的导数即为与其最近点的斜率
        return x, deriv1

    # 频域处理
    def frequency_domain_integral(self):
        from scipy import fftpack
        fs = self.SampleFraquency
        len_ = len(self.RawSignal)
        df = 1 / fs
        t = np.linspace(0.0, df * len_, len_)
        sig = self.RawSignal
        sig_fft = fftpack.fft(sig)  # 求取sig信号的FFT变换结果
        sig_fre = fftpack.fftfreq(len(sig_fft), d=1 / fs)  # 求取sig信号的FFT变换频率
        sig_fft[1:] = sig_fft[1:] / (1j * 2 * np.pi * sig_fre[1:])  # 信号时域处理，注意0Hz的处理
        sig_vel = fftpack.ifft(sig_fft).real  # 转换为时域信号
        return t, sig_vel

    # 自相关分析
    def sig_corr(self):
        import numpy as np
        fs = self.SampleFraquency
        len_ = len(self.RawSignal)
        df = 1 / fs
        t = np.linspace(0.0, df * len_, len_)
        sig = self.RawSignal
        sig_corr = np.correlate(sig, sig, 'same') / (len(sig))
        return t, sig_corr

    # 偏向关分析
    def sig_pcorr(self):
        import numpy as np
        fs = self.SampleFraquency
        len_ = len(self.RawSignal)
        df = 1 / fs
        t = np.linspace(0.0, df * len_, len_)
        sig = self.RawSignal
        sig_2 = self.RawSignal2
        sig_corr = np.correlate(sig, sig_2, 'same') / (len(sig))
        return t, sig_corr

    # ####一阶差分##############
    def fun_calDiff(self):
        data_diff = []
        for i in range(len(self.RawSignal) - 1):
            data_diff.append(self.RawSignal[i + 1] - self.RawSignal[i])

        return data_diff

    # #####二阶差分##############
    def fun_calDiff2(self):
        data_diff = []
        for i in range(len(self.RawSignal) - 1):
            data_diff.append(self.RawSignal[i + 1] - self.RawSignal[i])
        data_diff2 = []
        for i in range(len(data_diff) - 1):
            data_diff2.append(data_diff[i + 1] - data_diff[i])
        return data_diff2

    # 频域积分
    def frequency_domain_integral(self):
        import numpy as np
        from scipy.integrate import cumtrapz
        fs = self.SampleFraquency
        len_ = len(self.RawSignal)
        df = 1 / fs
        t = np.linspace(0.0, df * len_, len_)
        signal = self.RawSignal
        # 频域积分
        # 计算信号的功率谱密度（PSD）
        psd = np.abs(np.fft.fft(signal)) ** 2

        # 构建频率轴
        sampling_rate = 1 / (t[1] - t[0])
        freq = np.fft.fftfreq(len(t), d=1 / sampling_rate)

        # 找到频率为0的索引
        zero_freq_index = np.where(freq == 0)[0][0]

        # 删除频率为0的分量
        psd = np.delete(psd, zero_freq_index)
        freq = np.delete(freq, zero_freq_index)

        positive_freq_index = np.where(freq >= 0)[0]

        # 只保留正频率部分的功率谱密度和频率
        psd = psd[positive_freq_index]
        freq = freq[positive_freq_index]
        t = t[positive_freq_index]
        # 频域积分
        cumulative_psd = cumtrapz(psd, dx=(freq[1] - freq[0]), initial=0)

        # 转换为位移频谱
        displacement_spectrum = cumulative_psd / ((2 * np.pi * freq) ** 2) * (1 / sampling_rate) ** 2

        return t, displacement_spectrum

    def covariance_pca_plot(self):
        # 计算协方差矩阵
        import numpy as np
        x = np.array(self.RawSignal)
        y = np.array(self.RawSignal2)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        x = np.subtract(x, x_mean)
        y = np.subtract(y, y_mean)
        # 归一化
        x_min = np.min(x)
        x_max = np.max(x)
        y_min = np.min(y)
        y_max = np.max(y)
        x = np.divide(np.subtract(x, x_min), x_max - x_min)
        y = np.divide(np.subtract(y, y_min), y_max - y_min)
        # 标准化
        x_std = np.std(x)
        y_std = np.std(y)
        x = np.divide(x, x_std)
        y = np.divide(y, y_std)

        if x.size > y.size:
            x = x[:y.size]
        else:
            y = y[:x.size]
        x = np.squeeze(x)
        y = np.squeeze(y)
        x = x.astype(float)
        y = y.astype(float)

        covariance_matrix = np.cov(np.vstack((x, y)))
        # 返回转换后的数据
        return covariance_matrix


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
