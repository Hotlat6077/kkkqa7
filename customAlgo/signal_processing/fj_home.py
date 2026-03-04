from __future__ import annotations

import numpy as np
from datetime import datetime

from api.device_tree.statistical import statistical_group_normal, statistical_machine_normal, \
    statistical_component_normal, statistical_sensor_normal
from mydb.get_mongo import get_db


def home_state( ):
    """
    获取系统状态统计信息

    主要统计项数据来源说明：
    1. 测点报警总数 (s1): 从event_data表获取，筛选条件为solving_flag=0（未解决）且event_level为报警级别
    2. 测点预警总数 (s11): 从event_data表获取，筛选条件为solving_flag=0（未解决）且event_level为预警级别
    3. 测点离线总数 (s111): 从event_data表获取，筛选条件为solving_flag=0（未解决）且event_level为offline

    event_data表字段说明：
    - event_level: 事件级别，如'alert'、'critical'、'high'为报警级别，'warning'、'medium'为预警级别，'offline'为离线
    - solving_flag: 解决标志，0表示未解决，1表示已解决
    - sensorID: 传感器ID，用于去重统计（同一传感器可能有多条未解决事件记录）

    其他统计项（氢机、压缩机、部件、测点的健康状态统计）仍从state_data表获取
    """
    db = get_db()
    collection1=db['indicator_data_1_1']
    all_time=list(collection1.find({},{'datetime':1}))
    if len(all_time) >= 1:
        first_datetime = all_time[0]['datetime']
        first_datetime = datetime.strptime(first_datetime, '%Y-%m-%d %H:%M:%S')
    else:
        first_datetime = datetime.now()

    current_datetime = datetime.now()
    time_difference = current_datetime - first_datetime
    days_difference = time_difference.days
##########################
    collection2 = db['group_data']
    group_data = collection2.count_documents({})
    collection3 = db['machine_data']
    machine_data = collection3.count_documents({})
    collection4 = db['component_data']
    component_data = collection4.count_documents({})
    collection5 = db['sensor_data']
    sensor_data = collection5.count_documents({})
##########################
    collection6=db['state_data']
    all_state = list(collection6.find({}, {'sensorID':1,'state': 1}))
    all_state=[[item['sensorID'], item['state']] for item in all_state]
    all_state = [[sensorID.replace('SE_', ''), state] for sensorID, state in all_state]

    # 从event_data表获取测点统计数据
    # 注意：以下统计均基于event_data表，筛选条件为solving_flag=0（未解决的事件）
    collection_event = db['event_data']

    # 获取未解决的报警事件（测点报警总数）
    # event_level包含: 'alert', 'critical', 'high' 等报警级别
    alarm_events = list(collection_event.find({
        'solving_flag': 0,  # 只统计未解决的事件
        'event_level': {'$in': ['alert', 'critical', 'high']}  # 报警级别
    }, {'sensorID': 1}))

    # 获取未解决的预警事件（测点预警总数）
    # event_level包含: 'warning', 'medium' 等预警级别
    warning_events = list(collection_event.find({
        'solving_flag': 0,  # 只统计未解决的事件
        'event_level': {'$in': ['warning', 'medium']}  # 预警级别
    }, {'sensorID': 1}))

    # 获取未解决的离线事件（测点离线总数）
    # event_level为: 'offline'
    offline_events = list(collection_event.find({
        'solving_flag': 0,  # 只统计未解决的事件
        'event_level': 'offline'  # 离线级别
    }, {'sensorID': 1}))

    # 去重统计：同一个传感器可能有多条未解决事件记录，只统计唯一传感器数量
    s1 = len(set([event['sensorID'] for event in alarm_events]))  # 测点报警总数
    s11 = len(set([event['sensorID'] for event in warning_events]))  # 测点预警总数
    s111 = len(set([event['sensorID'] for event in offline_events]))  # 测点离线总数

    # print(all_state)
