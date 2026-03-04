from flask import Flask
import os
import sys
import time
import warnings
from mydb.get_mongo import get_db
import numpy as np
from numpy import fft
import threading
from loguru import logger
from 去滑雪坡特征 import ski_slope
from 入库峰值峰峰值峭度 import update_data,update_alert_report
from datetime import datetime
from mqtt_client import MQTTClient
from rabbitmq_client import RabbitMQClient
from config import *


warnings.filterwarnings("ignore")
logger.remove()     
logger.add(sys.stdout, colorize=True, format="<g>{time:HH:MM:ss:SSS}</g> | <c>{level}</c> | <level>{message}</level>")

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.json.ensure_ascii = False

try:
    db = get_db()
    collection = db['pump_waveform_report']
    logger.success(f"MongoDB 连接成功")
except Exception as e:
    logger.error(f"MongoDB 初始化失败（服务仍可启动）: {e}")
    db = None
    collection = None

mqtt_client = MQTTClient()

# 心跳线程运行状态
heartbeat_running = True

# 数据处理函数
def process_data(queue_data):
    """处理从RabbitMQ接收的数据"""
    try:
        # 这里添加您的数据处理逻辑
        print(f"处理数据: {len(queue_data)}")
        print(f"处理数据: {queue_data.keys()}")
        datas = queue_data.get('datas')
        fs = queue_data.get('fs')
        data_time = queue_data.get('reportTime')
        thingsModel = queue_data.get('thingsModel')
        serialNum = queue_data.get('serialNum')
        # 发送数据要用到
        sensor_id = queue_data.get('sensorId')
        # print('sensor_id',sensor_id)
        # print("fs:",fs,"data_time:",data_time,"thingsModel:",thingsModel,"sensor_id:",sensor_id)
        data_id = thingsModel[:5]
        # 确保数据完整
        if datas is not None and fs is not None and data_time is not None and thingsModel is not None and sensor_id is not None:
            # print("update_data:","update_data")
            res_update = update_data(datas, fs, data_time, thingsModel)
            # print("res:","success")
            alert_res = update_alert_report(datas, fs, thingsModel, serialNum)
            print("alert_res",alert_res)
            print("res_update",res_update)
            send_data = [
            {"id":f"acc_rms_{data_id}","value":res_update["acc_rms"],"name":"加速度有效值","reportTime":data_time,"remark":""},
            {"id":f"vel_rms_{data_id}","value":res_update["velocity_rms"],"name":"速度有效值","reportTime":data_time,"remark":""},
            {"id":f"acc_peak_{data_id}","value":res_update["peak_acc"],"name":"加速度峰值","reportTime":data_time,"remark":""},
            {"id":f"vel_peak_{data_id}","value":res_update["peak_vel"],"name":"速度峰值","reportTime":data_time,"remark":""},
            {"id":f"acc_p2p_{data_id}","value":res_update["peak2peak"],"name":"加速度峰峰值","reportTime":data_time,"remark":""},
            {"id":f"vel_p2p_{data_id}","value":res_update["peak2peak_v"],"name":"速度峰峰值","reportTime":data_time,"remark":""},
            {"id":f"acc_kur_{data_id}","value":res_update["acc_kurtosis"],"name":"加速度峭度","reportTime":data_time,"remark":""},
            {"id":f"vel_kur_{data_id}","value":res_update["velocity_kurtosis"],"name":"速度峭度","reportTime":data_time,"remark":""},
            {"id":f"acc_std_{data_id}","value":alert_res["std"],"name":"加速度标准差","reportTime":data_time,"remark":""},
            {"id":f"acc_impulse_{data_id}","value":alert_res["impulse"],"name":"加速度脉冲","reportTime":data_time,"remark":""}
            ]

            try:
                mqtt_client.publish(send_data, topic=f'/136/{sensor_id}/property/post')
                logger.success(f"MQTT发布数据: {send_data}, topic: {f'/136/{sensor_id}/property/post'}")
            except Exception as e:
                logger.error(f"MQTT发布失败: {e}")
                return False
            time.sleep(1)
        else:
            logger.error(f"缺少参数,请检查数据完整性")
            return False
        # res = update_data(datas, fs, data_time, thingsModel)
        # print(res)
        # send_data = res[0]
        # print(res[0]['id'])
        # try:
        #     print(f"MQTT发布数据: {send_data}, topic: {f'/136/{sensor_id}/property/post'}")
        #     mqtt_client.publish(send_data, topic=f'/136/{sensor_id}/property/post')
        # except Exception as e:
        #     print(f"MQTT发布失败: {e}")
        #     return False
        time.sleep(1)
        # 入库测试  
        queue_data['creat_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db['pump_vel_test1'].insert_one(queue_data)
        # queue_data['datas'] = res[1]
        queue_data['datas'] = res_update['velocity_kurtosis']
        db['pump_acc_test1'].insert_one(queue_data)
        time.sleep(1)
        # 计算报警告
        if alert_res is not None:
            queue_data['datas'] = alert_res['alert_result']
            queue_data['status'] = 1
            db['pump_algorithm_alert_test'].insert_one(queue_data)
            logger.success(f"入库成功")
        else:
            logger.error(f"报警告计算失败")
            return False

        
        return True
    except Exception as e:
        logger.error(f"处理数据失败: {e}") 
        return False 
    

if __name__ == '__main__':
    rabbitmq_client = None
    try:
        # 仅在实际运行的子进程中初始化外部连接，避免 Flask debug 重载导致重复启动线程
        # 这行代码的含义是：如果 Flask 没有开启 debug（即正式环境），
        # 或者环境变量 WERKZEUG_RUN_MAIN 等于 'true'（即在 Flask debug 模式下，此进程为主进程），
        # 则 run_init 为 True。这样可以避免 Flask 调试模式下自动重载时重复初始化外部连接（如 MQTT、RabbitMQ、数据库等），
        # 确保只在主进程中执行初始化操作。
        run_init = (not FLASK_CONFIG.get('debug', False)) or os.environ.get('WERKZEUG_RUN_MAIN') == 'true'

        if run_init:
            # 连接MongoDB数据库
            # mongodb.connect()
            # 连接MQTT代理
            mqtt_client.connect()
            # 连接RabbitMQ并启动消费者线程
            rabbitmq_client = RabbitMQClient(process_data)
            rabbitmq_client.max_consume = 1  # 只消费1条数据，改这个数字来控制消费条数
            # 查询队列当前有多少条消息
            # count = rabbitmq_client.get_queue_message_count()
            # print(f"当前队列中有 {count} 条消息")
            rabbitmq_client.connect()
            # 配置RabbitMQ只消费1条消息 
            # rabbitmq_client.max_consume = 1  # 只取1条，需主动再次调用start_consuming获取新消息
            # 启动RabbitMQ消费线程 
            rabbitmq_thread = threading.Thread(target=rabbitmq_client.start_consuming, daemon=True)
            rabbitmq_thread.start()
        # 启动Flask应用（关闭 reloader 可使用 use_reloader=False）
        # 14:01:33:190 | INFO | 请求参数 data:{'analyseMethod': 'spectrum', 
        # 'dataProcess': 'raw', 'gatherId': '1077766956832', 
        # 'localfilename': '2026-01-29 00:01', 
        # 'measureSiteId': '1077766942496', 'method_type': 'raw', 
        # 'sensorId': 'SE_1_1_3_4', 'time': '20260129000100'} time:20260129000100
        app.run(
            host=FLASK_CONFIG['host'],
            port=FLASK_CONFIG['port'],
            debug=FLASK_CONFIG['debug']
        )
    except KeyboardInterrupt:
        logger.success(f"正在关闭服务...")
    finally:
        heartbeat_running = False
        if rabbitmq_client:
            # 仅关闭连接；消费在子线程中，关连接后其会自行退出， 停止消费线程 关掉RabbitMQ连接
            rabbitmq_client.stop_consuming()
            rabbitmq_client.close()
        mqtt_client.close()
        logger.success(f"服务已关闭")