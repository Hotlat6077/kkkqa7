import numpy as np
import heapq
from Signal2_frequency import frequencyx
from preprocess import *
from scipy.integrate import cumulative_trapezoid
from Signal1_index import indexx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
# matplotlib.use('Agg')  # 使用非交互式后端，适合服务器环境


# 曹学用修补 倒谱图
def update_mins_fj_signal_analysis7_cao_fix(data, fs, filetime, methods='raw'):
    signal = []
    signal = np.array(data)
    signal = (signal - np.mean(signal)).tolist()
    blank_dict = {}
    exec(f"blank_dict['out']={methods}(signal,fs)")
    Feaa = blank_dict['out'].tolist()

    T = frequencyx(RawSignal=Feaa, SampleFraquency=fs)
    Fea1y = T.cepstrumx()

    result = {}
    # 原信号数据
    result['fea_y'] = Feaa
    length = len(Feaa)
    f_x1 = ndarray2list0(np.arange(length) + 1)
    f_x = [x / fs for x in f_x1]
    f_x = [round(num, 2) for num in f_x]
    result['fea_x'] = f_x

    result['cyy'] = Fea1y.tolist()
    length2 = len(Fea1y)
    # result['fea_xaxis'] = ndarray2list0(np.arange(length2)+1)
    f_x2 = ndarray2list0(np.arange(length2) + 1)
    f_x2 = [x * 1000 / (fs / 4) for x in f_x2]
    result['fea_xaxis'] = f_x2


    # group_name = group_name[0]['name']
    # machine_name = machine_name[0]['name']
    # component_name = component_name[0]['name']
    # sensor_name = sensor_name[0]['name']
    # result['group_name'] = group_name
    # result['machine_name'] = machine_name
    # result['component_name'] = component_name
    # result['sensor_name'] = sensor_name
    result['file'] = ""  # file
    # time_add=localfilename[2:14]
    time_add = datetime.strptime(filetime, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    result['time_add'] = time_add
    # speed=speed.tolist()
    speed = 0
    result['speed'] = speed
    print("result in 倒谱.py:", result)
    return result

def plot_waveform(result, axs_x, axs_y, show_plot=True):
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
        # x_data = result['fea_xaxis']
        x_data = result[f'{axs_x}']
        # y_data = result['fea_y']
        y_data = result[f'{axs_y}']
        
        # 绘制波形图
        # plt.plot(x_data, y_data, linewidth=1, color='blue', label='Waveform')
        plt.plot(x_data, y_data, linewidth=1, color='red', label='Waveform')
        
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

if __name__ == '__main__':
    from mydb.get_mongo import get_db
    db = get_db()
    collection = db['pump_waveform_report']
    query = {
    'sensorId': 'SE_1_1_2_3',
    'time': '20251229180100'
    }
    document = collection.find_one(query)
    # 提取 fs 字段
    fs = document.get('fs')
    data = document.get('datas')
    res = update_mins_fj_signal_analysis7_cao_fix(data, fs, filetime='20251229180100', methods='raw')
    # x轴为result['fea_xaxis'] 
    # y轴为result['fea_y']
    plot_waveform(res,'fea_xaxis','fea_y')