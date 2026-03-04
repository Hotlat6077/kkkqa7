
import numpy as np
from mydb.get_mongo import get_client
from signal_processing.fft_xiao import fftx
from signal_processing.fftxx import fftxx
from data_all_liu import get_current_speed
import datetime
def ndarray2list0(data):
    list0=[]
    for temp in data:
        list0.append(temp.tolist())
    return list0
def ndarray2list1(data):
    list0=[]
    for temp in data:
        list0.append(temp.tolist())
    list1=[]
    for i in list0:
        for j in i:
            list1.append(j)
    return list1
def update_mins_zhaji1(path,sensor,machine,collection_name):
    samples=2000
    client = get_client()
    db=client.Br_zj
    collection=db[collection_name]
    data=list(collection.find({'machine':machine},{sensor:1,'dt':1}).sort([('dt', 1)]))#改动
    vib_data=[i.get(sensor)[:samples] for i in data]
    date_data=[i.get('dt') for i in data]
    position_data=[]
    for i in range(len(vib_data)):
        fea=vib_data[i]
        Feax1, Feay1 = fftx(fea)
        current_date=datetime.datetime.strftime(date_data[i],'%Y-%m-%d %H:%M:%S')
        position_x=[current_date]*len(Feax1)
        position_y=np.array(Feax1).ravel().tolist()
        position_z=np.array(Feay1).ravel().tolist()
        position_series=[list(i) for i in zip(position_x,position_y,position_z)]
        position_data+=position_series if i%2==1 else position_series[::-1]
    
    # 计算齿轮箱报警频率
    diag_collection=db['vibration_data']
    collection_tooth=db.fault_frequency
    collection_standard=db.fre_standard
    diag_vib=list(diag_collection.find({'machine':machine},{sensor:1,'dt':1}).sort([('dt', -1)]))[0].get(sensor)
    Feaxxx, Feayyy = fftxx(diag_vib)
    Feaxxx = Feaxxx[0:5000]
    Feayyy = Feayyy[0:5000]
    speed=get_current_speed(machine)
    tooth=collection_tooth.find({},{'gear'+str(machine)[1]+'_0':1})[0].get('gear'+str(machine)[1]+'_0')
    fault_frequency = 217  # 理论啮合频率(转速/60)*齿轮副1输入轴齿数
    fault_frequency = int(tooth*speed/60)  # 理论啮合频率(转速/60)*齿轮副1输入轴齿数
    # print(speed,tooth,fault_frequency)
    fre_index=list(collection_standard.find({},{machine+'_'+sensor+'_fft'}))[0].get(machine+'_'+sensor+'_fft')
    print(sensor)
    # fre_index = 1.21377092  # 健康工况前三阶频率范围和

    fre_1 = sum(Feayyy[int(fault_frequency*5)-75:int(fault_frequency*5)+75])
    fre_2 = sum(Feayyy[int(fault_frequency*5*2)-75:int(fault_frequency*5*2)+75])
    fre_3 = sum(Feayyy[int(fault_frequency*5*3)-75:int(fault_frequency*5*3)+75])

    percentx1 = ((fre_1 + fre_2 + fre_3) - (fre_index)) / 8
    percentx1 = round(percentx1 * 100, 3)

    if percentx1 >= 0:
        percentx1 = percentx1
    else:
        percentx1 = 0

    result= {}
    result['ddata'] = position_data
    result['percentx1']=percentx1





    return result



