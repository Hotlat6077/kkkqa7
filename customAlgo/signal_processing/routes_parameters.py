# routes_parameters.py

from flask import request, jsonify

def init_parameters_routes(app, db):
    """
    注册 parameters 相关路由
    :param app: Flask 实例
    :param db:  已初始化好的 MongoDB 数据库实例
    """
    collection = db["parameters"]

    @app.route("/parameters", methods=["GET"])
    def get_parameters():
        """
        GET /parameters?model=PL1行星轮
        根据 model 获取对应的 transfer_speed_coefficient
        """
        model = request.args.get("model", type=str)
        if not model:
            return jsonify({"error": "missing model"}), 400

        doc = collection.find_one({"model": model})
        if not doc:
            return jsonify({"error": "data not found"}), 404

        # 移除 _id，不返回给前端
        if "_id" in doc:
            del doc["_id"]

        return jsonify(doc), 200

    @app.route("/parameters", methods=["POST"])
    def update_parameters():
        """
        POST /parameters
        接收 JSON, 写入或更新指定 model 对应的 transfer_speed_coefficient
        示例请求体:
        {
          "model": "PL1行星轮",
          "transfer_speed_coefficient": 123.456
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

        # upsert=True: 若数据不存在则新建，存在则更新
        query = {"model": model}
        update_data = {"$set": {"transfer_speed_coefficient": float(coef)}}

        result = collection.update_one(query, update_data, upsert=True)
        if result.acknowledged:
            return jsonify({"message": "update success"}), 200
        else:
            return jsonify({"error": "db operation failed"}), 500
