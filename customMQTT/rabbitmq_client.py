import pika
import threading
import json
from config import RABBITMQ_CONFIG

class RabbitMQClient:
    def __init__(self, message_callback):
        self.config = RABBITMQ_CONFIG
        self.connection = None
        self.channel = None
        self.message_callback = message_callback
        self.consumer_tag = None
        # self.max_consume = None  # None=不限，否则消费 N 条后停止
        self.max_consume = 1  # None=不限，否则消费 N 条后停止
        self._consumed = 0
        
    def connect(self):
        """连接到RabbitMQ服务器"""
        try:
            # 创建连接参数
            credentials = pika.PlainCredentials(self.config['username'], self.config['password'])
            params = pika.ConnectionParameters(
                host=self.config['host'],
                port=self.config['port'],
                virtual_host=self.config['virtual_host'],
                credentials=credentials
            )
            
            # 建立连接和通道
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            
            # 声明队列（如果不存在则创建）
            self.channel.queue_declare(queue=self.config['queue_name'], durable=True)
            
            print(f"成功连接到RabbitMQ，监听队列: {self.config['queue_name']}")
        except Exception as e:
            print(f"RabbitMQ连接失败: {e}")
            raise
    
    def start_consuming(self):
        """开始消费消息"""
        def on_message(ch, method, properties, body):
            try:
                message = json.loads(body.decode('utf-8'))
                # print(f"收到RabbitMQ消息: {message}")
                print(f"收到RabbitMQ消息:")
                print(message.keys())
                self.message_callback(message)
                # 该行代码用于向RabbitMQ确认已成功处理这条消息，防止消息被重复投递
                ch.basic_ack(delivery_tag=method.delivery_tag)

                self._consumed += 1
                if self.max_consume is not None and self._consumed >= self.max_consume:
                    # 这里的 tag 实际上就是当前消费者的 consumer_tag，用于唯一标识这个消费者实例，
                    # 调用 ch.basic_cancel(tag) 时就会停止这个特定的消费者接收消息
                    tag = self.consumer_tag
                    
                    self.consumer_tag = None
                    # 传入None表示取消所有消费者或默认消费者（官方文档ch.basic_cancel(None)会取消default consumer）。
                    # 但此处应传递有效的consumer_tag以取消当前消费者。
                    ch.basic_cancel(tag)
                    return
            except Exception as e:
                print(f"处理RabbitMQ消息失败: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

        # 该行代码用于启动RabbitMQ的消费者，将on_message回调绑定到指定队列，实现消息的异步监听和处理；
        # 返回的consumer_tag用于后续取消消费时标识本次消费者。
        self.consumer_tag = self.channel.basic_consume(
            queue=self.config['queue_name'],
            on_message_callback=on_message
        )

        print("开始消费RabbitMQ消息...")
        try:
            self.channel.start_consuming()
        except (KeyboardInterrupt, Exception):
            pass
        finally:
            if self.channel and self.consumer_tag:
                try:
                    self.channel.basic_cancel(self.consumer_tag)
                except Exception:
                    pass
                self.consumer_tag = None
    
    def stop_consuming(self):
        """停止消费（仅在消费线程内使用）；主线程关闭请直接 close()"""
        if self.channel and self.consumer_tag:
            try:
                self.channel.basic_cancel(self.consumer_tag)
            except Exception:
                pass
            self.consumer_tag = None

    def close(self):
        """关闭 RabbitMQ 连接；会中断消费线程的 start_consuming"""
        if self.connection and self.connection.is_open:
            try:
                self.connection.close()
            except Exception as e:
                print(f"关闭 RabbitMQ 时异常: {e}")
            print("RabbitMQ连接已关闭")
