# 理论频率
def theory_frequencies(group58, machine58, component, sensor, rotating_frequency):
    result = {}

    speed = rotating_frequency[0]

    if group58 == 3 and machine58 == 7:
        if component == 1 and sensor == 1:
            result_fre = {'轴承内圈': 4.07487, '外圈': 3.72513, '滚动体': 2.7611, '保持架': 0.0620855}
            result = {key: round(value * speed / 0.13, 4) for key, value in result_fre.items()}
        elif component == 1 and sensor == 2:
            result_fre = {'轴承内圈': 3.87899, '外圈': 3.53101, '滚动体': 2.63133, '保持架': 0.0619475}
            result = {key: round(value * speed / 0.13, 4) for key, value in result_fre.items()}
        elif component == 2 and sensor == 1:
            result_fre = {'轴承1内圈': 5.7733, '1外圈': 5.4067, '1滚动体': 3.8792, '1保持架': 0.0624,
                          '轴承2内圈': 4.4096, '2外圈': 4.0404, '2滚动体': 2.9133, '2保持架': 0.0624,
                          '啮合频率': 13, '齿圈边频': 0.13, '行星轮边频': 0.37, '太阳轮边频': 0.56}
            result = {key: round(value * speed / 0.13, 4) for key, value in result_fre.items()}
        elif component == 2 and sensor == 2:
            result_fre = {'轴承1内圈': 5.7733, '1外圈': 5.4067, '1滚动体': 3.8792, '1保持架': 0.0624,
                          '轴承2内圈': 4.4096, '2外圈': 4.0404, '2滚动体': 2.9133, '2保持架': 0.0624,
                          '轴承3内圈': 4.7878 / 3, '3外圈': 3.7111 / 3, '3滚动体': 2.8786 / 3, '3保持架': 0.2035 / 3,
                          '啮合频率': 13, '齿圈边频': 0.13, '行星轮边频': 0.37, '太阳轮边频': 0.56}
            result = {key: round(value * speed / 0.13, 4) for key, value in result_fre.items()}
        elif component == 2 and sensor == 3:
            result_fre = {'轴承1内圈': 19.8408, '1外圈': 18.2392, '1滚动体': 12.9528, '1保持架': 0.2688,
                          '轴承2内圈': 13.8676, '2外圈': 12.4544, '2滚动体': 8.708, '2保持架': 0.2632,
                          '轴承3内圈': 21.0048 / 3.42, '3外圈': 15.456 / 3.42, '3滚动体': 12.3456 / 3.42,
                          '3保持架': 1.0944 / 3.42,
                          '啮合频率': 82.78, '齿圈边频': 0.56, '行星轮边频': 1.92, '太阳轮边频': 4.012}
            result = {key: round(value * speed / 0.56, 4) for key, value in result_fre.items()}
        elif component == 2 and sensor == 4:
            result_fre = {'啮合频率': 429.3333, '大齿轮边频': 4.012, '小齿轮边频': 18.67}
            result = {key: round(value * speed / 4.012, 4) for key, value in result_fre.items()}
        elif component == 2 and sensor == 5:
            result_fre = {'轴承1内圈': 260.4465, '1外圈': 206.3035, '1滚动体': 153.4674, '1保持架': 8.2148,
                          '轴承2内圈': 213.5848, '2外圈': 159.8152, '2滚动体': 123.0353, '2保持架': 8.0281,
                          '啮合频率': 429.3333, '大齿轮边频': 4.012, '小齿轮边频': 18.67}
            result = {key: round(value * speed / 18.67, 4) for key, value in result_fre.items()}
        elif component == 3 and sensor == 1:
            result_fre = {'轴承1内圈': 117.914, '1外圈': 87.4197, '1滚动体': 122.921, '1保持架': 7.94724,
                          '轴承2内圈': 201.737, '2外圈': 152.93, '2滚动体': 133.076, '2保持架': 8.04893}
            result = {key: round(value * speed / 18.67, 4) for key, value in result_fre.items()}
        elif component == 3 and sensor == 2:
            result_fre = {'轴承内圈': 201.737, '外圈': 152.93, '滚动体': 133.076, '保持架': 8.04893}
            result = {key: round(value * speed / 18.67, 4) for key, value in result_fre.items()}
    else:
        if component == 1 and sensor == 1:
            result_fre = {'轴承内圈': 3.79131, '外圈': 3.40869, '滚动体': 2.36559, '保持架': 0.0631238}
            result = {key: round(value * speed / 0.133, 4) for key, value in result_fre.items()}
        elif component == 1 and sensor == 2:
            result_fre = {'轴承内圈': 3.45844, '外圈': 3.0749, '滚动体': 2.12689, '保持架': 0.062753}
            result = {key: round(value * speed / 0.133, 4) for key, value in result_fre.items()}
        elif component == 2 and sensor == 1:
            result_fre = {'轴承内圈': 1.51221, '外圈': 1.14779, '滚动体': 0.47747, '保持架': 0.07448,
                          '啮合频率': 13.333, '齿圈边频': 0.133, '行星轮边频': 0.248, '太阳轮边频': 0.578}
            result = {key: round(value * speed / 0.133, 4) for key, value in result_fre.items()}
        elif component == 2 and sensor == 2:
            result_fre = {'轴承内圈': 1.51221, '外圈': 1.14779, '滚动体': 0.47747, '保持架': 0.07448,
                          '啮合频率': 13.333, '齿圈边频': 0.133, '行星轮边频': 0.248, '太阳轮边频': 0.578}
            result = {key: round(value * speed / 0.133, 4) for key, value in result_fre.items()}
        elif component == 2 and sensor == 3:
            result_fre = {'轴承内圈': 8.84275, '外圈': 6.64225, '滚动体': 2.81175, '保持架': 0.46455,
                          '啮合频率': 84.933, '齿圈边频': 0.578, '行星轮边频': 0.815, '太阳轮边频': 4.117}
            result = {key: round(value * speed / 0.815, 4) for key, value in result_fre.items()}
        elif component == 2 and sensor == 4:
            result_fre = {'轴承内圈': 59.16129, '外圈': 47.88071, '滚动体': 38.65863, '保持架': 1.85265,
                          '啮合频率': 477.533, '大齿轮边频': 4.117, '小齿轮轮边频': 19.101}
            result = {key: round(value * speed / 4.117, 4) for key, value in result_fre.items()}
        elif component == 2 and sensor == 5:
            result_fre = {'轴承内圈': 188.9853, '外圈': 135.8081, '滚动体': 113.842, '保持架': 8.02242,
                          '啮合频率': 477.533, '大齿轮边频': 4.117, '小齿轮轮边频': 19.101}
            result = {key: round(value * speed / 19.101, 4) for key, value in result_fre.items()}
        elif component == 3 and sensor == 1:
            result_fre = {'轴承1内圈': 151.145, '1外圈': 116.274, '1滚动体': 143.992, '1保持架': 8.30526,
                          '轴承2内圈': 253.775, '2外圈': 204.657, '2滚动体': 176.233, '2保持架': 8.52738}
            result = {key: round(value * speed / 19.101, 4) for key, value in result_fre.items()}
        elif component == 3 and sensor == 2:
            result_fre = {'轴承内圈': 253.775, '外圈': 204.657, '滚动体': 176.233, '保持架': 8.52738}
            result = {key: round(value * speed / 19.101, 4) for key, value in result_fre.items()}
    return result


# 测试代码
if __name__ == "__main__":
    result = {}
    group58 = 2
    # machine58 = 1
    machine58 = 2
    # component = 1
    component = 2
    sensor = 1
    # rotating_frequency = 1.2
    rotating_frequency = [1.2, 1.2]
    # 这个只是在获取一些阈值 在原来的字典中定义的一些阈值
    # 通过传入的工帮 设备 组件 传感器 和旋转频率 这些字典的key来获取一些阈值
    frexx = str(theory_frequencies(group58, machine58, component, sensor, rotating_frequency))
    print(frexx)
    frexxx = frexx.replace("{", "").replace("}", "")
    print(frexxx)
    frexxxx = frexxx.replace("'", " ")
    # biqini onino 
    print(frexxxx)
    # 又变成一个字典
    result['xxxx'] = frexxxx
    print(result)
