
import numpy as np
from signal_processing.fft_xiao import fftx
from signal_processing.vmd_xiao import vmd

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
def update_mins_zhaji3(path,sensor_index):
    db = get_db()
    collection1=db['show']#实时刷新表
    collection2=db['data']#主表，但需要再考量一下聚合的问题
    collection3=db['thres']#
    # collection3=db['training_data']#
    data=list(collection1.find({},{'_id':1,'date':1,'sensor1':1}))
    signal=[i.get('sensor1') for i in data]#mongodb 的表格为一次性的，遍历一次就自动删除了
    signal=np.reshape(signal,(-1,1))
    Fea = signal
    Fea2x, Fea2y = fftx(signal)



    result= {}
    result['shiyu']=ndarray2list1(Fea)
    length=len(Fea)
    result['fea_xaxis']=ndarray2list0(np.arange(length)+1)
    result['xxx'] = (Fea2x).tolist()
    result['yyy'] = (Fea2y).tolist()


    return result

'''
def check_data(collection,level):
    if collection.count_documents({})>=level:
'''




