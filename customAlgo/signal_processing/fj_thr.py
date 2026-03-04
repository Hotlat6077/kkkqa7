
import numpy as np
import datetime
import statistics

from mydb.get_mongo import get_db


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


def get_thr(model, group, machine, component, sensor):
    """
    获取阈值数据。如果不存在对应的文档，则打印缺失信息并插入默认阈值文档。
    """
    db = get_db()
    collectiont = db['threshold_data']
    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)

    query = {
        'machine': machine,
        'group': group,
        'component': component,
        'sensor': sensor,
        'model': model
    }
    projection = {'thr': 1}
    cursor = collectiont.find(query, projection)
    data = list(cursor)  # 将游标转换为列表

    if not data:
        # 打印缺失的模型信息
        print(f"缺少阈值文档: model={model}, group={group}, machine={machine}, component={component}, sensor={sensor}")

        # 定义默认阈值，根据不同的model设置不同的默认值
        default_thr = {}
        if model in ['std', 'rms', 'kur', 'peak', 'speed_rms', 'impulse']:
            default_thr = {
                'thr': {
                    'warning': 1.0,  # 这里设置你需要的默认值
                    'fault': 3.0,
                    'update_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        elif model == 'fault':
            default_thr = {
                'thr': {
                    'outer': 1.0,
                    'inner': 1.0,
                    'ball': 1.0,
                    'sun': 1.0,
                    'planet': 1.0,
                    'race': 1.0,
                    'update_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        else:
            print(f"未知的model类型: {model}")
            
            return None  # 或者你可以选择抛出异常

        # 插入默认阈值文档
        try:
            collectiont.insert_one({
                'machine': machine,
                'group': group,
                'component': component,
                'sensor': sensor,
                'model': model,
                **default_thr
            })
            print(
                f"已插入默认阈值文档: model={model}, group={group}, machine={machine}, component={component}, sensor={sensor}")
            data = [default_thr]  # 使用默认值
        except Exception as e:
            print(f"插入默认阈值文档时出错: {e}")
            
            return None  # 或者你可以选择抛出异常

    

    if data:
        return data[0]
    else:
        return None  # 或者你可以选择抛出异常


def update_thr(para_dict: dict):
    db = get_db()
    collection = db['threshold_data']
    para_dict['update_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    collection.update_one({'_id': para_dict['_id']}, {'$set': para_dict})



def set_thr(model, group, machine, component, sensor, thres0, thres1):
    thr = get_thr(model=model, group=int(group), machine=int(machine), component=int(component), sensor=int(sensor))
    if thr is None:
        print(
            f"无法设置阈值，因为缺少阈值文档: model={model}, group={group}, machine={machine}, component={component}, sensor={sensor}")
        return
    thr['thr']['warning'] = float(thres0)
    thr['thr']['fault'] = float(thres1)
    thr['thr']['update_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_thr(thr)


def set_thr2(model, group, machine, component, sensor, thres0, thres1, thres2):
    thr = get_thr(model=model, group=int(group), machine=int(machine), component=int(component), sensor=int(sensor))
    if thr is None:
        print(
            f"无法设置阈值，因为缺少阈值文档: model={model}, group={group}, machine={machine}, component={component}, sensor={sensor}")
        return
    thr['thr']['outer'] = float(thres0)
    thr['thr']['inner'] = float(thres1)
    thr['thr']['ball'] = float(thres2)
    thr['thr']['update_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_thr(thr)


def set_thr3(model, group, machine, component, sensor, thres0, thres1, thres2):
    thr = get_thr(model=model, group=int(group), machine=int(machine), component=int(component), sensor=int(sensor))
    if thr is None:
        print(
            f"无法设置阈值，因为缺少阈值文档: model={model}, group={group}, machine={machine}, component={component}, sensor={sensor}")
        return
    thr['thr']['sun'] = float(thres0)
    thr['thr']['planet'] = float(thres1)
    thr['thr']['race'] = float(thres2)
    thr['thr']['update_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_thr(thr)


def Thres_inds1(group, machine, component, sensor, thres0, thres1):
    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)
    model = 'std'
    set_thr(model, group, machine, component, sensor, thres0, thres1)
    return {}


def Thres_inds2(group, machine, component, sensor, thres0, thres1):
    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)
    model = 'rms'
    set_thr(model, group, machine, component, sensor, thres0, thres1)
    return {}


def Thres_inds3(group, machine, component, sensor, thres0, thres1):
    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)
    model = 'kur'
    set_thr(model, group, machine, component, sensor, thres0, thres1)
    return {}


def Thres_inds4(group, machine, component, sensor, thres0, thres1, thres2):
    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)
    model = 'fault'
    set_thr2(model, group, machine, component, sensor, thres0, thres1, thres2)
    return {}


def Thres_inds5(group, machine, component, sensor, thres0, thres1, thres2):
    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)
    model = 'fault'
    set_thr3(model, group, machine, component, sensor, thres0, thres1, thres2)
    return {}


# 自动阈值设置函数
def Thres_auto1(group, machine, component, sensor):
    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)
    db = get_db()
    model = 'std'
    collection_thr = db[f'indicator_data_{group}_{machine}']
    signal1 = []
    collectiont = db['system_config']
    thr_starttime = list(collectiont.find({}, {'thr_starttime': 1}))
    thr_endtime = list(collectiont.find({}, {'thr_endtime': 1}))
    thr_starttime_value = thr_starttime[0]['thr_starttime']
    thr_endtime_value = thr_endtime[0]['thr_endtime']
    # print(thr_starttime_value, thr_endtime_value)
    result_list1 = list(collection_thr.find({
        "$and": [
            {"datetime": {"$gte": str(thr_starttime_value), "$lte": str(thr_endtime_value)}},
            {'component': component, 'sensor': sensor}
        ]
    }, {'std': 1}))
    for i in range(len(result_list1)):
        signal1.append(result_list1[i].get('std'))
    signal1 = [item for sublist in signal1 for item in sublist]
    if len(signal1) == 0:
        print(
            f"没有找到数据用于自动设置阈值: group={group}, machine={machine}, component={component}, sensor={sensor}, model={model}")

        return {}
    auto_thr3 = sum(signal1) / len(signal1)
    auto_thrx = np.array(auto_thr3)
    auto_thrx = auto_thrx * 5
    auto_thrx = np.round(auto_thrx, 1)
    thres0 = auto_thrx
    thres1 = auto_thrx * 3
    set_thr(model, group, machine, component, sensor, thres0, thres1)
    
    return {}


def Thres_auto2(group, machine, component, sensor):
    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)
    db = get_db()
    model = 'rms'
    collection_thr = db[f'indicator_data_{group}_{machine}']
    signal1 = []
    collectiont = db['system_config']
    thr_starttime = list(collectiont.find({}, {'thr_starttime': 1}))
    thr_endtime = list(collectiont.find({}, {'thr_endtime': 1}))
    thr_starttime_value = thr_starttime[0]['thr_starttime']
    thr_endtime_value = thr_endtime[0]['thr_endtime']
    # print(thr_starttime_value, thr_endtime_value)
    result_list1 = list(collection_thr.find({
        "$and": [
            {"datetime": {"$gte": str(thr_starttime_value), "$lte": str(thr_endtime_value)}},
            {'component': component, 'sensor': sensor}
        ]
    }, {'rms': 1}))
    for i in range(len(result_list1)):
        signal1.append(result_list1[i].get('rms'))
    signal1 = [item for sublist in signal1 for item in sublist]
    if len(signal1) == 0:
        print(
            f"没有找到数据用于自动设置阈值: group={group}, machine={machine}, component={component}, sensor={sensor}, model={model}")

        return {}
    auto_thr3 = sum(signal1) / len(signal1)
    auto_thrx = np.array(auto_thr3)
    auto_thrx = auto_thrx * 5
    auto_thrx = np.round(auto_thrx, 1)
    thres0 = auto_thrx
    thres1 = auto_thrx * 3
    set_thr(model, group, machine, component, sensor, thres0, thres1)

    return {}


def Thres_auto3(group, machine, component, sensor):
    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)
    db = get_db()
    model = 'kur'
    collection_thr = db[f'indicator_data_{group}_{machine}']
    signal1 = []
    collectiont = db['system_config']
    thr_starttime = list(collectiont.find({}, {'thr_starttime': 1}))
    thr_endtime = list(collectiont.find({}, {'thr_endtime': 1}))
    thr_starttime_value = thr_starttime[0]['thr_starttime']
    thr_endtime_value = thr_endtime[0]['thr_endtime']
    # print(thr_starttime_value, thr_endtime_value)
    result_list1 = list(collection_thr.find({
        "$and": [
            {"datetime": {"$gte": str(thr_starttime_value), "$lte": str(thr_endtime_value)}},
            {'component': component, 'sensor': sensor}
        ]
    }, {'kur': 1}))
    for i in range(len(result_list1)):
        signal1.append(result_list1[i].get('kur'))
    signal1 = [item for sublist in signal1 for item in sublist]
    if len(signal1) == 0:
        print(
            f"没有找到数据用于自动设置阈值: group={group}, machine={machine}, component={component}, sensor={sensor}, model={model}")

        return {}
    auto_thr3 = sum(signal1) / len(signal1)
    auto_thrx = np.array(auto_thr3)
    auto_thrx = auto_thrx * 5
    auto_thrx = np.round(auto_thrx, 1)
    thres0 = auto_thrx
    thres1 = auto_thrx * 3
    set_thr(model, group, machine, component, sensor, thres0, thres1)

    return {}


