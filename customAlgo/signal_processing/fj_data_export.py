# fj_data_export.py
# -*- coding: utf-8 -*-

import os
import re
import datetime
import shutil
import zipfile
import json

from flask import request, jsonify, send_file
from loguru import logger

###############################################################################
# 全局变量：外部传入的 db，以及缓存的字典
###############################################################################
db = None  # 将在 init_fj_data_export(app, passed_db) 中赋值

group_map     = {}
machine_map   = {}
component_map = {}
sensor_map    = {}

###############################################################################
# 波形类型与目录映射(双向)
###############################################################################
wave_type_to_dir = {
    "16k速度波形":       "16k速度波形",
    "128k加速度波形2k":  "128k加速度波形",
    "128k加速度波形10k": "256k加速度波形"
}
dir_to_wave_type = {
    "16k速度波形":       "16k速度波形",
    "128k加速度波形":    "128k加速度波形2k",
    "256k加速度波形":    "128k加速度波形10k"
}

###############################################################################
# 一次性加载数据库缓存
###############################################################################
def load_db_cache():
    global group_map, machine_map, component_map, sensor_map, db

    # group_data
    tmp_group_map = {}
    for doc in db["group_data"].find({}):
        gid   = doc.get("groupID")  # e.g. "GR_1"
        gname = doc.get("name", "")
        if gid and gid.startswith("GR_"):
            group_no = gid.replace("GR_", "")
            tmp_group_map[group_no] = gname
    group_map.update(tmp_group_map)

    # machine_data
    tmp_machine_map = {}
    pat_machine = re.compile(r"MA_(\d+)_(\d+)")
    machine_docs = list(db["machine_data"].find({}))
    for doc in machine_docs:
        mid   = doc.get("machineID")  # e.g. "MA_1_1"
        mname = doc.get("name", "")
        if mid:
            mm = pat_machine.match(mid)
            if mm:
                gno, mno = mm.groups()
                tmp_machine_map[(gno, mno)] = mname
    machine_map.update(tmp_machine_map)

    # component_data
    tmp_component_map = {}
    pat_comp = re.compile(r"CO_(\d+)_(\d+)_(\d+)")
    component_docs = list(db["component_data"].find({}))
    for doc in component_docs:
        cid   = doc.get("componentID")
        cname = doc.get("name", "")
        if cid:
            mc = pat_comp.match(cid)
            if mc:
                gno, mno, cno = mc.groups()
                tmp_component_map[(gno, mno, cno)] = cname
    component_map.update(tmp_component_map)

    # sensor_data
    tmp_sensor_map = {}
    pat_sens = re.compile(r"SE_(\d+)_(\d+)_(\d+)_(\d+)")
    sensor_docs = list(db["sensor_data"].find({}))
    for doc in sensor_docs:
        sid   = doc.get("sensorID")
        sname = doc.get("name", "")
        if sid:
            ms = pat_sens.match(sid)
            if ms:
                gno, mno, cno, sno = ms.groups()
                tmp_sensor_map[(gno, mno, cno, sno)] = sname
    sensor_map.update(tmp_sensor_map)

###############################################################################
# 工具函数：速度范围过滤
###############################################################################
def speed_in_range(speed_value, speed_range_list):
    """speed_range_list 为空表示不限制"""
    if not speed_range_list:
        return True
    low  = speed_range_list[0] if len(speed_range_list) > 0 else None
    high = speed_range_list[1] if len(speed_range_list) > 1 else None
    if low is not None and high is not None:
        return (speed_value >= low) and (speed_value < high)
    elif low is not None and high is None:
        return speed_value >= low
    elif low is None and high is not None:
        return speed_value < high
    else:
        return True

