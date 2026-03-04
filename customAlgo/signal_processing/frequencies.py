
import os
import numpy as np
import math
from config import stable_faultfre_raitos
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


def create_fault_frequency_dict(data):
    fault_frequency_dict = {}
    # 遍历数据库中的每一项数据
    group_number = int(data["Group_number"])
    machine_number = int(data["Machine_number"])
    component_number = int(data["Component_number"])
    # 为每个组生成报警频率字典
    for g in range(1, group_number + 1):
        for m in range(1, machine_number + 1):
            for c in range(1, component_number + 1):
                # 假设每个组件有三个位置，编号为1到3
                for position in range(1, 4):  # 组件的三个位置
                    # 根据组、机器、组件和位置的不同设置不同的报警频率值
                    fault_frequency = 100
                    key = f'g{g}_m{m}_c{c}_s{position}'
                    fault_frequency_dict[key] = float(fault_frequency)
    return fault_frequency_dict


def import_frequency():
    db = get_db()
    collection=db['fault_frequency']
    if len(list(collection.find({},{'_id':1})))==0:
        collection1 = db['composition_data']  # 实时刷新表
        db_data = list(collection1.find({}))[0]
        # 根据获取的数量生成报警频率字典
        fault_frequency_para = create_fault_frequency_dict(db_data)
        # print(fault_frequency_para)
        collection.insert_one(fault_frequency_para)
    else:
        pass

def query_latest_value(group, machine, component, p):
    db = get_db()
    collection3=db['fault_frequency_para']#实时刷新表
    # 构建查询字段名
    field_name = 'g' + group + '_m' + machine + '_c' + component + '_p' + str(p)
    # 查询并获取最新的一个记录的值
    result = list(collection3.find({}, {field_name: 1, '_id': 1}).sort([('_id', -1)]).limit(1))
    if result:
        return result[0].get(field_name)
    else:
        return None

def dbfre_update(p,group,machine,fault1,fault2,fault3,fault4,num,name):
    db = get_db()
    collection = db['sensor_data']
    id = collection.find({'componentID': 'CO_' + group + '_' + machine + '_'+p,'name':name},
                         {'_id': 1, 'componentID': 1, 'faultfre': 1}).sort([('_id', -1)]).limit(2)[num].get('_id')
    condition3 = {'_id': id}
    para_part3 = {'$set': {'faultfre.outer': float(fault1),
                           'faultfre.inner': float(fault2),
                           'faultfre.ball': float(fault3),'faultfre.cage': float(fault4)}}
    collection.update_many(condition3, para_part3)

def fault_fre1(group,machine,p1,p2,p3,p4,p5,p6):#需要给函数增加一个sensor_index参数
    db = get_db()
    collection3=db['sensor_data']#实时刷新表
    # p1_d1 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_1','name':'前轴承径向'}, {'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数1']
    # p1_d2 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_1','name':'前轴承径向'}, {'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数2']
    # p1_d3 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_1','name':'前轴承径向'}, {'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数3']
    # p1_d4 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_1','name':'前轴承径向'}, {'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数4']
    #
    # p1_s = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_1','name':'前轴承径向'}, {'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['输入转速']
    p1_d1 = float(p1)
    p1_d2 = float(p2)
    p1_d3 = float(p3)
    p1_d4 = float(p4)

    p1_s = float(p5)
    speed=float(p6)
    p1_s=p1_s*speed

    # print(p1_d1,p1_d2,p1_d3,p1_d4,p1_s,)
    # print(p1,p2,p3,p4,p5)
    if p1_d1==0:
        fault1_1='D不能为0！'
    elif p1_d1<p1_d2:
        fault1_1='D<d！'
    else:
        fault1_1=round((p1_d3/2)*(p1_s/60)*(1-(p1_d2/p1_d1)*np.cos(math.radians(p1_d4))),5)
        fault1_2=round((p1_d3/2)*(p1_s/60)*(1+(p1_d2/p1_d1)*np.cos(math.radians(p1_d4))),5)
        fault1_3=round(((p1_d1/p1_d2))*(p1_s/60)*(1-(p1_d2/p1_d1)*(p1_d2/p1_d1)*np.cos(math.radians(p1_d4))*np.cos(math.radians(p1_d4))),5)
        fault1_4=round(((1/2))*(p1_s/60)*(1-(p1_d2/p1_d1)*np.cos(math.radians(p1_d4))),5)

        dbfre_update('1',group,machine,fault1_1,fault1_2,fault1_3,fault1_4,0,'前轴承径向')
        # dbfre_update('1',group,machine,fault1_1,fault1_2,fault1_3,fault1_4,1,'前轴承径向')

    result= {}
    result["fault1_1"]=fault1_1
    result["fault1_2"]=fault1_2
    result["fault1_3"]=fault1_3
    result["fault1_4"]=fault1_4

    return result