def Thres_auto4(group, machine, component, sensor):
    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)
    db = get_db()
    model = 'fault'
    collection_thr = db[f'indicator_data_{group}_{machine}']
    signal1 = []
    collectiont = db['system_config']
    thr_starttime = list(collectiont.find({}, {'thr_starttime': 1}))
    thr_endtime = list(collectiont.find({}, {'thr_endtime': 1}))
    thr_starttime_value = thr_starttime[0]['thr_starttime']
    thr_endtime_value = thr_endtime[0]['thr_endtime']
    # print(thr_starttime_value, thr_endtime_value)
    result_list1 = list(collection_thr.find({
        "$and": [
            {"datetime": {"$gte": str(thr_starttime_value), "$lte": str(thr_endtime_value)}},
            {'component': component, 'sensor': sensor}
        ]
    }, {'fault': 1}))
    for i in range(len(result_list1)):
        signal1.append(result_list1[i].get('fault'))
    signal1 = [item for sublist in signal1 for item in sublist]
    if len(signal1) == 0:
        print(
            f"没有找到数据用于自动设置阈值: group={group}, machine={machine}, component={component}, sensor={sensor}, model={model}")

        return {}
    auto_thr3 = sum(signal1) / len(signal1)
    auto_thrx = np.array(auto_thr3)
    auto_thrx = auto_thrx * 5
    auto_thrx = np.round(auto_thrx, 1)
    thres0 = auto_thrx
    thres1 = auto_thrx * 3
    set_thr2(model, group, machine, component, sensor, thres0, thres1)

    return {}