###############################################################################
# 路由函数：主导出逻辑
###############################################################################
def export_data():
    """
    POST /export_data
    {
      "start_date": "2025-01-06",
      "end_date": "2025-01-06",
      "group_id": "GR_1",
      "machine_id": ["MA_1_1", "MA_1_2", "MA_1_3", "MA_1_4"],
      "speed_range": [],
      "wave_type": ["16k速度波形", "128k加速度波形10k"],
      "file_type": "csv"
    }
    """

    data = request.get_json() or {}
    logger.debug(f"Request JSON: {data}")

    wave_types      = data.get("wave_type", [])
    start_date      = data.get("start_date")
    end_date        = data.get("end_date")
    group_id        = data.get("group_id")
    machine_id_list = data.get("machine_id", [])
    speed_range     = data.get("speed_range", [])
    file_type       = data.get("file_type")

    # === 1) 参数校验
    missing_params = []
    if not start_date:
        missing_params.append("start_date")
    if not end_date:
        missing_params.append("end_date")
    if not group_id:
        missing_params.append("group_id")
    if not machine_id_list:
        missing_params.append("machine_id")
    if not file_type:
        missing_params.append("file_type")

    if missing_params:
        msg_detail = ", ".join(missing_params)
        logger.warning(f"Missing parameters: {msg_detail}")
        return jsonify({"code": 400, "msg": f"缺少必要参数: {msg_detail}"}), 400

    if file_type not in ["txt", "csv"]:
        logger.warning(f"Unsupported file_type: {file_type}")
        return jsonify({"code": 400, "msg": "file_type 仅支持 txt 或 csv"}), 400

    # === 2) 日期解析
    try:
        start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_dt   = datetime.datetime.strptime(end_date,   "%Y-%m-%d")
        if start_dt > end_dt:
            logger.warning(f"Invalid date range: {start_date} - {end_date}")
            return jsonify({"code": 400, "msg": "开始日期不能大于结束日期"}), 400
    except:
        logger.exception("日期解析错误:")
        return jsonify({"code": 400, "msg": "日期格式错误，应为YYYY-MM-DD"}), 400

    # === 3) 路径检查
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    base_dir   = os.path.join(parent_dir, "data", "fj_local")
    logger.debug(f"Calculated base_dir: {base_dir}")
    if not os.path.isdir(base_dir):
        logger.error(f"Data directory not found: {base_dir}")
        return jsonify({"code": 500, "msg": f"数据目录不存在: {base_dir}"}), 500

    # 提取 group_no （可能会用到）
    group_no = group_id.replace("GR_", "")

    # === 4) 针对发电机的“8、9测点”（即组件=3、测点=1或2），先收集有效的【时间戳sample_time】
    # key: (machineID, date_str) => set of valid sample_time
    valid_sample_times_map = {}

    day_count = (end_dt - start_dt).days + 1
    for d in range(day_count):
        cur_date = start_dt + datetime.timedelta(days=d)
        date_str = cur_date.strftime("%Y%m%d")

        for mid in machine_id_list:
            pat_machine = re.compile(r"MA_(\d+)_(\d+)")
            mm = pat_machine.match(mid)
            if not mm:
                continue
            gno, mno = mm.groups()

            machine_path = os.path.join(base_dir, gno, mno)
            if not os.path.isdir(machine_path):
                continue

            # 压缩机的 发电机组件=3
            cno = "3"
            cno_path = os.path.join(machine_path, cno)
            if not os.path.isdir(cno_path):
                continue

            # 发电机下的 8测点/9测点 => 其实对应 sno=1, sno=2
            # （源需求里说 “8、9测点”，示例目录是 1/1/3/1、1/1/3/2）
            candidate_snos = ["1", "2"]

            cur_valid_times = set()

            for sno in candidate_snos:
                sno_path = os.path.join(cno_path, sno)
                if not os.path.isdir(sno_path):
                    continue

                # 如果 wave_type 不为空，则只遍历 wave_type 对应目录
                if wave_types:
                    wave_dir_list = []
                    for wt in wave_types:
                        if wt in wave_type_to_dir:
                            wave_dir_list.append(wave_type_to_dir[wt])
                        else:
                            logger.warning(f"Unrecognized wave type: {wt}, skip.")
                else:
                    # 如果 wave_type 为空，遍历所有子目录
                    wave_dir_list = [
                        sub for sub in os.listdir(sno_path)
                        if os.path.isdir(os.path.join(sno_path, sub))
                    ]

                for wave_dir in wave_dir_list:
                    wave_path = os.path.join(sno_path, wave_dir)
                    if not os.path.isdir(wave_path):
                        continue

                    # 遍历文件，找出文件名中包含当前 date_str 的，并且符合速度范围
                    for root, dirs, files in os.walk(wave_path):
                        for fname in files:
                            if date_str not in fname:
                                continue
                            full_path = os.path.join(root, fname)
                            if not os.path.isfile(full_path):
                                continue

                            # 文件名形如:  0_20250102165600%0.00.txt
                            part_a, _ = os.path.splitext(fname)
                            if '%' not in part_a:
                                continue
                            try:
                                left_part, speed_str = part_a.split('%', 1)
                                speed_val = float(speed_str)
                            except:
                                continue

                            # 判断速度是否在范围内
                            if speed_in_range(speed_val, speed_range):
                                # 提取采样时间
                                # left_part 示例: 0_20250102165600
                                left_arr = left_part.split('_')
                                if len(left_arr) < 2:
                                    continue
                                sample_time = left_arr[1]
                                cur_valid_times.add(sample_time)

            if cur_valid_times:
                valid_sample_times_map[(mid, date_str)] = cur_valid_times

    # === 5) 根据 valid_sample_times_map，遍历所有传感器文件，并收集
    found_files = []
    for d in range(day_count):
        cur_date = start_dt + datetime.timedelta(days=d)
        date_str = cur_date.strftime("%Y%m%d")

        for mid in machine_id_list:
            pat_machine = re.compile(r"MA_(\d+)_(\d+)")
            mm = pat_machine.match(mid)
            if not mm:
                continue
            gno, mno = mm.groups()

            machine_path = os.path.join(base_dir, gno, mno)
            if not os.path.isdir(machine_path):
                continue

            # 如果在 valid_sample_times_map 中没记录，则说明该压缩机当日没有符合速度的采样时间
            key_for_valid = (mid, date_str)
            if key_for_valid not in valid_sample_times_map:
                # 说明该压缩机这天没有符合速度要求的“8/9测点”数据 => 整台压缩机当日都不导出
                continue

            valid_times_set = valid_sample_times_map[key_for_valid]

            # 第3层 component_no
            cno_list = [
                cdir for cdir in os.listdir(machine_path)
                if os.path.isdir(os.path.join(machine_path, cdir))
            ]
            for cno in cno_list:
                cno_path = os.path.join(machine_path, cno)
                if not os.path.isdir(cno_path):
                    continue

                # 第4层 sensor_no
                sno_list = [
                    sdir for sdir in os.listdir(cno_path)
                    if os.path.isdir(os.path.join(cno_path, sdir))
                ]
                for sno in sno_list:
                    sno_path = os.path.join(cno_path, sno)
                    if not os.path.isdir(sno_path):
                        continue

                    # 处理波形目录
                    if wave_types:
                        wave_dir_list = []
                        for wt in wave_types:
                            if wt in wave_type_to_dir:
                                wave_dir_list.append(wave_type_to_dir[wt])
                            else:
                                logger.warning(f"Unrecognized wave type: {wt}, skip.")
                    else:
                        wave_dir_list = [
                            sub for sub in os.listdir(sno_path)
                            if os.path.isdir(os.path.join(sno_path, sub))
                        ]

                    for wave_dir in wave_dir_list:
                        wave_path = os.path.join(sno_path, wave_dir)
                        if not os.path.isdir(wave_path):
                            continue

                        # 深度遍历 wave_path
                        for root, dirs, files in os.walk(wave_path):
                            for fname in files:
                                if date_str not in fname:
                                    continue
                                full_path = os.path.join(root, fname)
                                if not os.path.isfile(full_path):
                                    continue

                                part_a, _ = os.path.splitext(fname)
                                if '%' not in part_a:
                                    continue

                                # 拆分，拿到采样时间
                                left_part, speed_str = part_a.split('%', 1)
                                left_arr = left_part.split('_')
                                if len(left_arr) < 2:
                                    continue
                                sample_time = left_arr[1]

                                # 如果采样时间在 valid_times_set，则说明“8/9测点”已有一个满足速度
                                # => 当前整台压缩机该采样时间的所有测点都应导出
                                if sample_time in valid_times_set:
                                    found_files.append(full_path)

    # 若无结果
    if not found_files:
        return jsonify({
            "code": 200,
            "msg": "未找到符合条件的文件",
            "files": []
        })

    # === 6) 复制 & 重命名 => 临时目录
    temp_dir = os.path.join(script_dir, "temp_export")
    os.makedirs(temp_dir, exist_ok=True)
    logger.debug(f"Created/using temp_dir: {temp_dir}")

    copied_files = []
    for fpath in found_files:
        rel_path = os.path.relpath(fpath, base_dir)
        parts    = rel_path.split(os.sep)
        if len(parts) < 6:
            logger.warning(f"Unexpected file path structure: {rel_path}")
            continue

        gno    = parts[0]
        mno    = parts[1]
        cno    = parts[2]
        sno    = parts[3]
        wave_d = parts[4]
        fname  = parts[5]

        # 映射库
        gname  = group_map.get(gno, f"未知加氢站{gno}")
        mname  = machine_map.get((gno, mno), f"未知压缩机{gno}_{mno}")
        cname_ = component_map.get((gno, mno, cno), f"未知组件{gno}_{mno}_{cno}")
        sname_ = sensor_map.get((gno, mno, cno, sno), f"未知测点{gno}_{mno}_{cno}_{sno}")

        wave_name = dir_to_wave_type.get(wave_d, wave_d)

        part_a, ext = os.path.splitext(fname)
        if '%' not in part_a:
            logger.warning(f"File name lacks '%': {fname}")
            continue

        left_part, speed_str = part_a.split('%', 1)
        left_arr = left_part.split('_')
        if len(left_arr) < 2:
            logger.warning(f"File name structure not recognized: {fname}")
            continue

        sample_time = left_arr[1]

        new_ext = f".{file_type}"
        new_fname = f"{gname}_{mname}_{cname_}_{sname_}_{wave_name}_{speed_str}_{sample_time}{new_ext}"

        new_path = os.path.join(temp_dir, new_fname)

        try:
            shutil.copy2(fpath, new_path)
            copied_files.append(new_path)
        except Exception as e:
            logger.exception(f"Failed to copy file: {fpath}")
            continue

    if not copied_files:
        return jsonify({
            "code": 200,
            "msg": "文件符合检索条件，但重命名/复制阶段全部失败或跳过",
            "files": []
        })

    # === 7) 打包 ZIP (只存储, 不压缩)
    download_dir = os.path.join(parent_dir, "static", "download")
    os.makedirs(download_dir, exist_ok=True)

    zip_filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".zip"
    zip_path = os.path.join(download_dir, zip_filename)
    try:
        with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_STORED) as zf:
            for cf in copied_files:
                arcname = os.path.basename(cf)
                zf.write(cf, arcname=arcname)
    except Exception as e:
        logger.exception("Error during zip creation:")
        return jsonify({"code": 500, "msg": f"打包文件时出现错误: {str(e)}"}), 500

    # 新增代码：清理导出目录中超过1个月的文件
    cleanup_old_exports(download_dir)

    # 清理临时文件
    for cf in copied_files:
        try:
            os.remove(cf)
        except:
            logger.exception(f"Failed to remove temp file: {cf}")

    rel_download_path = f"/static/download/{zip_filename}"

    # === 8) 记录导出日志到 MongoDB 的 export_data_logs 集合
    username = ""  # 不记录用户名
    export_fields_dict = {
        "start_date":     start_date,
        "end_date":       end_date,
        "group_id":       group_id,
        "machine_id":     machine_id_list,
        "speed_range":    speed_range,
        "wave_type":      wave_types,
        "file_type":      file_type
    }
    export_fields_str = json.dumps(export_fields_dict, ensure_ascii=False)

    log_doc = {
        "username":       username,
        "export_fields":  export_fields_str,
        "export_url":     rel_download_path,
        "timestamp":      datetime.datetime.utcnow()
    }

    try:
        db["export_data_logs"].insert_one(log_doc)
    except Exception as e:
        logger.exception("Failed to insert export log:")

    # === 9) 返回成功信息
    return jsonify({
        "code": 200,
        "msg": "OK",
        "download_url": rel_download_path
    })

def download_file(filename):
    """
    GET /download/<filename>
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path  = os.path.join(script_dir, "static", "download", filename)

    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"code": 404, "msg": "文件不存在"}), 404

def cleanup_old_exports(download_dir):
    """
    清理 download_dir 目录中导出时间超过1个月的导出文件，
    防止数据文件过多占用磁盘空间。
    """
    now = datetime.datetime.now()
    one_month_ago = now - datetime.timedelta(days=30)
    for fname in os.listdir(download_dir):
        file_path = os.path.join(download_dir, fname)
        if os.path.isfile(file_path):
            # 获取文件的最后修改时间
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if mtime < one_month_ago:
                try:
                    os.remove(file_path)
                    logger.info(f"已删除超过1个月的导出文件: {file_path}")
                except Exception as e:
                    logger.exception(f"删除旧导出文件失败: {file_path}")


###############################################################################
# 初始化函数
###############################################################################
def init_fj_data_export(app, passed_db):
    global db
    db = passed_db

    load_db_cache()

    app.add_url_rule('/export_data',         view_func=export_data,    methods=['POST'])
    app.add_url_rule('/download/<filename>', view_func=download_file,  methods=['GET'])
