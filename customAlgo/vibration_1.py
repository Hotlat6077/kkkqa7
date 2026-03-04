# vibration_scheduler.py
from __future__ import annotations

import re
import os

import config
import config as cfg
from datetime import datetime
import datetime as DT
import pandas as pd
import shutil
from tqdm import tqdm

from fault_report import VibrationDiagnosis
from health_monitor.health_train_kmeans import Train_KMeans, Test_KMeans
from health_monitor.health_train_lstm import Train_LSTM, Test_LSTM
from health_monitor.health_train_som import Train_SOM, analyze_feature_importance_som, Test_SOM
from health_monitor.healthassess_KMeans_paixu import analyze_feature_importance_kmeans
from health_monitor.healthassess_lstm_paixu import analyze_feature_importance_lstm
from index_calculation import index_result, frequency_index, speed_rms
from signal_processing.order_ana import order_frequency
import numpy as np
import shutil
import time
import re
import winsound
from database_init import fre_update_liu
import logging
import subprocess
from loguru import logger  # 使用 loguru 进行日志记录
import json  # 用于解析 JSON 字符串
import glob  # 用于文件扫描

from lstm_server import get_lstm_param
from mydb.get_mongo import get_db, get_client

# 全局 loguru 日志初始化标志
LOGURU_INITIALIZED = False


def init_loguru():
    global LOGURU_INITIALIZED
    if not LOGURU_INITIALIZED:
        today = datetime.now()
        # 日志写入到 .\logging\YYYYMM 文件夹中
        log_folder = os.path.join(".", "logging", today.strftime("%Y%m"))
        os.makedirs(log_folder, exist_ok=True)
        # 普通日志文件：vibration_YYYYMMDD.log（INFO 级别）
        log_file = os.path.join(log_folder, f"vibration_{today.strftime('%Y%m%d')}.log")
        logger.add(log_file, rotation="00:00", retention="30 days", encoding="utf8", level="INFO")
        LOGURU_INITIALIZED = True


