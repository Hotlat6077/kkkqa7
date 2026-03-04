
import numpy as np
from signal_processing.fft_xiao import fftx
from signal_processing.fftxx import fftxx
from data_all_liu import get_current_speed
from mydb.get_mongo import get_db


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
def update_mins_zhaji1(path,sensor,machine):
    db = get_db()
    collection=db['vibration_data']
    collection_tooth=db.fault_frequency
    collection_standard=db.fre_standard
    # print(machine,sensor)
    data=list(collection.find({'machine':machine},{sensor:1}).sort([('dt', -1)]).limit(1))[0]#改动
    #,当前是64000点,之前不是说搞成10*6400吗
    signal=data.get(sensor)#mongodb 的表格为一次性的，遍历一次就自动删除了


    Fea1 = signal[0:8000]
    Feax1, Feay1 = fftx(Fea1)

    Fea2 = signal[8000:16000]
    Feax2, Feay2 = fftx(Fea2)

    Fea3 = signal[16000:24000]
    Feax3, Feay3 = fftx(Fea3)

    Fea4 = signal[24000:32000]
    Feax4, Feay4 = fftx(Fea4)

    Fea5 = signal[32000:40000]
    Feax5, Feay5 = fftx(Fea5)

    Fea6 = signal[40000:48000]
    Feax6, Feay6 = fftx(Fea6)

    Fea7 = signal[48000:56000]
    Feax7, Feay7 = fftx(Fea7)

    Fea8 = signal[56000:64000]
    Feax8, Feay8 = fftx(Fea8)


#######
    Feaz1 = [1 for _ in range(4000)]
    a=Feay1
    ddata=[]
    y=len(Feaz1)
    for j in range(y):
        temp=[1,j,abs(a[j])]
        ddata.append(temp)

    Feaz2 = [1 for _ in range(4000)]
    a2=Feay2
    ddata2=[]
    y2=len(Feaz2)
    for j in range(y2):
        temp=[2,j,abs(a2[j])]
        ddata2.append(temp)

    Feaz3 = [1 for _ in range(4000)]
    a3=Feay3
    ddata3=[]
    y3=len(Feaz3)
    for j in range(y3):
        temp=[3,j,abs(a3[j])]
        ddata3.append(temp)

    Feaz4 = [1 for _ in range(4000)]
    a4=Feay4
    ddata4=[]
    y4=len(Feaz4)
    for j in range(y4):
        temp=[4,j,abs(a4[j])]
        ddata4.append(temp)

    Feaz5 = [1 for _ in range(4000)]
    a5=Feay5
    ddata5=[]
    y5=len(Feaz5)
    for j in range(y5):
        temp=[5,j,abs(a5[j])]
        ddata5.append(temp)

    Feaz6 = [1 for _ in range(4000)]
    a6=Feay6
    ddata6=[]
    y6=len(Feaz6)
    for j in range(y6):
        temp=[6,j,abs(a6[j])]
        ddata6.append(temp)

    Feaz7 = [1 for _ in range(4000)]
    a7=Feay7
    ddata7=[]
    y7=len(Feaz7)
    for j in range(y7):
        temp=[7,j,abs(a7[j])]
        ddata7.append(temp)

    Feaz8 = [1 for _ in range(4000)]
    a8=Feay8
    ddata8=[]
    y8=len(Feaz8)
    for j in range(y8):
        temp=[8,j,abs(a8[j])]
        ddata8.append(temp)



    # 计算齿轮箱报警频率
    Feaxxx, Feayyy = fftxx(signal)
    Feaxxx = Feaxxx[0:5000]
    Feayyy = Feayyy[0:5000]
    speed=get_current_speed(machine)
    tooth=collection_tooth.find({},{'gear'+str(machine)+'_0':1})[0].get('gear'+str(machine)+'_0')
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

#############
    result= {}
    result['ddata'] = ddata
    result['ddata2'] = ddata2
    result['ddata3'] = ddata3
    result['ddata4'] = ddata4
    result['ddata5'] = ddata5
    result['ddata6'] = ddata6
    result['ddata7'] = ddata7
    result['ddata8'] = ddata8
    result['percentx1']=percentx1





    return result
'''
def check_data(collection,level):
    if collection.count_documents({})>=level:
'''




