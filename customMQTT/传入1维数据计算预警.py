import math
from traceback import print_tb
import numpy as np
from fault_report import VibrationDiagnosis
# test
def alert_report(indicator_dict: dict, thresholds_dict: dict):
    """计算报警告"""

    return alert_report

def index_result(data):
    '''接受一维振动信号，支持传入1D数组或形状为(1,N)/(N,1)的2D数组'''
    arr = np.asarray(data)
    if arr.ndim == 1:
        x = arr.astype(float)
    elif arr.ndim == 2 and 1 in arr.shape:
        x = arr.ravel().astype(float)
    else:
        raise ValueError('data must be 1D or 2D with one row/column')

    n = x.size
    if n == 0:
        raise ValueError('input data is empty')

    mean_ = x.mean()  # 1.均值
    var_ = x.var()  # 2.方差
    std_ = x.std(ddof=0)  # 3.标准差
    max_ = x.max()
    min_ = x.min()
    x_p = max(abs(max_), abs(min_))  # 4.峰值

    x_rms = math.sqrt(np.mean(x ** 2))  # 5.均方根值
    absXbar = x_rms / n  # 6.绝对平均值

    denom_mean = abs(mean_) if abs(mean_) > 1e-12 else 1e-12
    I = x_p / denom_mean  # 7.脉冲指标（取绝对值保护除零）
    L = x_p / x_rms if x_rms != 0 else float('inf')  # 8.裕度指标

    # 9.偏斜度（近似）
    S = x_rms / ((n - 1) * (std_ ** 3)) if std_ != 0 and n > 1 else 0.0

    # 10.峭度
    K = np.sum((x - mean_) ** 4)
    K = K / ((n - 1) * (std_ ** 4)) if std_ != 0 and n > 1 else 0.0

    fea = [mean_, var_ / 10.0, std_, x_p, x_rms, absXbar, I, L, S / 8.0, K / 5.0]
    return fea

from scipy import fftpack


def speed_rms(vibration_signal):
#     vibration_signal (array-like): 振动加速度信号数据，可为1D或2D数组格式
#     result (list): 速度域均方根值列表，从时域特征提取的第5列数据
# 处理步骤:
#     1. 信号预处理：将输入信号转换为二维数组并提取第一列
#     2. 频域变换：对信号进行FFT快速傅里叶变换
#     3. 频率坐标计算：基于1000Hz采样频率计算FFT对应的频率轴
#     4. 域变换：在频域将加速度信号除以(j*2*π*f)转换为速度信号
#     5. 时域恢复：进行逆FFT变换将速度信号转回时域
#     6. 特征提取：调用index_result函数提取时域特征，取均方根值列
# 注意:
#     - 采样频率固定为1000Hz
#     - 频域变换时排除直流分量(f=0处理)
#     - 最终返回的是均方根值特征的列表形式
    """
    将振动信号从加速度域转换到速度域，并提取均方根值特征。
    
    参数:
        vibration_signal: 振动信号数据
    
    返回:
        result: 速度域均方根值列表
    """
    # 将输入信号转换为二维数组并提取第一列
    signal3 = np.vstack(vibration_signal)
    signal3 = signal3[:, 0]
    sig = np.array(signal3)
    
    # 对信号进行FFT变换
    sig_fft = fftpack.fft(sig)
    
    # 计算FFT对应的频率坐标（采样频率1000Hz）
    sig_fre = fftpack.fftfreq(len(sig_fft), d=1 / 1000)
    
    # 加速度转速度：在频域除以(j*2*π*f)
    sig_fft[1:] = sig_fft[1:] / (1j * 2 * np.pi * sig_fre[1:])
    
    # 进行逆FFT变换得到时域速度信号
    sig_vel = fftpack.ifft(sig_fft).real
    sig_vel = np.array(sig_vel)
    
    # 提取时域特征，取第5列（均方根值）
    result = index_result(sig_vel)
    # result = resultn[:, 4].ravel().tolist()
    
    return result


