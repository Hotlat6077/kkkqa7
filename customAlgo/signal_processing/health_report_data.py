
import numpy as np
import datetime
import os
import config as cfg
from mydb.get_mongo import get_db


def get_all_group():
    db = get_db()
    collection = db.group_data
    group_id_list = [i.get('groupID') for i in list(collection.find({'onlineflag': True}, {}))]
    return group_id_list


def get_machineID(groupID):
    db = get_db()
    collection = db.machine_data
    machine_id_list = [i.get('machineID') for i in list(collection.find({'onlineflag': True, 'groupID': groupID}, {}))]
    return machine_id_list


def get_componentID(machineID):
    db = get_db()
    collection = db.component_data
    componentid_list = [i.get('componentID') for i in
                        list(collection.find({'onlineflag': True, 'machineID': machineID}, {}))]
    return componentid_list


def get_sensorID(componentID):
    db = get_db()
    collection = db.sensor_data
    sensorid_list = [[i.get('sensorID')] for i in
                     list(collection.find({'onlineflag': True, 'componentID': componentID}, {}))]
    return sensorid_list


# ------------------ 新增: 根据需求生成 failureType 的辅助函数 ------------------
def parse_sub_state(sub_state):
    """
    sub_state: [x, y]
    x => 标准差(0:正常,1:预警,2:报警)
    y => 均方根(0:正常,1:预警,2:报警)
    返回形如 "标准差:预警, 均方根:报警" 的字符串；如果为 [0,0] 则返回空字符串供后续逻辑判断
    """
    if not isinstance(sub_state, list) or len(sub_state) < 2:
        return ""  # 若格式不对，直接返回空

    # 映射关系
    mapping = {0: "正常", 1: "预警", 2: "报警"}
    part_list = []
    if sub_state[0] != 0:
        part_list.append(f"标准差:{mapping.get(sub_state[0], '')}")
    if sub_state[1] != 0:
        part_list.append(f"均方根:{mapping.get(sub_state[1], '')}")
    return ", ".join(part_list)


def get_failure_type(item, component_name):
    """
    根据需求，综合 state、faultstr、sub_state、component_name 来生成最终的 failureType 字符串
    """
    # 1) 先取出 sub_state，若 [0,0] 则最终是 "无"
    sub_state = item.get('sub_state', None)
    faultstr = item.get('faultstr', "")
    state = item.get('state', -1)  # 默认 -1 表示无效

    # 如果 sub_state == [0, 0]，则直接返回 "无"
    if isinstance(sub_state, list) and len(sub_state) == 2 and sub_state[0] == 0 and sub_state[1] == 0:
        return "无"

    ##现在移动到描述里

    return item.get('description','_')

    #
    # # 若 sub_state 非 [0,0]，则看具体逻辑
    # # 2) state=0
    # if state == 0:
    #     # 2.1) faultstr="频率未预警" => "无"
    #     if faultstr == "频率未预警":
    #         return "无"
    #     # 2.2) faultstr="指标预警" => component_name+"报警" (若 component_name="主轴承"，则 "主轴承报警")
    #     if faultstr == "指标预警":
    #         if component_name == "主轴承":
    #             return "主轴承报警"
    #         else:
    #             return f"{component_name}报警"
    #     # 如果不是上述两种 faultstr，且 state=0，就不做额外处理，返回原有 faultstr
    #     return faultstr
    #
    # # 3) state=1 或 2
    # if state in [1, 2]:
    #     # 3.1) faultstr="频率未预警" => 根据 sub_state 值，生成 "标准差:预警, 均方根:报警" 等
    #     if faultstr == "频率未预警":
    #         sub_state_str = parse_sub_state(sub_state)
    #         if sub_state_str == "":
    #             # 如果解析为空，说明 sub_state 都是0 或格式不正确，就返回原 faultstr 或 "无"
    #             # 但需求没有提到 sub_state 不正确怎么办，这里按空字符串则表示无
    #             return "无"
    #         else:
    #             return sub_state_str
    #
    #     # 3.2) faultstr="指标预警" => component_name+"报警"(若为主轴承则 "主轴承报警") + "|" + sub_state_str
    #     if faultstr == "指标预警":
    #         if component_name == "主轴承":
    #             comp_fault = "主轴承报警"
    #         else:
    #             comp_fault = f"{component_name}报警"
    #         sub_state_str = parse_sub_state(sub_state)
    #         if sub_state_str == "":
    #             # 如果 sub_state_str 为空，则仅返回 "component_name 报警"
    #             return comp_fault
    #         else:
    #             return comp_fault + "|" + sub_state_str
    #
    #     # 如果都不符合上述 faultstr，则默认返回原有 faultstr
    #     return faultstr
    #
    # # 兜底：state 不在 [0,1,2] 时，直接返回原 faultstr
    # return faultstr


