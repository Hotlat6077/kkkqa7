from flask import Flask, request, jsonify
from mydb.get_mongo import get_db
import numpy as np
from numpy import fft
from loguru import logger
import sys
import warnings
from spectrum_ointface import spectrum
from preprocess_data import raw, tintegral, cderiv, routliers
from rms_velocity_ointface import velocity
from 速度有效值 import update_mins_fj_signal_analysis5_cao_fix
from 最小熵反褶积 import update_mins_fj_signal_analysis_MED_cao_fix
from 共振调解 import update_mins_fj_signal_analysis_resonance_cao_fix
from 倒谱 import update_mins_fj_signal_analysis7_cao_fix
from 自相关系数 import update_mins_fj_signal_analysis_acf_cao_fix
from 自功率分析 import update_mins_fj_signal_analysis_aps_cao_fix
from 加速度有效值 import update_mins_fj_signal_analysis3_cao_fix
from 加速度峰值 import update_mins_fj_signal_analysis2_cao_fix
from 波形趋势分析 import update_mins_fj_signal_analysis4_cao_fix
from 介次分析 import update_mins_fj_signal_analysis_14_cao_fix
from 三维频谱图 import update_mins_fj_signal_analysis_fft3d_cao_fix
from 包络图 import update_mins_fj_signal_analysis_HE_cao_fix
from 小波阈值降噪 import update_mins_fj_signal_analysis_waveletd_cao_fix

warnings.filterwarnings("ignore")
logger.remove()
logger.add(sys.stdout, colorize=True, format="<g>{time:HH:MM:ss:SSS}</g> | <c>{level}</c> | <level>{message}</level>")



# 添加文件输出（保存到文件）
logger.add(
    "IOT.log",  # 文件名
    format="{time:YYYY-MM-DD HH:mm:ss:SSS} | {level} | {message}",  # 文件格式（通常不用颜色）
    level="INFO",           # 日志级别
    rotation="10 MB",       # 日志文件达到10MB时轮转
    retention="7 days",     # 保留最近7天的日志
    compression="zip",      # 压缩旧日志为zip
    encoding="utf-8",       # 编码
    enqueue=True            # 异步安全写入（多线程/多进程推荐）
)


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.json.ensure_ascii = False

db = get_db()
#collection = db['pump_waveform_report']
#collection = db['pump_acc_test1']
collection = db['pump_vel_test1']

