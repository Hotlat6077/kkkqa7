import paho.mqtt.client as mqtt
import json
import time
import random
from config import MQTT_CONFIG

class MQTTClient:
    def __init__(self):
        self.config = MQTT_CONFIG
        self.client = None
        self.connected = False
        self.reconnect_delay = 1  # 初始重连延迟（秒）
        self.max_reconnect_delay = 30  # 最大重连延迟（秒）
        
    def on_connect(self, client, userdata, flags, rc):
        """连接回调函数"""
        if rc == 0:
            self.connected = True
            self.reconnect_delay = 1  # 重置重连延迟
            print("成功连接到MQTT代理")
        else:
            print(f"MQTT连接失败，错误代码: {rc}")
            # 根据错误代码提供更详细的信息
            error_messages = {
                1: "连接被拒绝 - 协议版本错误",
                2: "连接被拒绝 - 客户端标识符被拒绝",
                3: "连接被拒绝 - 服务器不可用",
                4: "连接被拒绝 - 用户名或密码错误",
                5: "连接被拒绝 - 未授权",
                7: "连接被拒绝 - 客户端标识符错误"
            }
            if rc in error_messages:
                print(f"错误原因: {error_messages[rc]}")
    
    def on_disconnect(self, client, userdata, rc):
        """断开连接回调函数"""
        self.connected = False
        print(f"MQTT断开连接，错误代码: {rc}")
        
        # 自动重连
        if rc != 0:  # 如果不是正常断开连接（rc=0）
            self._reconnect()
    
    def _reconnect(self):
        """自动重连机制"""
        print(f"尝试重新连接到MQTT代理...")
        try:
            # 增加重连延迟（指数退避）
            time.sleep(self.reconnect_delay)
            self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)
            
            # 生成新的客户端ID避免冲突
            new_client_id = f"{self.config['client_id'].split('_')[0]}_{int(time.time())}_{random.randint(1, 1000)}"
            # 重新创建客户端 (paho-mqtt 2.0+ 版本)
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=new_client_id)
            
            # 重新设置回调和认证
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            
            if self.config['username'] and self.config['password']:
                self.client.username_pw_set(
                    self.config['username'],
                    self.config['password']
                )
            
            self.client.connect(
                self.config['broker'],
                self.config['port'],
                keepalive=60
            )
        except Exception as e:
            print(f"MQTT重连失败: {e}")
            # 递归调用，继续尝试重连
            self._reconnect()
    
    def connect(self):
        """连接到MQTT代理"""
        try:
            # 确保client_id有效
            client_id = self.config.get('client_id', f"mqtt_client_{int(time.time())}")
            
            # 创建MQTT客户端 (paho-mqtt 2.0+ 需要指定回调API版本)
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=client_id)
            
            # 设置回调函数
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            
            # 设置认证信息（如果需要）
            if self.config['username'] and self.config['password']:
                self.client.username_pw_set(
                    self.config['username'],
                    self.config['password']
                )
            
            # 连接到MQTT代理
            self.client.connect(
                self.config['broker'],
                self.config['port'],
                keepalive=60
            )
            
            # 启动客户端循环
            self.client.loop_start()
            
            # 等待连接成功
            max_wait = 10
            while not self.connected and max_wait > 0:
                time.sleep(1)
                max_wait -= 1
            
            if not self.connected:
                # 尝试重新连接
                self._reconnect()
                
        except Exception as e:
            print(f"MQTT连接失败: {e}")
            raise
    
    def publish(self, data, topic=None, qos=0):
        """发布消息到MQTT主题"""
        if not self.connected:
            print("MQTT未连接，无法发布消息")
            return False
            
        try:
            # 使用指定主题或默认主题
            publish_topic = topic if topic else self.config.get('topic', 'default_topic')
            
            # 转换数据为JSON字符串
            payload = json.dumps(data)
            
            # 发布消息
            result = self.client.publish(publish_topic, payload, qos=qos)
            
            # 等待发布完成
            result.wait_for_publish()
            
            print(f"成功发布MQTT消息到主题 {publish_topic}")
            return True
            
        except Exception as e:
            print(f"MQTT消息发布失败: {e}")
            return False
    
    def close(self):
        """关闭MQTT连接"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            print("MQTT连接已关闭")
