import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import matplotlib.gridspec as gridspec

# 设置中文字体（可选）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

def generate_sample_data(duration=2, sampling_rate=1000):
    """生成示例波形数据"""
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    
    # 生成原始信号：正弦波 + 噪声 + 高频成分
    freq1, freq2 = 5, 50  # Hz
    original_signal = (np.sin(2 * np.pi * freq1 * t) + 
                       0.5 * np.sin(2 * np.pi * freq2 * t))
    
    # 添加随机噪声
    noise = 0.3 * np.random.normal(size=len(t))
    raw_data = original_signal + noise
    
    return t, raw_data, original_signal

def process_data(raw_data, sampling_rate=1000):
    """数据处理示例：滤波和去噪"""
    # 设计低通滤波器去除高频噪声
    nyquist = sampling_rate / 2
    cutoff_freq = 30  # Hz
    normal_cutoff = cutoff_freq / nyquist
    
    # 巴特沃斯低通滤波器
    b, a = signal.butter(4, normal_cutoff, btype='low', analog=False)
    processed_data = signal.filtfilt(b, a, raw_data)
    
    # 进一步平滑处理（可选）
    window_size = 51
    if len(processed_data) > window_size:
        processed_data = np.convolve(processed_data, 
                                   np.ones(window_size)/window_size, 
                                   mode='same')
    
    return processed_data

def plot_waveforms(x1, y1, x2, y2=0):
    """绘制波形图"""
    fig = plt.figure(figsize=(12, 8))
    
    # 方法1：使用subplot2grid创建上下布局
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])
    
    # 上图：原始数据（散点图+线图）
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.scatter(x1[::10], y1[::10], s=8, alpha=0.6, color='blue', label='原始数据点', zorder=1)  # 蓝色的点
    ax1.plot(x1, y1, linewidth=1, color='red', alpha=0.7, label='原始数据线', zorder=2)  # 红色的线
    ax1.set_title('原始数据波形', fontsize=14, fontweight='bold')  # 标题
    ax1.set_ylabel('幅值', fontsize=12)  # y坐标
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 下图：处理后的数据（仅线图）
    # ax2 = fig.add_subplot(gs[1, 0])
    # ax2.plot(x1, x2, linewidth=2, color='green', label='处理后数据')
    # ax2.set_title('处理后数据波形', fontsize=14, fontweight='bold')
    # ax2.set_xlabel('时间 (s)', fontsize=12)
    # ax2.set_ylabel('幅值', fontsize=12)
    # ax2.legend()
    # ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def plot_waveforms_alternative(t, raw_data, processed_data):
    """另一种布局方式：更紧凑的版本 drvc voen xg es su hko """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
    
    # 上图配置 
    ax1.plot(t, raw_data, 'b-', linewidth=1, alpha=0.8, label='原始数据线')
    ax1.scatter(t[::20], raw_data[::20], c='red', s=15, alpha=0.7, label='采样点', zorder=5)
    ax1.set_title('原始数据 - 线图与散点组合显示')
    ax1.set_ylabel('Amplitude')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    # 下图配置
    ax2.plot(t, processed_data, 'g-', linewidth=1.5, label='Filtered Signal')
    ax2.set_title('Processed Data - Line Plot Only')
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Amplitude')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.show()

# 主程序 khqdnghivqrqk 
if __name__ == "__main__":
    # 生成数据
    print("生成示例数据...")
    t, raw_data, clean_signal = generate_sample_data(duration=3, sampling_rate=1000)
    
    # 处理数据
    print("处理数据...")
    processed_data = process_data(raw_data, sampling_rate=1000)
    
    # 显示数据统计信息 
    print(f"数据点数: {len(t)}")
    print(f"原始数据范围: [{raw_data.min():.3f}, {raw_data.max():.3f}]")
    print(f"处理后数据范围: [{processed_data.min():.3f}, {processed_data.max():.3f}]")
    
    # 绘制图形
    print("绘制波形图...")
    plot_waveforms(t, raw_data, processed_data)
    
    # 也可以尝试另一种布局
    # plot_waveforms_alternative(t, raw_data, processed_data)
