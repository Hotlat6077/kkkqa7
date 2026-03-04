from __future__ import annotations
from typing import Any

from flask import request, jsonify
from datetime import datetime
from loguru import logger
import sys
import math

from pymongo import UpdateOne

logger.remove()
logger.add(sys.stderr, level="DEBUG")


# 曹学勇修补
def init_machine_thresholds_routes_fix(app, db):
    """
    在一个文件中，提供三个路由：
      1) GET /machine-thresholds?group=&machine=      => 查询压缩机测点阈值
      2) POST /machine-thresholds                    => 接收 points 数组，更新(或插入)某台压缩机的多个测点阈值
      3) POST /machine-thresholds/apply-sync         => 读取已有阈值并按 machine/group/farm 批量套用后，自动同步到 threshold_data
    """
    machine_data = db["machine_data"]  # 同步压缩机
    threshold_data = db["threshold_data"]  # 同步时会用到
    sensor_data = db["sensor_data"]  # 全部的测点

    # -----------------------------------------------------------------------
    # 1) GET /machine-thresholds?group=1&machine=2 查询
    # -----------------------------------------------------------------------
    @app.route("/machine-thresholds", methods=["GET"])
    def get_machine_thresholds():
        logger.info("[GET /machine-thresholds] Received request-1")
        
        group = request.args.get("group")
        machine = request.args.get("machine")
        if group is None or machine is None:
            return jsonify({"code": 400, "error": "missing group or machine"})

        group = group.split("_")[-1]
        machine = machine.split("_")[-1]
        # 查询这个加氢站-压缩机下面全部的测点
        sensors = list(sensor_data.find({"componentID": f"CO_{group}_{machine}_1"}))
        if len(sensors) == 0:
            return jsonify({"code": 300, "error": "data not found"})
        # 重新组装一个新的表格
        sensor_new = []
        for sensor in sensors:
            one_data = find_threshold_data(sensorID=sensor["sensorID"])
            ns = {
                "sensorID": sensor["sensorID"],
                "sensorName": sensor["name"],
                "typeName": sensor["equipkind"],
                "eigenData": {
                    "rms": get_value(one_data, "rms", [0, 0]),  # 均方根
                    "kur": get_value(one_data, "kur", [0, 0]),  # 鞘度
                    "std": get_value(one_data, "std", [0, 0]),  # 标准差
                    "peak": get_value(one_data, "peak", [0, 0]),  # 加速度峰值
                    "impulse": get_value(one_data, "impulse", [0, 0]),  # 脉冲
                    "temperature": get_value(one_data, "temperature", [0, 0]),  # 温度
                    "pressure": get_value(one_data, "pressure", [0, 0]),  # 压力
                    "rpm": get_value(one_data, "rpm", [0, 0]),  # 均转速
                    "speed_rms": get_value(one_data, "speed_rms", [0, 0]),  # 速度有效值
                }
            }
            sensor_new.append(ns)
        return jsonify({"code": 200, "data": sensor_new})

    # -----------------------------------------------------------------------
    # 2) POST /machine-thresholds 设置情况
    # -----------------------------------------------------------------------
    @app.route("/machine-thresholds", methods=["POST"])
    def update_machine_thresholds():
        data = request.get_json()
        if not data:
            logger.warning("[POST /machine-thresholds] No valid JSON in request")
            return jsonify({"code": 300, "error": "invalid request body"})
        # 处理数据
        list_data = data["list"]
        docs = []
        for one_data in list_data:
            sensor_id = one_data["sensorID"]
            docs.append(add_threshold_data(sensor_id, one_data))

        # 在阈值数据这个表中
        threshold_data.create_index("sensorID", unique=True)
        result = threshold_data.bulk_write(docs)

        if len(result.upserted_ids) >= 1 or result.matched_count >= 1 or result.modified_count >= 1:
            return jsonify({"code": 200, "message": "add success"})
        else:
            return jsonify({"code": 300, "message": "添加失败"})

    # -----------------------------------------------------------------------
    # 3) POST /machine-thresholds/apply-sync
    # -----------------------------------------------------------------------
    @app.route("/machine-thresholds/apply-sync", methods=["POST"])
    def apply_and_sync_thresholds():
        data = request.get_json()
        if not data:
            logger.warning("[POST /machine-thresholds] No valid JSON in request")
            return jsonify({"code": 300, "error": "invalid request body"})
        # 找到本站全部的压缩机
        groupID = data["groupID"]
        if groupID == "-1":
            list_machine = machine_data.find(filter={"groupID": groupID})
        else:
            list_machine = machine_data.find(filter={})


        list_data = data["list"]
        docs = []
        for machine in list_machine:
            for one_data in list_data:
                ##设备ID
                machine_id = machine["machineID"]
                new_mid = machine_id[3:]
                sensor_id = one_data["sensorID"]
                sensor_id1 = sensor_id[0:2]
                sensor_id2 = sensor_id[7:]
                nsid = f"{sensor_id1}_{new_mid}_{sensor_id2}"
                # print(nsid)
                docs.append(add_threshold_data(nsid, one_data))

        # 在阈值数据这个表中
        threshold_data.create_index("sensorID", unique=True)
        result = threshold_data.bulk_write(docs)

        if len(result.upserted_ids) >= 1 or result.matched_count >= 1 or result.modified_count >= 1:
            return jsonify({"code": 200, "message": "同步成功"})
        else:
            return jsonify({"code": 300, "message": "同步失败"})



    # 查询阈值数据表
    def find_threshold_data(sensorID: str):
        data = threshold_data.find_one({"sensorID": sensorID})
        return data

    # 获取值
    def get_value(data: dict, key: str, val: Any):
        if data is None or key not in data:
            return val
        return data[key]

    # 添加阈值数据
    def add_threshold_data(sensor_id: str, one_data: dict):
        sensors = sensor_id.split("_")
        # 要添加的数据
        add_data = {
            "update_time": datetime.now(),
            "group": int(sensors[1]),
            "machine": int(sensors[2]),
            "component": int(sensors[3]),
            "sensor": int(sensors[4]),
            "sensorID": sensor_id,
            "rms": one_data["rms"],  # 均方根
            "kur": one_data["kur"],  # 鞘度
            "std": one_data["std"],  # 标准差
            "peak": one_data["peak"],  # 加速度峰值
            "impulse": one_data["impulse"],  # 脉冲
            "temperature": one_data["temperature"],  # 温度
            "pressure": one_data["pressure"],  # 压力
            "rpm": one_data["rpm"],  # 均转速
            "speed_rms":one_data["speed_rms"],  # 速度有效值
        }
        return UpdateOne({"sensorID": sensor_id}, {"$set": add_data}, upsert=True)


