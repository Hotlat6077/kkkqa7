
import pymongo
# import os
# import datetime
from flask import Flask, render_template,request,url_for,request,make_response,redirect,flash

from mydb.get_mongo import get_client, get_db


# def create_fault_frequency_para_dict(data):
#     para_dict = {}
#     # 遍历数据库中的每一项数据
#     group_number = int(data["Group_number"])
#     machine_number = int(data["Machine_number"])
#     component_number = int(data["Component_number"])
#     # 为每个组生成报警频率参数字典
#     for g in range(1, group_number + 1):
#         for m in range(1, machine_number + 1):
#             for c in range(1, component_number + 1):
#                 # 假设每个组件有三个位置，编号为1到3
#                 for position in range(1, 4):  # 组件的三个位置
#                     for pa in range(1,4):
#                         # 根据组、机器、组件和位置的不同设置不同的报警频率参数值
#                         para = 20
#                         key = f'g{g}_m{m}_c{c}_p{position}_set{pa}'
#                         para_dict[key] = float(para)
#                     para_dict[f'g{g}_m{m}_c{c}_p{position}_s'] = float(300)
#
#     return para_dict
#
#
# def import_machine_para():
#     client = get_client()
#     db=client['yueyangfan']
#     collection=db['fault_frequency_para']
#     if len(list(collection.find({},{'_id':1})))==0:
#         collection1 = db['composition_data']  # 实时刷新表
#         db_data = list(collection1.find({}))[0]
#         # 根据获取的数量生成报警频率字典
#         fault_frequency_para = create_fault_frequency_para_dict(db_data)
#         print(fault_frequency_para)
#         collection.insert_one(fault_frequency_para)
#     else:
#         pass

# def gear1(para1,para2,para3,para4,group,machine,component):
#     client = get_client()
#     db=client['yueyangfan']
#     collection=db['fault_frequency_para']
#     id=collection.find({},{'_id':1,'g'+group+'_m'+machine+'_c'+component+'_p1'+'_set1':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
#     condition1={'_id':id}
#     para_part1={'$set':{'g'+group+'_m'+machine+'_c'+component+'_p1'+'_set1':float(para1)}}
#
#     id=collection.find({},{'_id':1,'g'+group+'_m'+machine+'_c'+component+'_p1'+'_set2':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
#     condition2={'_id':id}
#     para_part2={'$set':{'g'+group+'_m'+machine+'_c'+component+'_p1'+'_set2':float(para2)}}
#
#     id=collection.find({},{'_id':1,'g'+group+'_m'+machine+'_c'+component+'_p1'+'_set3':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
#     condition3={'_id':id}
#     para_part3={'$set':{'g'+group+'_m'+machine+'_c'+component+'_p1'+'_set3':float(para3)}}
#     id=collection.find({},{'_id':1,'g'+group+'_m'+machine+'_c'+component+'_p1'+'_s':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
#     condition4={'_id':id}
#     para_part4={'$set':{'g'+group+'_m'+machine+'_c'+component+'_p1'+'_s':float(para4)}}
#
#     if float(para1)==0:
#         p1="D不能为0！"
#         print(p1)
#     elif float(para1)<float(para2):
#         p1='D<d!'
#         print(p1)
#     else:
#         p1='p1'
#         collection.update_one(condition1, para_part1), collection.update_one(condition2,para_part2), collection.update_one(condition3, para_part3), collection.update_one(condition4, para_part4)
#
#     result= {}
#     result["p1"]=p1
#     return result


