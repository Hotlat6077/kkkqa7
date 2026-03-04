from mydb.get_mongo import get_db
from datetime import datetime
import json
from flask import jsonify
from mydb.get_mongo import get_db


try:
    db = get_db()
    collection_name = 'pumpt_testy'
    if collection_name not in db.list_collection_names():
        # 可在此定义表结构或者创建索引等
        db.create_collection(collection_name)
        print(f"新表已创建: {collection_name}")
    collection = db[collection_name]
except Exception as e:
    print(f"MongoDB 初始化失败（服务仍可启动）: {e}")
    db = None
    collection = None




# ========== 删除集合（表）的代码示例 ==========
# 下面代码根据需要解除注释并使用

# 方法1: 删除整个集合（表）
if __name__ == '__main__':
    def get_data():   
        # 使用全局的 db 连接，避免创建新连接
        if db is None:
            from mydb.get_mongo import get_db
            temp_db = get_db()
        else:
            temp_db = db
        collection = temp_db['pump_waveform_report']
        query = {
            # 'sensorId':'SE_1_1_2_1',
            'measureSiteId':1077691462944,
            'measureGatherId':1077691480608,
            'time':'20260109040100'
    }
        document = collection.find_one(query)
        if document:
            document['creat_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("document:",type(document))
        return document  # 必须返回 document，否则返回 None
    
    data = get_data()
    db['test_students'].insert_one(data)
    # db.client.close()
        # # 不要使用 jsonify，MongoDB 需要字典格式
    # # 1. 保存运行参数数据
    # # 插入到运行数据集合
    # if db is not None:
    #     document = get_data()
    #     if document is None:
    #         print("错误：无法获取源数据，请检查查询条件")
    #     else:
    #         try:
    #             collection_operating = db['sensor_operating_dataex']
                
    #             # 重要步骤1：确保集合存在（如果是新建的表）
    #             # MongoDB 虽然会自动创建集合，但显式创建可以确保集合立即存在
    #             if 'sensor_operating_dataex' not in db.list_collection_names():
    #                 db.create_collection('sensor_operating_dataex')
    #                 print(f"✓ 新集合已创建: sensor_operating_dataex")
                
    #             print(f"准备插入数据到集合: sensor_operating_dataex")
    #             # print(f"插入的数据: {document}")
                
    #             # 重要步骤2：处理 _id 字段，避免重复键错误
    #             # 从源集合获取的文档包含 _id，需要删除它让 MongoDB 自动生成新的 _id
    #             # 或者使用 copy() 创建副本，避免修改原始文档
    #             document_to_insert = document.copy()
    #             if '_id' in document_to_insert:
    #                 # 删除 _id 字段，让 MongoDB 自动生成新的 _id
    #                 del document_to_insert['_id']
    #                 print("✓ 已删除原文档的 _id 字段，将使用新的自动生成的 _id")
                
    #             # 重要步骤3：执行插入操作
    #             operating_result = collection_operating.insert_one(document_to_insert)
                
    #             # 验证插入结果
    #             if operating_result.inserted_id:
    #                 print(f"✓ 数据插入成功，文档ID: {operating_result.inserted_id}")
                    
    #                 # 重要步骤4：立即验证数据是否存在
    #                 # 对于新建的表，可能需要稍等片刻才能查询到
    #                 import time
    #                 time.sleep(0.1)  # 等待100毫秒，确保写入完成
                    
    #                 inserted_doc = collection_operating.find_one({'_id': operating_result.inserted_id})
    #                 if inserted_doc:
    #                     print(f"✓ 验证成功：数据已存在于数据库中")
    #                     print(f"文档数量统计: {collection_operating.count_documents({})}")
    #                 else:
    #                     print("⚠ 警告：插入返回了ID，但立即查询不到数据")
    #                     print("提示：这可能是正常的，MongoDB 可能需要几秒钟才能同步")
    #                     print("建议：稍后使用数据库工具或重新运行查询来验证")
    #             else:
    #                 print("⚠ 警告：插入操作未返回文档ID")
                    
    #         except Exception as e:
    #             print(f"❌ 插入数据时发生错误: {e}")
    #             import traceback
    #             traceback.print_exc()
    # else:
    #     print("❌ 数据库未初始化，无法插入数据")
    # db = get_db()
    # students = db['test_students']  # 如果 students 集合不存在，会在第一次插入数据时自动创建

    # # 4. 插入单条数据
    # student1 = {
    #     "name": "张三",
    #     "age": 20,
    #     "major": "计算机科学"
    # }
    # insert_result = students.insert_one(student1)
    # print(f"插入单条数据成功，ID: {insert_result.inserted_id}")

    # # 5. 插入多条数据
    # students_list = [
    #     {"name": "李四", "age": 21, "major": "数学"},
    #     {"name": "王五", "age": 22, "major": "物理"},
    #     {"name": "赵六", "age": 19, "major": "化学"}
    # ]
    # insert_many_result = students.insert_many(students_list)
    # print(f"插入多条数据成功，IDs: {insert_many_result.inserted_ids}")
    # db.client.close()
    # # 6. 关闭连接（可选，脚本结束会自动关闭）
    # # client.close()