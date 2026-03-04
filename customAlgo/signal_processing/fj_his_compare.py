########################
# 文件名：fj_his_compare.py
########################


from loguru import logger
import time
import sys

from mydb.get_mongo import get_db

# ==========修改开始：日志配置==========
# 先移除所有默认/已有的日志配置，避免冲突
logger.remove()

# 重新添加文件输出
logger.add("fj_his_compare.log", rotation="10 MB", enqueue=True, level="DEBUG")

# 再添加控制台输出
logger.add(sys.stdout, level="DEBUG")
# ==========修改结束==========

def ndarray2list0(data):
    """
    把 numpy 数组列表转为 Python 列表
    """
    list0 = []
    for temp in data:
        list0.append(temp.tolist())
    return list0

def ndarray2list1(data):
    """
    二次转换，把二维或更高维数组摊平并合并到一个列表
    """
    list0 = []
    for temp in data:
        list0.append(temp.tolist())
    list1 = []
    for i in list0:
        for j in i:
            list1.append(j)
    return list1

def fj_his_compare(query_order, group, machine, component, sensor, index):
    """
    根据传入的查询条件 (start_time, end_time...) 进行 MongoDB 查询并处理返回。
    """
    # 记录函数进入日志
    logger.info(f"[fj_his_compare] Start function with group={group}, "
                f"machine={machine}, component={component}, sensor={sensor}, index={index}")

    start_func_time = time.time()

    signal3 = []
    signal5 = []
    signal8 = []

    # MongoDB 连接
    mongo_start = time.time()
    db = get_db()
    logger.debug("[fj_his_compare] Connected to MongoDB in {:.4f}s", time.time() - mongo_start)

    # 动态选择集合
    collection_name = f'indicator_data_{group}_{machine}'
    logger.debug(f"[fj_his_compare] Will access collection: {collection_name}")

    collection2 = eval(f'db.{collection_name}')

    # 参数转换
    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)

    # 获取查询时间
    start_time = query_order.get("start_time")
    end_time = query_order.get("end_time")

    # 结果结构
    result = {'fea_xaxis': []}

    if start_time and end_time:
        start_time_format = str(start_time)
        end_time_format = str(end_time)

        logger.info(f"[fj_his_compare] Query range: {start_time_format} ~ {end_time_format}")

        # 打点：开始查询
        query_start = time.time()
        result_list1 = list(collection2.find(
            {"$and": [
                {"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                {'component': component, 'sensor': sensor}
            ]},
            {'var': 1, 'rms': 1, 'kur': 1, 'peak': 1, 'speed_rms': 1, 'datetime': 1}
        ))
        query_cost = time.time() - query_start
        logger.info(f"[fj_his_compare] MongoDB query finished, found {len(result_list1)} docs, cost={query_cost:.4f}s")

        # 处理数据  --  20241231--zenghw-
        process_start = time.time()
        # 1) 批量获取所有 index 值（如 'rms'/'var'/'kur' 等）
        signal3_list = [doc.get(index) for doc in result_list1]
        # 2) 批量获取所有 datetime
        fea_xaxis_list = [doc.get('datetime') for doc in result_list1]

        # 3) 一次性拼到 result['fea_xaxis'] 里
        result['fea_xaxis'].extend(fea_xaxis_list)

        # 4) signal3_list 是一个二维列表(如[[...],[...],...])，这里用推导式压平
        signal3 = [item for sublist in signal3_list for item in sublist]

        process_cost = time.time() - process_start
        logger.debug(f"[fj_his_compare] Data processing done, cost={process_cost:.4f}s")

    # 写入到返回结构
    result['trend3'] = signal3
    logger.debug(f"[fj_his_compare] trend3 length={len(signal3)}")

    # 将 group/machine 等转换或拼接到 result
    result['group'] = str(group)
    result['machine'] = str(machine)
    result['component'] = component
    result['sensor'] = sensor

    total_cost = time.time() - start_func_time
    logger.info(f"[fj_his_compare] Completed, total cost={total_cost:.4f}s")

    return result

def fj_his_compare2(query_order, group, machine, component, sensor, index):
    """
    与 fj_his_compare 类似的处理逻辑，可同样打点日志分析。
    """
    logger.info(f"[fj_his_compare2] Start function with group={group}, "
                f"machine={machine}, component={component}, sensor={sensor}, index={index}")

    start_func_time = time.time()

    signal3 = []
    signal5 = []
    signal8 = []

    # MongoDB 连接
    mongo_start = time.time()
    db = get_db()
    logger.debug("[fj_his_compare2] Connected to MongoDB in {:.4f}s", time.time() - mongo_start)

    # 动态选择集合
    collection_name = f'indicator_data_{group}_{machine}'
    logger.debug(f"[fj_his_compare2] Will access collection: {collection_name}")

    # 尽量避免在生产环境中使用 eval  --20241231--zenghw
    # collection2 = eval(f'db.{collection_name}')
    collection2 = db[collection_name]

    # 参数转换
    group = int(group)
    machine = int(machine)
    component = int(component)
    sensor = int(sensor)

    # 获取查询时间
    start_time = query_order.get("start_time")
    end_time = query_order.get("end_time")

    result = {'fea_xaxis': []}

    if start_time and end_time:
        start_time_format = str(start_time)
        end_time_format = str(end_time)

        logger.info(f"[fj_his_compare2] Query range: {start_time_format} ~ {end_time_format}")

        # 打点：开始查询
        query_start = time.time()
        result_list1 = list(collection2.find(
            {"$and": [
                {"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                {'component': component, 'sensor': sensor}
            ]},
            {'var': 1, 'rms': 1, 'kur': 1, 'peak': 1, 'speed_rms': 1, 'datetime': 1}
        ))
        query_cost = time.time() - query_start
        logger.info(f"[fj_his_compare2] MongoDB query finished, found {len(result_list1)} docs, cost={query_cost:.4f}s")

        # 处理数据 --20241231-zenghw 在底层一次性构建 list，会比循环多次 append() 更高效
        process_start = time.time()
        # 1) 批量获取所有 index 值（如 'rms'/'var'/'kur' 等）
        signal3_list = [doc.get(index) for doc in result_list1]
        # 2) 批量获取所有 datetime
        fea_xaxis_list = [doc.get('datetime') for doc in result_list1]

        # 3) 一次性拼到 result['fea_xaxis'] 里
        result['fea_xaxis'].extend(fea_xaxis_list)

        # 4) signal3_list 是一个二维列表(如[[...],[...],...])，这里用推导式压平
        signal3 = [item for sublist in signal3_list for item in sublist]

        process_cost = time.time() - process_start
        logger.debug(f"[fj_his_compare] Data processing done, cost={process_cost:.4f}s")

    result['trend3'] = signal3
    logger.debug(f"[fj_his_compare2] trend3 length={len(signal3)}")

    result['group'] = str(group)
    result['machine'] = str(machine)
    result['component'] = component
    result['sensor'] = sensor

    total_cost = time.time() - start_func_time
    logger.info(f"[fj_his_compare2] Completed, total cost={total_cost:.4f}s")

    return result
