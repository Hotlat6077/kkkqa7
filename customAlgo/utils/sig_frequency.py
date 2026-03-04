# 二、频域分析的算法放这里
import numpy as np
import sys
import os
import numpy.fft as fft
    

class frequencyx():
    def __init__(self, RawSignal=None, RawSignal2=None, SampleFraquency=None):
        self.RawSignal = RawSignal
        self.RawSignal2 = RawSignal2
        self.SampleFraquency = SampleFraquency

    # 1.频谱分析
    def fftx(self):
        fs = self.SampleFraquency  # 采样频率 每秒对信号的记录次数
        Sampling_points = len(self.RawSignal)  # 样本长度，fft后的点数就是这个数 在这一秒采了多少个点 
        df = 1 / fs  # 采样间隔时间 每隔多少时间采样一个点
        y = self.RawSignal[:]  # 复制一份信号数据 相当于 self.RawSignal.copy()
        y = list(map(float, y))  # 把数据都转成float类型 [float(x) for x in y]
        y = np.array(y)  # 转成numpy的array类型
        f_values = np.linspace(0.0, fs / 2.0, Sampling_points // 2)  # 频率范围 0到采样频率的一半，采样点数为采样点数的一半 等分成 Sampling_points // 2 份 频率中取1半
        fft_values_ = fft.fft(y) # 对信号进行傅里叶变换 将时域信号变成频域信号
        # 所以 2.0 / Sampling_points 的核心作用是：将FFT结果转换为物理上有意义的幅度值，使得频域幅度直接对应时域信号的真实振幅。
        fft_values = 2.0 / Sampling_points * np.abs(fft_values_[0:Sampling_points // 2])
        return f_values, fft_values  # 频率分辨率 频率幅值 fft_values_ 包含了原始信号在所有频率分量上的复振幅信息

    # 2.倒谱分析
    def cepstrumx(self):
        y = np.fft.fft(self.RawSignal)
        y = np.log(np.abs(y))  # 对信号的频谱取对数
        # 倒谱分析（Cepstrum Analysis）是语音信号处理和故障诊断中的重要工具，它的核心价值在于分离卷积信号中的激励源和系统响应。
        y = np.fft.ifft(y).real  # 再进行逆傅里叶变换 并取实部
        return y

    # 3.实倒谱分析
    def recepstrumx(self):
        y = np.fft.fft(self.RawSignal)
        y = np.log(np.abs(y))
        y = np.fft.ifft(y).real
        return y

    # 4.实倒谱分析
    def logcepstrumx(self):
        y = np.fft.fft(self.RawSignal)
        y = np.log(np.abs(y))
        y = np.fft.ifft(y).real
        return y

    # 6.包络谱分析
    def envelopex(self):
        from scipy.fftpack import hilbert, fft, ifft
        fmin = 200  # 选取频率范围：最小
        fmax = 1000  # 选取频率范围：最大
        n = 1  # 选择分析列数
        m = len(self.RawSignal)  # 采样点数 采了多少个点
        f = np.arange(0, m) * self.SampleFraquency / m  # 频域波形很坐标 ：频率    这个公式是计算每个频率分辨率 对应的频率值 
        f_half = f[0:int(np.round(m / 2))]  # 取一半 频率分辨率
        fmin_number = int(np.round(fmin * m / self.SampleFraquency))  # 获取点数
        fmax_number = int(np.round(fmax * m / self.SampleFraquency))  # 获取点数
        y_new = [0 * i for i in range(m)]  # 快速创建一个元素为0的列表 长度为m
        y = np.array(self.RawSignal)  # 转成numpy的array类型
        y_fft = fft(y)  # fft 变换
        y_new[fmin_number:fmax_number] = y_fft[fmin_number:fmax_number]  # 频率分辨率切片
        y_new[m - fmax_number: m - fmin_number] = y_fft[m - fmax_number: m - fmin_number]  # 频率分辨率切片
        y_ifft = ifft(y_new).real  # 逆变换并取复数的实部 又变成时域信号 
        H = np.abs(hilbert(y_ifft) - np.mean(y_ifft))  # 包络计算
        HP = np.abs(fft(H - np.mean(H))) * 2 / m  # 计算包络的频谱
        HP_half = HP[0:int(np.round(m / 2))]  #  计算包络单边频谱 
        # return f_half, HP_half
        return f_half, HP_half # h_half 包络频谱分辨率 Half 包络单边频谱 

    # 6.二维全息谱
    def holospectrum3(self):
        import numpy.fft as fft
        fs = self.SampleFraquency  # 采样频率
        Sampling_points = len(self.RawSignal)  # 采样点数，fft后的点数就是这个数
        df = 1 / fs  # 采样间隔时间
        y = self.RawSignal[:]
        y = list(map(float, y))
        y = np.array(y)
        f_values = np.linspace(0.0, fs / 2.0, Sampling_points // 2)
        fft_values_ = fft.fft(y)
        fft_values = 2.0 / Sampling_points * np.abs(fft_values_[0:Sampling_points // 2])
        return f_values, fft_values

    # 7.三维全息谱

    # 9.小波包络分析
    def WT_envelope(self):
        import pywt
        from scipy import signal
        # Create wavelet object and define parameters
        w = pywt.Wavelet('db8')  # 选用Daubechies8小波
        maxlev = pywt.dwt_max_level(len(self.RawSignal), w.dec_len)
        print("maximum level is " + str(maxlev))
        # Decompose into wavelet components, to the level selected:
        coeffs = pywt.wavedec(self.RawSignal, 'db8', level=maxlev)  # 将信号进行小波分解
        for i in range(1, len(coeffs)):
            coeffs[i] = pywt.threshold(coeffs[i], 0.2 * max(coeffs[i]))  # 将噪声滤波
        datarec = pywt.waverec(coeffs, 'db8')  # 将信号进行小波重构
        xh = signal.hilbert(datarec)
        xe = np.abs(xh)
        xe = xe - np.mean(xe)
        xh3 = np.fft.rfft(xe) / len(xe)
        amp = abs(xh3) * 2
        return xe, amp

    # 10.高中低频分析
    def hmlfrequencyx(self):
        from scipy.signal import butter, lfilter
        fs = self.SampleFraquency  # 采样频率
        n = len(self.RawSignal)  # 点数
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
        y1 = lfilter(b1, a1, self.RawSignal)
        # 带通滤波后的中频时域信号
        nyq = 0.5 * fs  # 奈奎斯特频率为采样频率的一半
        low = lowcut / nyq
        high = highcut / nyq
        order = 2
        b2, a2 = butter(order, [low, high], btype='band', analog=False)
        y2 = lfilter(b2, a2, self.RawSignal)
        # 高通滤波后的高频时域信号
        nyq = 0.5 * fs
        normal_highcut = highcut / nyq
        order = 5
        b3, a3 = butter(order, normal_highcut, btype='high', analog=False)
        y3 = lfilter(b3, a3, self.RawSignal)
        return y1, y2, y3

    # 11.自功率谱
    def aps(self, window='hann', nperseg=None, noverlap=None, nfft=None,
            detrend='constant', return_onesided=True, scaling='spectrum',
            axis=-1, average='mean'):
        r"""
        Estimate auto power spectrum using Welch's method.

        """
        from scipy.signal import csd
        freqs, Pxx = csd(self.RawSignal, self.RawSignal, fs=self.SampleFraquency, window=window, nperseg=nperseg,
                         noverlap=noverlap, nfft=nfft, detrend=detrend,
                         return_onesided=return_onesided, scaling=scaling,
                         axis=axis, average=average)
        aps = np.sqrt(Pxx.real)
        return freqs, aps

    # 12.互功率谱
    def cps(self, window='hann', nperseg=None, noverlap=None, nfft=None,
            detrend='constant', return_onesided=True, scaling='spectrum',
            axis=-1, average='mean'):
        """Estimate the cross power spectrum, Pxy, using Welch's method."""
        from scipy.signal.spectral import _spectral_helper, _median_bias
        freqs, _, Pxy = _spectral_helper(self.RawSignal, self.RawSignal2, self.SampleFraquency, window, nperseg,
                                         noverlap, nfft,
                                         detrend, return_onesided, scaling, axis,
                                         mode='psd')
        # Average over windows.
        if len(Pxy.shape) >= 2 and Pxy.size > 0:
            if Pxy.shape[-1] > 1:
                if average == 'median':
                    Pxy = np.median(Pxy, axis=-1) / _median_bias(Pxy.shape[-1])
                elif average == 'mean':
                    Pxy = Pxy.mean(axis=-1)
                else:
                    raise ValueError('average must be "median" or "mean", got %s'
                                     % (average,))
            else:
                Pxy = np.reshape(Pxy, Pxy.shape[:-1])
        cps = np.abs(Pxy)
        return freqs, cps

    # 13.1自功率谱密度
    def apd(self, window='hann', nperseg=None, noverlap=None, nfft=None,
            detrend='constant', return_onesided=True, scaling='density',
            axis=-1, average='mean'):
        r"""
        Estimate auto power spectral density using Welch's method.

        """
        from scipy.signal import csd
        freqs, Pxx = csd(self.RawSignal, self.RawSignal, fs=self.SampleFraquency, window=window, nperseg=nperseg,
                         noverlap=noverlap, nfft=nfft, detrend=detrend,
                         return_onesided=return_onesided, scaling=scaling,
                         axis=axis, average=average)
        apd = Pxx.real
        return freqs, apd

    # 13.2互功率谱密度
    def cpd(self, window='hann', nperseg=None, noverlap=None, nfft=None,
            detrend='constant', return_onesided=True, scaling='density',
            axis=-1, average='mean'):
        """Estimate the cross power spectrum density, Pxy, using Welch's method."""
        from scipy.signal.spectral import _spectral_helper, _median_bias
        freqs, _, Pxy = _spectral_helper(self.RawSignal, self.RawSignal2, self.SampleFraquency, window, nperseg,
                                         noverlap, nfft,
                                         detrend, return_onesided, scaling, axis,
                                         mode='psd')
        # Average over windows.
        if len(Pxy.shape) >= 2 and Pxy.size > 0:
            if Pxy.shape[-1] > 1:
                if average == 'median':
                    Pxy = np.median(Pxy, axis=-1) / _median_bias(Pxy.shape[-1])
                elif average == 'mean':
                    Pxy = Pxy.mean(axis=-1)
                else:
                    raise ValueError('average must be "median" or "mean", got %s'
                                     % (average,))
            else:
                Pxy = np.reshape(Pxy, Pxy.shape[:-1])
        cpd = np.abs(Pxy)
        return freqs, cpd

    # 14.1自相关函数
    def autocorr(self):
        fs = self.SampleFraquency  # 采样频率
        Sampling_points = len(self.RawSignal)  # 采样点数，fft后的点数就是这个数
        n = np.arange(0, Sampling_points)
        t = n / fs
        acf = np.correlate(self.RawSignal, self.RawSignal, mode='full')
        N = len(self.RawSignal)
        acf = acf[N - 1:]
        acf = acf / np.arange(N, 0, -1)
        result = acf / acf[0]
        return t, result

    # 14.2互相关函数
    def crosscorr(self):
        fs = self.SampleFraquency  # 采样频率
        Sampling_points = len(self.RawSignal)  # 采样点数，fft后的点数就是这个数
        n = np.arange(0, Sampling_points)
        t = n / fs
        acf = np.correlate(self.RawSignal, self.RawSignal2, mode='full')
        N = len(self.RawSignal)
        acf = acf[N - 1:]
        acf = acf / np.arange(N, 0, -1)
        result = acf / acf[0]
        return t, result

    # 14.3相干频谱
    def cohes(self):
        from scipy import signal
        # Coherence computing
        faux, Caux = signal.coherence(self.RawSignal, self.RawSignal2, fs=self.SampleFraquency)
        return faux, Caux

    # 15.功率谱

    # 16.伯德图
    # 17.启停机伯德图
    def bodex(self):
        N = len(self.RawSignal)
        dft = np.fft.fft(self.RawSignal)
        abs_dft = np.abs(dft)
        angle_dft = 180 * np.angle(dft) / np.pi
        new_dft = abs_dft[range(int(N / 2))] * 2 / N
        new_angle = angle_dft[range(int(N / 2))]
        return new_dft, new_angle

    # 18.棒值图

    # 19.Nyquist采样
    def Nyquistx(self):
        from scipy import signal
        r = 5
        data = self.RawSignal
        y = signal.decimate(data, r)
        fs = self.SampleFraquency / r
        return y, fs

    # 20.相位分析
    def phasex(self):
        x = self.RawSignal[:2000]
        fs = self.SampleFraquency  # 采样频率
        Sampling_points = len(x)  # 采样点数
        fft = np.fft.fft(self.RawSignal)
        fft_freq = np.arange(Sampling_points) * fs / Sampling_points
        fft_phase = np.angle(fft)
        return fft_freq, fft_phase

    # 21.自谱FFT
    def apfft(self):
        # from numpy.dual import fft
        from numpy import fft
        fs = self.SampleFraquency  # 采样频率
        Sampling_points = len(self.RawSignal)  # 采样点数
        freqs = np.arange(Sampling_points) * fs / Sampling_points
        cor_x = np.correlate(self.RawSignal, self.RawSignal, 'same')
        cor_X = fft(cor_x, Sampling_points)
        ps_cor = np.abs(cor_X)
        ps_cor = ps_cor / np.max(ps_cor)
        result = 20 * np.log10(ps_cor[:Sampling_points])
        return freqs, result

    # 22.交叉相位（相位差）
    def phasediff(self):
        fs = self.SampleFraquency  # 采样频率
        Sampling_points = len(self.RawSignal)  # 采样点数
        freqs = np.arange(Sampling_points) * fs / Sampling_points
        # 进行傅立叶变换，时域变频域
        data1 = np.fft.fft(self.RawSignal)
        data2 = np.fft.fft(self.RawSignal2)
        data11 = np.angle(data1, deg=True)
        data21 = np.angle(data2, deg=True)
        # 对数据进行解卷绕unwrap#
        data12 = data11 / 180 * np.pi
        data13 = np.unwrap(data12)
        data22 = data21 / 180 * np.pi
        data23 = np.unwrap(data22)
        phasediff = (data23 - data13) * 180 / np.pi
        return freqs, phasediff

    # 23.相位矫正
    def phasecx(self):
        from scipy.fftpack import fft, ifft
        import cmath
        lengthx = len(self.RawSignal)
        lengthy = len(self.RawSignal2)
        px = np.ceil(np.log2(np.abs(lengthx))).astype('long')
        py = np.ceil(np.log2(np.abs(lengthy))).astype('long')
        nfftx = 2 ** px
        nffty = 2 ** py
        x = np.array(self.RawSignal)
        y = np.array(self.RawSignal2)
        X = fft(x, nfftx)
        Y = fft(y, nffty)
        indx = np.argmax(abs(X), axis=0)
        indy = np.argmax(abs(Y))
        angle_y = np.angle(Y[indy])  # atan
        angle_x = np.angle(X[indx])
        PhDiff = angle_x - angle_y
        n = 500  # 转速 rpm;
        w = n * cmath.pi / 30  # 转速转化为rad/s
        Diff = PhDiff / w
        fy = fft(np.array(Y))
        Y1 = fy * cmath.exp(-1j * w * Diff)
        Y1 = ifft(Y1)  # 校正后信号
        Y1 = Y1.real
        return Y1

    # 25.频率响应分析
    def frfx(self):
        z = np.exp(self.RawSignal)
        num = z ** 5 - z ** 4 + z ** 3 - z ** 2
        denom = z ** 5 + 0.54048 * z ** 4 - 0.62519 * z ** 3 - 0.66354 * z ** 2 + 0.60317 * z + 0.69341
        x_final = num / denom
        return x_final

    # ICA分析
    def ica_denoise(self, algorithm, input3):
        # 预处理：中心化信号
        import numpy as np
        from sklearn.decomposition import FastICA
        from middle.SignalProcessing2_27_ica import choose_algorithm

        noisy_signal = np.array(self.RawSignal)
        # 创建ICA模型
        algorithm = choose_algorithm(algorithm)
        ica = FastICA(n_components=input3, algorithm=algorithm, whiten='arbitrary-variance')

        # 对信号进行降噪和提取
        ica_signal = ica.fit_transform(noisy_signal.reshape(-1, 1)).flatten()

        return ica_signal

    # 1.5维谱
    def compute_1and5_envelopex(self):
        from scipy.fftpack import hilbert, fft, ifft
        fmin = 200
        fmax = 1000
        SampleFraquency = 1000
        n = 1
        m = len(self.RawSignal)
        f = np.arange(0, m) * SampleFraquency / m
        f_half = f[0:int(np.round(m / 2))]
        fmin_number = int(np.round(fmin * m / SampleFraquency))
        fmax_number = int(np.round(fmax * m / SampleFraquency))
        y_new = [0 * i for i in range(m)]
        y = np.array(self.RawSignal)
        y_fft = fft(y)  # fft
        y_new[fmin_number:fmax_number] = y_fft[fmin_number:fmax_number]
        y_new[m - fmax_number:m - fmin_number] = y_fft[m - fmax_number:m - fmin_number]
        y_ifft = ifft(y_new).real
        H = np.abs(hilbert(y_ifft) - np.mean(y_ifft))  # 包络
        HP = np.abs(fft(H - np.mean(H))) * 2 / m
        y = HP[0:int(np.round(m / 2))]  #
        y = y.reshape(y.shape[0], 1)
        # 对包络信号进行1.5维谱分析
        y = np.fft.fft(y)
        y = y.real
        return f_half, y

    def FVS(self):
        import numpy as np
        from scipy.fft import fft
        from scipy.signal.windows import hann
        # 假设这是采集到的振动信号数据

        sample_rate = self.SampleFraquency
        signal = self.RawSignal

        # 消除DC偏移
        signal = signal - np.mean(signal)

        # 应用窗函数
        window = hann(len(signal))
        windowed_signal = signal * window

        # 应用FFT获取频谱
        fft_result = fft(windowed_signal)
        frequencies = np.fft.fftfreq(len(fft_result), 1 / sample_rate)

        # 计算幅度（归一化）和相位
        amplitudes = np.abs(fft_result) / len(signal)
        phases = np.angle(fft_result)

        # 只保留正频率部分
        half_len = len(frequencies) // 2
        positive_frequencies = frequencies[:half_len]
        positive_amplitudes = amplitudes[:half_len]
        positive_phases = phases[:half_len]
        return positive_phases, positive_amplitudes

    def socs(self):
        from scipy.sparse import coo_matrix
        # 生成信号
        x = self.RawSignal
        Fs = self.SampleFraquency
        N = len(x)
        alphas = np.linspace(-Fs / 2, Fs / 2, N // 50)
        # FFT长度
        Nfft = 2 ** np.ceil(np.log2(N)).astype(int)  # 调整FFT长度

        # 计算二阶循环谱
        f, alphas, Sxx_alpha = cyclic_spectrum_sparse(x, alphas, N, Fs, Nfft)
        Sxx_alpha = Sxx_alpha.tocoo()
        # FFT频率数组（考虑FFT Shift）
        f_shifted = np.fft.fftshift(np.fft.fftfreq(Nfft, d=1 / Fs))

        # 筛选正频率
        positive_freq_indices = f_shifted > 0

        # 筛选出对应正频率的数据点
        mask_positive_freqs = positive_freq_indices[Sxx_alpha.col]  # 根据FFT频率的索引筛选
        data_positive_freqs = Sxx_alpha.data[mask_positive_freqs]
        rows_positive_freqs = Sxx_alpha.row[mask_positive_freqs]
        cols_positive_freqs = Sxx_alpha.col[mask_positive_freqs]

        # 计算幅值并筛选高幅值点
        magnitude = np.log10(np.abs(data_positive_freqs) + 1)
        threshold = np.percentile(magnitude, 99)  # 幅值的99百分位作为阈值
        high_magnitude_indices = magnitude > threshold

        # 获取高幅值点的循环频率、FFT频率和幅值
        alpha_points_high_mag = alphas[rows_positive_freqs[high_magnitude_indices]]
        f_points_high_mag = f_shifted[cols_positive_freqs][high_magnitude_indices]
        magnitude_high_mag = magnitude[high_magnitude_indices]
        return alpha_points_high_mag, f_points_high_mag, magnitude_high_mag


# 24.扭转振动频响图
class tvdx():
    def __init__(self, RawSignal=None, SampleFraquency=None):
        self.RawSignal = RawSignal
        self.SampleFraquency = SampleFraquency

    def tvd(self):
        sig = self.RawSignal
        t_pass, fre_res = cal_fre(sig, 0.1)
        # 计算扭振信号
        ##计算时间差
        deta_t = t_pass[1:] - t_pass[:-1]
        ##计算瞬时扭转角
        w = 2 * np.pi * (fre_res / 100 - fre_res.mean() / 100)
        ##计算随时扭转角度
        theta = deta_t * w
        for i in range(theta.shape[0] - 1):
            theta[i + 1] = theta[i + 1] + theta[i]
        # frf分析
        z = np.exp(theta[1:])
        num = z ** 5 - z ** 4 + z ** 3 - z ** 2
        denom = z ** 5 + 0.54048 * z ** 4 - 0.62519 * z ** 3 - 0.66354 * z ** 2 + 0.60317 * z + 0.69341
        x_final = num / denom

        return x_final


# 计算转频
def cal_fre(sig, pass_value, dt=1 / 400000):
    # 1 计算穿越点位置
    judge = (sig[:-1] <= pass_value) & (sig[1:] >= pass_value)
    _index = np.where(judge == 1)[0]
    # 2 计算穿越点时间
    t_pass = []
    for i in _index:
        # 如果穿越点上数值为pass_value，则穿越位置确认
        if sig[i] == pass_value:
            t_pass.append(i * dt)
        elif sig[i + 1] == pass_value:
            t_pass.append((i + 1) * dt)
        # 如果穿越点上数值均不为pass_value，则穿越位置通过两点直线拟合
        else:
            t_pass.append((i + (-1) * (pass_value - sig[i]) / (sig[i] - sig[i + 1])) * dt)

    # 3 计算时间间隔
    t_pass = np.array(t_pass)
    deta_t = t_pass[1:] - t_pass[:-1]
    # 4 计算转频
    fre_res = 1 / deta_t

    return t_pass, fre_res


# 2.5 Zoom-FFT
class ZoomFFT():

    def __init__(self, low_freq, high_freq, fs, signal=None):
        self.low_freq = low_freq
        self.high_freq = high_freq
        self.fs = fs
        if (low_freq < 0) or (high_freq > fs) or ((high_freq - low_freq) > fs):
            raise Exception("invalid inputs. Program Terminated! ")
        if signal:
            self.signal = signal
            self.length = len(signal)
        else:
            # the default now is a sine signal, for demo purpose
            pass

    def compute_fft(self):
        from numpy.fft import fft, fftshift
        import sys
        try:
            X = fft(self.signal)
            X = np.abs(fftshift(X))  # unscaled
            return X
        except NameError:
            print("signal not defined. Program terminated!")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def plot_fft(self, d=None):
        from numpy.fft import fftfreq
        import sys
        try:
            d = 1 / self.fs if d is None else d
            X = self.compute_fft()
            freq = fftfreq(self.length, d)
            self.original_sample_range = 1 / (self.length * d)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def compute_zoomfft(self, resample_number=None):
        from numpy.fft import fft, fftshift
        from numpy import pi
        from scipy import signal
        import logging
        # try:
        bw_of_interest = self.high_freq - self.low_freq
        if self.length % bw_of_interest != 0:
            logging.warning(
                "length of signal should be divisible by bw_of_interest. Zoom FFT Spectrum may distort!")
            input("Press Enter to continue...")

        fc = (self.low_freq + self.high_freq) / 2
        bw_factor = np.floor(self.fs / bw_of_interest).astype(np.uint8)

        # mix the signal down to DC, and filter it through the FIR decimator
        ind_vect = np.arange(self.length)
        y = self.signal * np.exp(-1j * 2 * pi * ind_vect * fc / self.fs)
        resample_number = bw_of_interest / self.original_sample_range if resample_number is None else resample_number
        resample_range = bw_of_interest / resample_number
        if resample_range != self.original_sample_range:
            logging.warning("resample resolution != original sample resolution. Zoom FFT Spectrum may distort!")
            input("Press Enter to continue...")
        xd = signal.resample(y, np.int(resample_number))
        fftlen = len(xd)
        Xd = fft(xd)
        Xd = np.abs(fftshift(Xd))  # unscaled
        Ld = self.length / bw_factor
        fsd = self.fs / bw_factor
        F = fc + fsd / fftlen * np.arange(fftlen) - fsd / 2
        xxx = F
        yyy = Xd / Ld
        return xxx, yyy


def cyclic_spectrum_sparse(x, alphas, N, Fs, Nfft):
    from scipy.sparse import lil_matrix  # 导入稀疏矩阵库
    # 使用稀疏矩阵
    Sxx_alpha = lil_matrix((len(alphas), Nfft), dtype=np.complex64)
    X = np.fft.fft(x, n=Nfft)
    f = np.fft.fftfreq(Nfft, d=1 / Fs)

    for i, alpha in enumerate(alphas):
        alpha_index = np.round(alpha * Nfft / Fs).astype(int)
        if np.abs(alpha) > Fs / 4:  # 假设只有频率低于Fs/4的部分包含重要信息
            continue
        X_alpha = np.roll(X, alpha_index) * np.conj(X)
        Rxx_alpha = np.fft.ifft(X_alpha, n=Nfft)
        Sxx_alpha[i, :] = np.fft.fftshift(Rxx_alpha)
    return f, alphas, Sxx_alpha.tocsr()
