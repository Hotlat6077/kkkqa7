import numpy as np
from envlop_xiao import env
import os
from scipy import fftpack
from Signal1_index import indexx
# from mq.fs_table import FSTableService
from mydb.get_mongo import get_db
from preprocess  import *
from datetime import datetime 
from 去滑雪坡特征 import ski_slope


#曹学勇修补 加速度峰值
def update_mins_fj_signal_analysis2_cao_fix(data, fs, filetime='20251229180100', methods='raw'):

    signal = []

    # 转速信号提取
    speed = 0
    speed = np.array([float(speed)])/60
    speed = np.round(speed, 5)

    signal=np.array(data)
    signal=(signal-np.mean(signal)).tolist()

    # fs = 20000
    blank_dict={}
    exec(f"blank_dict['out']={methods}(signal,fs)")
    Feaa=blank_dict['out'].tolist()
    # print(Feaa)

    index13_interval=1000
    T = indexx(RawSignal=Feaa, SampleFraquency=fs,Sampleinterval=index13_interval)
    Fea = T.time_domainx( )

    result= {}
    # 原信号数据 ydh ip nu rfaj 2
    result['fea_y'] = Feaa
    length = len(Feaa)
    f_x1=ndarray2list0(np.arange(length)+1)
    f_x=[x / fs for x in f_x1]
    result['fea_x'] = f_x

    if len(Fea) >=1:
        result['rms']=Fea[:,0].tolist()
        result['peak']=Fea[:,1].tolist()
        length=len(Fea[:,0])
    else:
        result['rms'] = []
        result['peak'] = []
        length = 0

    result['fea_xaxis']=ndarray2list0(np.arange(length)+1)


    result['file']=""
    time_add = datetime.strptime(filetime.split('.')[0], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    result['time_add']=time_add
    speed=speed.tolist()
    result['speed']=speed

    #print("result: ", result)

    return result


if __name__ == '__main__':
    from mydb.get_mongo import get_db
    db = get_db()
    collection = db['pump_waveform_report']
    query = {
        # 'sensorId':sesor_id,
        'measureSiteId':int(1077691462944),
        'measureGatherId':int(1077691480608),
        'time':'20260109040100'
    }
    print("query",query)
    document = collection.find_one(query)
    # 提取 fs 字段
    fs = document.get('fs')
    data = document.get('datas')
    res = update_mins_fj_signal_analysis2_cao_fix(data, fs, filetime='20251229180100', methods='raw')
    from draw2plot import plot_waveform_dual
    # plot_waveform_dual(res, 'fea_x', 'fea_y','fea_xaxis', 'peak',top_label= 'Fea',bottom_label='peak')