def Thres_auto5(group, machine, component, sensor):
    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)
    db = get_db()
    model = 'fault'
    collection_thr = db[f'indicator_data_{group}_{machine}']
    signal1 = []
    collectiont = db['system_config']
    thr_starttime = list(collectiont.find({}, {'thr_starttime': 1}))
    thr_endtime = list(collectiont.find({}, {'thr_endtime': 1}))
    thr_starttime_value = thr_starttime[0]['thr_starttime']
    thr_endtime_value = thr_endtime[0]['thr_endtime']
    # print(thr_starttime_value, thr_endtime_value)
    result_list1 = list(collection_thr.find({
        "$and": [
            {"datetime": {"$gte": str(thr_starttime_value), "$lte": str(thr_endtime_value)}},
            {'component': component, 'sensor': sensor}
        ]
    }, {'fault': 1}))
    for i in range(len(result_list1)):
        signal1.append(result_list1[i].get('fault'))
    signal1 = [item for sublist in signal1 for item in sublist]
    if len(signal1) == 0:
        print(
            f"没有找到数据用于自动设置阈值: group={group}, machine={machine}, component={component}, sensor={sensor}, model={model}")

        return {}
    auto_thr3 = sum(signal1) / len(signal1)
    auto_thrx = np.array(auto_thr3)
    auto_thrx = auto_thrx * 5
    auto_thrx = np.round(auto_thrx, 1)
    thres0 = auto_thrx
    thres1 = auto_thrx * 3
    set_thr3(model, group, machine, component, sensor, thres0, thres1)

    return {}


