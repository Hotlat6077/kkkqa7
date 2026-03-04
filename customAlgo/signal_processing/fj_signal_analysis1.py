
from signal_processing.envlop_xiao import env

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
def update_mins_fj_signal_analysis1(path,group,machine,component,sensor):
    db = get_db()
    collection=db['vibration_data']
    group=int(group)
    machine=int(machine)
    component=str(component)
    sensor=str(sensor)
    data1 = list(collection.find({'machine': machine,'group':group}, {component+'_'+sensor:1}).sort([('datetime', -1)]).limit(1))[0]  # 改动
    signal=data1.get(component+'_'+sensor)



    Feax, Feay = env(signal)
    Feax = Feax
    Feay = Feay

    ll=2000
    low=0.33
    high=0.6

    Feax1=Feax[0:int(ll*low)]
    Feay1=Feay[0:int(ll*low)]
    Feax2=Feax[int(ll*low):int(ll*high)]
    Feay2=Feay[int(ll*low):int(ll*high)]
    Feax3=Feax[int(ll*high):ll]
    Feay3=Feay[int(ll*high):ll]

    result= {}
    result['fea_xaxis1'] = (Feax1).tolist()
    result['pinpu1'] = (Feay1).tolist()
    result['fea_xaxis2'] = (Feax2).tolist()
    result['pinpu2'] = (Feay2).tolist()
    result['fea_xaxis3'] = (Feax3).tolist()
    result['pinpu3'] = (Feay3).tolist()


    result['group'] = str(group)
    result['machine'] = str(machine)
    result['component'] = component
    result['sensor'] = sensor
    return result