def _evaluate_indicator_level(level_value: float, indicator_name: str,
                                  warning_threshold: float = 30,
                                  fault_threshold: float = 70) -> tuple[int, str]:
        """
        评估指标等级并返回状态和描述

        Args:
            level_value: 指标值（百分比）
            indicator_name: 指标中文名称
            warning_threshold: 预警阈值，默认30
            fault_threshold: 报警阈值，默认70

        Returns:
            (状态码, 描述文本) - 状态码: 0=正常, 1=预警, 2=报警
        """
        if fault_threshold < level_value:
            state = 2  # 报警
            desc = f"{indicator_name}故障报警({level_value})"
        elif warning_threshold < level_value <= fault_threshold:
            state = 1  # 预警
            desc = f"{indicator_name}故障预警({level_value})"
        else:
            state = 0  # 正常
            desc = f"{indicator_name}故障正常({level_value})"
        return state, desc

def judge_vibration_sensor_state(indicator_dict: dict, thresholds_dict: dict):
        """判断振动传感器状态"""
        metrics = ["impulse", "kur", "peak", "rms", "std"]
        metrics_CHN = ["脉冲指标", "峭度", "加速度峰值", "均方根值", "标准差"]
        information_list = ["正常", "预警", "报警", "离线"]

        state_list = [] # 存放各指标状态
        description = [] # 存放各指标描述

        for i, metric_name in enumerate(metrics):
            metric_values = indicator_dict.get(metric_name, [])
            if not isinstance(metric_values, list) or len(metric_values) == 0:
                metric_values = [0.0]
            measured_value = metric_values[0]

            thresholds = thresholds_dict[metric_name]  # 这里从数据库取   键对照的值是一个列表
            print(thresholds)
            if not isinstance(thresholds, list) or len(thresholds) < 2:
                # 如果没有有效阈值，默认为正常状态
                cur_state = 0
            else:
                # warning_threshold = thresholds[0]
                warning_threshold = float(thresholds[0])
                # fault_threshold = thresholds[1]
                fault_threshold = float(thresholds[1])

                # 状态判断逻辑
                if fault_threshold is not None and measured_value >= fault_threshold:
                    cur_state = 2  # 报警
                elif warning_threshold is not None and measured_value >= warning_threshold:
                    cur_state = 1  # 预警
                else:
                    cur_state = 0  # 正常

            state_list.append(cur_state)
            desc_str = f"{metrics_CHN[i]}:{information_list[cur_state]} "
            description.append(desc_str)
        ###############
        ##故障分析
        # 1. 不平衡/偏心故障检测
        unbalance_state, unbalance_desc = _evaluate_indicator_level(
            indicator_dict['unbalance_level'], "不平衡或偏心", warning_threshold=30, fault_threshold=70
        )
        state_list.append(unbalance_state)
        description.append(unbalance_desc)

        # 2. 不对中故障检测
        misalignment_state, misalignment_desc = _evaluate_indicator_level(
            indicator_dict['misalignment_level'], "不对中", warning_threshold=30, fault_threshold=70
        )
        state_list.append(misalignment_state)
        description.append(misalignment_desc)

        # 3. 机械松动故障检测
        looseness_state, looseness_desc = _evaluate_indicator_level(
            indicator_dict['looseness_level'], "机械松动", warning_threshold=30, fault_threshold=70
        )
        state_list.append(looseness_state)
        description.append(looseness_desc)
        # 3个算法
        # 存数据库 定一表 



        overall_state = max(state_list) if state_list else 0
        return overall_state, state_list, description

