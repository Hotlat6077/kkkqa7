import numpy as np
import heapq
from Signal2_frequency import frequencyx
from preprocess import *
from scipy.integrate import cumulative_trapezoid
from Signal1_index import indexx


#曹学勇修补 速度有效值
def update_mins_fj_signal_analysis5_cao_fix(data, fs, filetime, methods='raw'):
    # 转速信号提取
    speed = 0
    speed = np.array([float(speed)])/60
    speed = np.round(speed, 4)
    # -------------------------   以下为之前读数据库的模式，需要被替换掉
    # data1 = list(collection.find({'machine': machine,'group':group,'component':component,'sensor':sensor}, {'vib':1,'speed':1}).sort([('datetime', -1)]).limit(1))[0]  # 改动
    # signal=data1.get('vib')
    signal=np.array(data)
    signal=(signal-np.mean(signal)).tolist()
    # fs = 25600
    blank_dict={}
    exec(f"blank_dict['out']={methods}(signal,fs)")
    Feaa=blank_dict['out'].tolist()

    index13_interval=100

    # sig = np.array(Feaa)
    # sig_fft = fftpack.fft(sig)
    # sig_fre = fftpack.fftfreq(len(sig_fft), d=1 / 1000)
    # sig_fft[1:] = sig_fft[1:] / (1j * 2 * np.pi * sig_fre[1:])
    # sig_vel = fftpack.ifft(sig_fft).real
    # sig_vel = np.array(sig_vel)
    # sig_vel = sig_vel*-100

    time = np.arange(0, len(Feaa)/fs, 1/fs)  # 时间数组，0到10秒
    velocity = cumulative_trapezoid(Feaa, time, initial=0)

    T = indexx(RawSignal=velocity, SampleFraquency=fs,Sampleinterval=index13_interval)
    Fea = T.time_domainx( )

    result= {}
    # 原信号数据
    result['fea_y'] = Feaa
    length = len(Feaa)
    f_x1=ndarray2list0(np.arange(length)+1)
    f_x=[x / fs for x in f_x1]
    f_x=[round(num,2) for num in f_x ]
    result['fea_x'] = f_x
    if len(Fea) >= 1:
        result['rms']=Fea[:,0].tolist()
        length2 = len(Fea[:,0])
    else:
        result['rms'] = []
        length2 = 0

    result['fea_xaxis']=ndarray2list0(np.arange(length2)+1)


    # group_name = group_name[0]['name']
    # machine_name = machine_name[0]['name']
    # component_name = component_name[0]['name']
    # sensor_name = sensor_name[0]['name']
    # result['group_name']=group_name
    # result['machine_name']=machine_name
    # result['component_name']=component_name
    # result['sensor_name']=sensor_name
    result['file']=""
    time_add = datetime.strptime(filetime, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    result['time_add']=time_add
    speed=speed.tolist()
    result['speed']=speed
    print("result in 加速度有效值.py:", result)
    return result


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
    update_mins_fj_signal_analysis5_cao_fix(data, fs, filetime='20251229180100', methods='raw')