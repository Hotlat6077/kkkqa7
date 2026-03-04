# routes_threshold_data_sync.py
from flask import request, jsonify
from .update_threshold_data import update_threshold_data

def init_threshold_data_sync_routes(app, db):
    """
    注册 'threshold-data-sync' 相关路由
    :param app: Flask 实例
    :param db: 已初始化好的 MongoDB 数据库实例
    """
    @app.route("/threshold-data-sync", methods=["POST"])
    def threshold_data_sync():
        """
        POST /threshold-data-sync

        用于触发阈值同步逻辑 (update_threshold_data)，
        可选参数: group, machine
        """
        # 从 Query String 获取可选参数 group, machine
        # 也可改为从 JSON Body 获取
        group = request.args.get("group", type=int)
        machine = request.args.get("machine", type=int)

        try:
            update_threshold_data(db, group=group, machine=machine)
            return jsonify({"message": "threshold_data sync success"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