# 这个是老的方法--
def init_machine_thresholds_routes(app, db):
    """
    在一个文件中，提供三个路由：
      1) GET /machine-thresholds?group=&machine=      => 查询压缩机测点阈值
      2) POST /machine-thresholds                    => 接收 points 数组，更新(或插入)某台压缩机的多个测点阈值
      3) POST /machine-thresholds/apply-sync         => 读取已有阈值并按 machine/group/farm 批量套用后，自动同步到 threshold_data
    """
    coll_thresholds = db["machine_thresholds"]
    coll_data = db["threshold_data"]  # 同步时会用到
    collection = db["machine_thresholds"]  # 原有代码保留，但在POST中不再使用

    # -----------------------------------------------------------------------
    # 1) GET /machine-thresholds?group=1&machine=2 查询
    # -----------------------------------------------------------------------
    # @app.route("/machine-thresholds", methods=["GET"])
    # def get_machine_thresholds():
        
    #     logger.info("[GET /machine-thresholds] Received request-2")
    #     group = request.args.get("group")
    #     machine = request.args.get("machine")
    #     if group is None or machine is None:
    #         return jsonify({"code": 400, "error": "missing group or machine"})

    #     group = group.split("_")[-1]
    #     machine = machine.split("_")[-1]

    #     docs = list(coll_thresholds.find({"group": group, "machine": machine}))
    #     if not docs:
    #         return jsonify({"code": 300, "error": "data not found"})

    #     for d in docs:
    #         d.pop("_id", None)  # 去掉 _id 字段

    #     return jsonify({"code": 200, "data": docs})

    # -----------------------------------------------------------------------
    # 2) POST /machine-thresholds 设置情况
    # -----------------------------------------------------------------------
    @app.route("/machine-thresholds", methods=["POST"])
    def update_machine_thresholds():
        data = request.get_json()
        logger.debug(f"[POST /machine-thresholds] Received JSON: {data}")

        if not data:
            logger.warning("[POST /machine-thresholds] No valid JSON in request")
            return jsonify({"error": "invalid request body"}), 400

        try:
            group = int(data["group"])
            machine = int(data["machine"])
        except (KeyError, ValueError, TypeError):
            return jsonify({"error": "invalid group or machine"}), 400

        logger.info(f"[POST /machine-thresholds] group={group}, machine={machine}")

        if group is None or machine is None:
            logger.warning("[POST /machine-thresholds] Missing 'group' or 'machine' in request body")
            return jsonify({"error": "missing group or machine"}), 400

        points_data = data.get("points", [])
        if not isinstance(points_data, list):
            logger.warning("[POST /machine-thresholds] 'points' must be a list")
            return jsonify({"error": "points must be a list"}), 400

        def merge_dict(base, updates):
            for k, v in updates.items():
                if isinstance(v, dict) and isinstance(base.get(k), dict):
                    merge_dict(base[k], v)
                else:
                    base[k] = v

        for pd in points_data:
            pt = pd.get("point")
            if not pt:
                logger.warning("[POST /machine-thresholds] A point entry is missing 'point' key, skipped.")
                continue

            logger.debug(f"[POST /machine-thresholds] Processing point={pt}")

            query = {
                "group": group,
                "machine": machine,
                "point": pt
            }

            existing_doc = collection.find_one(query)
            logger.debug(f"[POST /machine-thresholds] Existing doc: {existing_doc}")

            if existing_doc:
                existing_thr = existing_doc.get("thr", {})
                new_thr = pd.get("thr", {})
                merge_dict(existing_thr, new_thr)
                pd["thr"] = existing_thr

            update_data = {"$set": pd}
            result = collection.update_one(query, update_data, upsert=True)
            logger.debug(
                f"[POST /machine-thresholds] Upsert result matched={result.matched_count}, "
                f"modified={result.modified_count}, upserted_id={result.upserted_id}"
            )

        logger.info("[POST /machine-thresholds] Update success")
        return jsonify({"message": "update success"}), 200

    # -----------------------------------------------------------------------
    # 3) POST /machine-thresholds/apply-sync
    # -----------------------------------------------------------------------
    @app.route("/machine-thresholds/apply-sync", methods=["POST"])
    def apply_and_sync_thresholds():
        data = request.get_json()
        if not data:
            return jsonify({"error": "invalid request body"}), 400

        try:
            group = int(data["group"])
            machine = int(data["machine"])
        except (KeyError, ValueError, TypeError):
            return jsonify({"error": "invalid group or machine"}), 400

        apply_scope = data.get("apply_scope")
        if group is None or machine is None or not apply_scope:
            return jsonify({"error": "missing group, machine or apply_scope"}), 400
        if apply_scope not in ["machine", "group", "farm"]:
            return jsonify({"error": "apply_scope must be 'machine','group' or 'farm'"}), 400

        # 1) 读取 (group,machine) 阈值文档
        current_docs = list(coll_thresholds.find({"group": group, "machine": machine}))
        if not current_docs:
            return jsonify({"error": "no threshold data found for this machine"}), 404

        now_str = datetime.now().isoformat()

        # 用来收集所有受影响的 (group,machine)
        affected_pairs = set()

        # 2) 复制到目标范围
        try:
            if apply_scope == "machine":
                # 仅覆盖自身
                affected_pairs.add((group, machine))

            elif apply_scope == "group":
                all_machines = coll_thresholds.distinct("machine", {"group": group})
                for target_m in all_machines:
                    for doc in current_docs:
                        pt = doc["point"]
                        thr = doc.get("thr", {})
                        doc_update_date = doc.get("update_date", now_str)
                        query_group = {
                            "group": group,
                            "machine": target_m,
                            "point": pt
                        }
                        update_group = {
                            "$set": {
                                "thr": thr,
                                "point": pt,
                                "update_date": doc_update_date,
                                "group": group,
                                "machine": target_m
                            }
                        }
                        coll_thresholds.update_one(query_group, update_group, upsert=True)
                    affected_pairs.add((group, target_m))

            elif apply_scope == "farm":
                all_groups = coll_thresholds.distinct("group")
                for g in all_groups:
                    all_machines_in_g = coll_thresholds.distinct("machine", {"group": g})
                    for target_m in all_machines_in_g:
                        for doc in current_docs:
                            pt = doc["point"]
                            thr = doc.get("thr", {})
                            doc_update_date = doc.get("update_date", now_str)
                            query_farm = {
                                "group": g,
                                "machine": target_m,
                                "point": pt
                            }
                            update_farm = {
                                "$set": {
                                    "thr": thr,
                                    "point": pt,
                                    "update_date": doc_update_date,
                                    "group": g,
                                    "machine": target_m
                                }
                            }
                            coll_thresholds.update_one(query_farm, update_farm, upsert=True)
                        affected_pairs.add((g, target_m))

        except Exception as e:
            return jsonify({"error": "db operation failed", "details": str(e)}), 500

        # 3) 同步到 threshold_data
        try:
            for (g, m) in affected_pairs:
                logger.debug(f"update_threshold_data for group={g}, machine={m}")
                update_threshold_data(db, group=g, machine=m)
        except Exception as e:
            return jsonify({"error": f"sync to threshold_data failed: {e}"}), 500

        return jsonify({"message": "apply & sync success"}), 200

    # -----------------------------------------------------------------------
    # 内部函数: 将 machine_thresholds -> threshold_data
    # 修改逻辑：根据 sensorID 和 model 删除老的数据，然后写入新的数据，不再使用 $unset/$set 操作
    # -----------------------------------------------------------------------
    def update_threshold_data(db, group=None, machine=None):
        time_keys = ["rms", "kur", "std", "peak", "speed_rms", "impulse"]

        # 针对 3V/4V/5V 做固定映射：inner -> PL1_inner / race -> race1 ... 等
        fixed_mappings_by_point = {
            "1V": {},
            "2V": {},
            "8H": {},
            "9H": {},
            "3V": {
                "race": "race1",
                "inner": "PL1_inner",
                "outer": "PL1_outer",
                "ball": "PL1_ball",
                "cage": "PL1_cage"
            },
            "4V": {
                "race": "race1",
                "inner": "PL1_inner",
                "outer": "PL1_outer",
                "ball": "PL1_ball",
                "cage": "PL1_cage"
            },
            "5V": {
                "race": "race2",
                "inner": "PL2_inner",
                "outer": "PL2_outer",
                "ball": "PL2_ball",
                "cage": "PL2_cage"
            }
            # 6A / 7V 后面单独处理
        }

        point_map = {
            "1V": (1, 1),
            "2V": (1, 2),
            "3V": (2, 1),
            "4V": (2, 2),
            "5V": (2, 3),
            "6A": (2, 4),
            "7V": (2, 5),
            "8H": (3, 1),
            "9H": (3, 2)
        }

        def to_float(x):
            try:
                return float(x)
            except (ValueError, TypeError):
                return None

        coll_thresholds = db["machine_thresholds"]
        coll_data = db["threshold_data"]

        find_q = {}
        if group is not None:
            find_q["group"] = group
        if machine is not None:
            find_q["machine"] = machine

        cursor = coll_thresholds.find(find_q)
        for doc in cursor:
            g = doc["group"]
            m = doc["machine"]
            p = doc["point"]
            if p not in point_map:
                continue

            comp, sens = point_map[p]
            thr_obj = doc.get("thr", {})
            if not isinstance(thr_obj, dict):
                continue

            doc_thr_update = doc.get("update_date")
            now_str = datetime.now().isoformat()
            final_update_date = doc_thr_update if doc_thr_update else now_str

            # 修复 sensorID 写入错误，将 group、machine、comp、sens 均转换为整数
            sensorID = doc.get("sensorID")
            if not sensorID:
                sensorID = f"SE_{int(g)}_{int(m)}_{int(comp)}_{int(sens)}"

            # ---------------- 处理 6 个时域键 ----------------
            for tk in time_keys:
                sub_val = thr_obj.get(tk)
                if sub_val is None:
                    continue

                w = None
                f_val = None
                if isinstance(sub_val, dict):
                    w = to_float(sub_val.get("warning"))
                    f_val = to_float(sub_val.get("fault"))
                else:
                    w = to_float(sub_val)
                    f_val = None

                if w is None and f_val is None:
                    continue

                query_time = {
                    "group": g,
                    "machine": m,
                    "component": comp,
                    "sensor": sens,
                    "model": tk,
                    "sensorID": sensorID
                }
                # 删除旧数据
                coll_data.delete_one(query_time)
                new_thr = {"update_date": final_update_date}
                if w is not None and not math.isnan(w):
                    new_thr["warning"] = w
                if f_val is not None and not math.isnan(f_val):
                    new_thr["fault"] = f_val
                new_doc = {
                    "group": g,
                    "machine": m,
                    "component": comp,
                    "sensor": sens,
                    "sensorID": sensorID,
                    "model": tk,
                    "thr": new_thr
                }
                coll_data.insert_one(new_doc)

            # ---------------- 处理故障类 (model="fault") ----------------
            fault_data = {}
            base_mapping = fixed_mappings_by_point.get(p, {})
            for k_in_thr, v_in_thr in thr_obj.items():
                if k_in_thr in time_keys or k_in_thr == "update_date":
                    continue

                w = None
                f_val = None
                if isinstance(v_in_thr, dict):
                    w = to_float(v_in_thr.get("warning"))
                    f_val = to_float(v_in_thr.get("fault"))
                    if w is None and f_val is None:
                        continue
                else:
                    w = to_float(v_in_thr)
                    f_val = None
                    if w is None or math.isnan(w):
                        continue

                # 针对 6A 和 7V 点的特殊处理
                if p == "6A":
                    if k_in_thr in ["inner", "outer", "ball", "cage"]:
                        final_keys = [f"HIS_{k_in_thr}", f"HSS_{k_in_thr}"]
                    else:
                        final_keys = [k_in_thr]
                elif p == "7V":
                    if k_in_thr in ["inner", "outer", "ball", "cage"]:
                        final_keys = [f"HSS_{k_in_thr}"]
                    else:
                        final_keys = [k_in_thr]
                else:
                    final_key = base_mapping.get(k_in_thr, k_in_thr)
                    final_keys = [final_key]

                for fk in final_keys:
                    if fk not in fault_data:
                        fault_data[fk] = {}
                    if w is not None and not math.isnan(w):
                        fault_data[fk]["warning"] = w
                    if f_val is not None and not math.isnan(f_val):
                        fault_data[fk]["fault"] = f_val
            if fault_data:
                fault_data["update_date"] = final_update_date
                query_fault = {
                    "group": g,
                    "machine": m,
                    "component": comp,
                    "sensor": sens,
                    "model": "fault",
                    "sensorID": sensorID
                }
                coll_data.delete_one(query_fault)
                new_doc_fault = {
                    "group": g,
                    "machine": m,
                    "component": comp,
                    "sensor": sens,
                    "sensorID": sensorID,
                    "model": "fault",
                    "thr": fault_data
                }
                coll_data.insert_one(new_doc_fault)