#########################氢机情况统计
    gw1 = gw2 = gw3 = gw4 = 0
    has_two = False  # 用于记录是否存在第二个元素为2的情况
    for item in all_state:
        if item[1] == 2:
            has_two = True
            break  # 一旦找到第二个元素为2的情况，就停止遍历
    if not has_two:
        for item in all_state:
            if item[0][0] == '1' and item[1] == 1:
                gw1 = 1
            if item[0][0] == '2' and item[1] == 1:
                gw2 = 1
            if item[0][0] == '3' and item[1] == 1:
                gw3 = 1
            if item[0][0] == '4' and item[1] == 1:
                gw4 = 1
    gw = gw1 + gw2 + gw3 + gw4

    gf1=gf2=gf3=gf4 = 0
    for item in all_state:
        if item[0][0] == '1' and item[1] == 2:
            gf1 = 1
        if item[0][0] == '2' and item[1] == 2:
            gf2 = 1
        if item[0][0] == '3' and item[1] == 2:
            gf3 = 1
        if item[0][0] == '4' and item[1] == 2:
            gf4 = 1

    gf=gf1+gf2+gf3+gf4
    go = 0
    gh=4-gw-gf-go
######################报警机器统计
    mw = 0
    for i in range(0, len(all_state), 9):
        group1 = all_state[i:i + 9]
        # 检查每组中是否至少有一个子列表的第二个元素是1
        # 且没有任何一个子列表的第二个元素是2
        if any(item[1] == 1 for item in group1) and all(item[1] != 2 for item in group1):
            mw += 1
    mf=0
    for i in range(0, len(all_state), 9):
        group2 = all_state[i:i + 9]
        # 检查每组中是否至少有一个子列表的第二个元素是1
        if any(item[1] == 2 for item in group2):
            mf += 1
    mo=0
    mh=24-mw-mf-mo
    # print(mw,mf)
######################部件机器统计
    cw = 0
    for i in range(0, len(all_state), 9):
        block1 = all_state[i:i + 2]  # 第一个块，大小为2
        block2 = all_state[i + 2:i + 7]  # 第二个块，大小为5
        block3 = all_state[i + 7:i + 9]  # 第三个块，大小为2
        # 检查每个块中是否至少有一个子列表的第二个元素是1
        if any(item[1] == 1 for item in block1) or any(item[1] == 1 for item in block2) or any(
                item[1] == 1 for item in block3):
            cw += 1
    cf = 0
    for i in range(0, len(all_state), 9):
        block1 = all_state[i:i + 2]  # 第一个块，大小为2
        block2 = all_state[i + 2:i + 7]  # 第二个块，大小为5
        block3 = all_state[i + 7:i + 9]  # 第三个块，大小为2
        # 检查每个块中是否至少有一个子列表的第二个元素是1
        if any(item[1] == 2 for item in block1) or any(item[1] == 2 for item in block2) or any(
                item[1] == 2 for item in block3):
            cf += 1
    co = 0
    for i in range(0, len(all_state), 9):
        block1 = all_state[i:i + 2]  # 第一个块，大小为2
        block2 = all_state[i + 2:i + 7]  # 第二个块，大小为5
        block3 = all_state[i + 7:i + 9]  # 第三个块，大小为2
        # 检查每个块中是否至少有一个子列表的第二个元素是1
        if any(item[1] == 3 for item in block1) or any(item[1] == 3 for item in block2) or any(
                item[1] == 3 for item in block3):
            co += 1
    ch=72-cw-cf-co
    # print(ch,cw,cf,co)

  # 注意：s1（测点报警总数）、s11（测点预警总数）、s111（测点离线总数）已从event_data表获取
    # 原来从state_data表计算这些数值的代码已被替换为基于event_data的查询
    s2 = sensor_data - s1  # 计算非报警传感器数量（正常传感器数量）