class vibration_timer():
    def __init__(self) -> None:
        self.vib_path = cfg.load_path
        self.buffer_path = cfg.buffer_path
        self.generate_folder = lambda x: os.makedirs(x) if not os.path.exists(x) else ''
        self.generate_folder(self.buffer_path)
        self.history_path = cfg.his_path
        self.generate_folder(self.history_path)
        self.local_path = cfg.local_data_path
        self.generate_folder(self.local_path)
        self.vib_limit = 1000
        self.fault_chinse_mapping = cfg.chinese_fault_mapping
        self.speed_coef = cfg.speed_coef

        # 记录配置路径信息
        logger.info(f"Initialized vibration_timer with vibration data path: {self.vib_path}")

        # 检查关键路径是否存在
        if os.path.exists(self.vib_path):
            logger.info(f"Vibration path exists and ready for monitoring")
        else:
            logger.error(f"Vibration path does NOT exist: {self.vib_path}")

        # 新增：已处理文件记录
        self.processed_files = set()
        self.load_processed_files()

    def load_processed_files(self):
        """加载已处理文件列表"""
        processed_file_path = os.path.join(self.buffer_path, "processed_files.txt")

        if os.path.exists(processed_file_path):
            try:
                with open(processed_file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    self.processed_files = set(line.strip() for line in lines if line.strip())
                logger.info(f"Loaded {len(self.processed_files)} processed files from record.")

            except Exception as e:
                logger.error(f"Error loading processed files: {str(e)}")
                self.processed_files = set()
        else:
            logger.info("Starting with empty processed files list.")
            self.processed_files = set()

    def save_processed_files(self):
        """保存已处理文件列表"""
        processed_file_path = os.path.join(self.buffer_path, "processed_files.txt")
        try:
            with open(processed_file_path, 'w', encoding='utf-8') as f:
                for file_path in self.processed_files:
                    f.write(f"{file_path}\n")
        except Exception as e:
            logger.error(f"Error saving processed files: {str(e)}")

    def mark_file_processed(self, file_path):
        """标记文件为已处理"""
        self.processed_files.add(file_path)
        self.save_processed_files()

    def scan_new_files(self):
        """扫描本地数据文件夹，查找未处理的数据文件"""
        new_files = []

        if not os.path.exists(self.vib_path):
            logger.warning(f"Data path does not exist: {self.vib_path}")
            return new_files

        # 只扫描CSV文件
        file_path_pattern = os.path.join(self.vib_path, '**', '*.csv')
        files = glob.glob(file_path_pattern, recursive=True)

        valid_files = 0
        already_processed = 0

        for file_path in files:
            filename = os.path.basename(file_path)

            # 检查文件名格式是否符合要求
            if self.is_valid_filename_format(filename):
                valid_files += 1

                if file_path not in self.processed_files:
                    new_files.append(file_path)
                else:
                    already_processed += 1

        logger.info(
            f"File scan complete - Total CSV: {len(files)}, Valid format: {valid_files}, Already processed: {already_processed}, New files: {len(new_files)}")

        return new_files

    def is_valid_filename_format(self, filename):
        """检查文件名是否符合格式：YYYYMMDDHHMMSS.csv"""
        pattern = r'^\d{14}\.csv$'
        return bool(re.match(pattern, filename))

    def parse_filename(self, filename):
        """
        解析文件名，提取时间
        返回: datetime_str
        """
        try:
            # 移除文件扩展名
            name_without_ext = filename.replace('.csv', '')

            if len(name_without_ext) != 14:
                raise ValueError(f"Filename format error, expected 14 digits, got {len(name_without_ext)}")

            # 解析时间
            dt = datetime.strptime(name_without_ext, '%Y%m%d%H%M%S')
            datetime_str = dt.strftime('%Y-%m-%d %H:%M:%S')

            return datetime_str

        except Exception as e:
            logger.error(f"Error parsing filename {filename}: {str(e)}")
            return None

    def extract_sensor_info_from_path(self, file_path):
        """
        从文件路径中提取传感器信息
        路径格式：D:\DREOMS\data\fj_local\group\machine\component\sensor\YYYYMMDDHHMMSS.csv
        """
        try:
            # 获取相对于数据根目录的路径
            rel_path = os.path.relpath(file_path, self.vib_path)
            path_parts = rel_path.split(os.sep)

            # 路径格式: group/machine/component/sensor/filename
            if len(path_parts) >= 5:  # 包含文件名
                group = path_parts[0]
                machine = path_parts[1]
                component = path_parts[2]
                sensor = path_parts[3]

                # 构造sensorID
                sensorid = f"SE_{group}_{machine}_{component}_{sensor}"
                return sensorid, group, machine, component, sensor
            else:
                logger.warning(f"Invalid directory structure for file: {file_path}")
                return None, None, None, None, None

        except Exception as e:
            logger.error(f"Error extracting sensor info from {file_path}: {str(e)}")
            return None, None, None, None, None

    def get_sensor_type_from_db(self, sensorid):
        """从数据库获取传感器类型"""
        try:
            with get_client() as client:
                db = client['yueyangfan']
                collection = db.sensor_data

                sensor_doc = collection.find_one({'sensorID': sensorid}, {'equipkind': 1})

                if sensor_doc:
                    equipkind = sensor_doc.get('equipkind', '').strip()
                    return equipkind if equipkind else '振动'
                else:
                    logger.warning(f"Sensor {sensorid} not found in database, treating as vibration")
                    return '振动'

        except Exception as e:
            logger.error(f"Error getting sensor type for {sensorid}: {str(e)}")
            return '振动'  # 默认为振动类型

    def extract_data_from_csv(self, file_path, sensor_type):
        """根据测点类型从CSV文件中提取数据"""
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            # 检查文件是否为空
            if not content:
                logger.warning(f"File {file_path} is empty")
                return None

            # 按逗号分割数据
            try:
                data_items = []
                for item in content.split(','):
                    item = item.strip()
                    if item:  # 跳过空字符串
                        data_items.append(float(item))
            except ValueError as e:
                logger.error(f"Error converting data to float in {file_path}: {str(e)}")
                return None

            # 根据传感器类型处理数据
            if sensor_type in ['转速', '温度', '压力']:
                # 对于转速、温度、压力，只取第一个值作为指标
                if len(data_items) > 0:
                    return data_items[0]
                else:
                    logger.warning(f"File {file_path} contains no data for {sensor_type} sensor")
                    return None

            else:
                # 对于振动类型或其他类型，返回完整的数据数组
                if len(data_items) < 100:
                    logger.warning(f"File {file_path} contains insufficient data: {len(data_items)} points")
                    return None
                logger.debug(f"Successfully extracted {len(data_items)} data points from {file_path}")
                return data_items

        except Exception as e:
            logger.error(f"Error extracting data from {file_path}: {str(e)}")
            return None

    def get_all_group(self):
        """获取所有组ID"""
        db = get_db()
        collection = db.group_data
        group_id_list = [i.get('groupID') for i in list(collection.find({'onlineflag': True}, {}))]

        return group_id_list

    def get_machine(self, groupID):
        """获取组下的所有设备ID"""
        db = get_db()
        collection = db.machine_data
        machine_id_list = [i.get('machineID') for i in
                           list(collection.find({'onlineflag': True, 'groupID': groupID}, {}))]

        return machine_id_list

    def restartMongo(self):
        """重启MongoDB"""
        subprocess.run(cfg.MongoCheckBAT, shell=True)

    def create_log_file(self, log_path, today_str):
        """创建日志文件"""
        with open(log_path, 'w+', encoding='utf-8') as f:
            f.seek(0)
            f.write(f'This is a daily log file: {today_str}')

    def write_log(self, log_path, context):
        """写入日志"""
        with open(log_path, 'r+', encoding='utf-8') as f:
            original_content = f.read()
            f.seek(0)
            f.write(f'{context}\n{original_content}')

    def main(self):
        """主处理函数"""
        #########
        today_str = datetime.now().strftime('%Y%m%d')
        YM, D = today_str[:6], today_str[6:]
        self.generate_folder(os.path.join(cfg.logging_path, YM))
        log_path = os.path.join(cfg.logging_path, YM, f"{today_str}.log")
        if not os.path.exists(log_path):
            self.create_log_file(log_path, today_str)

        # 检查数据库连接和运行数据表
        try:
            with get_client() as client:
                db = client['yueyangfan']
                collection_operating = db.sensor_operating_data
                self.check_vibtable(collection_operating)
        except Exception as e:
            logger.error(f"Database error when accessing sensor_operating_data: {str(e)[-100:]}")
            self.write_log(log_path,
                           f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Database error: \n {str(e)[-100:]}")
            self.restartMongo()
            return False  # 返回False表示处理失败

        # 扫描新文件
        new_files = self.scan_new_files()
        if not new_files:
            logger.info("No new files found to process.")
            return True  # 返回True表示处理成功（虽然没有新文件）

        excute_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        processed_count = 0
        failed_count = 0

        # 使用进度条处理文件
        for file_path in tqdm(new_files, desc=f"{excute_date} Processing files"):
            try:
                success = self.process_single_file(file_path)
                if success:
                    processed_count += 1
                    # 标记文件为已处理
                    self.mark_file_processed(file_path)
                else:
                    failed_count += 1

                self.write_log(log_path, f"{excute_date}: {file_path}: {'Success' if success else 'Failed'}")

            except Exception as e:
                failed_count += 1
                logger.error(f"Error processing file {file_path}: {str(e)[-100:]}")
                self.write_log(log_path, f"{excute_date}: {file_path}: Error - {str(e)[-100:]}")

        # 执行数据库更新操作
        try:
            groupid_list = self.get_all_group()
            for groupid in groupid_list:
                machineid_list = self.get_machine(groupid)
                for machineid in machineid_list:
                    fre_update_liu(1, machineid)
                    fre_update_liu(2, machineid)
                    fre_update_liu(3, machineid)
                    fre_update_liu('03', machineid)
                    fre_update_liu(5, machineid)
                    fre_update_liu(6, machineid)
        except Exception as e:
            logger.error(f"Error updating frequency data: {str(e)}")
            self.write_log(log_path, f"{excute_date}: Frequency update error: {str(e)[-100:]}")

        logger.info(f"File processing completed. Processed: {processed_count}, Failed: {failed_count}")
        self.write_log(log_path,
                       f"{excute_date}: Processing summary - Processed: {processed_count}, Failed: {failed_count}")

        return True  # 返回True表示处理成功

    def run_continuous(self):
        """持续运行模式 - 单线程，每10分钟扫描一次"""
        logger.info("Starting continuous data monitoring...")

        while True:
            try:
                # 执行主处理函数
                logger.info("Starting new scan cycle...")
                success = self.main()

                if success:
                    logger.info("Scan cycle completed successfully.")
                else:
                    logger.warning("Scan cycle completed with errors.")

                # 每天凌晨2点清理旧数据（保留30天）
                current_time = datetime.now()
                if current_time.hour == 2 and current_time.minute <= 10:  # 在2:00-2:10之间执行
                    logger.info("Starting daily cleanup...")
                    cleanup_result = self.cleanup_old_data(days=30)
                    if cleanup_result:
                        logger.info(f"Cleanup completed: {cleanup_result}")

                    # 输出统计信息
                    stats = self.get_statistics(days=7)
                    if stats:
                        logger.info(f"Weekly statistics: {stats}")

                # 等待10分钟后继续下一轮扫描
                logger.info("Waiting 10 minutes before next scan...")
                time.sleep(60)  # 10分钟 = 600秒

            except KeyboardInterrupt:
                logger.info("Data timer stopped by user.")
                break
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {str(e)}")
                # 出现异常时也等待10分钟，避免连续错误
                logger.info("Waiting 10 minutes before retry due to error...")
                time.sleep(60)

        logger.info("Data timer shutdown completed.")

    def get_statistics(self, days=7):
        """获取最近几天的处理统计信息"""
        try:
            with get_client() as client:
                db = client['yueyangfan']

                # 计算日期范围
                end_date = datetime.now()
                start_date = end_date - DT.timedelta(days=days)
                start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
                end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')

                # 统计运行数据记录数量
                records_count = db.sensor_operating_data.count_documents({
                    'datetime': {'$gte': start_date_str, '$lte': end_date_str}
                })

                # 统计报警事件数量
                fault_count = db.event_data.count_documents({
                    'begin_date': {'$gte': start_date_str, '$lte': end_date_str}
                })

                # 按传感器统计
                sensor_pipeline = [
                    {'$match': {'datetime': {'$gte': start_date_str, '$lte': end_date_str}}},
                    {'$group': {
                        '_id': '$sensorID',
                        'count': {'$sum': 1},
                        'latest_time': {'$max': '$datetime'}
                    }},
                    {'$sort': {'count': -1}}
                ]
                sensor_stats = list(db.sensor_operating_data.aggregate(sensor_pipeline))

                stats = {
                    'time_range': f"{start_date_str} to {end_date_str}",
                    'total_records': records_count,
                    'fault_events': fault_count,
                    'active_sensors': len(sensor_stats),
                    'top_sensors': sensor_stats[:10]  # 前10个最活跃的传感器
                }

                return stats

        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")
            return None

    def cleanup_old_data(self, days=30):
        """清理旧数据"""
        try:
            with get_client() as client:
                db = client['yueyangfan']

                # 计算清理日期
                cleanup_date = datetime.now() - DT.timedelta(days=days)
                cleanup_date_str = cleanup_date.strftime('%Y-%m-%d %H:%M:%S')

                # 清理旧的运行数据记录
                operating_result = db.sensor_operating_data.delete_many({
                    'datetime': {'$lt': cleanup_date_str}
                })

                # 清理旧的事件记录
                events_result = db.event_data.delete_many({
                    'begin_date': {'$lt': cleanup_date_str}
                })

                logger.info(
                    f"Cleaned up old data: {operating_result.deleted_count} operating records, {events_result.deleted_count} events")

                return {
                    'operating_deleted': operating_result.deleted_count,
                    'events_deleted': events_result.deleted_count
                }

        except Exception as e:
            logger.error(f"Error cleaning up old data: {str(e)}")
            return None

    def save_sensor_record(self, sensorid, datetime_str, data, group, machine, component, sensor, sensor_type, file_name):
        """
        根据传感器类型保存数据记录

        Args:
            sensorid: 传感器ID
            datetime_str: 时间字符串
            data: 数据（振动数据数组或单一数值）
            group, machine, component, sensor: 设备层级信息
            sensor_type: 传感器类型（温度、压力、转速、振动）
        """
        try:
            with get_client() as client:
                db = client['yueyangfan']

                # 1. 保存运行参数数据
                operating_record = {
                    'datetime': datetime_str,
                    'sensorID': sensorid,
                    'group': int(group),
                    'machine': int(machine),
                    'component': int(component),
                    'sensor': int(sensor),
                    'sensor_type': sensor_type,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

                # 插入到运行数据集合
                collection_operating = db.sensor_operating_data
                operating_result = collection_operating.insert_one(operating_record)

                # 2. 根据传感器类型处理数据
                if sensor_type in ['转速', '温度', '压力']:
                    # 对于转速、温度、压力，直接保存单一指标值
                    self.save_simple_indicator(db, sensorid, datetime_str, data, sensor_type,
                                               group, machine, component, sensor)

                else:
                    # 对于振动类型，按原有逻辑处理
                    self.save_vibration_record_simple(db, sensorid, datetime_str, data,
                                                      group, machine, component, sensor, file_name)

                return True

        except Exception as e:
            logger.error(f"Error saving sensor record for {sensorid}: {str(e)}")
            return False

    def save_simple_indicator(self, db, sensorid, datetime_str, value, sensor_type,
                              group, machine, component, sensor):
        """保存简单指标数据（转速、温度、压力）"""
        try:
            # 构建指标数据字典
            dict_index = {
                'datetime': datetime_str,
                'sensorID': sensorid,
                'component': int(component),
                'sensor': int(sensor),
                'sensor_type': sensor_type,
                'value': value,  # 单一指标值
                'samplingfrequency': 1  #
            }

            # 简单指标的状态判断
            state, sub_state, description = self.judge_simple_sensor_state(value, sensor_type, sensorid, datetime_str)

            # 更新指标字典
            dict_index.update({'state': state, 'sub_state': sub_state, 'description': description})

            # 插入到指标集合
            collection_name = f"indicator_data_{group}_{machine}"
            collection_index = db[collection_name]
            collection_index.insert_one(dict_index)

            # 更新传感器状态
            self.update_sensor_status(sensorid, datetime_str, state, sub_state, description, '')

            # 如果有异常，记录事件
            if state != 0:
                self.record_fault_event(sensorid, datetime_str, state, '', description)

            logger.debug(f"Successfully saved {sensor_type} indicator for sensor {sensorid}, value: {value}")

        except Exception as e:
            logger.error(f"Error saving simple indicator for {sensorid}: {str(e)}")

    def save_vibration_record_simple(self, db, sensorid, datetime_str, vib_data,
                                     group, machine, component, sensor, file_name):
        """保存振动数据记录（简化版，去除频率诊断）"""
        try:

            table = db['sensor_file_fs']
            data = table.find_one({"sensor_id": sensorid, "file": file_name}, {"fs": 1, "_id": 0})
            fs = 10000
            if data is not None:
                fs = int(data['fs'])
            ###########
            # 计算振动指标
            indicators = self.calculate_indicators(sensorid, vib_data, fs)
            # 构建指标数据字典
            dict_index = {
                'datetime': datetime_str,
                'sensorID': sensorid,
                'component': int(component),
                'sensor': int(sensor),
                'sensor_type': '振动',
                'samplingfrequency': fs
            }
            dict_index.update(indicators)

            # 进行状态判断（去除频率诊断）
            state, sub_state, description = self.judge_vibration_sensor_state(indicators, sensorid, datetime_str)

            # 更新指标字典
            dict_index.update({'state': state, 'sub_state': sub_state})

            # 插入到指标集合
            collection_name = f"indicator_data_{group}_{machine}"
            collection_index = db[collection_name]
            collection_index.insert_one(dict_index)

            # 更新传感器状态
            self.update_sensor_status(sensorid, datetime_str, state, sub_state, description, description)

            # 如果有异常，记录事件和异常数据
            if state != 0:
                self.record_fault_event(sensorid, datetime_str, state, description, description)
                self.abnormal_import(vib_data, sensorid, state, sub_state, datetime_str, description, description)

            logger.debug(f"Successfully saved vibration record for sensor {sensorid}")

        except Exception as e:
            logger.error(f"Error saving vibration record for {sensorid}: {str(e)}")

    def judge_simple_sensor_state(self, value, sensor_type, sensorid, datetime_str):
        """判断简单传感器状态（转速、温度、压力）

        逻辑：
        - 单点测量值 < 阈值1：预警（低于下限）
        - 单点测量值 > 阈值2：预警（高于上限）
        - 其他情况：正常
        """
        try:
            # 根据传感器类型确定阈值字段名
            threshold_field_map = {
                '转速': 'rpm',
                '温度': 'temperature',
                '压力': 'pressure'
            }

            threshold_field = threshold_field_map.get(sensor_type, sensor_type.lower())

            # 获取该传感器类型的阈值
            thresholds = self.get_threshold(threshold_field, sensorid)

            if not isinstance(thresholds, list) or len(thresholds) < 2:
                # 如果没有阈值或阈值格式不正确，默认为正常
                return 0, [0], [f"{sensor_type}: 正常（无阈值配置）"]

            lower_threshold = thresholds[0]  # 下限阈值
            upper_threshold = thresholds[1]  # 上限阈值

            # 状态判断逻辑
            if lower_threshold is not None and value < lower_threshold:
                state = 1  # 预警
                description = [f"{sensor_type}: 预警 - 低于下限 (值: {value}, 下限: {lower_threshold})"]
            elif upper_threshold is not None and value > upper_threshold:
                state = 1  # 预警
                description = [f"{sensor_type}: 预警 - 高于上限 (值: {value}, 上限: {upper_threshold})"]
            else:
                state = 0  # 正常
                description = [f"{sensor_type}: 正常 (值: {value})"]

            return state, [state], description

        except Exception as e:
            logger.error(f"Error judging simple sensor state for {sensorid}: {str(e)}")
            return 0, [0], [f"{sensor_type}: 正常（判断异常）"]

    def _evaluate_indicator_level(self, level_value: float, indicator_name: str,
                                  warning_threshold: float = 30,
                                  fault_threshold: float = 70) -> tuple[int, str]:
        """
        评估指标等级并返回状态和描述

        Args:
            level_value: 指标值（百分比）
            indicator_name: 指标中文名称
            warning_threshold: 预警阈值，默认30
            fault_threshold: 报警阈值，默认70

        Returns:
            (状态码, 描述文本) - 状态码: 0=正常, 1=预警, 2=报警
        """
        if fault_threshold < level_value:
            state = 2  # 报警
            desc = f"{indicator_name}故障报警({level_value})"
        elif warning_threshold < level_value <= fault_threshold:
            state = 1  # 预警
            desc = f"{indicator_name}故障预警({level_value})"
        else:
            state = 0  # 正常
            desc = f"{indicator_name}故障正常({level_value})"
        return state, desc

    def judge_vibration_sensor_state(self, indicator_dict: dict, sensorid: str, date_str: str):
        """判断振动传感器状态"""
        metrics = ["impulse", "kur", "peak", "rms", "std"]
        metrics_CHN = ["脉冲指标", "峭度", "加速度峰值", "均方根值", "标准差"]
        information_list = ["正常", "预警", "报警", "离线"]

        state_list = []
        description = []

        for i, metric_name in enumerate(metrics):
            metric_values = indicator_dict.get(metric_name, [])
            if not isinstance(metric_values, list) or len(metric_values) == 0:
                metric_values = [0.0]
            measured_value = metric_values[0]

            thresholds = self.get_threshold(metric_name, sensorid)

            if not isinstance(thresholds, list) or len(thresholds) < 2:
                # 如果没有有效阈值，默认为正常状态
                cur_state = 0
            else:
                warning_threshold = thresholds[0]
                fault_threshold = thresholds[1]

                # 状态判断逻辑
                if fault_threshold is not None and measured_value >= fault_threshold:
                    cur_state = 2  # 报警
                elif warning_threshold is not None and measured_value >= warning_threshold:
                    cur_state = 1  # 预警
                else:
                    cur_state = 0  # 正常

            state_list.append(cur_state)
            desc_str = f"{metrics_CHN[i]}:{information_list[cur_state]} "
            description.append(desc_str)
        ###############
        ##故障分析
        # 1. 不平衡/偏心故障检测
        unbalance_state, unbalance_desc = self._evaluate_indicator_level(
            indicator_dict['unbalance_level'], "不平衡或偏心", warning_threshold=30, fault_threshold=70
        )
        state_list.append(unbalance_state)
        description.append(unbalance_desc)

        # 2. 不对中故障检测
        misalignment_state, misalignment_desc = self._evaluate_indicator_level(
            indicator_dict['misalignment_level'], "不对中", warning_threshold=30, fault_threshold=70
        )
        state_list.append(misalignment_state)
        description.append(misalignment_desc)

        # 3. 机械松动故障检测
        looseness_state, looseness_desc = self._evaluate_indicator_level(
            indicator_dict['looseness_level'], "机械松动", warning_threshold=30, fault_threshold=70
        )
        state_list.append(looseness_state)
        description.append(looseness_desc)



        overall_state = max(state_list) if state_list else 0
        return overall_state, state_list, description

    def calculate_indicators(self, sensor_id: str, vib: list, fs: int):
        """计算振动指标"""
        signal_index = index_result(vib, len(vib))
        dic_index = {}
        dic_index['mean'] = signal_index[:, 0].ravel().tolist()  # 均值
        dic_index['var'] = signal_index[:, 1].ravel().tolist()  # 方差
        dic_index['std'] = signal_index[:, 2].ravel().tolist()  # 标准差
        dic_index['peak'] = signal_index[:, 3].ravel().tolist()  # 加速度峰值
        dic_index['rms'] = signal_index[:, 4].ravel().tolist()  # 均方根
        dic_index['avg'] = signal_index[:, 5].ravel().tolist()  # 绝对平均值
        dic_index['impulse'] = signal_index[:, 6].ravel().tolist()  # 脉冲
        dic_index['margin'] = signal_index[:, 7].ravel().tolist()  # 裕度指标
        dic_index['skew'] = signal_index[:, 8].ravel().tolist()  # 偏斜度
        dic_index['speed_rms'] = speed_rms(vib)  # 速度有效值
        dic_index['kur'] = signal_index[:, 9].ravel().tolist()  # 峭度

        #####加入som,lstm,kmeans
        ###
        hidden_num, num_layer = get_lstm_param(sensor_id)
        #########
        vib2 = vib - np.mean(vib)
        dic_index['kmeans'] = np.mean(Test_KMeans(sensor_id, vib2).get("hindex")).ravel().tolist()
        dic_index['Som'] = np.mean(Test_SOM(sensor_id, vib2).get("hindex")).ravel().tolist()
        dic_index['Lstm'] = np.mean(Test_LSTM(sensor_id, vib2, hidden_num=hidden_num, num_layer=num_layer).get('hindex')).ravel().tolist()
        #########
        ##雪飞算法
        # model_dir = f'{config.work_path}\\health_monitor\\som_model'

        rpm = 1450
        vib_diag = VibrationDiagnosis(fs)
        # 1. 不平衡/偏心故障检测
        unbalance_level = vib_diag.unbalance_eccentric(vib, rpm)
        dic_index['unbalance_level'] = unbalance_level
        print(f"不平衡/偏心故障程度: {unbalance_level:.2f}%")

        # 2. 不对中故障检测
        misalignment_level = vib_diag.misalignment(vib, rpm)
        dic_index['misalignment_level'] = misalignment_level
        print(f"不对中故障程度: {misalignment_level:.2f}%")

        # 3. 机械松动故障检测
        looseness_level = vib_diag.mechanical_looseness(vib, rpm)
        dic_index['looseness_level'] = looseness_level
        print(f"机械松动故障程度: {looseness_level:.2f}%")

        ###############
        return dic_index

    def update_sensor_status(self, sensorid, datetime_str, state, sub_state, description, fault_str):
        """更新传感器状态到state_data表"""
        try:
            with get_client() as client:
                db = client['yueyangfan']
                collection = db.state_data

                # 查找现有记录
                existing_record = collection.find_one({"sensorID": sensorid})

                status_update = {
                    "sensorID": sensorid,
                    "state": state,
                    "last_state": existing_record.get("state", 0) if existing_record else 0,
                    "connection_flag": 1,
                    "latest_date": datetime_str,
                    "begin_date": datetime_str,
                    "check_date": datetime_str,
                    "sub_state": sub_state,
                    "description": description,
                    "fault_info": fault_str,
                    "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

                # 更新或插入记录
                collection.update_one(
                    {"sensorID": sensorid},
                    {"$set": status_update},
                    upsert=True
                )

        except Exception as e:
            logger.error(f"Error updating sensor status for {sensorid}: {str(e)}")

    def record_fault_event(self, sensorid, datetime_str, state, fault_str, description):
        """记录报警事件"""
        try:
            with get_client() as client:
                db = client['yueyangfan']
                collection = db.event_data

                parts = sensorid.split('_')
                event_record = {
                    'begin_date': datetime_str,
                    'end_date': datetime_str,
                    'sensorID': sensorid,
                    'group': parts[1],
                    'machine': parts[2],
                    'component': parts[3],
                    'sensor': parts[4],
                    'event_level': ['healthy', 'warning', 'fault', 'offline'][state],
                    'event_fault': fault_str,
                    'solving_flag': 0,
                    'solving': description,
                    'attention': description
                }

                collection.insert_one(event_record)
                logger.warning(f"Fault event recorded for sensor {sensorid}, level: {event_record['event_level']}")

        except Exception as e:
            logger.error(f"Error recording fault event for {sensorid}: {str(e)}")

    def abnormal_import(self, vib, sensorid, state, substate, date_str, fault_str, description):
        """异常数据导入（使用原始代码逻辑）"""
        if state == 0:
            return
        db = get_db()
        collection = db.alert_data
        folder_path = os.path.join(cfg.alert_path, *sensorid.split('_')[1:])
        self.generate_folder(folder_path)
        format_date = re.sub(r'\D', '', date_str)
        save_path = os.path.join(folder_path, f"{format_date}.txt")
        vib_str = ','.join([str(i) for i in vib])
        with open(save_path, 'w+', encoding='utf8') as f:
            f.write(vib_str)
        dict_import = {
            'date': date_str,
            'sensorID': sensorid,
            'group': int(sensorid.split('_')[-4]),
            'machine': int(sensorid.split('_')[-3]),
            'component': int(sensorid.split('_')[-2]),
            'sensor': int(sensorid.split('_')[-1]),
            'state': state,
            'substate': substate,
            'frefault': fault_str,
            'vib_path': save_path,
            'des': description
        }
        collection.insert_one(dict_import)

    def check_vibtable(self, collection):
        """检查运行数据表记录数量，超过限制时删除旧记录"""
        counts = collection.count_documents({})
        if counts <= self.vib_limit:
            logger.debug(f"sensor_operating_data collection count {counts} within limit {self.vib_limit}.")
        else:
            # 删除最旧的记录
            oldest_records = list(collection.find({}, {'_id': 1, 'datetime': 1})
                                  .sort([('datetime', 1)])
                                  .limit(counts - self.vib_limit))

            if oldest_records:
                oldest_ids = [record['_id'] for record in oldest_records]
                result = collection.delete_many({'_id': {'$in': oldest_ids}})
                logger.warning(f"Deleted {result.deleted_count} old records to maintain limit {self.vib_limit}.")

    def get_latest_sensor_date(self, sensorid):
        """获取传感器最新数据时间"""
        try:
            with get_client() as client:
                db = client['yueyangfan']
                collection = db.sensor_operating_data

                latest_record = collection.find_one(
                    {'sensorID': sensorid},
                    {'datetime': 1},
                    sort=[('datetime', -1)]
                )

                if latest_record:
                    return datetime.strptime(latest_record['datetime'], '%Y-%m-%d %H:%M:%S')
                else:
                    return datetime(1900, 1, 1)  # 返回很早的时间

        except Exception as e:
            logger.error(f"Error getting latest sensor date for {sensorid}: {str(e)}")
            return datetime(1900, 1, 1)

    def get_threshold(self, indicator_name, sensorid):
        """
        获取阈值 - 适配新的数据结构
        新结构中每个指标都是独立字段，值为 [预警阈值, 报警阈值]

        Args:
            indicator_name: 指标名称 (如 'rms', 'temperature', 'rpm' 等)
            sensorid: 传感器ID

        Returns:
            list: [预警阈值, 报警阈值] 或 [None, None] 如果未找到
        """
        try:
            with get_client() as client:
                db = client['yueyangfan']
                collection = db.threshold_data

                # 查询该传感器的阈值文档
                threshold_doc = collection.find_one({'sensorID': sensorid})

                if not threshold_doc:
                    logger.warning(f"No threshold document found for sensorID: {sensorid}")
                    return [None, None]

                # 检查指标字段是否存在
                if indicator_name not in threshold_doc:
                    logger.warning(f"Indicator '{indicator_name}' not found in threshold document for {sensorid}")
                    return [None, None]

                thresholds = threshold_doc[indicator_name]

                # 验证阈值格式
                if not isinstance(thresholds, list) or len(thresholds) < 2:
                    logger.warning(f"Invalid threshold format for {indicator_name} in {sensorid}: {thresholds}")
                    return [None, None]

                # 返回 [预警阈值, 报警阈值]
                warning_threshold = thresholds[0] if thresholds[0] != 0 else None
                fault_threshold = thresholds[1] if thresholds[1] != 0 else None

                logger.debug(
                    f"Found thresholds for {sensorid}.{indicator_name}: warning={warning_threshold}, fault={fault_threshold}")

                return [warning_threshold, fault_threshold]

        except Exception as e:
            logger.error(f"Error getting threshold for {sensorid}.{indicator_name}: {str(e)}")
            return [None, None]

    def alarm(self):
        """报警提示"""
        frequency = 1000  # Hz
        duration = 1000  # 毫秒
        # winsound.Beep(frequency, duration) # 非 Windows 环境可注释

    def process_single_file(self, file_path):
        """处理单个数据文件"""
        try:
            # 检查文件名格式
            filename = os.path.basename(file_path)
            if not self.is_valid_filename_format(filename):
                logger.warning(f"Invalid filename format: {filename}")
                return False

            # 解析文件名获取时间
            datetime_str = self.parse_filename(filename)
            if datetime_str is None:
                logger.warning(f"Cannot parse filename: {filename}")
                return False

            # 从路径提取传感器信息
            sensorid, group, machine, component, sensor = self.extract_sensor_info_from_path(file_path)
            if not sensorid:
                logger.warning(f"Cannot extract sensor info from path: {file_path}")
                return False

            # 检查是否需要处理（比较文件时间与数据库中最新时间）
            file_date = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            latest_sensor_date = self.get_latest_sensor_date(sensorid)

            if file_date <= latest_sensor_date:
                logger.debug(f"File {file_path} is not newer than latest sensor date, skipping.")
                return False

            # 获取传感器类型
            sensor_type = self.get_sensor_type_from_db(sensorid)
            logger.debug(f"Processing {sensor_type} sensor: {sensorid}")

            # 根据传感器类型提取数据
            data = self.extract_data_from_csv(file_path, sensor_type)
            if data is None:
                logger.warning(f"Cannot extract data from file: {file_path}")
                return False

            file_name = file_path[-18:]
            # 保存处理结果到数据库
            success = self.save_sensor_record(
                sensorid, datetime_str, data, group, machine, component, sensor, sensor_type, file_name
            )

            if success:
                logger.info(
                    f"Successfully processed file: {os.path.basename(file_path)}, sensor: {sensorid}, type: {sensor_type}")
                return True
            else:
                logger.error(f"Failed to save sensor record for file: {file_path}")
                return False

        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            return False


if __name__ == '__main__':
    init_loguru()
    timer = vibration_timer()

    # 启动后马上开始工作，采用单线程持续扫描模式
    timer.run_continuous()
