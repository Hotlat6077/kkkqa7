from flask import Flask, request, jsonify
import numpy.fft as fft
import numpy as np

app = Flask(__name__)

# 要执行的函数示例
def process_data(signal_data=None, fs=None, pro_type=None):
    result = f"原始信号数据 {signal_data}，频率采样率 {fs}，处理类型 {pro_type} "
    # if pro_type == 'fs':
    #     pass
    #     # 开始拿到数据进行信号处理
    # fs = self.SampleFraquency  # 采样频率
    fs = fs  # 采样频率
    # Sampling_points = len(self.RawSignal)  # 采样点数，fft后的点数就是这个数
    Sampling_points = len(signal_data)  # 采样点数，fft后的点数就是这个数
    df = 1 / fs  # 采样间隔时间 每两个相邻采样点之间的时间间隔。这是正确的。
    # y = self.RawSignal[:]
    y = signal_data[:]
    y = list(map(float, y))
    y = np.array(y)
    # 取前半部分 fs/2.0 相当于数学公理定义 每个频率分量的幅度需要除以采样点数来归一化
    f_values = np.linspace(0.0, fs / 2.0, Sampling_points // 2)
    # 对所有数据进行fft变换 #
    fft_values_ = fft.fft(y)
    fft_values = 2.0 / Sampling_points * np.abs(fft_values_[0:Sampling_points // 2])
    # return f_values, fft_values
    # print("result", result)
    # 这里可以添加你的业务逻辑
    return {
        "status": "success",
        "message": result,
        "data": {
            "signal_data": signal_data,
            "fs": fs,
            "pro_type": pro_type,
            "f_values": f_values,
            "fft_values": fft_values
        }
    }


# 要用到地数据处理过程 fs参数：采样频率
def raw(vib, fs):
    vib = np.array(vib)
    fs = fs
    return vib


def ndarray2list0(data):
    list0 = []
    for temp in data:
        list0.append(temp.tolist())
    return list0


def ndarray2list1(data):
    list0 = []
    for temp in data:
        list0.append(temp.tolist())
    list1 = []
    for i in list0:
        for j in i:
            list1.append(j)
    return list1


@app.route('/api/process', methods=['GET', 'POST'])
def handle_request():
    try:
        # 根据请求方法获取参数
        if request.method == 'GET':
            # 从查询字符串获取参数
            name = request.args.get('sensorId')
            age = request.args.get('time')
            city = request.args.get('fs')
            city = request.args.get('fs')
        else:  # POST 请求
            # 从表单数据或 JSON 获取数据
            if request.is_json:
                data = request.get_json()
                name = data.get('name')
                print("name", name)
                age = data.get('age')
                city = data.get('city')
            else:
                name = request.form.get('name')
                age = request.form.get('age', type=int)
                city = request.form.get('city')

        # 验证必需参数
        if not name or age is None:
            return jsonify({
                "status": "error",
                "message": "缺少必需参数：name 和 age"
            }), 400

        # 执行函数
        result = process_data(name, age, city)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"服务器错误：{str(e)}"
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