########################
    # 用于存储统计结果的字典
    count_by_first_char = {}
    # 遍历数据列表
    for item in all_state:
        first_char = item[0][0]  # 第一个元素的第一个字符
        if first_char in count_by_first_char:
            count_by_first_char[first_char] += 1
        else:
            count_by_first_char[first_char] = 1
    # 只统计有实际计数的项
    middata1 = [count for char, count in count_by_first_char.items() if count > 0]

    # 初始化计数器
    count_by_first_char2 = {}
    # 遍历数据列表
    for item in all_state:
        if item[1] == 1:
            first_char2 = item[0][0]  # 取第一个字符
            if first_char2 in count_by_first_char2:
                count_by_first_char2[first_char2] += 1
            else:
                count_by_first_char2[first_char2] = 1
    middata2 = list(count_by_first_char.values())
    middata=[]

    for x, y in zip(middata1, middata2):
        middata.append((x - (s11+s1+s111)) / x)


    collection33=db['state_data']
    outline1=list(collection33.find({}, {'state': 1,'group':1}))

    #################################################
    group_counts = {1: 0, 2: 0, 3: 0, 4: 0}
    # 遍历数据列表，统计每个group的数量
    for item in outline1:
        if 'group' in item:
            group = item['group']
            if group in group_counts:
                group_counts[group] += 1
    # 将计数器转换为列表，按照group的顺序
    group_count_list = [group_counts[1], group_counts[2], group_counts[3], group_counts[4]]
    # 初始化计数器
    group_last_state_counts = {1: 0, 2: 0, 3: 0, 4: 0}
    # 遍历数据列表，统计每个group中last_state为0的数量
    for item in outline1:
        if 'group' in item:
            group = item['group']
            if item['state'] == 0 and group in group_last_state_counts:
                group_last_state_counts[group] += 1
    # 将计数器转换为列表，按照group的顺序
    group_last_state_count_list = [group_last_state_counts[1], group_last_state_counts[2], group_last_state_counts[3],
                                   group_last_state_counts[4]]
    middata = [group_last_state_count / group_count if group_count != 0 else 0 for
               group_last_state_count, group_count in zip(group_last_state_count_list, group_count_list)]

    result={}
    result['days_difference']=days_difference
    result['group_data'] = group_data
    result['machine_data'] = machine_data
    result['component_data'] = component_data
    result['sensor_data'] = sensor_data


    #测点报警总数
    result['s1']=s1
    result['s2']=s2
    #测点预警总数
    result['s11']=s11

    #测点离线总数
    result['s111']=s111
    middata=[round(num,2) for num in middata]
    #就一个氢机
    middata=[middata[0]]
    result['middata'] = middata
#####################
    result['gh']=gh
    result['gw']=gw
    result['gf']=gf
    result['go']=go

    result['mh']=mh
    result['mw']=mw
    result['mf']=mf
    result['mo']=mo

    result['ch']=ch
    result['cw']=cw
    result['cf']=cf
    result['co']=co

    result['sh']=216-s1-s11-s111

    #曹学勇修补
    result['gh'] = statistical_group_normal(db)
    result['mh'] = statistical_machine_normal(db)
    result['ch'] = statistical_component_normal(db)
    result['sh'] = statistical_sensor_normal(db)
    return result


"""

### event_data (事件数据)

#### 表结构

| 字段名       | 类型   | 数组元素类型 | 注释           |
| ------------ | ------ | ------------ | -------------- |
| _id          | 对象ID |              | 文档唯一标识符 |
| begin_date   | 字符串 |              | 开始日期       |
| end_date     | 字符串 |              | 结束日期       |
| sensorID     | 字符串 |              | 传感器ID       |
| group        | 整数   |              | 组编号         |
| machine      | 整数   |              | 机器编号       |
| component    | 整数   |              | 组件编号       |
| sensor       | 整数   |              | 传感器编号     |
| event_level  | 字符串 |              | 事件级别       |
| event_fault  | 字符串 |              | 事件故障       |
| solving_flag | 整数   |              | 解决标志       |
| solving      | 字符串 |              | 解决方法       |
| attention    | 字符串 |              | 注意事项       |

#### 样例数据（前1条）

| 字段名       | 样例1                                |
| ------------ | ------------------------------------ |
| _id          | 6723669e5224577797e28897             |
| attention    | 检查传感器、采集卡和通信电缆是否正常 |
| begin_date   | 2024-10-31 19:14:38                  |
| component    | 2                                    |
| end_date     | 2024-10-31 19:14:38                  |
| event_fault  | planet                               |
| event_level  | offline                              |
| group        | 4                                    |
| machine      | 5                                    |
| sensor       | 5                                    |
| sensorID     | SE_4_5_2_5                           |
| solving      | 检查该位置传感器                     |
| solving_flag | 0                                    |

#### JSON格式数据

```json
{
  "_id": "6723669e5224577797e28897",
  "begin_date": "2024-10-31 19:14:38",
  "end_date": "2024-10-31 19:14:38",
  "sensorID": "SE_4_5_2_5",
  "group": 4,
  "machine": 5,
  "component": 2,
  "sensor": 5,
  "event_level": "offline",
  "event_fault": "planet",
  "solving_flag": 0,
  "solving": "检查该位置传感器",
  "attention": "检查传感器、采集卡和通信电缆是否正常"
}
```

"""