def fault_fre2(group,machine,p1,p2,p3,p4,p5,p6):#需要给函数增加一个sensor_index参数
    db = get_db()
    collection3=db['sensor_data']#实时刷新表

    p2_d1 = float(p1)
    p2_d2 = float(p2)
    p2_d3 = float(p3)
    p2_d4 = float(p4)

    p2_s = float(p5)
    speed=float(p6)
    p2_s=p2_s*speed
    # p2_d1 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_1','name':'后轴承径向'},{'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数1']
    # p2_d2 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_1','name':'后轴承径向'},{'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数2']
    # p2_d3 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_1','name':'后轴承径向'},{'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数3']
    # p2_d4 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_1','name':'后轴承径向'},{'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数4']
    #
    # p2_s = collection3.find({'componentID':'CO_'+group+'_'+machine+'_1','name':'后轴承径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('hardpara')['输入转速']
    if p2_d1==0:
        fault2_1='D不能为0！'
    elif p2_d1<p2_d2:
        fault2_1='D<d！'
    else:
        fault2_1=round((p2_d3/2)*(p2_s/60)*(1-(p2_d2/p2_d1)*np.cos(math.radians(p2_d4))),5)
        fault2_2=round((p2_d3/2)*(p2_s/60)*(1+(p2_d2/p2_d1)*np.cos(math.radians(p2_d4))),5)
        fault2_3=round(((p2_d1/p2_d2))*(p2_s/60)*(1-(p2_d2/p2_d1)*(p2_d2/p2_d1)*np.cos(math.radians(p2_d4))*np.cos(math.radians(p2_d4))),5)
        fault2_4=round(((1/2))*(p2_s/60)*(1-(p2_d2/p2_d1)*np.cos(math.radians(p2_d4))),5)

        dbfre_update('1',group,machine,fault2_1,fault2_2,fault2_3,fault2_4,0,'后轴承径向')
        # dbfre_update('1',group,machine,fault2_1,fault2_2,fault2_3,fault2_4,1,'后轴承径向')
    result= {}
    result["fault2_1"]=fault2_1
    result["fault2_2"]=fault2_2
    result["fault2_3"]=fault2_3
    result["fault2_4"]=fault2_4

    return result