def Thres_auto6(group, machine, component, sensor):
    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)
    db = get_db()
    model1 = 'std'
    model2 = 'rms'
    model3 = 'kur'
    collection_thr = db[f'indicator_data_{group}_{machine}']
    signal1 = []
    collectiont = db['system_config']
    thr_starttime = list(collectiont.find({}, {'thr_starttime': 1}))
    thr_endtime = list(collectiont.find({}, {'thr_endtime': 1}))
    thr_starttime_value = thr_starttime[0]['thr_starttime']
    thr_endtime_value = thr_endtime[0]['thr_endtime']

    collection_rawthr = db['threshold_data']

    # std
    std_raw_thr = list(collection_rawthr.find({'machine': machine, 'group': group, 'model': 'std'}, {'thr': 1}))
    if not std_raw_thr:
        print(f"缺少std阈值文档: machine={machine}, group={group}")
        
        return {}
    warning_values = [item['thr']['warning'] for item in std_raw_thr]
    number = len(warning_values)
    result_list1 = list(collection_thr.find({
        "$and": [
            {"datetime": {"$gte": str(thr_starttime_value), "$lte": str(thr_endtime_value)}}
        ]
    }, {'std': 1}))
    std_values = [item['std'][0] for item in result_list1 if 'std' in item]
    if not std_values:
        print(
            f"没有找到std数据用于自动设置阈值: group={group}, machine={machine}, component={component}, sensor={sensor}")

        return {}
    std_sublists = [std_values[i:i + number] for i in range(0, len(std_values), number)]
    std_averages = [statistics.mean(values) for values in zip(*std_sublists)]
    std_averages1 = [x * 5 for x in std_averages]
    std_averages2 = [x * 15 for x in std_averages]
    # 遍历std_raw_thr并替换warning值，然后更新到数据库
    for i, document in enumerate(std_raw_thr):
        if i < len(std_averages1):
            document['thr']['warning'] = std_averages1[i]
            document['thr']['fault'] = std_averages2[i]
            # 更新数据库中的文档
            collection_rawthr.update_one(
                {'_id': document['_id']},
                {'$set': {'thr.warning': document['thr']['warning'], 'thr.fault': document['thr']['fault']}}
            )
            print(
                f"更新std阈值文档: _id={document['_id']}, warning={document['thr']['warning']}, fault={document['thr']['fault']}")

    # rms
    rms_raw_thr = list(collection_rawthr.find({'machine': machine, 'group': group, 'model': 'rms'}, {'thr': 1}))
    if not rms_raw_thr:
        print(f"缺少rms阈值文档: machine={machine}, group={group}")

        return {}
    warning_values = [item['thr']['warning'] for item in rms_raw_thr]
    number = len(warning_values)
    result_list2 = list(collection_thr.find({
        "$and": [
            {"datetime": {"$gte": str(thr_starttime_value), "$lte": str(thr_endtime_value)}}
        ]
    }, {'rms': 1}))
    rms_values = [item['rms'][0] for item in result_list2 if 'rms' in item]
    if not rms_values:
        print(
            f"没有找到rms数据用于自动设置阈值: group={group}, machine={machine}, component={component}, sensor={sensor}")

        return {}
    rms_sublists = [rms_values[i:i + number] for i in range(0, len(rms_values), number)]
    rms_averages = [statistics.mean(values) for values in zip(*rms_sublists)]
    rms_averages1 = [x * 5 for x in rms_averages]
    rms_averages2 = [x * 15 for x in rms_averages]
    # 遍历rms_raw_thr并替换warning值，然后更新到数据库
    for i, document in enumerate(rms_raw_thr):
        if i < len(rms_averages1):
            document['thr']['warning'] = rms_averages1[i]
            document['thr']['fault'] = rms_averages2[i]
            # 更新数据库中的文档
            collection_rawthr.update_one(
                {'_id': document['_id']},
                {'$set': {'thr.warning': document['thr']['warning'], 'thr.fault': document['thr']['fault']}}
            )
            print(
                f"更新rms阈值文档: _id={document['_id']}, warning={document['thr']['warning']}, fault={document['thr']['fault']}")

    # kur
    kur_raw_thr = list(collection_rawthr.find({'machine': machine, 'group': group, 'model': 'kur'}, {'thr': 1}))
    if not kur_raw_thr:
        print(f"缺少kur阈值文档: machine={machine}, group={group}")

        return {}
    warning_values = [item['thr']['warning'] for item in kur_raw_thr]
    number = len(warning_values)
    result_list3 = list(collection_thr.find({
        "$and": [
            {"datetime": {"$gte": str(thr_starttime_value), "$lte": str(thr_endtime_value)}}
        ]
    }, {'kur': 1}))
    kur_values = [item['kur'][0] for item in result_list3 if 'kur' in item]
    if not kur_values:
        print(
            f"没有找到kur数据用于自动设置阈值: group={group}, machine={machine}, component={component}, sensor={sensor}")

        return {}
    kur_sublists = [kur_values[i:i + number] for i in range(0, len(kur_values), number)]
    kur_averages = [statistics.mean(values) for values in zip(*kur_sublists)]
    kur_averages1 = [x * 5 for x in kur_averages]
    kur_averages2 = [x * 15 for x in kur_averages]
    # 遍历kur_raw_thr并替换warning值，然后更新到数据库
    for i, document in enumerate(kur_raw_thr):
        if i < len(kur_averages1):
            document['thr']['warning'] = kur_averages1[i]
            document['thr']['fault'] = kur_averages2[i]
            # 更新数据库中的文档
            collection_rawthr.update_one(
                {'_id': document['_id']},
                {'$set': {'thr.warning': document['thr']['warning'], 'thr.fault': document['thr']['fault']}}
            )
            print(
                f"更新kur阈值文档: _id={document['_id']}, warning={document['thr']['warning']}, fault={document['thr']['fault']}")


    return {}


