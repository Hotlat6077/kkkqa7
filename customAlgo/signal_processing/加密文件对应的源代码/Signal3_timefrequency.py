# 三、时频分析的算法放这里
import numpy as np


class timefrequencyx():
    def __init__(self,RawSignal=None,SampleFraquency=None,totalscal=None):
        self.RawSignal=RawSignal
        self.SampleFraquency=SampleFraquency
        self.totalscal=totalscal

    # 1.短时傅里叶变换
    def stftx(self):
        from scipy import signal
        f, t, Zxx = signal.stft(self.RawSignal.flatten(), self.SampleFraquency, nperseg=600)
        z = np.abs(Zxx)
        return f, t, z

    # 2.Wigner-Ville时频分布
    def wignervx(self):
        import tftb
        dt = 1 / self.SampleFraquency
        ts = np.arange(len(self.RawSignal)) * (1 / self.SampleFraquency)
        # print(len(self.RawSignal))
        wvd = tftb.processing.WignerVilleDistribution(self.RawSignal, timestamps=ts)
        tfr_wvd, t_wvd, f_wvd = wvd.run()
        f_wvd = np.fft.fftshift(np.fft.fftfreq(tfr_wvd.shape[0], d=2 * (1 / self.SampleFraquency)))
        df_wvd = f_wvd[1] - f_wvd[0]
        wv2 = np.fft.fftshift(tfr_wvd)
        zz = np.abs(wv2)
        xx = np.arange(ts[0] - dt / 2, ts[-1] + dt / 2, dt)
        yy = np.arange(f_wvd[0], f_wvd[-1], df_wvd)
        return xx, yy, zz

    # 3.小波时频分析
    def cwt(self):
        import pywt
        #  参数totalscal为尺寸序列的长度，提高其值，频率分辨率更高
        wfc = pywt.central_frequency(wavelet='cgau8')  # 计算小波函数的信号中心频率。
        a = 2 * wfc * self.totalscal / (np.arange(self.totalscal, 1, -1))
        period = 1.0 / self.SampleFraquency  # 周期
        [cwtmar, fre] = pywt.cwt(self.RawSignal, a, 'cgau8', period)
        # x：输入信号；
        # a：尺度因子（要使用的小波尺度），低频(大尺度因子)对应着信号的全局信息(贯穿整个信号)，而高频(小尺度因子)对应着信号中的细节(通常持续很短时间)；
        # wavelet：Wavelet 对象或名字；period：频率输出的采样周期
        amp = abs(cwtmar)
        return fre, amp # amp:幅值；fre:频率

    # 4.三维瀑布图
    def fftxx(self):
        import numpy.fft as fft
        fs = self.SampleFraquency  # 采样频率
        Sampling_points = len(self.RawSignal)  # 采样点数，fft后的点数就是这个数
        df = 1 / fs  # 采样间隔时间
        y = self.RawSignal[:]
        y = list(map(float, y))
        y = np.array(y)
        f_values = np.linspace(0.0, fs/2.0, Sampling_points//2)
        fft_values_ = fft.fft(y)
        fft_values = 2.0/Sampling_points * np.abs(fft_values_[0:Sampling_points//2])
        return ['{:.1f}'.format(i) for i in f_values], fft_values

    # 5. 双谱分析
    def bispectrumx(self, norm, *ofreqs):
        import numpy as np
        from scipy.fftpack import next_fast_len
        from scipy.signal import spectrogram
        flim1 = None
        flim2 = None
        synthetic = ()
        N = len(self.RawSignal)
        kwargs = dict(nperseg=N // 10, noverlap=N // 20, nfft=next_fast_len(N // 2))
        kwargs.setdefault('nfft', next_fast_len(N // 10))

        norm1, norm2 = get_norm(norm)
        freq, t, spec = spectrogram(self.RawSignal, fs=self.SampleFraquency, mode='complex', **kwargs)
        spec = np.require(spec, 'complex64')
        spec = np.transpose(spec, [1, 0])  # transpose (f, t) -> (t, f)
        if flim1 is None:
            flim1 = (0, (np.max(freq) - np.sum(ofreqs)) / 2)
        if flim2 is None:
            flim2 = (0, (np.max(freq) - np.sum(ofreqs)) / 2)
        ind1 = np.arange(*np.searchsorted(freq, flim1))
        ind2 = np.arange(*np.searchsorted(freq, flim2))
        ind3 = freq_ind(freq, ofreqs)
        otemp = product_other_freqs(spec, ind3, synthetic, t)[:, None, None]
        sumind = ind1[:, None] + ind2[None, :] + sum(ind3)
        temp = spec[:, ind1, None] * spec[:, None, ind2] * otemp
        if norm is not None:
            temp2 = np.mean(np.abs(temp) ** norm1, axis=0)
        temp *= np.conjugate(spec[:, sumind])
        coh = np.mean(temp, axis=0)
        del temp
        if norm is not None:
            coh = np.abs(coh, out=coh)
            coh **= 2
            temp2 *= np.mean(np.abs(spec[:, sumind]) ** norm2, axis=0)
            coh /= temp2
            coh **= 0.5

        df1 = freq[ind1][1] - freq[ind1][0]
        df2 = freq[ind2][1] - freq[ind2][0]
        freq1 = np.append(freq[ind1], freq[ind1][-1] + df1) - 0.5 * df1
        freq2 = np.append(freq[ind2], freq[ind2][-1] + df2) - 0.5 * df2
        return freq1, freq2, np.abs(coh)

    # 6. 双相干谱分析
    def bicoherencex(self, norm=2, *ofreqs):
        import numpy as np
        from scipy.fftpack import next_fast_len
        from scipy.signal import spectrogram
        flim1 = None
        flim2 = None
        synthetic = ()
        N = len(self.RawSignal)
        kwargs = dict(nperseg=N // 10, noverlap=N // 20, nfft=next_fast_len(N // 2))
        kwargs.setdefault('nfft', next_fast_len(N // 10))

        norm1, norm2 = get_norm(norm)
        freq, t, spec = spectrogram(self.RawSignal, fs=self.SampleFraquency, mode='complex', **kwargs)
        spec = np.require(spec, 'complex64')
        spec = np.transpose(spec, [1, 0])  # transpose (f, t) -> (t, f)
        if flim1 is None:
            flim1 = (0, (np.max(freq) - np.sum(ofreqs)) / 2)
        if flim2 is None:
            flim2 = (0, (np.max(freq) - np.sum(ofreqs)) / 2)
        ind1 = np.arange(*np.searchsorted(freq, flim1))
        ind2 = np.arange(*np.searchsorted(freq, flim2))
        ind3 = freq_ind(freq, ofreqs)
        otemp = product_other_freqs(spec, ind3, synthetic, t)[:, None, None]
        sumind = ind1[:, None] + ind2[None, :] + sum(ind3)
        temp = spec[:, ind1, None] * spec[:, None, ind2] * otemp
        if norm is not None:
            temp2 = np.mean(np.abs(temp) ** norm1, axis=0)
        temp *= np.conjugate(spec[:, sumind])
        coh = np.mean(temp, axis=0)
        del temp
        if norm is not None:
            coh = np.abs(coh, out=coh)
            coh **= 2
            temp2 *= np.mean(np.abs(spec[:, sumind]) ** norm2, axis=0)
            coh /= temp2
            coh **= 0.5

        df1 = freq[ind1][1] - freq[ind1][0]
        df2 = freq[ind2][1] - freq[ind2][0]
        freq1 = np.append(freq[ind1], freq[ind1][-1] + df1) - 0.5 * df1
        freq2 = np.append(freq[ind2], freq[ind2][-1] + df2) - 0.5 * df2
        return freq1, freq2, np.abs(coh)

    def Bispectral_Slicing(self):
        import numpy as np
        from scipy.fftpack import fft
        signal=self.RawSignal
        fs=self.SampleFraquency
        lag_max=int(len(self.RawSignal)/8)
        N = len(signal)
        R1D = np.zeros(lag_max)
        for r in range(lag_max):
            sum_val = 0.0
            for n in range(N - r):
                sum_val += signal[n] * signal[n + r] * signal[n + r]
            R1D[r] = sum_val / (N - r)
        B1D_full = fft(R1D)
        # 选择FFT结果的一半，排除直流分量
        half_n = len(B1D_full) // 2
        # FFT结果的前半部分是正频率，第一个元素是直流分量
        B1D_positive = B1D_full[1:half_n]
        # 计算频率轴（仅正频率）
        freqs = np.linspace(0, fs / 2, len(B1D_positive))
        freqs=np.round(freqs,2)
        return freqs, np.abs(B1D_positive)






def get_norm(norm):
    if norm == 0 or norm is None:
        return None, None
    else:
        try:
            norm1, norm2 = norm
        except TypeError:
            norm1 = norm2 = norm
        return norm1, norm2

def freq_ind(freq, f0):
    try:
        return [np.argmin(np.abs(freq - f)) for f in f0]
    except TypeError:
        return np.argmin(np.abs(freq - f0))

def product_other_freqs(spec, indices, synthetic=(), t=None):
    p1 = np.prod([amplitude * np.exp(2j * np.pi * freq * t + phase)
                  for (freq, amplitude, phase) in synthetic], axis=0)
    p2 = np.prod(spec[:, indices[len(synthetic):]], axis=1)
    return p1 * p2


