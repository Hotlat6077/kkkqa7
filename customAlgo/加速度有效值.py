import numpy as np
from preprocess import *

def acceleration_rms(acceleration_samples):
    """
    计算加速度样本的有效值（RMS）
    
    参数:
        acceleration_samples: list 或 np.ndarray，加速度采样序列（单位 m/s² 等）
    
    返回:
        float: 加速度有效值
    """
    acc_array = np.array(acceleration_samples)
    rms_acc = np.sqrt(np.mean(acc_array ** 2))
    return rms_acc

def update_mins_fj_signal_analysis3_cao_fix(data, fs , methods='raw', index13_interval = 100):
    # db = get_db()
    # collection = db['vibration_data']
    # group = int(group)
    # machine = int(machine)
    # component = int(component)
    # sensor = int(sensor)

    # fs = FSTableService.get_fs2(group, machine, component, sensor, file_name, db)
    # folder_path = config.local_data_path + f"/{group}/{machine}/{component}/{sensor}/"
    # signal = []
    # with open(f"{folder_path}/{file_name}", 'r+') as f:
    #     data = f.readlines()[0]
    #     signal.extend(list(map(float, data.split(','))))

    # 转速信号提取
    speed = 0
    speed = np.array([float(speed)]) / 60
    speed = np.round(speed, 5)
    # print(localfilename)
    # -------------------------   以下为之前读数据库的模式，需要被替换掉
    # data1 = list(collection.find({'machine': machine,'group':group,'component':component,'sensor':sensor}, {'vib':1,'speed':1}).sort([('datetime', -1)]).limit(1))[0]  # 改动
    # signal=data1.get('vib')
    blank_dict = {}
    signal = np.array(data)
    methods='raw'
    exec(f"blank_dict['out']={methods}(signal,fs)")
    Feaa = blank_dict['out'].tolist()

    acc = acceleration_rms(signal)
    result = {}
    # 原信号数据
    result['fea_y'] = Feaa
    length = len(Feaa)
    f_x1 = ndarray2list0(np.arange(length) + 1)
    f_x = [x / fs for x in f_x1]
    result['fea_x'] = f_x
    if len(Feaa) >= 1:
        result['rms_acc'] = acc
        # length = len(Feaa[:, 0])
    else:
        result['rms'] = []
        # result['peak'] = []
        length = 0


    result['fea_xaxis'] = ndarray2list0(np.arange(length) + 1)
    # print(result['rms_acc'])
    return result

    
# 示例
# if __name__ == "__main__":
#     # 假设有一组加速度采样数据（单位 m/s²）
#     sample_data = [0.1, -0.2, 0.3, -0.4, 0.5, -0.3, 0.2, -0.1]
    
#     rms_value = acceleration_rms(sample_data)
#     print(f"加速度有效值 (RMS): {rms_value:.4f} m/s²")
if __name__ == '__main__':
    from mydb.get_mongo import get_db
    db = get_db()
    collection = db['pump_waveform_report']
    # query = {
    # 'sensorId': 'SE_1_1_2_3',
    # 'time': '20251229180100'
    # }

    query = {
        # 'sensorId':sesor_id,
        'measureSiteId':int(1077691462944),
        'measureGatherId':int(1077691480608),
        'time':'20260109040100'
    }
    print("query",query)
    document = collection.find_one(query)
    
    document = collection.find_one(query)
    print("数据Data是否为不为空",document is not None)
    # 提取 fs 字段
    fs = document.get('fs')
    data = document.get('datas')
    update_mins_fj_signal_analysis3_cao_fix(data, fs, methods='raw')
