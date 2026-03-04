import time
# Flask配置
FLASK_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': False
}


# RabbitMQ配置
RABBITMQ_CONFIG = {
    'host': '222.242.225.74',  # RabbitMQ服务器地址
    'port': 10266,         # RabbitMQ端口
    'username': 'admin',  # 用户名
    'password': 'wyzx@123456',  # 密码
    'virtual_host': '/',  # 虚拟主机
    # 'queue_name': 'pump.algorithm.mono'  # 监听的队列名称 修改
    'queue_name': 'pump.algorithm.quota'  # 监听的队列名称 修改
}

# MQTT配置
MQTT_CONFIG = {
    'broker': '222.242.225.74',  # MQTT代理地址
    'port': 10253,           # MQTT端口
    'username': 'admin',         # 用户名（如果需要）
    'password': 'weiot@12345',
    'client_id': 'pump_algorithm_' + str(int(time.time())),
}


# 告警判断阈值
ALARM_THRESHOLD = {
    'warning_threshold':30,
    'fault_threshold':70
}