
import numpy as np
from signal_processing.envlop_xiao import env
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
def update_mins_zhaji5(path,sensor,machine):
    db = get_db()
    collection=db['vibration_data']
    collection_tooth=db.fault_frequency
    collection_standard=db.fre_standard
    # print(machine,sensor)
    data=list(collection.find({'machine':machine},{sensor:1}).sort([('dt', -1)]).limit(1))[0]#改动
    #,当前是64000点,之前不是说搞成10*6400吗
    signal=data.get(sensor)#mongodb 的表格为一次性的，遍历一次就自动删除了
    Fea = signal
    Feax, Feay = env(signal)
    Feax = Feax[0:5000]
    Feay = Feay[0:5000]


    speed = get_current_speed(machine)
    tooth = collection_tooth.find({}, {'gear' + str(machine)[1] + '_0': 1})[0].get('gear' + str(machine)[1] + '_0')
    fault_frequency = int(tooth * speed / 60)  # 理论啮合频率(转速/60)*齿轮副1输入轴齿数

### 1/2倍频率
    Fea05x = Feax[int(fault_frequency * 5*0.5) - 100:int(fault_frequency * 5*0.5) + 100]
    Fea05y = Feay[int(fault_frequency * 5*0.5) - 100:int(fault_frequency * 5*0.5) + 100]
### 一倍频率
    Fea1x=Feax[int(fault_frequency*5)-100:int(fault_frequency*5)+100]
    Fea1y=Feay[int(fault_frequency*5)-100:int(fault_frequency*5)+100]
### 二倍频率
    Fea2x = Feax[int(fault_frequency * 5*2) - 100:int(fault_frequency * 5*2) + 100]
    Fea2y = Feay[int(fault_frequency * 5*2) - 100:int(fault_frequency * 5*2) + 100]
### 三倍频率
    Fea3x = Feax[int(fault_frequency * 5*3) - 100:int(fault_frequency * 5*3) + 100]
    Fea3y = Feay[int(fault_frequency * 5*3) - 100:int(fault_frequency * 5*3) + 100]


    fre_1 = sum(Feay[int(fault_frequency*5*0.5)-100:int(fault_frequency*5*0.5)+100])
    fre_2 = sum(Feay[int(fault_frequency*5)-100:int(fault_frequency*5)+100])
    fre_3 = sum(Feay[int(fault_frequency*5*1.5)-100:int(fault_frequency*5*1.5)+100])
    fre_4 = sum(Feay[int(fault_frequency*5*2)-100:int(fault_frequency*5*2)+100])
    fre_5 = sum(Feay[int(fault_frequency*5*3)-100:int(fault_frequency*5*3)+100])


    result= {}


    result['d05']=[list(i) for i in zip(Fea05x.tolist(),Fea05y.tolist())]
    result['d11']=[list(i) for i in zip(Fea1x.tolist(),Fea1y.tolist())]
    result['d22']=[list(i) for i in zip(Fea2x.tolist(),Fea2y.tolist())]
    result['d33']=[list(i) for i in zip(Fea3x.tolist(),Fea3y.tolist())]

    # result['xxx05'] = (Fea05x).tolist()
    # result['yyy05'] = (Fea05y).tolist()
    # result['xxx1'] = (Fea1x).tolist()
    # result['yyy1'] = (Fea1y).tolist()
    # result['xxx2'] = (Fea2x).tolist()
    # result['yyy2'] = (Fea2y).tolist()
    # result['xxx3'] = (Fea3x).tolist()
    # result['yyy3'] = (Fea3y).tolist()

    result['har1'] = fre_1
    result['har2'] = fre_2
    result['har3'] = fre_3
    result['har4'] = fre_4
    result['har5'] = fre_5


    return result

'''
def check_data(collection,level):
    if collection.count_documents({})>=level:
'''