# ------------------ 新增函数结束 ------------------

def get_health_report_date(his_1_order, new_index, health_indicator, fault_indicator):
    db = get_db()
    collection_alert = db['alert_data']
    health_indicator = str(health_indicator)
    fault_indicator = str(fault_indicator)

    group_name_collection = db['group_data']
    machine_name_collection = db['machine_data']
    component_name_collection = db['component_data']
    sensor_name_collection = db['sensor_data']

    response_data = []
    start_time = his_1_order.get("start_time")
    end_time = his_1_order.get("end_time")

    if start_time and end_time:
        start_time_format = str(start_time)
        end_time_format = str(end_time)

        if len(new_index) == 1:
            # new_index=['GR_1']
            machineid_list = get_machineID(new_index[0])

            for machineid in machineid_list:
                collection_index = eval(f"db.indicator_data_{machineid.split('_')[1]}_{machineid.split('_')[-1]}")
                # collection_index='indicator_data_2_1'
                componentid_list = get_componentID(machineid)

                for componentid in componentid_list:
                    sensorid_list = get_sensorID(componentid)

                    for sensorid in sensorid_list:
                        result_predictive = list(collection_index.find(
                            {"$and": [
                                {"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                {"sensorID": sensorid[0]}
                            ]}
                        ))

                        for item in result_predictive:
                            group_name = list(group_name_collection.find(
                                {'onlineflag': True, 'groupID': f"GR_{machineid.split('_')[1]}"},
                                {}
                            ))[0]['name']
                            machine_name = list(machine_name_collection.find(
                                {'onlineflag': True, 'machineID': machineid},
                                {}
                            ))[0]['name']
                            component_name = list(component_name_collection.find(
                                {
                                    'onlineflag': True,
                                    'componentID': f"CO_{machineid.split('_')[1]}_{machineid.split('_')[-1]}_{item['component']}"
                                },
                                {}
                            ))[0]['name']
                            sensor_name = list(sensor_name_collection.find(
                                {
                                    'onlineflag': True,
                                    'sensorID': f"SE_{machineid.split('_')[1]}_{machineid.split('_')[-1]}_{item['component']}_{item['sensor']}"
                                },
                                {}
                            ))[0]['name']

                            # ========== 新增：生成最终的 failureType ==========
                            final_failure_type = get_failure_type(item, component_name)
                            # ========== 新增结束 ==========

                            result = {
                                'time': item['datetime'],
                                'group': group_name,
                                'machine': machine_name,
                                'component': component_name,
                                'sensor': sensor_name,
                                'warningValue': [f"{value:.5f}" for value in item.get(health_indicator, [])],
                                'failureValue': [f"{value:.5f}" for value in item.get('kur', [])],
                                'failureType': final_failure_type,  # 使用修正后的 failureType
                                'healthIndex': item['state']
                            }
                            # response_data.append(result)
                            interception_result(response_data, item, result, health_indicator)

        elif len(new_index) == 2:
            # new_index=['GR_2', 'MA_2_2'] 或 ['GR_2', 'all']
            if new_index[1] == 'all':
                machineid_list = get_machineID(new_index[0])

                for machineid in machineid_list:
                    collection_index = eval(f"db.indicator_data_{machineid.split('_')[1]}_{machineid.split('_')[-1]}")
                    componentid_list = get_componentID(machineid)

                    for componentid in componentid_list:
                        sensorid_list = get_sensorID(componentid)

                        for sensorid in sensorid_list:
                            result_predictive = list(collection_index.find(
                                {"$and": [
                                    {"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                    {"sensorID": sensorid[0]}
                                ]}
                            ))

                            for item in result_predictive:
                                group_name = list(group_name_collection.find(
                                    {'onlineflag': True, 'groupID': f"GR_{machineid.split('_')[1]}"},
                                    {}
                                ))[0]['name']
                                machine_name = list(machine_name_collection.find(
                                    {'onlineflag': True, 'machineID': machineid},
                                    {}
                                ))[0]['name']
                                component_name = list(component_name_collection.find(
                                    {
                                        'onlineflag': True,
                                        'componentID': f"CO_{machineid.split('_')[1]}_{machineid.split('_')[-1]}_{item['component']}"
                                    },
                                    {}
                                ))[0]['name']
                                sensor_name = list(sensor_name_collection.find(
                                    {
                                        'onlineflag': True,
                                        'sensorID': f"SE_{machineid.split('_')[1]}_{machineid.split('_')[-1]}_{item['component']}_{item['sensor']}"
                                    },
                                    {}
                                ))[0]['name']

                                # ========== 新增：生成最终的 failureType ==========
                                final_failure_type = get_failure_type(item, component_name)
                                # ========== 新增结束 ==========

                                result = {
                                    'time': item['datetime'],
                                    'group': group_name,
                                    'machine': machine_name,
                                    'component': component_name,
                                    'sensor': sensor_name,
                                    #'warningValue': [f"{value:.5f}" for value in item[health_indicator]],
                                    # 'failureValue': [f"{value:.5f}" for value in item['kur']],
                                    'failureType': final_failure_type,
                                    'healthIndex': item['state']
                                }
                                # response_data.append(result)
                                interception_result(response_data, item, result, health_indicator)
            else:
                machineid = new_index[1]

                collection_index = eval(f"db.indicator_data_{machineid.split('_')[1]}_{machineid.split('_')[-1]}")
                componentid_list = get_componentID(machineid)

                for componentid in componentid_list:
                    sensorid_list = get_sensorID(componentid)

                    for sensorid in sensorid_list:
                        result_predictive = list(collection_index.find(
                            {"$and": [
                                {"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                {"sensorID": sensorid[0]}
                            ]}
                        ))
                        for item in result_predictive:
                            group_name = list(group_name_collection.find(
                                {'onlineflag': True, 'groupID': f"GR_{machineid.split('_')[1]}"},
                                {}
                            ))[0]['name']
                            machine_name = list(machine_name_collection.find(
                                {'onlineflag': True, 'machineID': machineid},
                                {}
                            ))[0]['name']
                            component_name = list(component_name_collection.find(
                                {
                                    'onlineflag': True,
                                    'componentID': f"CO_{machineid.split('_')[1]}_{machineid.split('_')[-1]}_{item['component']}"
                                },
                                {}
                            ))[0]['name']
                            sensor_name = list(sensor_name_collection.find(
                                {
                                    'onlineflag': True,
                                    'sensorID': f"SE_{machineid.split('_')[1]}_{machineid.split('_')[-1]}_{item['component']}_{item['sensor']}"
                                },
                                {}
                            ))[0]['name']

                            # ========== 新增：生成最终的 failureType ==========
                            final_failure_type = get_failure_type(item, component_name)
                            # ========== 新增结束 ==========

                            result = {
                                'time': item['datetime'],
                                'group': group_name,
                                'machine': machine_name,
                                'component': component_name,
                                'sensor': sensor_name,
                                #'warningValue': [f"{value:.5f}" for value in item[health_indicator]],
                                # 'failureValue': [f"{value:.5f}" for value in item['kur']],
                                'failureType': final_failure_type,
                                'healthIndex': item['state']
                            }
                            # response_data.append(result)
                            interception_result(response_data, item, result, health_indicator)

        elif len(new_index) == 3:
            # new_index 可能是 ['GR_x','MA_x_x','all'] 或 ['GR_x','MA_x_x','CO_x_x_x']
            if new_index[2] == 'all':
                machineid = new_index[1]

                collection_index = eval(f"db.indicator_data_{machineid.split('_')[1]}_{machineid.split('_')[-1]}")
                componentid_list = get_componentID(machineid)

                for componentid in componentid_list:
                    sensorid_list = get_sensorID(componentid)

                    for sensorid in sensorid_list:
                        result_predictive = list(collection_index.find(
                            {"$and": [
                                {"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                {"sensorID": sensorid[0]}
                            ]}
                        ))
                        for item in result_predictive:
                            group_name = list(group_name_collection.find(
                                {'onlineflag': True, 'groupID': f"GR_{machineid.split('_')[1]}"},
                                {}
                            ))[0]['name']
                            machine_name = list(machine_name_collection.find(
                                {'onlineflag': True, 'machineID': machineid},
                                {}
                            ))[0]['name']
                            component_name = list(component_name_collection.find(
                                {
                                    'onlineflag': True,
                                    'componentID': f"CO_{machineid.split('_')[1]}_{machineid.split('_')[-1]}_{item['component']}"
                                },
                                {}
                            ))[0]['name']
                            sensor_name = list(sensor_name_collection.find(
                                {
                                    'onlineflag': True,
                                    'sensorID': f"SE_{machineid.split('_')[1]}_{machineid.split('_')[-1]}_{item['component']}_{item['sensor']}"
                                },
                                {}
                            ))[0]['name']

                            # ========== 新增：生成最终的 failureType ==========
                            final_failure_type = get_failure_type(item, component_name)
                            # ========== 新增结束 ==========

                            result = {
                                'time': item['datetime'],
                                'group': group_name,
                                'machine': machine_name,
                                'component': component_name,
                                'sensor': sensor_name,
                                #'warningValue': [f"{value:.5f}" for value in item[health_indicator]],
                                # 'failureValue': [f"{value:.5f}" for value in item['kur']],
                                'failureType': final_failure_type,
                                'healthIndex': item['state']
                            }
                            # response_data.append(result)
                            interception_result(response_data, item, result, health_indicator)
            else:
                componentid = new_index[2]

                collection_index = eval(f"db.indicator_data_{componentid.split('_')[1]}_{componentid.split('_')[2]}")
                sensorid_list = get_sensorID(componentid)

                for sensorid in sensorid_list:
                    result_predictive = list(collection_index.find(
                        {"$and": [
                            {"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                            {"sensorID": sensorid[0]}
                        ]}
                    ))
                    for item in result_predictive:
                        group_name = list(group_name_collection.find(
                            {'onlineflag': True, 'groupID': f"GR_{componentid.split('_')[1]}"},
                            {}
                        ))[0]['name']
                        machine_name = list(machine_name_collection.find(
                            {
                                'onlineflag': True,
                                'machineID': f"MA_{componentid.split('_')[1]}_{componentid.split('_')[2]}"
                            },
                            {}
                        ))[0]['name']
                        component_name = list(component_name_collection.find(
                            {'onlineflag': True, 'componentID': componentid},
                            {}
                        ))[0]['name']
                        sensor_name = list(sensor_name_collection.find(
                            {
                                'onlineflag': True,
                                'sensorID': f"SE_{componentid.split('_')[1]}_{componentid.split('_')[2]}_{componentid.split('_')[3]}_{item['sensor']}"
                            },
                            {}
                        ))[0]['name']

                        # ========== 新增：生成最终的 failureType ==========
                        final_failure_type = get_failure_type(item, component_name)
                        # ========== 新增结束 ==========

                        result = {
                            'time': item['datetime'],
                            'group': group_name,
                            'machine': machine_name,
                            'component': component_name,
                            'sensor': sensor_name,
                            #'warningValue': [f"{value:.5f}" for value in item[health_indicator]],
                            # 'failureValue': [f"{value:.5f}" for value in item['kur']],
                            'failureType': final_failure_type,
                            'healthIndex': item['state']
                        }
                        # response_data.append(result)
                        interception_result(response_data, item, result, health_indicator)

        elif len(new_index) == 4:
            # new_index 可能是 ['GR_x','MA_x_x','CO_x_x_x','all'] 或 ['GR_x','MA_x_x','CO_x_x_x','SE_x_x_x_x']
            if new_index[3] == 'all':
                componentid = new_index[2]

                collection_index = eval(f"db.indicator_data_{componentid.split('_')[1]}_{componentid.split('_')[2]}")
                sensorid_list = get_sensorID(componentid)

                for sensorid in sensorid_list:
                    result_predictive = list(collection_index.find(
                        {"$and": [
                            {"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                            {"sensorID": sensorid[0]}
                        ]}
                    ))
                    for item in result_predictive:
                        group_name = list(group_name_collection.find(
                            {'onlineflag': True, 'groupID': f"GR_{componentid.split('_')[1]}"},
                            {}
                        ))[0]['name']
                        machine_name = list(machine_name_collection.find(
                            {
                                'onlineflag': True,
                                'machineID': f"MA_{componentid.split('_')[1]}_{componentid.split('_')[2]}"
                            },
                            {}
                        ))[0]['name']
                        component_name = list(component_name_collection.find(
                            {'onlineflag': True, 'componentID': componentid},
                            {}
                        ))[0]['name']
                        sensor_name = list(sensor_name_collection.find(
                            {
                                'onlineflag': True,
                                'sensorID': f"SE_{componentid.split('_')[1]}_{componentid.split('_')[2]}_{componentid.split('_')[3]}_{item['sensor']}"
                            },
                            {}
                        ))[0]['name']

                        # ========== 新增：生成最终的 failureType ==========
                        final_failure_type = get_failure_type(item, component_name)
                        # ========== 新增结束 ==========

                        result = {
                            'time': item['datetime'],
                            'group': group_name,
                            'machine': machine_name,
                            'component': component_name,
                            'sensor': sensor_name,
                            #'warningValue': [f"{value:.5f}" for value in item[health_indicator]],
                            # 'failureValue': [f"{value:.5f}" for value in item['kur']],
                            'failureType': final_failure_type,
                            'healthIndex': item['state']
                        }
                        # response_data.append(result)
                        interception_result(response_data, item, result, health_indicator)
            else:
                sensorid = new_index[3]
                collection_index = eval(f"db.indicator_data_{sensorid.split('_')[1]}_{sensorid.split('_')[2]}")
                result_predictive = list(collection_index.find(
                    {"$and": [
                        {"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                        {"sensorID": sensorid}
                    ]}
                ))
                for item in result_predictive:
                    group_name = list(group_name_collection.find(
                        {'onlineflag': True, 'groupID': f"GR_{sensorid.split('_')[1]}"},
                        {}
                    ))[0]['name']
                    machine_name = list(machine_name_collection.find(
                        {
                            'onlineflag': True,
                            'machineID': f"MA_{sensorid.split('_')[1]}_{sensorid.split('_')[2]}"
                        },
                        {}
                    ))[0]['name']
                    component_name = list(component_name_collection.find(
                        {
                            'onlineflag': True,
                            'componentID': f"CO_{sensorid.split('_')[1]}_{sensorid.split('_')[2]}_{sensorid.split('_')[3]}"
                        },
                        {}
                    ))[0]['name']
                    sensor_name = list(sensor_name_collection.find(
                        {'onlineflag': True, 'sensorID': sensorid},
                        {}
                    ))[0]['name']

                    # ========== 新增：生成最终的 failureType ==========
                    final_failure_type = get_failure_type(item, component_name)
                    # ========== 新增结束 ==========

                    result = {
                        'time': item['datetime'],
                        'group': group_name,
                        'machine': machine_name,
                        'component': component_name,
                        'sensor': sensor_name,
                        #'warningValue': [f"{value:.5f}" for value in item[health_indicator]],
                        # 'failureValue': [f"{value:.5f}" for value in item['kur']],
                        'failureType': final_failure_type,
                        'healthIndex': item['state']
                    }

                    # response_data.append(result)
                    interception_result(response_data, item, result, health_indicator)

    return response_data


# 曹学勇修补
# 拦截结果，把温度1，转速2，压力34 使用特征值
def interception_result(response, item, result, health_indicator):
    result['warningValue'] = item.get(health_indicator, '0')
    result['failureValue'] = item.get('kur', '')
        
    sensor_id = item.get('sensor')
    if sensor_id == 1:
        result['warningValue'] = item.get('value', '0')
    elif sensor_id == 2:
        result['warningValue'] = item.get('value', '0')
    elif sensor_id == 3:
        result['warningValue'] = item.get('value', '0')
    elif sensor_id == 4:
        result['warningValue'] = item.get('value', '0')

    # 最后都添加进去
    response.append(result)