# 上传服务器 现在在用 需要修改的
@app.route('/api/process', methods=['GET', 'POST'])
def handle_request():
    try:
        # 根据请求方法获取参数
        if request.method == 'GET':
            # 从查询字符串获取参数
            return None
        else:  # POST 请求
            # 从表单数据或 JSON 获取数据
            logger.info(f"请求方式: {request.method}")
            if request.is_json:
                #result = None
                request_result = {
                        "code": 200,
                        "msg": "处理成功",
                        "data":None
                        }

                request_data = request.get_json()
                
                #local_filename = request_data.get('localfilename')
                things_model = request_data.get('thingsModel')
                analyse_method = request_data.get('analyseMethod')
                serial_num = request_data.get('serialNum')
                #measure_site_id = request_data.get('measureSiteId')
                report_time = request_data.get('reportTime')

                #measure_gather_id = data.get('measureGatherId')
                #measure_gather_id = request_data.get('gatherId')
                # sesor_id = data.get('sensorId')
                data_process = request_data.get('dataProcess')
                #time_ = local_filename.replace("-", "").replace(" ", "").replace(":", "")+'00'
                logger.info(f"请求参数 data:{request_data}")
  
                # print("sensor_id: ", gather_id)
                # 通过sensorId取信号原始数据
                query = {
                    # 'sensorId':sesor_id,
                    'thingsModel':things_model,
                    'serialNum':serial_num,
                    'reportTime':report_time
                }
                document = collection.find_one(query)
                # 判断是否在数据库中找到这条数据
                if document is not None:
                    fs = document.get('fs')
                    #fs = int(fs)/2.56
                    fs1 = int(fs)
                    fs = int(fs)*0.78125
                    data = document.get('datas')
                    logger.success(f"数据库查询成功 采样频率: {fs}, 总采样点数: {len(data)}")
                else:
                    #logger.error(f"未查询到数据 localfilename: {local_filename}, gatherId: {measure_gather_id}, measureSiteId: {measure_site_id}")
                    logger.error("未查询到数据")
                    return jsonify({
                        "status": "error",
                        "msg": "没有找到要查询的数据"
                        }), 400
                if analyse_method=='spectrum' and document is not None:
                    logger.success(f"频谱图")
                    result = spectrum(data, fs1, methods=data_process)
                    request_result['data'] = result
                    return jsonify(request_result),200
                elif analyse_method=='rms' and document is not None:  # Root Mean Square
                    logger.success(f"速度有效值")
                    result = update_mins_fj_signal_analysis5_cao_fix(data, fs, methods=data_process)
                    request_result['data'] = result
                    return jsonify(request_result),200
                    # request_result['data'] = result 
                    # return jsonify(request_result),200
                elif analyse_method=='envelope' and document is not None:  # Root Mean Square
                    logger.success(f"包络")
                    result = update_mins_fj_signal_analysis_HE_cao_fix(data, fs, methods=data_process)
                    request_result['data'] = result
                    return jsonify(request_result),200
                elif analyse_method=='timeAnalysis' and document is not None:
                # 介次分析
                    logger.success(f"介次分析")
                    result = update_mins_fj_signal_analysis_14_cao_fix(data, fs, methods=data_process)
                    request_result['data'] = result
                    return jsonify(request_result),200
                elif analyse_method=='smallWave' and document is not None:
                # 小波阈值降噪-这个先不做
                    logger.success(f"小波阈值降噪")
                    result = update_mins_fj_signal_analysis_waveletd_cao_fix(data, fs, methods=data_process)
                    request_result['data'] = result
                    return jsonify(request_result),200
                elif analyse_method=='miniEntropy' and document is not None:
                # 最小熵反褶积
                    logger.success(f"最小熵反褶积")
                    result = update_mins_fj_signal_analysis_MED_cao_fix(data, fs, methods=data_process)
                    request_result['data'] = result
                    return jsonify(request_result),200
                elif analyse_method=='syntony' and document is not None:
                # 共振解调
                    logger.success(f"共振解调")
                    result = update_mins_fj_signal_analysis_resonance_cao_fix(data, fs, methods=data_process)
                    request_result['data'] = result
                    return jsonify(request_result),200
                elif analyse_method=='cepstrum' and document is not None:
                # 倒谱
                    logger.success(f"倒谱")
                    result = update_mins_fj_signal_analysis7_cao_fix(data, fs, methods=data_process)
                    request_result['data'] = result
                    return jsonify(request_result),200
                elif analyse_method=='selfCorr' and document is not None:
                # 自相关分析
                    logger.success(f"自相关分析")
                    result = update_mins_fj_signal_analysis_acf_cao_fix(data, fs, methods=data_process)
                    request_result['data'] = result
                    return jsonify(request_result),200
                elif analyse_method=='selfPower' and document is not None:
                # 自功率分析
                    logger.success(f"自功率分析")
                    result = update_mins_fj_signal_analysis_aps_cao_fix(data, fs, methods=data_process)
                    request_result['data'] = result
                    return jsonify(request_result),200
                elif analyse_method=='acc' and document is not None:
                # 加速度有效值
                    logger.success(f"加速度有效值")
                    result = update_mins_fj_signal_analysis3_cao_fix(data, fs, methods=data_process)
                    request_result['data'] = result
                    return jsonify(request_result),200
                elif analyse_method=='peakAcc' and document is not None:
                # 加速度峰值 
                    logger.success(f"加速度峰值")
                    result = update_mins_fj_signal_analysis2_cao_fix(data, fs, methods=data_process)
                    request_result['data'] = result
                    return jsonify(request_result),200
                elif analyse_method=='waveform' and document is not None:
                # 波形趋势分析
                    logger.success(f"波形趋势分析")
                    result = update_mins_fj_signal_analysis4_cao_fix(data, fs, methods=data_process)
                    request_result['data'] = result
                    return jsonify(request_result),200
               # elif analyse_method=='temperature' and document is not None:
                # 温度趋势分析
                #    logger.success(f"温度趋势分析")
                
                elif analyse_method=='3D' and document is not None:
                    logger.success(f"三维频谱绘制计算")
                    result = update_mins_fj_signal_analysis_fft3d_cao_fix(data,fs)
                    request_result['data'] = result
                    return jsonify(request_result),200
                else:
                    return jsonify({
                        "status": "error",
                        "msg": "请求参数错误"
                        }), 400

        # 验证必需参数
                # things_model = request_data.get('thingsModel')
        if things_model is None:
            return jsonify({
                "status": "error",
                "message": "缺少必需参数：sensor_id"
            }), 400
        # 执行函数
        # result = process_data(sensor_id)

        return jsonify(things_model)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"服务器错误：{str(e)}"
        }), 500


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=6100)
    import os
    if os.name == 'nt':  # Windows
        from waitress import serve
        serve(app, host='0.0.0.0', port=6100)
    else:  # Linux
        app.run(debug=False, host='0.0.0.0', port=6100)