def fault_fre3(group,machine,p1,p2,p3,p4,p5,p6):#需要给函数增加一个sensor_index参数
    db = get_db()
    collection3=db['sensor_data']#实时刷新表
    p3_d1 = float(p1)
    p3_d2 = float(p2)
    p3_d3 = float(p3)
    p3_d4 = float(p4)

    p3_s = float(p5)
    speed=float(p6)
    p3_s=p3_s*speed
    # p3_d1 = collection3.find({'componentID':'CO_'+group+'_'+machine+'_2','name':'一级行星齿圈径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('hardpara')['测试硬件参数1']
    # p3_d2 = collection3.find({'componentID':'CO_'+group+'_'+machine+'_2','name':'一级行星齿圈径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('hardpara')['测试硬件参数2']
    # p3_d3 = collection3.find({'componentID':'CO_'+group+'_'+machine+'_2','name':'一级行星齿圈径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('hardpara')['测试硬件参数3']
    # p3_d4 = collection3.find({'componentID':'CO_'+group+'_'+machine+'_2','name':'一级行星齿圈径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('hardpara')['测试硬件参数4']
    # p3_s = collection3.find({'componentID':'CO_'+group+'_'+machine+'_2','name':'一级行星齿圈径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('hardpara')['输入转速']

    fc=p3_d1/(p3_d1+p3_d3)*(p3_s/60)
    fm=fc*p3_d3

    fault3_1=round((fm/p3_d2),5)
    fault3_2=round((fm/p3_d1)*p3_d4,5)
    fault3_3=round((fm/p3_d3)*p3_d4,5)
    

    result= {}
    result["fault3_1"]=fault3_1
    result["fault3_2"]=fault3_2
    result["fault3_3"]=fault3_3

    collection=db['sensor_data']

    ####################### 1010 Liu修改 ######################
    id=collection.find({'componentID':'CO_'+group+'_'+machine+'_2','name':'一级行星齿圈径向'},{'_id':1,'componentID':1,'faultfre':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
    condition3={'_id':id}
    para_part3={'$set':{'faultfre.sun':float(fault3_1),
                        'faultfre.planet':float(fault3_2),
                        'faultfre.race1':float(fault3_3),
                        'faultfre.PL1_inner':stable_faultfre_raitos['PL1_inner']*p3_s/60,
                        'faultfre.PL1_outer':stable_faultfre_raitos['PL1_outer']*p3_s/60,
                        'faultfre.PL1_ball':stable_faultfre_raitos['PL1_ball']*p3_s/60,
                        'faultfre.PL1_cage':stable_faultfre_raitos['PL1_cage']*p3_s/60,
                        'faultfre.fm':float(round(fm,5))}}
    collection.update_many(condition3, para_part3)
    id=collection.find({'componentID':'CO_'+group+'_'+machine+'_2','name':'输入轴径向'},{'_id':1,'componentID':1,'faultfre':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
    condition3={'_id':id}
    para_part3={'$set':{'faultfre.sun':float(fault3_1),
                        'faultfre.planet':float(fault3_2),
                        'faultfre.race1':float(fault3_3),
                        'faultfre.PL1_inner':stable_faultfre_raitos['PL1_inner']*p3_s/60,
                        'faultfre.PL1_outer':stable_faultfre_raitos['PL1_outer']*p3_s/60,
                        'faultfre.PL1_ball':stable_faultfre_raitos['PL1_ball']*p3_s/60,
                        'faultfre.PL1_cage':stable_faultfre_raitos['PL1_cage']*p3_s/60,
                        'faultfre.fm':float(round(fm,5))}}
    collection.update_many(condition3, para_part3)
    return result
    ####################### 1010 Liu修改 ######################

def fault_fre03(group,machine,p1,p2,p3,p4,p5,p6):#需要给函数增加一个sensor_index参数
    db = get_db()
    collection3=db['sensor_data']#实时刷新表
    p3_d1 = float(p1)
    p3_d2 = float(p2)
    p3_d3 = float(p3)
    p3_d4 = float(p4)

    p3_s = float(p5)
    speed=float(p6)
    p3_s=p3_s*speed
    # p3_d1 = collection3.find({'componentID':'CO_'+group+'_'+machine+'_2','name':'二级行星齿圈径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('hardpara')['测试硬件参数1']
    # p3_d2 = collection3.find({'componentID':'CO_'+group+'_'+machine+'_2','name':'二级行星齿圈径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('hardpara')['测试硬件参数2']
    # p3_d3 = collection3.find({'componentID':'CO_'+group+'_'+machine+'_2','name':'二级行星齿圈径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('hardpara')['测试硬件参数3']
    # p3_d4 = collection3.find({'componentID':'CO_'+group+'_'+machine+'_2','name':'二级行星齿圈径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('hardpara')['测试硬件参数4']
    # p3_s = collection3.find({'componentID':'CO_'+group+'_'+machine+'_2','name':'二级行星齿圈径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('hardpara')['输入转速']


    fc=p3_d1/(p3_d1+p3_d3)*(p3_s/60)
    fm=fc*p3_d3

    fault3_1=round((fm/p3_d2),5)
    fault3_2=round((fm/p3_d1)*p3_d4,5)
    fault3_3=round((fm/p3_d3)*p3_d4,5)

    result= {}
    result["fault03_1"]=fault3_1
    result["fault03_2"]=fault3_2
    result["fault03_3"]=fault3_3
    print(result)
    collection=db['sensor_data']

    ####################### 1010 Liu修改 ######################
    id=collection.find({'componentID':'CO_'+group+'_'+machine+'_2','name':'二级行星齿圈径向'},{'_id':1,'componentID':1,'faultfre':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
    condition3={'_id':id}
    para_part3={'$set':{'faultfre.sun':float(fault3_1),
                        'faultfre.planet':float(fault3_2),
                        'faultfre.race2':float(fault3_3),
                        'faultfre.PL2_inner':stable_faultfre_raitos['PL2_inner']*p3_s/60,
                        'faultfre.PL2_outer':stable_faultfre_raitos['PL2_outer']*p3_s/60,
                        'faultfre.PL2_ball':stable_faultfre_raitos['PL2_ball']*p3_s/60,
                        'faultfre.PL2_cage':stable_faultfre_raitos['PL2_cage']*p3_s/60,
                        'faultfre.fm':float(round(fm,5))}}
    collection.update_many(condition3, para_part3)

    id=collection.find({'componentID':'CO_'+group+'_'+machine+'_2','name':'高速轴径向'},{'_id':1,'componentID':1,'faultfre':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
    condition3={'_id':id}
    para_part3={'$set':{'faultfre.gear3b':float(fault3_1),
                        'faultfre.gear3s':float(fault3_2),
                        'faultfre.HSS_inner':stable_faultfre_raitos['HSS_inner']*p3_s/60,
                        'faultfre.HSS_outer':stable_faultfre_raitos['HSS_outer']*p3_s/60,
                        'faultfre.HSS_ball':stable_faultfre_raitos['HSS_ball']*p3_s/60,
                        'faultfre.HSS_cage':stable_faultfre_raitos['HSS_cage']*p3_s/60,}}
    collection.update_many(condition3, para_part3)

    id=collection.find({'componentID':'CO_'+group+'_'+machine+'_2','name':'高速轴轴向'},{'_id':1,'componentID':1,'faultfre':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
    condition3={'_id':id}
    para_part3={'$set':{'faultfre.gear3b':float(fault3_1),
                        'faultfre.gear3s':float(fault3_2),
                        'faultfre.HSS_inner':stable_faultfre_raitos['HIS_inner']*p3_s/60,
                        'faultfre.HSS_outer':stable_faultfre_raitos['HIS_outer']*p3_s/60,
                        'faultfre.HSS_ball':stable_faultfre_raitos['HIS_ball']*p3_s/60,
                        'faultfre.HSS_cage':stable_faultfre_raitos['HIS_cage']*p3_s/60,}}
    collection.update_many(condition3, para_part3)
    ####################### 1010 Liu修改 ######################


    # collection=db['sensor_data']
    # id=collection.find({'componentID':'CO_'+group+'_'+machine+'_3','name':'二级行星齿圈径向'},{'_id':1,'componentID':1,'faultfre':1}).sort([('_id',-1)]).limit(1)[1].get('_id')
    # condition3={'_id':id}
    # para_part3={'$set':{'faultfre.sun':float(fault3_1),
    #                     'faultfre.planet':float(fault3_2),
    #                     'faultfre.race':float(fault3_3)}}
    # collection.update_many(condition3, para_part3)
    return result

def fault_fre4(group,machine,p1,p2,p5,p6):#需要给函数增加一个sensor_index参数
    db = get_db()
    collection3=db['sensor_data']#实时刷新表
    p2_d1 = float(p1)
    p2_d2 = float(p2)
    # p2_d3 = float(p3)
    # p2_d4 = float(p4)
    #
    p2_s = float(p5)
    speed=float(p6)
    p2_s=p2_s*speed
    # p2_d1 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_2','name':'高速轴径向'},{'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数1']
    # p2_d2 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_2','name':'高速轴径向'},{'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数2']
    # p2_d3 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_2','name':'高速轴径向'},{'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数3']
    # p2_d4 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_2','name':'高速轴径向'},{'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数4']
    #
    # p2_s = collection3.find({'componentID':'CO_'+group+'_'+machine+'_2','name':'高速轴径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('hardpara')['输入转速']

        # fault2_1=round((p2_d3/2)*(p2_s/60)*(1-(p2_d2/p2_d1)*np.cos(math.radians(p2_d4))),2)
        # fault2_2=round((p2_d3/2)*(p2_s/60)*(1+(p2_d2/p2_d1)*np.cos(math.radians(p2_d4))),2)
        # fault2_3=round(((p2_d1/p2_d2))*(p2_s/60)*(1-(p2_d2/p2_d1)*(p2_d2/p2_d1)*np.cos(math.radians(p2_d4))*np.cos(math.radians(p2_d4))),2)
        # fault2_4=round(((1/2))*(p2_s/60)*(1-(p2_d2/p2_d1)*np.cos(math.radians(p2_d4))),2)

    fc = (p2_s / 60)
    fm = fc * p2_d1

    fault2_1 = round(fm, 5)
    fault2_2 = round(fm, 5)


        # dbfre_update('2',group,machine,fault2_1,fault2_2,fault2_3,fault2_4,0,'高速轴径向')
        # dbfre_update('2',group,machine,fault2_1,fault2_2,fault2_3,fault2_4,1,'高速轴径向')
    result= {}
    result["fault4_1"]=fault2_1
    result["fault4_2"]=fault2_2

    # result["fault4_4"]=fault2_4

    return result


def fault_fre5(group,machine,p1,p2,p3,p4,p5,p6):#需要给函数增加一个sensor_index参数
    db = get_db()
    collection3=db['sensor_data']#实时刷新表

    # p2_d1 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_3','name':'驱动端径向'},{'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数1']
    # p2_d2 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_3','name':'驱动端径向'},{'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数2']
    # p2_d3 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_3','name':'驱动端径向'},{'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数3']
    # p2_d4 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_3','name':'驱动端径向'},{'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数4']
    #
    # p2_s = collection3.find({'componentID':'CO_'+group+'_'+machine+'_3','name':'驱动端径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('hardpara')['输入转速']
    p2_d1 = float(p1)
    p2_d2 = float(p2)
    p2_d3 = float(p3)
    p2_d4 = float(p4)

    p2_s = float(p5)
    speed=float(p6)
    p2_s=p2_s*speed
    if p2_d1==0:
        fault2_1='D不能为0！'
    elif p2_d1<p2_d2:
        fault2_1='D<d！'
    else:
        fault2_1=round((p2_d3/2)*(p2_s/60)*(1-(p2_d2/p2_d1)*np.cos(math.radians(p2_d4))),5)
        fault2_2=round((p2_d3/2)*(p2_s/60)*(1+(p2_d2/p2_d1)*np.cos(math.radians(p2_d4))),5)
        fault2_3=round(((p2_d1/p2_d2))*(p2_s/60)*(1-(p2_d2/p2_d1)*(p2_d2/p2_d1)*np.cos(math.radians(p2_d4))*np.cos(math.radians(p2_d4))),5)
        fault2_4=round(((1/2))*(p2_s/60)*(1-(p2_d2/p2_d1)*np.cos(math.radians(p2_d4))),5)

        dbfre_update('3',group,machine,fault2_1,fault2_2,fault2_3,fault2_4,0,'驱动端径向')
        # dbfre_update('2',group,machine,fault2_1,fault2_2,fault2_3,fault2_4,1,'驱动端径向')
    result= {}
    result["fault5_1"]=fault2_1
    result["fault5_2"]=fault2_2
    result["fault5_3"]=fault2_3
    result["fault5_4"]=fault2_4

    return result


def fault_fre6(group,machine,p1,p2,p3,p4,p5,p6):#需要给函数增加一个sensor_index参数
    db = get_db()
    collection3=db['sensor_data']#实时刷新表

    # p2_d1 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_3','name':'自由端径向'},{'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数1']
    # p2_d2 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_3','name':'自由端径向'},{'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数2']
    # p2_d3 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_3','name':'自由端径向'},{'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数3']
    # p2_d4 = collection3.find({'componentID': 'CO_' + group + '_' + machine + '_3','name':'自由端径向'},{'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('hardpara')['测试硬件参数4']
    #
    # p2_s = collection3.find({'componentID':'CO_'+group+'_'+machine+'_3','name':'自由端径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('hardpara')['输入转速']
    p2_d1 = float(p1)
    p2_d2 = float(p2)
    p2_d3 = float(p3)
    p2_d4 = float(p4)

    p2_s = float(p5)
    speed=float(p6)
    p2_s=p2_s*speed
    if p2_d1==0:
        fault2_1='D不能为0！'
    elif p2_d1<p2_d2:
        fault2_1='D<d！'
    else:
        fault2_1=round((p2_d3/2)*(p2_s/60)*(1-(p2_d2/p2_d1)*np.cos(math.radians(p2_d4))),5)
        fault2_2=round((p2_d3/2)*(p2_s/60)*(1+(p2_d2/p2_d1)*np.cos(math.radians(p2_d4))),5)
        fault2_3=round(((p2_d1/p2_d2))*(p2_s/60)*(1-(p2_d2/p2_d1)*(p2_d2/p2_d1)*np.cos(math.radians(p2_d4))*np.cos(math.radians(p2_d4))),5)
        fault2_4=round(((1/2))*(p2_s/60)*(1-(p2_d2/p2_d1)*np.cos(math.radians(p2_d4))),5)

        dbfre_update('3',group,machine,fault2_1,fault2_2,fault2_3,fault2_4,0,'自由端径向')
        # dbfre_update('2',group,machine,fault2_1,fault2_2,fault2_3,fault2_4,1,'自由端径向')
    result= {}
    result["fault6_1"]=fault2_1
    result["fault6_2"]=fault2_2
    result["fault6_3"]=fault2_3
    result["fault6_4"]=fault2_4

    return result
# import_frequency()