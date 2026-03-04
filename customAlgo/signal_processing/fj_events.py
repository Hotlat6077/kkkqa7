
from config import start_time0, end_time0
from signal_processing.Signal2_frequency import frequencyx
from index_calculation import index_result
from signal_processing.order_ana import *

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

def update_fj_event( ):
    db = get_db()
    collection = db['event_data']
    result = list(collection.find(({"begin_date": {"$gte": str(start_time0), "$lte": str(end_time0)}})))
    for i in result:
        i['_id'] = str(i['_id'])
    res = {'result': result}
    return res

def update_mins_fj_events_index(fault_inf):
    db = get_db()
    collection = db['alert_data']
    datex=fault_inf[0:10]+' '+fault_inf[13:21]
    sensorx=fault_inf[22:]

    datapath = list(collection.find({'date': datex, 'sensorID': sensorx},
                                 {'vib_path': 1,'frefault':1}))[0]
    frefault= datapath.get('frefault')
    datapath = datapath.get('vib_path')
    with open(datapath, 'r') as file:
        signal = file.readlines()
    signal2 = [float(item) for item in signal[0].split(',')]

    fs = 1000
    T = frequencyx(RawSignal=signal2, SampleFraquency=fs)
    Feax,Feay = T.envelopex()

    signal_index = index_result(signal2, 1000)

    y3=signal_index[:, 4].ravel().tolist()  # 5.均方根值
    y4=signal_index[:, 9].ravel().tolist()  # 10.峭度
    y5=signal_index[:, 2].ravel().tolist()  # 3.标准差

    result={}
    result['y1'] = signal2
    length = len(signal2)
    result['x1'] = ndarray2list0(np.arange(length)+1)

    result['y2']=(Feay).tolist()
    result['x2']=(Feax).tolist()

    result['y3'] = y3
    length = len(y3)
    result['x3'] = ndarray2list0(np.arange(length)+1)

    result['y4'] = y4

    result['y5'] = y5

    speed=int(600)
    Feaxo, Feayo = order_analysis(signal2, fs, speed)
    result['y6'] = Feayo.tolist()
    result['x6'] = Feaxo.tolist()

    group=sensorx[3]
    machine=sensorx[5]
    component=sensorx[7]
    sensor=sensorx[9]

    result['group']=group
    result['machine']=machine
    result['component']=component
    result['sensor']=sensor

    result['frefault']=frefault


    collection_group=db['group_data']
    group_name = list(collection_group.find({'groupID': 'GR_' + str(group)}, {'name': 1}))
    collection_machine=db['machine_data']
    machine_name = list(collection_machine.find({'machineID': 'MA_'+ str(group) + '_' + str(machine)}, {'name': 1}))
    collection_component=db['component_data']
    component_name = list(collection_component.find({'componentID': 'CO_' + str(group)+ '_'+str(machine)+'_'+str(component)}, {'name': 1}))
    collection_sensor=db['sensor_data']
    sensor_name = list(collection_sensor.find({'sensorID': 'SE_' + str(group)+ '_'+str(machine)+'_'+str(component)+'_'+str(sensor)}, {'name': 1}))
    group_name = group_name[0]['name']
    machine_name = machine_name[0]['name']
    component_name = component_name[0]['name']
    sensor_name = sensor_name[0]['name']
    result['group_name']=group_name
    result['machine_name']=machine_name
    result['component_name']=component_name
    result['sensor_name']=sensor_name

    return result

