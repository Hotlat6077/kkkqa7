from flask import Flask, request, jsonify
from mydb.get_mongo import get_db
import numpy as np
from numpy import fft

db = get_db()
collection = db['pump_waveform_report']

app = Flask(__name__)


def draw_plot(f_values, fft_values):
    # 画图
    return None


# 要执行的函数示例
def frequency_domain(original_data, fs, ansy_method=None, pro_method=None):
    # signal = np.array(original_data)  # 1. 处理成 np.array
    # signal = (signal - np.mean(signal)).tolist()  #  2. 减去均值
    # 这里收到的原始数据就是array  不需要做np.array的处理
    print(f"original_data: {original_data}")
    signal = (original_data - np.mean(original_data)).tolist()  # 2. 减去均值
    Sampling_points = len(original_data)  # 采样点数，fft后的点数就是这个数
    df = 1 / fs  # 采样间隔时间 那样才能计算频率
    y = signal[:]
    y = list(map(float, y))
    y = np.array(y)
    f_values = np.linspace(0.0, fs / 2.0, Sampling_points // 2)
    fft_values_ = fft.fft(y)
    fft_values = 2.0 / Sampling_points * np.abs(fft_values_[0:Sampling_points // 2])
    print("f_values", f_values)
    print("fft_values", fft_values)
    # return f_values, fft_values
    result = f"原始数据长度 {len(signal)}，频率 {fs}，算法分析方法 {ansy_method}， 预处理类型 {pro_method}"
    # 这里可以添加你的业务逻辑
    jsonify = {
        "status": "success",
        "message": result,
        "data": {
            "signal": signal,
            "fs": fs,
            "ansy_method": ansy_method,
            "pro_method": pro_method,
            "f_values": f_values,
            "fft_values": fft_values
        }
    }
    # print("jsonify: ", jsonify)
    return jsonify


#  #请求入口
@app.route('/api/process', methods=['GET', 'POST'])
def handle_request():
    try:
        # 根据请求方法获取参数
        if request.method == 'POST':
            # 从表单数据或 JSON 获取数据
            if request.is_json:
                data = request.get_json()
                sensor_id = data.get('sensorId')
                time = data.get('time')
                analyse_method = data.get('analyseMethod')
                print("sensor_id: ", sensor_id)
                print("analyseMethod: ", analyse_method)
                # 通过sensorId 和 时间轴 来取信号原始数据 这里是查询关键字段
                query = {
                    'sensorId': sensor_id,
                    'time': time
                }
                document = collection.find_one(query)
                if document is not None:
                    # 提取 fs 字段
                    fs = document.get('fs')
                    data = document.get('datas')
                    print(f"Sensor ID: {sensor_id}, fs: {fs}")
                    print(f", dataType: {type(data)}")
                    # 进行时域算法计算
                    frequency_domain(data, fs)
                else:
                    print(f"No document found with sensorId: {sensor_id}")
            return jsonify(sensor_id)
        else:  # POST 请求
            # 从表单数据或 JSON 获取数据
            pass
            return None

        # # 验证必需参数
        # if sensor_id is None:
        #     return jsonify({
        #         "status": "error",
        #         "message": "缺少必需参数：sensor_id"
        #     }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"服务器错误：{str(e)}"
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
