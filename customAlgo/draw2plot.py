import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
import numpy as np 

matplotlib.use('TkAgg')
# matplotlib.use('Agg')  # 使用非交互式后端，适合服务器环境


def plot_waveform_dual(result, axs_x_top, axs_y_top, axs_x_bottom, axs_y_bottom,top_label='', bottom_label='',
                      color_top='g', color_bottom='r', show_plot=True):
    """
    绘制双子图波形图（上下两个图同时展示）
    top图：x轴为result[axs_x_top], y轴为result[axs_y_top]
    bottom图：x轴为result[axs_x_bottom], y轴为result[axs_y_bottom]
    
    Parameters:
    -----------
    result : dict
        分析结果字典
    axs_x_top : str
        上图x轴数据键名
    axs_y_top : str  
        上图y轴数据键名
    axs_x_bottom : str
        下图x轴数据键名
    axs_y_bottom : str
        下图y轴数据键名
    color_top : str
        上图线条颜色
    color_bottom : str
        下图线条颜色
    show_plot : bool
        是否尝试显示图形（在支持的环境中）
    """
    try:
        # 创建图形和子图（1行2列布局）
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial']
        plt.rcParams['axes.unicode_minus'] = False
        
        # ========== 绘制上图 ==========
        x_data_top = result[f'{axs_x_top}']
        y_data_top = result[f'{axs_y_top}']
        
        ax1.plot(x_data_top, y_data_top, linewidth=1, color=f'{color_top}', label=f'{top_label}')
        ax1.set_xlabel('Time (ms)', fontsize=7)
        ax1.set_ylabel(f'{top_label}', fontsize=12)
        ax1.set_title(f'{top_label} Analysis', fontsize=12, fontweight=f'bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # 自动调整上图坐标轴范围
        ax1.set_xlim(min(x_data_top), max(x_data_top))
        y_min_top, y_max_top = min(y_data_top), max(y_data_top)
        y_range_top = y_max_top - y_min_top
        if y_range_top > 0:
            ax1.set_ylim(y_min_top - 0.1 * y_range_top, y_max_top + 0.1 * y_range_top)
        
        # ========== 绘制下图 ==========
        x_data_bottom = result[f'{axs_x_bottom}']
        y_data_bottom = result[f'{axs_y_bottom}']
        
        ax2.plot(x_data_bottom, y_data_bottom, linewidth=1, color=f'{color_bottom}', label=f'{bottom_label}')
        ax2.set_xlabel('Time (ms)', fontsize=7)
        ax2.set_ylabel(f'{bottom_label}', fontsize=12)
        ax2.set_title(f'{bottom_label} Analysis', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # 自动调整下图坐标轴范围
        ax2.set_xlim(min(x_data_bottom), max(x_data_bottom))
        y_min_bottom, y_max_bottom = min(y_data_bottom), max(y_data_bottom)
        y_range_bottom = y_max_bottom - y_min_bottom
        if y_range_bottom > 0:
            ax2.set_ylim(y_min_bottom - 0.1 * y_range_bottom, y_max_bottom + 0.1 * y_range_bottom)
        
        # 整体标题
        # fig.suptitle('Dual Signal Analysis', fontsize=12, fontweight='bold')
        
        # 优化布局
        plt.tight_layout()
        
        # 调整子图间距
        plt.subplots_adjust(top=0.93, hspace=0.3)
        
        # 保存图片到文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"dual_waveform_plot_{timestamp}.png"
        # plt.savefig(filename, dpi=300, bbox_inches='tight')
        # print(f"双波形图已保存为: {filename}")
        
        # 只在明确指定且环境支持时才显示
        if show_plot:
            try:
                plt.show()
                print(f"显示双图形（交互式环境）: {timestamp}")
            except Exception as e:
                print(f"无法显示图形（可能是非交互式环境）: {e}")
        
        # 关闭图形以释放内存
        plt.close()
        
    except Exception as e:
        print(f"绘制双波形图时出错: {e}")
        plt.close('all')


# 如果你想要垂直排列的两个独立图（而不是子图），可以使用这个函数：
def plot_two_separate_waveforms(result, axs_x1, axs_y1, axs_x2, axs_y2, 
                               color1='red', color2='blue', show_plot=True,top_label='', botton_label=''):
    """
    绘制两个独立的垂直排列的波形图（上下排列但独立图形）
    """
    try:
        # 创建图形和子图（2行1列，共享x轴可选）
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=False)
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial']
        plt.rcParams['axes.unicode_minus'] = False
        
        # ========== 第一个图 ==========
        x_data1 = result[f'{axs_x1}']
        y_data1 = result[f'{axs_y1}']
        
        ax1.plot(x_data1, y_data1, linewidth=1, color=f'{color1}', label=f'{top_label}')
        ax1.set_ylabel('Amplitude', fontsize=12)
        ax1.set_title('Signal {top_label}', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # 自动调整坐标轴范围
        ax1.set_xlim(min(x_data1), max(x_data1))
        y_min1, y_max1 = min(y_data1), max(y_data1)
        y_range1 = y_max1 - y_min1
        if y_range1 > 0:
            ax1.set_ylim(y_min1 - 0.1 * y_range1, y_max1 + 0.1 * y_range1)
        
        # ========== 第二个图 ==========
        x_data2 = result[f'{axs_x2}']
        y_data2 = result[f'{axs_y2}']
        
        ax2.plot(x_data2, y_data2, linewidth=1, color=f'{color2}', label=f'{botton_label}')
        ax2.set_xlabel('Time (ms)', fontsize=12)
        ax2.set_ylabel('Amplitude', fontsize=12)
        ax2.set_title(f'Signal {botton_label}', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # 自动调整坐标轴范围
        ax2.set_xlim(min(x_data2), max(x_data2))
        y_min2, y_max2 = min(y_data2), max(y_data2)
        y_range2 = y_max2 - y_min2
        if y_range2 > 0:
            ax2.set_ylim(y_min2 - 0.1 * y_range2, y_max2 + 0.1 * y_range2)
        
        # 整体标题
        fig.suptitle('Two Separate Signal Waveforms', fontsize=7, fontweight='bold')
        
        # 优化布局
        plt.tight_layout()
        plt.subplots_adjust(top=0.93, hspace=0.3)
        
        # 保存图片
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"two_separate_waveforms_{timestamp}.png"
        # plt.savefig(filename, dpi=300, bbox_inches='tight')
        # print(f"两个独立波形图已保存为: {filename}")
        
        # 显示图形
        if show_plot:
            try:
                plt.show()
                print(f"显示两个独立图形（交互式环境）: {timestamp}")
            except Exception as e:
                print(f"无法显示图形（可能是非交互式环境）: {e}")
        
        plt.close()
        
    except Exception as e:
        print(f"绘制两个独立波形图时出错: {e}")
        plt.close('all')


# 使用示例：
if __name__ == "__main__":
    # 示例数据
    sample_result = {
        'time_ms': list(range(100)),
        'amplitude1': [np.sin(x/10) + np.random.normal(0, 0.1) for x in range(100)],
        'amplitude2': [np.cos(x/10) + np.random.normal(0, 0.1) for x in range(100)],
        'frequency': list(range(100)),
        'phase': [np.sin(x/5) for x in range(100)]
    }
    
    # 使用修改后的函数
    plot_waveform_dual(
        sample_result, 
        'time_ms', 'amplitude1',  # 上图数据
        'time_ms', 'amplitude2',  # 下图数据
        color_top='red', 
        color_bottom='blue'
    )
