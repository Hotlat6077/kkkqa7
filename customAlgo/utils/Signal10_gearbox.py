# 十、齿轮箱算法放这里

import math
import numpy as np
from scipy.signal import butter, filtfilt

class gearboxx():
    def __init__(self,RawSignal=None,SampleFraquency=None):
        self.RawSignal=RawSignal
        self.SampleFraquency=SampleFraquency

    # 1.时域同步平均
    def tsax(self):
        w = 10
        period = 1 / w
        N = int(period * self.SampleFraquency)
        P = int(np.floor(len(self.RawSignal) / N))
        x_tsa = np.zeros(N)
        if P > 10:
            P = int(10)
        else:
            pass
        for i in range(P):
            x_tsa += self.RawSignal[0 + i * N:N + i * N]
        x_final = x_tsa / P
        return x_final
    # 2.边际谱分析
    def marginalx(self):
        import emd
        data = np.array(self.RawSignal)
        # emd分解
        imf = emd.sift.sift(data)
        # 瞬时相位/幅值/频率
        IP, IF, IA = emd.spectra.frequency_transform(imf, 1024, 'hilbert')
        # HHT 谱
        freq_range = (100, 800, 300)  # 0 to 10Hz in 100 steps
        f, hht = emd.spectra.hilberthuang(IF, IA, freq_range, sum_time=False)
        # 边际谱
        bjp = np.sum(hht,1)
        return f,bjp

    # 3.最小熵反褶积(MED)
    def medx(self,filterSize = None,termIter = None,termDelta = None):
        from scipy.linalg import inv,toeplitz
        from scipy.signal import lfilter
        # from scipy.stats import *
        x = np.array(self.RawSignal)
        filterSize = np.array(filterSize)
        termIter = np.array(termIter)
        termDelta = np.array(termDelta)
        x=np.reshape(x,(len(x),1))
        L = filterSize
        autoCorr = np.zeros((1,L))
        for k in range(0,L):
            x2 = np.zeros((len(x),1))
            x2[k:] = x[0:len(x)-k]
            # 计算自相关
            autoCorr[0,k] = autoCorr[0,k] + sum(np.dot(x[:,0],x2))
        A = toeplitz(autoCorr)
        A_inv = inv(A)
        # 矩阵初始化
        f = np.zeros((L))
        y = np.zeros((len(x),1))
        b = np.zeros((L,1))
        kurtIter = []
        f[1] = 1
        # 循环调整最小熵滤波器系数
        n = 0
        while n == 0 or (n < termIter and ((kurt(y) - kurtIter[n - 1]) > termDelta)):
            # 输出信号
            y = filter_matlab(f,x)
            y = np.asarray(y)

            # 计算峭度值
            kurtIter[n:] = (kurt(y),)
            # 计算矩阵 g = weighted av{ crosscorr( y.^3, x) }
            yc = np.dot(y , 3)
            weightedCrossCorr = np.zeros((L,1))
            for k in range(0,L):
                x2 = np.zeros((len(x),1))
                x2[k:] = x[0:len(x)-k]
                # 计算互相关
                weightedCrossCorr[k,0] = weightedCrossCorr[k,0] + sum(np.dot(y[:,0]**3,x2))

            # weightedCrossCorr = weightedCrossCorr / x.shape[2-1]
            # 新的滤波器系数
            f = np.dot(A_inv,weightedCrossCorr)
            f = f / np.sqrt(sum(f**2))
            n = n + 1
        #更新结果
        f_final = f
        y_final =filter_matlab(f_final,x)
        return y_final, f_final

    # 7.相位的时域平均
    def ptda(self,num_samples =None,num_cycles = None,num_averages =None):

        # num_averages = 10
        davg = np.zeros(num_samples)
        for _ in range(num_averages):
            dft = np.fft.fft(self.RawSignal)
            davg += np.abs(dft)
        davg /= num_averages

        # 估计确定性信号
        estimated_deterministic_signals = []
        for i in range(num_cycles):
            d = davg * np.exp(1j * np.angle(np.fft.fft(self.RawSignal)))  # 使用相位信息
            idft = np.fft.ifft(d)
            estimated_deterministic_signals.append(idft)
        pt_sig=[]
        for i, signal in enumerate(estimated_deterministic_signals):
           pt_sig.append(signal.real)
        flat_pt_sig = [item for sublist in pt_sig for item in sublist]
        return flat_pt_sig
    # 10.广义s变换
    def gst(self,t, freqlow, freqhigh, alpha,  p):
        import numpy as np

        # % t: 时间序列
        # % Sig: 输入信号
        # % freqlow, freqhigh: 频率范围
        # % alpha: 频率分辨率
        # %= == == =输出 == == == %
        # % wcoefs: ST变换计算结果
        TimeLen = len(t)
        dt = t[1] - t[0]
        nLevel = int((freqhigh - freqlow) / alpha) + 1
        fre = np.linspace(freqlow, freqhigh, nLevel)
        wcoefs = np.zeros((nLevel, TimeLen), dtype=complex)
        temp = np.zeros((1, TimeLen), dtype=complex)
        sigma_f = np.power(np.abs(fre) ** p, -1)
        for m in range(0, nLevel):
            f = fre[m]
            for n in range(0, TimeLen):
                Gauss_st = (1 / (math.sqrt(2 * math.pi) * sigma_f[m])) * np.exp(
                    -0.5 * (np.power(n * dt - t, 2) / (sigma_f[m] * sigma_f[m]))) * np.exp(-1.0j * 2 * math.pi * f * t)
                temp[0, n] = np.sum(np.dot(self.RawSignal, Gauss_st)) * dt
            wcoefs[[m], :] = temp
        return wcoefs

    #改进边带能量比
    def compute_improved_sideband_energy_ratio(self,spectrum, freqs, center_freq, sideband_freqs, weights):
        iser = 0
        for i, f in enumerate(sideband_freqs):
            mask = (freqs >= (center_freq - f)) & (freqs <= (center_freq + f))
            iser += weights[i] * np.sum(spectrum[mask] ** 2)
        return iser

    def preprocess_signal(self,signal, fs, lowcut, highcut):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(1, [low, high], btype='band')
        filtered_signal = filtfilt(b, a, signal)
        return filtered_signal
    #21二阶循环平稳分析

    def cyclic_autocorrelation(self,signal, max_lag, alpha):
        n = len(signal)
        R_alpha = np.zeros((2 * max_lag + 1,), dtype=complex)
        for lag in range(-max_lag, max_lag + 1):
            shifted_signal = np.roll(signal, lag)
            product = signal * np.conj(shifted_signal)
            exponential = np.exp(-2j * np.pi * alpha * np.arange(n))
            R_alpha[lag + max_lag] = np.sum(product * exponential)
        return R_alpha / n

    def cyclic_spectrum_density(self,R_alpha):
        from scipy.fftpack import fft
        S_alpha = fft(R_alpha)
        return S_alpha

    #22自适应核时频分布


    def adaptive_kernel_tfd(self,signal, t, f_range):
        from scipy.fft import fftshift, fft
        n = len(signal)
        tfd = np.zeros((len(f_range), n), dtype=complex)

        for ti in range(n):
            # Define an adaptive kernel (for simplicity, we use a Gaussian kernel here)
            sigma_t = np.var(signal[max(0, ti - 10):min(n, ti + 10)])  # Local variance as a simple adaptation
            kernel = np.exp(-0.5 * (t - t[ti]) ** 2 / sigma_t ** 2)

            # Apply the kernel to the signal
            windowed_signal = signal * kernel
            spectrum = fftshift(fft(windowed_signal))

            # Fill the time-frequency distribution
            tfd[:, ti] = np.interp(f_range, np.linspace(-0.5, 0.5, n), np.abs(spectrum))

        return tfd

def filter_matlab(b,x1):
    y = []
    y.append(b[0] * x1[0])

    for i in range(1,len(x1)):
        y.append(0)
        for j in range(len(b)):
            if i  >=  j:
                y[i] = y[i] + b[j] * x1[i - j ]
                j += 1
        i += 1
    return y

def kurt(x):
    x = np.array(x)
    result = np.mean((sum((x - np.ones((len(x),1)) * np.mean(x)) ** 4) / (len(x) - 2)) / (np.std(x) ** 4))
    return result

def generate_signal(t):
    from scipy.signal import chirp
    # Generate a signal: sum of two chirps
    signal = chirp(t, f0=6, t1=1, f1=1, method='linear') + chirp(t, f0=1, t1=1, f1=6, method='quadratic')
    return signal

