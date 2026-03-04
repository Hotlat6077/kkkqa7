import numpy as np
from scipy import signal
import numpy.fft as fft


def fftx(self):
    """
    对原始信号进行FFT频谱分析，并可选地进行带阻滤波（去除指定频率范围）
    
    返回:
        f_values: 频率数组 (0到fs/2)
        fft_values: 对应的幅度谱
    """
    fs = self.SampleFraquency  # 采样频率
    Sampling_points = len(self.RawSignal)  # 采样点数，fft后的点数就是这个数
    df = 1 / fs  # 采样间隔时间
    y = self.RawSignal[:]  #
    y = list(map(float, y))  #
    y = np.array(y)  # 
    
    # 创建原始信号的副本用于滤波处理
    y_filtered = y.copy()
    
    # ========== 新增：带阻滤波器设计 ==========
    # 定义要滤除的频率范围 (20-1000 Hz)
    low_cutoff = 1   # 低频截止频率 10-1000
    high_cutoff = 1000  # 高频截止频率
    
    # 检查频率范围是否有效
    if high_cutoff >= fs/2:
        print(f"警告：截止频率{high_cutoff}Hz超过奈奎斯特频率{fs/2}Hz，将使用{np.floor(fs/2)-1}Hz作为上限")
        high_cutoff = int(np.floor(fs/2)) - 1
    
    # 方法1：使用巴特沃斯带阻滤波器
    # 计算归一化截止频率 (相对于奈奎斯特频率fs/2)
    nyquist_freq = fs / 2
    low_normalized = low_cutoff / nyquist_freq
    high_normalized = high_cutoff / nyquist_freq
    
    # 设计带阻滤波器
    # 参数说明：
    # N=4: 滤波器阶数，阶数越高过渡带越陡 
    # Wn=[low_normalized, high_normalized]: 归一化的截止频率
    # btype='bandstop': 带阻滤波器类型
    filter_order = 4
    b, a = signal.butter(filter_order, [low_normalized, high_normalized], btype='bandstop')
    
    # 应用滤波器
    y_filtered = signal.filtfilt(b, a, y_filtered)
    # 使用filt filt而不是lfilter可以避免相位失真，实现零相位滤波
    
    # ========== 可选：使用方法2 - FFT直接频域滤波 ==========
    # 如果需要更精确的频率控制，可以使用频域滤波方法：
    """
    # 计算FFT
    fft_values_full = fft.fft(y)
    frequencies = fft.fftfreq(len(y), 1/fs)
    
    # 创建频域掩码：保留不在20-1000Hz范围内的频率成分
    mask = ~((np.abs(frequencies) >= low_cutoff) & (np.abs(frequencies) <= high_cutoff))
    
    # 应用掩码（将20-1000Hz范围内的频率分量置零）
    fft_values_filtered = fft_values_full * mask
    
    # 逆FFT回到时域cl
    y_filtered = np.real(fft.ifft(fft_values_filtered))
    """
    
    # ========== 选择使用滤波后的信号进行频谱分析 ==========
    # 可以选择使用原始信号或滤波后的信号
    analysis_signal = y_filtered  # 使用滤波后的信号
    # analysis_signal = y  # 如果要使用原始信号，取消这行注释并注释上一行
    
    # 生成频率轴 (只取正频率部分)
    f_values = np.linspace(0.0, fs / 2.0, Sampling_points // 2)
    
    # 计算FFT
    fft_values_ = fft.fft(analysis_signal)
    
    # 计算单边幅度谱
    # 乘以2是因为能量集中在正频率部分，除以N进行归一化
    fft_values = 2.0 / Sampling_points * np.abs(fft_values_[0:Sampling_points // 2])
    
    # 打印滤波信息
    print(f"已应用带阻滤波器，滤除频率范围: {low_cutoff}-{high_cutoff} Hz")
    print(f"原始信号范围: {np.min(y):.3f} 到 {np.max(y):.3f}")
    print(f"滤波后信号范围: {np.min(y_filtered):.3f} 到 {np.max(y_filtered):.3f}")
    
    return f_values, fft_values