# vib 就是取的加速度有效值
def calculate_indicators(vib: list, fs: int):
        """计算振动指标"""
        print("threshold_data","success")
        signal_index = index_result(vib)
        dic_index = {}
        dic_index['mean'] = signal_index[0]  # 均值
        dic_index['var'] = signal_index[1]  # 方差
        dic_index['std'] = signal_index[2]  # 标准差
        dic_index['peak'] = signal_index[3]  # 加速度峰值
        dic_index['rms'] = signal_index[4]  # 均方根
        dic_index['avg'] = signal_index[5]  # 绝对平均值
        dic_index['impulse'] = signal_index[6]  # 脉冲
        dic_index['margin'] = signal_index[7]  # 裕度指标
        dic_index['skew'] = signal_index[8]  # 偏斜度
        # dic_index['speed_rms'] = speed_rms(vib)  # 速度有效值
        # dic_index['speed_rms'] = 0  # 速度有效值 这里不需要暂时 暂时设置为0
        dic_index['kur'] = signal_index[9]  # 峭度
        print("threshold_data","success")
        #####加入som,lstm,kmeans
        ###
        # hidden_num, num_layer = get_lstm_param(sensor_id)
        # #########
        # vib2 = vib - np.mean(vib)
        # dic_index['kmeans'] = np.mean(Test_KMeans(sensor_id, vib2).get("hindex")).ravel().tolist()
        # dic_index['Som'] = np.mean(Test_SOM(sensor_id, vib2).get("hindex")).ravel().tolist()
        # dic_index['Lstm'] = np.mean(Test_LSTM(sensor_id, vib2, hidden_num=hidden_num, num_layer=num_layer).get('hindex')).ravel().tolist()
        #########
        ##雪飞算法
        # model_dir = f'{config.work_path}\\health_monitor\\som_model'

        rpm = 1450
        vib_diag = VibrationDiagnosis(fs)
        # 1. 不平衡/偏心故障检测
        unbalance_level = vib_diag.unbalance_eccentric(vib, rpm)
        dic_index['unbalance_level'] = unbalance_level
        print(f"不平衡/偏心故障程度: {unbalance_level:.2f}%")

        # 2. 不对中故障检测
        misalignment_level = vib_diag.misalignment(vib, rpm)
        dic_index['misalignment_level'] = misalignment_level
        print(f"不对中故障程度: {misalignment_level:.2f}%")

        # 3. 机械松动故障检测
        looseness_level = vib_diag.mechanical_looseness(vib, rpm)
        dic_index['looseness_level'] = looseness_level
        print(f"机械松动故障程度: {looseness_level:.2f}%")
        dic_index = {k: round(float(v), 5) for k, v in dic_index.items()}
        ###############
        return dic_index

if __name__ == '__main__':
    from mydb.get_mongo import get_db
    db = get_db()
    collection = db['pump_waveform_report']
    pump_acc_test1 = db['pump_acc_test1']
    # 取阈值表
    pump_algorithm_alert_threshold = db['pump_algorithm_alert_threshold']

    query = {
        # 'sensorId':sesor_id,
         "reportTime":"20260202180139",
         "thingsModel": "wave_1_0_12",
         "serialNum":"3030191700"
    }
    threshold_query = {
        "thingsModel": "wave_1_0_11",
        "serialNum": "3030408000"
    }

    threshold_data = pump_algorithm_alert_threshold.find_one(threshold_query)
    thresholds_dict = threshold_data['indicator_threshold']
    # thresholds = threshold_data['thresholds']
    print(threshold_data)
    data = pump_acc_test1.find_one(query)
    # print(data)
    # thingsModel = data['thingsModel']
    # serialNum = data['serialNum']
    # reportTime = data['reportTime']
    # creat_time = data['creat_time']
    # type = data['type']
    fs =int(data['fs'])
    # # data['datas'] = data['datas'][:100]
    # print(thingsModel, serialNum, reportTime, creat_time, type, fs)
    res = calculate_indicators(data['datas'], fs)
    judge_res = judge_vibration_sensor_state(res, thresholds_dict)
    result = ','.join(judge_res[2])
    print(result)