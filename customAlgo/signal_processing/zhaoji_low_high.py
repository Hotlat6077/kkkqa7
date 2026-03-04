
import numpy as np
from signal_processing.filter import filter


def update_mins_zhaji_home(data):
    # #函数名字需要修改
    # client = get_client()
    # db=client.Br_zj
    # collection=db['vibration_data']
    # data=list(collection.find({'machine':machine},{sensor:1}).sort([('dt', -1)]).limit(1))[0]
    # signal=data.get(sensor)

    #原始信号参数如下
    fs = 12800 #采样频率
    n = 64000 # 点数

    # 设置滤波器参数
    order = 10
    lowcut =2100 #低频
    highcut=4200  #高频

    # 低通滤波后的低频时域信号
    y1 = filter().butter_lowpass_filter(data, lowcut, fs, order)

    # 带通滤波后的中频时域信号
    y2 = filter().butter_bandpass_filter(data, lowcut, highcut, fs, order)

    # 高通滤波后的高频时域信号
    y3 = filter().butter_highpass_filter(data, highcut, fs, order)
    return y1,y2,y3






