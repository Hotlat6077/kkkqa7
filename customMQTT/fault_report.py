import numpy as np


class VibrationDiagnosis:
    def __init__(self, sampling_rate):
        """
        初始化振动诊断类

        参数:
        sampling_rate: int/float - 信号采样率(Hz)
        """
        self.sampling_rate = sampling_rate

    def preprocess_signal(self, signal, denoising=True, wavelet='db4', level=3):
        """
        信号预处理：小波降噪和去趋势

        参数:
        signal: array - 输入振动信号
        denoising: bool - 是否应用小波降噪
        wavelet: str - 小波基类型
        level: int - 小波分解层数

        返回:
        processed_signal: array - 预处理后的信号
        """
        # 去趋势（减去均值）
        signal = signal - np.mean(signal)

        # 应用小波降噪
        # if denoising:
        #     signal = self.wavelet_denoising(signal, wavelet=wavelet, level=level)

        return signal

    def compute_spectrum(self, signal, nperseg=1024, window='hann'):
        """
        使用FFT计算信号的幅度谱

        参数:
        signal: array - 输入振动信号(速度信号，单位:mm/s)
        nperseg: int - FFT长度
        window: str - 窗函数类型

        返回:
        freqs: array - 频率数组(Hz)
        amplitude_spectrum: array - 幅度谱值(mm/s)
        """
        import numpy.fft as fft
        fs = self.sampling_rate  # 采样频率
        Sampling_points = len(signal)  # 采样点数，fft后的点数就是这个数
        df = 1 / fs  # 采样间隔时间
        y = signal[:]
        y = list(map(float, y))
        y = np.array(y)
        f_values = np.linspace(0.0, fs / 2.0, Sampling_points // 2)
        fft_values_ = fft.fft(y)
        fft_values = 2.0 / Sampling_points * np.abs(fft_values_[0:Sampling_points // 2])
        return f_values, fft_values

    def find_nearest_frequency_amplitude(self, target_freq, freqs, psd, bandwidth=1.0):
        """
        找到最接近目标频率的幅值

        参数:
        target_freq: float - 目标频率(Hz)
        freqs: array - 频率数组(Hz)
        psd: array - 功率谱密度数组
        bandwidth: float - 搜索带宽(Hz)

        返回:
        amplitude: float - 目标频率附近的峰值幅值(mm/s)
        """
        # 找到目标频率附近的索引
        idx = np.where((freqs >= target_freq - bandwidth) & (freqs <= target_freq + bandwidth))

        if len(idx[0]) == 0:
            return 0

        # 返回该频率范围内的最大幅值
        return np.max(psd[idx])

    def unbalance_eccentric(self, signal, rpm, threshold=5):
        """
        不平衡/偏心故障检测

        参数:
        signal: array - 输入振动信号(速度信号，单位:mm/s)
        rpm: float - 转速(RPM)
        threshold: float - 阈值(默认5.0 mm/s)

        返回:
        fault_level: float - 故障程度百分比(0-100%)
        """
        # 预处理信号
        signal = self.preprocess_signal(signal, denoising=True)

        # 计算频谱
        freqs, psd = self.compute_spectrum(signal)
        freq_1x = rpm / 60  # 转换为Hz
        amplitude = self.find_nearest_frequency_amplitude(freq_1x, freqs, psd)
        # 说是要设定成1倍幅值 是这里要/2??????????????
        return min(100, amplitude / threshold * 100)

    def misalignment(self, signal, rpm, threshold_amp=2.5, threshold_ratio=1.0):
        """
        不对中故障检测

        参数:
        signal: array - 输入振动信号(速度信号，单位:mm/s)
        rpm: float - 转速(RPM)
        threshold_amp: float - 二倍频幅值阈值(默认2.5 mm/s)
        threshold_ratio: float - 2X/1X比值阈值(默认1.0)

        返回:
        fault_level: float - 故障程度百分比(0-100%)
        """
        # 预处理信号
        signal = self.preprocess_signal(signal, denoising=True)

        # 计算频谱
        freqs, psd = self.compute_spectrum(signal)
        freq_1x = rpm / 60
        freq_2x = 2 * freq_1x

        amp_1x = self.find_nearest_frequency_amplitude(freq_1x, freqs, psd)
        amp_2x = self.find_nearest_frequency_amplitude(freq_2x, freqs, psd)

        ratio1 = amp_2x / threshold_amp
        ratio2 = (amp_2x / amp_1x) / threshold_ratio

        fault_level = max(ratio1, ratio2) * 100
        return min(100, fault_level)

    def mechanical_looseness(self, signal, rpm, threshold_ratio=0.5, threshold_total=15):
        """
        机械松动故障检测

        参数:
        signal: array - 输入振动信号(速度信号，单位:mm/s)
        rpm: float - 转速(RPM)
        threshold_ratio: float - 2X/1X比值阈值(默认0.5)
        threshold_total: float - 谐波总值阈值(默认15 mm/s)

        返回:
        fault_level: float - 故障程度百分比(0-100%)
        """
        # 预处理信号
        signal = self.preprocess_signal(signal, denoising=True)

        # 计算频谱
        freqs, psd = self.compute_spectrum(signal)
        freq_1x = rpm / 60
        harmonics = []

        for i in range(1, 6):  # 1x到5x
            freq = i * freq_1x
            amp = self.find_nearest_frequency_amplitude(freq, freqs, psd)
            harmonics.append(amp)

        harmonic_total = sum(harmonics)
        ratio_2x_1x = harmonics[1] / harmonics[0] if harmonics[0] > 0 else 0

        condition1 = ratio_2x_1x / threshold_ratio
        condition2 = harmonic_total / threshold_total

        fault_level = max(condition1, condition2) * 100
        return min(100, fault_level)



