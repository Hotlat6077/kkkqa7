import numpy as np
import numpy.fft as fft
from scipy.fftpack import hilbert, fft, ifft
from sig_frequency import frequencyx
from scipy.integrate import cumulative_trapezoid
from sig_frequency2 import indexx
from preprocess_data import raw, tintegral, cderiv, routliers

def ndarray2list0(data):
    list0 = []
    for temp in data:
        list0.append(temp.tolist())
    return list0


def ndarray2list1(data):
    list0 = []
    for temp in data:
        list0.append(temp.tolist())
    list1 = []
    for i in list0:
        for j in i:
            list1.append(j)
    return list1

# def update_mins_fj_signal_analysis5_cao_fix(data, fs, methods='raw'):
def velocity(data, fs, methods='raw'):
    signal = []
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
    print('velocity :', velocity)
    print('fs :', fs)
    print('index13_interval :', index13_interval)
    T = indexx(RawSignal=velocity, SampleFraquency=fs,Sampleinterval=index13_interval)
    Fea = T.time_domainx( )
    print('Fea :', Fea)
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

    print('fea_xaxis :', ndarray2list0(np.arange(length2)+1))
    result['fea_xaxis']=ndarray2list0(np.arange(length2)+1)

    # result['group'] = str(group)
    # result['machine'] = str(machine)
    # result['component'] = component
    # result['sensor'] = sensor



    # collection_group=db['group_data']
    # group_name = list(collection_group.find({'groupID': 'GR_' + str(group)}, {'name': 1}))

    # collection_machine=db['machine_data']
    # machine_name = list(collection_machine.find({'machineID': 'MA_'+ str(group) + '_' + str(machine)}, {'name': 1}))

    # collection_component=db['component_data']
    # component_name = list(collection_component.find({'componentID': 'CO_' + str(group)+ '_'+str(machine)+'_'+str(component)}, {'name': 1}))

    # collection_sensor=db['sensor_data']
    # sensor_name = list(collection_sensor.find({'sensorID': 'SE_' + str(group)+ '_'+str(machine)+'_'+str(component)+'_'+str(sensor)}, {'name': 1}))

    group_name = group_name[0]['name']
    machine_name = machine_name[0]['name']
    component_name = component_name[0]['name']
    sensor_name = sensor_name[0]['name']
    result['group_name']=group_name
    result['machine_name']=machine_name
    result['component_name']=component_name
    result['sensor_name']=sensor_name
    result['file']=""
    # time_add = datetime.strptime(file_name.split('.')[0], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    # result['time_add']=time_add
    speed=speed.tolist()
    result['speed']=speed
    return result


