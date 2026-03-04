import inspect

from pymongo import  MongoClient


# _IP ="127.0.0.1"
# 原来的ip地址
#_IP ="192.168.31.180"
# 新修改的IP地址
_IP ="222.242.225.74"

# _IP = "100.80.36.121"
# 获取数据库
def get_db():
    client = MongoClient(
        host=_IP,
        #port=27017,
        port=10247,
        username='admin',
        password='weiot@123!',
        serverSelectionTimeoutMS=3000  # 连接超时时间（毫秒）
    )
    # 测试连接有效性（可选）
    try:
        client.admin.command('ismaster')
        print("MongoDB连接成功！")
        ######
        # stack = inspect.stack()
        # # 调用者的帧是栈的第 1 项（索引 1），第 0 项是当前函数自身的帧
        # caller_frame_info = stack[1]
        # # 提取调用者的详细信息（文件路径、行号、函数名等）
        # caller_line = caller_frame_info.lineno  # 调用者调用此处的行号
        # caller_function = caller_frame_info.function  # 调用者的函数名
        # print(f"调用行号：第 {caller_line} 行")
        # print(f"调用函数：{caller_function}")

    except Exception as e:
        print(f"连接失败: {str(e)}")
        raise
    ####
    db = client['yueyangfan']
    return db


def get_client():
    client = MongoClient(
        host=_IP,
        port=27017,
        serverSelectionTimeoutMS=3000  # 连接超时时间（毫秒）
    )
    return client