def gear1(para0,para1,para2,para3,para4,para5, para6, group,machine):
    db = get_db()
    collection=db['sensor_data']
    if group=='3' and machine=='7':
        id=collection.find({'componentID':'CO_'+group+'_'+machine+'_1','name':'前轴承径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
    else:
        id=collection.find({'name':'前轴承径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)])
        id=[i.get('_id') for i in id]
        id0=collection.find({'componentID':'CO_3_7_1','name':'前轴承径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
        id.remove(id0)
    condition1={'_id':id}
    para_part1={'$set':{'hardpara.测试硬件参数1':float(para1),
                        'hardpara.测试硬件参数2':float(para2),
                        'hardpara.测试硬件参数3':float(para3),
                        'hardpara.测试硬件参数4': float(para4),
                        'hardpara.输入转速':float(para5)}}
    if float(para1)==0:
        p1="D不能为0！"
        print(p1)
    elif float(para1)<float(para2):
        p1='D<d!'
        print(p1)
    else:
        p1='p1'
        if group == '3' and machine == '7':
            collection.update_many(condition1,para_part1)
        else:
            [collection.update_many({'_id': i}, para_part1) for i in condition1['_id']]
    result= {}
    result["p1"]=p1

    # ----------------------- 以下为更新或插入 model_data -----------------------
    collection1=db['model_data']
    model_number = para0
    data_to_check = {'型号': model_number,'参数5':'主轴承前轴承'}

    existing_data = collection1.find_one(data_to_check)
    if existing_data:
        # 如果已经存在，则更新
        print(f"Data with model number '{model_number}' already exists. Updating existing data.")
        if group == '3':
            data_to_update = {
                '参数1': para1,
                '参数2': para2,
                '参数3': para3,
                '参数4': para4,
                '传动系数': para6,
                '压缩机类型': 'MySE10-242'
            }
        else:
            data_to_update = {
                '参数1': para1,
                '参数2': para2,
                '参数3': para3,
                '参数4': para4,
                '传动系数': para6,
                '压缩机类型': 'MySE8.5-230'
            }
        collection1.update_one(data_to_check, {'$set': data_to_update})
    else:
        # 如果不存在，则插入
        if group == '3':
            data_to_insert = {
                '型号': para0,
                '参数1': para1,
                '参数2': para2,
                '参数3': para3,
                '参数4': para4,
                '参数5': '主轴承前轴承',
                '传动系数': para6,
                '压缩机类型': 'MySE10-242'
            }
        else:
            data_to_insert = {
                '型号': para0,
                '参数1': para1,
                '参数2': para2,
                '参数3': para3,
                '参数4': para4,
                '参数5': '主轴承前轴承',
                '传动系数': para6,
                '压缩机类型': 'MySE8.5-230'
            }
        collection_new= collection1.insert_one(data_to_insert)
        print(f"Data inserted with ID: {collection_new.inserted_id}")
    return result

def gear2(para0,para1,para2,para3,para4,para5, para6, group,machine):
    db = get_db()
    collection=db['sensor_data']
    if group=='3' and machine=='7':
        id=collection.find({'componentID':'CO_'+group+'_'+machine+'_1','name':'后轴承径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
    else:
        id=collection.find({'name':'后轴承径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)])
        id=[i.get('_id') for i in id]
        id0=collection.find({'componentID':'CO_3_7_1','name':'后轴承径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
        id.remove(id0)

    condition1={'_id':id}
    para_part1={'$set':{'hardpara.测试硬件参数1':float(para1),
                        'hardpara.测试硬件参数2':float(para2),
                        'hardpara.测试硬件参数3':float(para3),
                        'hardpara.测试硬件参数4': float(para4),
                        'hardpara.输入转速':float(para5)}}

    if float(para1)==0:
        p1="D不能为0！"
        print(p1)
    elif float(para1)<float(para2):
        p1='D<d!'
        print(p1)
    else:
        p1='p1'
        if group == '3' and machine == '7':
            collection.update_many(condition1,para_part1)
        else:
            [collection.update_many({'_id': i}, para_part1) for i in condition1['_id']]

    result= {}
    result["p1"]=p1

    # ----------------------- 以下为更新或插入 model_data -----------------------
    collection1=db['model_data']
    model_number = para0
    data_to_check = {'型号': model_number,'参数5':'主轴承后轴承'}

    existing_data = collection1.find_one(data_to_check)
    if existing_data:
        print(f"Data with model number '{model_number}' already exists. Updating existing data.")
        if group == '3':
            data_to_update = {
                '参数1': para1,
                '参数2': para2,
                '参数3': para3,
                '参数4': para4,
                '传动系数': para6,
                '压缩机类型': 'MySE10-242'
            }
        else:
            data_to_update = {
                '参数1': para1,
                '参数2': para2,
                '参数3': para3,
                '参数4': para4,
                '传动系数': para6,
                '压缩机类型': 'MySE8.5-230'
            }
        collection1.update_one(data_to_check, {'$set': data_to_update})
    else:
        if group == '3':
            data_to_insert = {
                '型号': para0,
                '参数1': para1,
                '参数2': para2,
                '参数3': para3,
                '参数4': para4,
                '传动系数': para6,
                '参数5': '主轴承后轴承',
                '压缩机类型': 'MySE10-242'
            }
        else:
            data_to_insert = {
                '型号': para0,
                '参数1': para1,
                '参数2': para2,
                '参数3': para3,
                '参数4': para4,
                '传动系数': para6,
                '参数5': '主轴承后轴承',
                '压缩机类型': 'MySE8.5-230'
            }
        collection_new= collection1.insert_one(data_to_insert)
        print(f"Data inserted with ID: {collection_new.inserted_id}")
    return result

def gear3(para0,para1,para2,para3,para4,para5,para6, para7, para8, group,machine):

    db = get_db()
    collection=db['sensor_data']
    if group=='3' and machine=='7':
        id1 = collection.find({'componentID': 'CO_' + group + '_' + machine + '_2', 'name': '一级行星齿圈径向'},
                              {'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('_id')
        id2 = collection.find({'componentID': 'CO_' + group + '_' + machine + '_2', 'name': '输入轴径向'},
                              {'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('_id')
    else:
        id1=collection.find({'name':'一级行星齿圈径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)])
        id1=[i.get('_id') for i in id1]
        id10=collection.find({'componentID':'CO_3_7_2','name':'一级行星齿圈径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
        id1.remove(id10)

        id2=collection.find({'name':'输入轴径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)])
        id2=[i.get('_id') for i in id2]
        id20=collection.find({'componentID':'CO_3_7_2','name':'输入轴径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
        id2.remove(id20)

    condition1={'_id':id1}
    condition2={'_id':id2}

    para_part1={'$set':{'hardpara.测试硬件参数1':float(para1),
                        'hardpara.测试硬件参数2':float(para2),
                        'hardpara.测试硬件参数3':float(para3),
                        'hardpara.测试硬件参数4': float(para4),
                        'hardpara.输入转速':float(para5)}}

    if float(para1)==0:
        p1="D不能为0！"
        print(p1)
    else:
        p1='p1'
        if group == '3' and machine == '7':
            collection.update_many(condition1,para_part1)
            collection.update_many(condition2,para_part1)
        else:
            [collection.update_many({'_id': i}, para_part1) for i in condition1['_id']]
            [collection.update_many({'_id': i}, para_part1) for i in condition2['_id']]

    result= {}
    result["p1"]=p1

    # ----------------------- 以下为更新或插入 model_data -----------------------
    collection1=db['model_data']
    model_number = para0
    data_to_check = {'型号': model_number,'参数5':'一级行星齿圈'}

    existing_data = collection1.find_one(data_to_check)
    if existing_data:
        print(f"Data with model number '{model_number}' already exists. Updating existing data.")
        if group == '3':
            data_to_update = {
                '参数1': para1,
                '参数2': para2,
                '参数3': para3,
                '参数4': para4,
                '传动系数': para6,
                '传动系数2': para7,
                '传动系数3': para8,
                '压缩机类型': 'MySE10-242'
            }
        else:
            data_to_update = {
                '参数1': para1,
                '参数2': para2,
                '参数3': para3,
                '参数4': para4,
                '传动系数': para6,
                '传动系数2': para7,
                '传动系数3': para8,
                '压缩机类型': 'MySE8.5-230'
            }
        collection1.update_one(data_to_check, {'$set': data_to_update})
    else:
        if group == '3':
            data_to_insert = {
                '型号': para0,
                '参数1': para1,
                '参数2': para2,
                '参数3': para3,
                '参数4': para4,
                '传动系数': para6,
                '传动系数2': para7,
                '传动系数3': para8,
                '参数5': '一级行星齿圈',
                '压缩机类型': 'MySE10-242'
            }
        else:
            data_to_insert = {
                '型号': para0,
                '参数1': para1,
                '参数2': para2,
                '参数3': para3,
                '参数4': para4,
                '传动系数': para6,
                '传动系数2': para7,
                '传动系数3': para8,
                '参数5': '一级行星齿圈',
                '压缩机类型': 'MySE8.5-230'
            }
        collection_new= collection1.insert_one(data_to_insert)
        print(f"Data inserted with ID: {collection_new.inserted_id}")
    return result


def gear03(para0,para1,para2,para3,para4,para5, para6, para7, para8, group,machine):

    db = get_db()
    collection=db['sensor_data']
    if group=='3' and machine=='7':
        id1=collection.find({'componentID':'CO_'+group+'_'+machine+'_2','name':'二级行星齿圈径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
    else:
        id1 = collection.find({'name': '二级行星齿圈径向'}, {'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)])
        id1 = [i.get('_id') for i in id1]
        id10 = collection.find({'componentID': 'CO_3_7_2', 'name': '二级行星齿圈径向'},
                               {'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('_id')
        id1.remove(id10)

    condition1={'_id':id1}

    para_part1={'$set':{'hardpara.测试硬件参数1':float(para1),
                        'hardpara.测试硬件参数2':float(para2),
                        'hardpara.测试硬件参数3':float(para3),
                        'hardpara.测试硬件参数4': float(para4),
                        'hardpara.输入转速':float(para5)}}

    if float(para1)==0:
        p1="D不能为0！"
        print(p1)
    else:
        p1='p1'
        if group == '3' and machine == '7':
            collection.update_many(condition1, para_part1)
        else:
            [collection.update_many({'_id': i}, para_part1) for i in condition1['_id']]

    result= {}
    result["p1"]=p1

    # ----------------------- 以下为更新或插入 model_data -----------------------
    collection1=db['model_data']
    model_number = para0
    data_to_check = {'型号': model_number,'参数5':'二级行星齿圈'}

    existing_data = collection1.find_one(data_to_check)
    if existing_data:
        print(f"Data with model number '{model_number}' already exists. Updating existing data.")
        if group == '3':
            data_to_update = {
                '参数1': para1,
                '参数2': para2,
                '参数3': para3,
                '参数4': para4,
                '传动系数': para6,
                '传动系数2': para7,
                '传动系数3': para8,
                '压缩机类型': 'MySE10-242'
            }
        else:
            data_to_update = {
                '参数1': para1,
                '参数2': para2,
                '参数3': para3,
                '参数4': para4,
                '传动系数': para6,
                '传动系数2': para7,
                '传动系数3': para8,
                '压缩机类型': 'MySE8.5-230'
            }
        collection1.update_one(data_to_check, {'$set': data_to_update})
    else:
        if group == '3':
            data_to_insert = {
                '型号': para0,
                '参数1': para1,
                '参数2': para2,
                '参数3': para3,
                '参数4': para4,
                '传动系数': para6,
                '传动系数2': para7,
                '传动系数3': para8,
                '参数5': '二级行星齿圈',
                '压缩机类型': 'MySE10-242'
            }
        else:
            data_to_insert = {
                '型号': para0,
                '参数1': para1,
                '参数2': para2,
                '参数3': para3,
                '参数4': para4,
                '传动系数': para6,
                '传动系数2': para7,
                '传动系数3': para8,
                '参数5': '二级行星齿圈',
                '压缩机类型': 'MySE8.5-230'
            }

        collection_new= collection1.insert_one(data_to_insert)
        print(f"Data inserted with ID: {collection_new.inserted_id}")
    return result

def gear4(para0,para1,para2,para5,para7, para8, group,machine):
    db = get_db()
    collection=db['sensor_data']
    if group == '3' and machine == '7':
        id1 = collection.find({'componentID': 'CO_' + group + '_' + machine + '_2', 'name': '二级行星齿圈径向'},
                              {'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('_id')

    else:
        id1 = collection.find({'name': '二级行星齿圈径向'}, {'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)])
        id1 = [i.get('_id') for i in id1]
        id10 = collection.find({'componentID': 'CO_3_7_2', 'name': '二级行星齿圈径向'},
                               {'_id': 1, 'componentID': 1, 'hardpara': 1}).sort([('_id', -1)]).limit(1)[0].get('_id')
        id1.remove(id10)

    condition1 = {'_id': id1}

    para_part1 = {'$set': {'hardpara.测试硬件参数1': float(para1),
                           'hardpara.测试硬件参数2': float(para2),
                           'hardpara.输入转速': float(para5)}}

    if float(para1) == 0:
        p1 = "D不能为0！"
        print(p1)
    else:
        p1 = 'p1'
        if group == '3' and machine == '7':
            collection.update_many(condition1, para_part1)
        else:
            [collection.update_many({'_id': i}, para_part1) for i in condition1['_id']]

    result= {}
    result["p1"]=p1

    # ----------------------- 以下为更新或插入 model_data -----------------------
    collection1=db['model_data']
    model_number = para0
    data_to_check = {'型号': model_number,'参数5':'齿轮箱高速轴齿轮'}

    existing_data = collection1.find_one(data_to_check)
    if existing_data:
        print(f"Data with model number '{model_number}' already exists. Updating existing data.")
        if group=='3':
            data_to_update = {
                '参数1': para1,
                '参数2': para2,
                '传动系数2': para7,
                '传动系数3': para8,
                '压缩机类型': 'MySE10-242'
            }
        else:
            data_to_update = {
                '参数1': para1,
                '参数2': para2,
                '传动系数2': para7,
                '传动系数3': para8,
                '压缩机类型': 'MySE8.5-230'
            }
        collection1.update_one(data_to_check, {'$set': data_to_update})
    else:
        if group=='3':
            data_to_insert = {
                '型号': para0,
                '参数1':  para1,
                '参数2':  para2,
                '传动系数2': para7,
                '传动系数3': para8,
                '参数5': '齿轮箱高速轴齿轮',
                '压缩机类型': 'MySE10-242'
            }
        else:
            data_to_insert = {
                '型号': para0,
                '参数1':  para1,
                '参数2':  para2,
                '传动系数2': para7,
                '传动系数3': para8,
                '参数5': '齿轮箱高速轴齿轮',
                '压缩机类型': 'MySE8.5-230'
            }
        collection_new= collection1.insert_one(data_to_insert)
        print(f"Data inserted with ID: {collection_new.inserted_id}")
    return result


def gear5(para0,para1,para2,para3,para4,para5, para6, group,machine):
    client = get_client()
    db=client['yueyangfan']
    collection=db['sensor_data']
    if group=='3' and machine=='7':
        id=collection.find({'componentID':'CO_'+group+'_'+machine+'_3','name':'驱动端径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
    else:
        id=collection.find({'name':'驱动端径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)])
        id=[i.get('_id') for i in id]
        id0=collection.find({'componentID':'CO_3_7_3','name':'驱动端径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
        id.remove(id0)
    condition1={'_id':id}
    para_part1={'$set':{'hardpara.测试硬件参数1':float(para1),
                        'hardpara.测试硬件参数2':float(para2),
                        'hardpara.测试硬件参数3':float(para3),
                        'hardpara.测试硬件参数4': float(para4),
                        'hardpara.输入转速':float(para5)}}

    if float(para1)==0:
        p1="D不能为0！"
        print(p1)
    elif float(para1)<float(para2):
        p1='D<d!'
        print(p1)
    else:
        p1='p1'
        if group == '3' and machine == '7':
            collection.update_many(condition1,para_part1)
        else:
            [collection.update_many({'_id': i}, para_part1) for i in condition1['_id']]

    result= {}
    result["p1"]=p1

    # ----------------------- 以下为更新或插入 model_data -----------------------
    collection1=db['model_data']
    model_number = para0
    data_to_check = {'型号': model_number,'参数5':'发电机驱动端轴承'}

    existing_data = collection1.find_one(data_to_check)
    if existing_data:
        print(f"Data with model number '{model_number}' already exists. Updating existing data.")
        if group=='3':
            data_to_update = {
                '参数1':  para1,
                '参数2':  para2,
                '参数3':  para3,
                '参数4':  para4,
                '传动系数': para6,
                '压缩机类型':'MySE10-242'
            }
        else:
            data_to_update = {
                '参数1':  para1,
                '参数2':  para2,
                '参数3':  para3,
                '参数4':  para4,
                '传动系数': para6,
                '压缩机类型':'MySE8.5-230'
            }
        collection1.update_one(data_to_check, {'$set': data_to_update})
    else:
        if group=='3':
            data_to_insert = {
                '型号': para0,
                '参数1':  para1,
                '参数2':  para2,
                '参数3':  para3,
                '参数4':  para4,
                '传动系数': para6,
                '参数5': '发电机驱动端轴承',
                '压缩机类型':'MySE10-242'
            }
        else:
            data_to_insert = {
                '型号': para0,
                '参数1':  para1,
                '参数2':  para2,
                '参数3':  para3,
                '参数4':  para4,
                '传动系数': para6,
                '参数5': '发电机驱动端轴承',
                '压缩机类型':'MySE8.5-230'
            }
        collection_new= collection1.insert_one(data_to_insert)
        print(f"Data inserted with ID: {collection_new.inserted_id}")
    return result


def gear6(para0,para1,para2,para3,para4,para5, para6, group,machine):
    client = get_client()
    db=client['yueyangfan']
    collection=db['sensor_data']
    if group=='3' and machine=='7':
        id=collection.find({'componentID':'CO_'+group+'_'+machine+'_3','name':'自由端径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
    else:
        id=collection.find({'name':'自由端径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)])
        id=[i.get('_id') for i in id]
        id0=collection.find({'componentID':'CO_3_7_3','name':'自由端径向'},{'_id':1,'componentID':1,'hardpara':1}).sort([('_id',-1)]).limit(1)[0].get('_id')
        id.remove(id0)
    condition1={'_id':id}
    para_part1={'$set':{'hardpara.测试硬件参数1':float(para1),
                        'hardpara.测试硬件参数2':float(para2),
                        'hardpara.测试硬件参数3':float(para3),
                        'hardpara.测试硬件参数4': float(para4),
                        'hardpara.输入转速':float(para5)}}

    if float(para1)==0:
        p1="D不能为0！"
        print(p1)
    elif float(para1)<float(para2):
        p1='D<d!'
        print(p1)
    else:
        p1='p1'
        if group == '3' and machine == '7':
            collection.update_many(condition1,para_part1)
        else:
            [collection.update_many({'_id': i}, para_part1) for i in condition1['_id']]

    result= {}
    result["p1"]=p1

    # ----------------------- 以下为更新或插入 model_data -----------------------
    collection1=db['model_data']
    model_number = para0
    data_to_check = {'型号': model_number,'参数5':'发电机自由端轴承'}

    existing_data = collection1.find_one(data_to_check)
    if existing_data:
        print(f"Data with model number '{model_number}' already exists. Updating existing data.")
        if group=='3':
            data_to_update = {
                '参数1':  para1,
                '参数2':  para2,
                '参数3':  para3,
                '参数4':  para4,
                '传动系数': para6,
                '压缩机类型':'MySE10-242'
            }
        else:
            data_to_update = {
                '参数1':  para1,
                '参数2':  para2,
                '参数3':  para3,
                '参数4':  para4,
                '传动系数': para6,
                '压缩机类型':'MySE8.5-230'
            }
        collection1.update_one(data_to_check, {'$set': data_to_update})
    else:
        if group=='3':
            data_to_insert = {
                '型号': para0,
                '参数1':  para1,
                '参数2':  para2,
                '参数3':  para3,
                '参数4':  para4,
                '传动系数': para6,
                '参数5': '发电机自由端轴承',
                '压缩机类型':'MySE10-242'
            }
        else:
            data_to_insert = {
                '型号': para0,
                '参数1':  para1,
                '参数2':  para2,
                '参数3':  para3,
                '参数4':  para4,
                '传动系数': para6,
                '参数5': '发电机自由端轴承',
                '压缩机类型':'MySE8.5-230'
            }
        collection_new= collection1.insert_one(data_to_insert)
        print(f"Data inserted with ID: {collection_new.inserted_id}")
    return result

def find_model(p0,location):
    client = get_client()
    db = client['yueyangfan']
    collection = db['model_data']
    collection_name = 'model_data'
    model_number = p0
    data_to_check = {'型号': model_number,'参数5':location}
    if location=='齿轮箱高速轴齿轮':
        result = {}
        existing_data = collection.find_one(data_to_check)
        result["p0"] = '该型号已存在！将自动填充数据'
        result["p1"] = existing_data['参数1']
        result["p2"] = existing_data['参数2']
        result['p6']=existing_data['传动系数']
        result['p7']=existing_data['传动系数2']
        result['p8']=existing_data['传动系数3']
    else:
        result = {}
        existing_data = collection.find_one(data_to_check)
        result["p0"] = '该型号已存在！将自动填充数据'
        result["p1"] = existing_data['参数1']
        result["p2"] = existing_data['参数2']
        result["p3"] = existing_data['参数3']
        result["p4"] = existing_data['参数4']
        result['p6']=existing_data['传动系数']
        result['p7']=existing_data['传动系数2']
        result['p8']=existing_data['传动系数3']
    return result

def check_model(p0):
    client = get_client()
    db=client['yueyangfan']
    collection=db['model_data']
    collection_name='model_data'
    if not collection_name in db.list_collection_names():
        print(f"Collection '{collection_name}' does not exist. Creating it.")
        db.create_collection(collection_name)

    model_number = p0
    data_to_check = {'型号': model_number}
    result= {}
    existing_data = collection.find_one(data_to_check)

    if existing_data:
        result["p0"] ='该型号已存在！将自动填充数据'
        result["p1"] =existing_data['参数1']
        result["p2"] =existing_data['参数2']
        result["p3"] =existing_data['参数3']
        result["p4"] =existing_data['参数4']
        result['p7']=existing_data['传动系数2']
        result['p8']=existing_data['传动系数3']
    else:
        result["p0"]='该型号不存在，请手动填充数据！'
    return result

def inforamtionx(group,machine):
    db = get_db()
    collection_group=db['group_data']
    group_name = list(collection_group.find({'groupID': 'GR_' + str(group)}, {'name': 1}))

    collection_machine=db['machine_data']
    machine_name = list(collection_machine.find({'machineID': 'MA_'+ str(group) + '_' + str(machine)}, {'name': 1}))
    result={}
    group_name = group_name[0]['name']
    machine_name = machine_name[0]['name']
    result['group_name']=group_name
    result['machine_name']=machine_name
    return result


# if __name__=='__main__':
#     import_machine_para()
