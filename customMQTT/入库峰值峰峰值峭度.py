import numpy as np
from 去滑雪坡特征 import ski_slope
from datetime import datetime
from loguru import logger
import sys
import warnings
from 传入1维数据计算预警 import calculate_indicators, judge_vibration_sensor_state

from mydb.get_mongo import get_db
db = get_db()

# 取阈值表
pump_algorithm_alert_threshold = db['pump_algorithm_alert_threshold']




def update_alert_report(data, fs, things_model="wave_1_0_11", serial_num="3030408000"):
    # 先写固定值，后面再修改
    fs = int(fs)
    threshold_query = {
    "thingsModel": things_model,
    "serialNum": serial_num
    }
    threshold_data = pump_algorithm_alert_threshold.find_one(threshold_query)
    if threshold_data == None:
        print("threshold_data is None not db data .")
        return None
    print("threshold_data",threshold_data)
    thresholds_dict = threshold_data['indicator_threshold']
    print("thresholds_dict","success")
    res = calculate_indicators(data, fs)
    
    judge_res =judge_vibration_sensor_state(res, thresholds_dict)
    update_dict = {}

    result = ','.join(judge_res[2])
    update_dict['alert_result'] = result
    update_dict['std'] = res['std']
    update_dict['impulse'] = res['impulse']
    #入库到数据pump_algorithm_alert_test库
    return update_dict


# def update_data(data, fs, data_time, data_id, methods='raw'):
def update_data(data, fs, data_time, data_id, methods='raw'):
    # logger.info.success(f"参数完整算法启用")
    data_id = data_id[5:]
    signal = np.array(data)
    # 不tolist 就是数组信号 
    signal = (signal - np.mean(signal)) # 不处理signal就是加速度
    # 4.加速度有效值 
    acc_rms = float(np.sqrt(np.mean(signal ** 2)))
    acc_rms = round(acc_rms, 5)
    # 计算加速度均值 
    # acc_mean = np.mean(signal)
    signal_mean = np.mean(signal)  # 加速度均值
    signal_std = np.std(signal)    # 5.加速度标准差

    acc_kurtosis = float(np.mean((signal - signal_mean) ** 4) / (signal_std ** 4) if signal_std != 0 else 0)  # 加速度峭度
    acc_kurtosis = round(acc_kurtosis, 5)  # 2.加速度峭度
    # 加速度直接计算最大值 最小值 
    max_acc = float(np.max(signal))  # 加速度最大值 
    min_acc = float(np.min(signal))  # 加速度最小值 
    peak_acc = float(max(abs(max_acc), abs(min_acc)))  # 3.加速度峰值 
    peak_acc = round(peak_acc, 5)
    # 加速度脉冲 1.
    # acc_I = peak_acc / abs(signal_mean[0])  # 7.脉冲指标  -- 20250319 修改，取绝对值
    # 加速度峰峰值 
    peak2peak = float(max_acc - min_acc)  
    peak2peak = round(peak2peak, 5) # 加速度峰峰值
    print("peak_acc: ", peak_acc, "peak2peak: ", peak2peak, "加速度峭度: ", acc_kurtosis)

    # 梯形积分 加速度积分到速度 如果不对就用上面的
    # 确保 fs 是数值类型
    fs = float(fs) if not isinstance(fs, (int, float)) else fs
    dt = 1.0 / fs
    velocity = np.cumsum(signal) * dt
    # velocity 转就是速度波开要入库
    
    # 加速度积分后为速度 要去滑雪坡特征
    velocity_ski = ski_slope(velocity, fs)  # velocity_ski 是一个数组
    #
    # velocity_ski_f = velocity_ski.copy().tolist()
    velocity_ski_f = velocity_ski.copy()
    # 去滑雪坡特征后计算速度有效值
    velocity_rms = float(np.sqrt(np.mean(velocity_ski ** 2)))
    velocity_rms = round(velocity_rms, 5)
    # 去滑雪坡特征后入库
    # 计算速度均值（基于去滑雪坡特征后的速度）
    velocity_std = np.std(velocity_ski)
    velocity_mean = np.mean(velocity_ski)
    # 计算速度峭度（基于去滑雪坡特征后的速度）
    velocity_kurtosis = float(np.mean((velocity_ski - velocity_mean)**4) / (velocity_std**4) if velocity_std != 0 else 0)
    velocity_kurtosis = round(velocity_kurtosis, 5)
    # 速度峰峰值（基于去滑雪坡特征后的速度）
    max_v = float(np.max(velocity_ski))
    min_v = float(np.min(velocity_ski))
    peak_vel = float(max(abs(max_v), abs(min_v)) * 1000)  # 转为 mm/s
    peak_vel = round(peak_vel, 5)
    peak2peak_v = float((max_v - min_v) * 1000)  # 转为 mm/s
    peak2peak_v = round(peak2peak_v, 5)
    # print("velocity peak_acc:", peak_vel, "peak2peak_v:", peak2peak_v,"峭度:", velocity_kurtosis)

    result_dict = {
        "acc_rms":acc_rms,
        "velocity_rms":velocity_rms,
        "peak_acc":peak_acc,
        "peak_vel":peak_vel,
        "peak2peak":peak2peak,
        "peak2peak_v":peak2peak_v,
        "acc_kurtosis":acc_kurtosis,
        "velocity_kurtosis":velocity_kurtosis,
        "velocity_ski_f":velocity_ski_f
    }
    return result_dict


if __name__ == '__main__':
    from mydb.get_mongo import get_db
    db = get_db()
    db = get_db()
    # collection = db['pump_waveform_report']
    collection = db['pump_acc_test1']
    # 通过sensorId取信号原始数据
    query = {
        # 'sensorId':sesor_id,
         "reportTime":"20260202180139",
         "thingsModel": "wave_1_0_12",
         "serialNum":"3030191700"
    }
    print("query",query)
    document = collection.find_one(query)
    data = document.get('datas')
    fs = document.get('fs')
    data_time = document.get('reportTime')
    thingsModel = document.get('thingsModel')
    serialNum = document.get('serialNum')
    # 发送数据要用到
    sensor_id = document.get('sensorId')
    print("data_time:",data_time)
    print("fs:",fs)
    print("data:",data)
    print("thingsModel:",thingsModel)
    print("serialNum:",serialNum)
    print("sensor_id:",sensor_id)
    update_data(data, fs,data_time, sensor_id, methods='raw')
    # print("query",query)
    # document = collection.find_one(query)
    # # 提取 fs 字段
    # fs = document.get('fs')
    # data = document.get('datas')
    # res = update_data(data, fs, methods='raw')

