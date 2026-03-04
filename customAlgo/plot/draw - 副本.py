import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
matplotlib.use('TkAgg')
# matplotlib.use('Agg')  # 使用非交互式后端，适合服务器环境


def plot_waveform(result, axs_x, axs_y, color='red', show_plot=True):
    """
    绘制波段图
    x轴为result['fea_xaxis'] 
    y轴为result['fea_y']
    
    Parameters:
    -----------
    result : dict
        分析结果字典
    show_plot : bool
        是否尝试显示图形（在支持的环境中）
    """
    try:
        # 创建图形
        plt.figure(figsize=(12, 6))
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 获取数据
        x_data = result[f'{axs_x}']
        y_data = result[f'{axs_y}']
        
        # 绘制波形图
        # plt.plot(x_data, y_data, linewidth=1, color='blue', label='Waveform')
        plt.plot(x_data, y_data, linewidth=1, color=f'{color}', label='Waveform')
        
        # 设置图表属性
        plt.xlabel('Time (ms)', fontsize=12)
        plt.ylabel('Amplitude', fontsize=12)
        plt.title('Signal Waveform Analysis', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # 自动调整坐标轴范围
        plt.xlim(min(x_data), max(x_data))
        y_min, y_max = min(y_data), max(y_data)
        y_range = y_max - y_min
        if y_range > 0:  # 避免除零错误
            plt.ylim(y_min - 0.1 * y_range, y_max + 0.1 * y_range)
        
        # 优化布局
        plt.tight_layout()
        
        # 保存图片到文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"waveform_plot_{timestamp}.png"
        # plt.savefig(filename, dpi=300, bbox_inches='tight')
        # print(f"波形图已保存为: {filename}")
        
        # 只在明确指定且环境支持时才显示
        if show_plot:
            try:
                plt.show()
                print(f"显示图形（交互式环境）: {timestamp}")
            except Exception as e:
                print(f"无法显示图形（可能是非交互式环境）: {e}")
        
        # 关闭图形以释放内存
        plt.close()
        
    except Exception as e:
        print(f"绘制波形图时出错: {e}")
        plt.close('all')