def Thres_show(group, machine, component, sensor):
    """
    显示当前阈值。
    """
    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)

    thr_std = get_thr(model='std', group=group, machine=machine, component=component, sensor=sensor)
    thr_rms = get_thr(model='rms', group=group, machine=machine, component=component, sensor=sensor)
    thr_kur = get_thr(model='kur', group=group, machine=machine, component=component, sensor=sensor)
    thr_fault1 = get_thr(model='fault', group=group, machine=machine, component=component, sensor=sensor)
    thr_fault2 = get_thr(model='fault', group=group, machine=machine, component=4 - component, sensor=sensor)
    # peak  speed_rms   impulse
    thr_peak = get_thr(model='peak', group=group, machine=machine, component=component, sensor=sensor)
    thr_speed_rms = get_thr(model='speed_rms', group=group, machine=machine, component=component, sensor=sensor)
    thr_impulse_kur = get_thr(model='impulse', group=group, machine=machine, component=component, sensor=sensor)

    result = {}
    if thr_std and 'thr' in thr_std:
        result['std1'] = round(thr_std['thr'].get('warning', 0), 2)
        result['std2'] = round(thr_std['thr'].get('fault', 0), 2)
    else:
        result['std1'] = 0
        result['std2'] = 0
        print(f"std阈值未找到或缺失: group={group}, machine={machine}, component={component}, sensor={sensor}")

    if thr_rms and 'thr' in thr_rms:
        result['rms1'] = round(thr_rms['thr'].get('warning', 0), 2)
        result['rms2'] = round(thr_rms['thr'].get('fault', 0), 2)
    else:
        result['rms1'] = 0
        result['rms2'] = 0
        print(f"rms阈值未找到或缺失: group={group}, machine={machine}, component={component}, sensor={sensor}")

    if thr_kur and 'thr' in thr_kur:
        result['kur1'] = round(thr_kur['thr'].get('warning', 0), 2)
        result['kur2'] = round(thr_kur['thr'].get('fault', 0), 2)
    else:
        result['kur1'] = 0
        result['kur2'] = 0
        print(f"kur阈值未找到或缺失: group={group}, machine={machine}, component={component}, sensor={sensor}")

    if thr_peak and 'thr' in thr_peak:
        result['peak1'] = round(thr_peak['thr'].get('warning', 0), 2)
        result['peak2'] = round(thr_peak['thr'].get('fault', 0), 2)
    else:
        result['peak1'] = 0
        result['peak2'] = 0
        print(f"peak阈值未找到或缺失: group={group}, machine={machine}, component={component}, sensor={sensor}")

    if thr_speed_rms and 'thr' in thr_speed_rms:
        result['speed_rms1'] = round(thr_speed_rms['thr'].get('warning', 0), 2)
        result['speed_rms2'] = round(thr_speed_rms['thr'].get('fault', 0), 2)
    else:
        result['speed_rms1'] = 0
        result['speed_rms2'] = 0
        print(f"speed_rms阈值未找到或缺失: group={group}, machine={machine}, component={component}, sensor={sensor}")

    if thr_impulse_kur and 'thr' in thr_impulse_kur:
        result['impulse_kur1'] = round(thr_impulse_kur['thr'].get('warning', 0), 2)
        result['impulse_kur2'] = round(thr_impulse_kur['thr'].get('fault', 0), 2)
    else:
        result['impulse_kur1'] = 0
        result['impulse_kur2'] = 0
        print(f"impulse_kur阈值未找到或缺失: group={group}, machine={machine}, component={component}, sensor={sensor}")

    if thr_fault1 and 'thr' in thr_fault1:
        result['bearing1'] = round(thr_fault1['thr'].get('outer', 0), 2)
        result['bearing2'] = round(thr_fault1['thr'].get('inner', 0), 2)
        result['bearing3'] = round(thr_fault1['thr'].get('ball', 0), 2)
    else:
        # 如果 'thr' 键不存在，赋予 'bearing1', 'bearing2', 'bearing3' 均为默认值（例如1）
        result['bearing1'] = 1
        result['bearing2'] = 1
        result['bearing3'] = 1
        print(
            f"fault阈值（bearing）未找到或缺失: group={group}, machine={machine}, component={component}, sensor={sensor}")

    if thr_fault2 and 'thr' in thr_fault2:
        result['gear1'] = round(thr_fault2['thr'].get('sun', 0), 2)
        result['gear2'] = round(thr_fault2['thr'].get('planet', 0), 2)
        result['gear3'] = round(thr_fault2['thr'].get('race', 0), 2)
    else:
        # 如果 'thr' 键不存在，赋予 'gear1', 'gear2', 'gear3' 均为默认值（例如1）
        result['gear1'] = 1
        result['gear2'] = 1
        result['gear3'] = 1
        print(f"fault阈值（gear）未找到或缺失: group={group}, machine={machine}, component={component}, sensor={sensor}")

    return result
