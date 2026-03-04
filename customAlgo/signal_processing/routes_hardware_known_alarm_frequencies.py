# routes_hardware_known_alarm_frequencies.py

from flask import request, jsonify

def init_hardware_known_alarm_frequencies_routes(app, db):
    """
    注册 "已知报警频率硬件查询表格" 相关路由
    :param app: Flask 实例
    :param db:  MongoDB 数据库实例
    """
    collection = db["hardware_known_alarm_frequencies"]  # 集合改名

    @app.route("/hardware-known-alarm-frequencies", methods=["GET"])
    def get_hardware_known_alarm_frequencies():
        """
        GET /hardware-known-alarm-frequencies?model=PL1行星轮
        根据 model 获取对应的 transfer_speed_coefficient
        """
        model = request.args.get("model", type=str)
        if not model:
            return jsonify({"error": "missing model"}), 400

        doc = collection.find_one({"model": model})
        if not doc:
            return jsonify({"error": "data not found"}), 404

        # 不返回 _id
        if "_id" in doc:
            del doc["_id"]

        return jsonify(doc), 200

    @app.route("/hardware-known-alarm-frequencies", methods=["POST"])
    def update_hardware_known_alarm_frequencies():
        """
        POST /hardware-known-alarm-frequencies
        接收 JSON, 更新/插入指定 model 对应的 transfer_speed_coefficient

        示例请求体:
        {
          "model": "PL1行星轮",
          "transfer_speed_coefficient": 200.0
        }
        """
        data = request.get_json()
        if not data:
            return jsonify({"error": "invalid request body"}), 400

        model = data.get("model")
        coef = data.get("transfer_speed_coefficient")

        if not model:
            return jsonify({"error": "missing model"}), 400
        if coef is None:
            return jsonify({"error": "missing transfer_speed_coefficient"}), 400

        query = {"model": model}
        update_data = {"$set": {"transfer_speed_coefficient": float(coef)}}

        result = collection.update_one(query, update_data, upsert=True)
        if result.acknowledged:
            return jsonify({"message": "update success"}), 200
        else:
            return jsonify({"error": "db operation failed"}), 500
