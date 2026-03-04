import numpy as np
import heapq
from Signal2_frequency import frequencyx
from preprocess import *
from scipy.integrate import cumulative_trapezoid
from Signal1_index import indexx
from mydb.get_mongo import get_db
from scipy.signal import butter, filtfilt
from 去滑雪坡特征 import ski_slope


# 速度有效值修补
def update_mins_fj_signal_analysis5_cao_fix(data, fs, methods='raw'):
    # 转速信号提取
    speed = 0
    speed = np.array([float(speed)])/60
    speed = np.round(speed, 5)
    # -------------------------   以下为之前读数据库的模式，需要被替换掉
    signal=np.array(data)
    signal=(signal-np.mean(signal)).tolist()
    # fs = 25600
    blank_dict={}
    exec(f"blank_dict['out']={methods}(signal,fs)")
    Feaa=blank_dict['out'].tolist()
    print("进入了速度有效值")
    # index13_interval=100
    ##################速度有效值计算
    acc = Feaa  # 原始振动信号
    fs = fs
    dt = 1.0 / float(fs)
    # 转为 numpy 数组
    a = np.asarray(acc, dtype=float)
    # 2. 0–1000 Hz滤波
    lowcut = 10.0
    highcut = 1000.0
    order = 4
    # wn = highcut / (fs / 2)
    nyquist = fs / 2.0  # 奈奎斯特频率
    low = lowcut / nyquist
    high = highcut / nyquist
    # b, c = butter(order, wn, btype='low')
    b, c = butter(order, [low, high], btype='band')
    a_filt = filtfilt(b, c, a)
    # 3. 时域积分得到速度信号
    a_filt = a_filt - np.mean(a_filt)
    # 梯形积分
    v = np.cumsum(a_filt) * dt
    # 4. 速度均方根值（RMS）
    v_rms = np.sqrt(np.mean(v ** 2))
    # ===== 输出 =====
    Fea = v_rms * 1000

    result = {}
    # 原信号数据
    result['fea_y'] = Feaa
    result['fea_y'] = [float(x) * 9.8 for x in Feaa]
    length = len(Feaa)
    f_x1 = ndarray2list0(np.arange(length) + 1)
    f_x = [x / fs for x in f_x1]
    f_x = [round(num, 5) for num in f_x]
    result['fea_x'] = f_x
    # #################速度有效值修改
    Fea = [Fea]
    result['rms'] = Fea
    length2 = len(Fea)
    result['fea_xaxis'] = ndarray2list0(np.arange(length2) + 1)

    return result
