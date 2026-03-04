from scipy.fftpack import fft, fftshift, ifft
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import pywt


def wavex(signal):
    signal2=np.array(signal)
    yy=signal2[60001:70000]
    coeffs = pywt.wavedec(yy, 'bior3.7', level=3)
    y2 = coeffs[2]
    return y2

def plot_(data,a,b):
    img=io.BytesIO()
    img1 = plt.figure(figsize=(a, b))
    plt.plot(data, linewidth=1)
    ax1 = img1.gca()
    ax1.spines['bottom'].set_color('w')
    ax1.spines['top'].set_color('w')
    ax1.spines['left'].set_color('w')
    ax1.spines['right'].set_color('w')
    plt.xticks(fontproperties='Times New Roman', size=16)
    plt.yticks(fontproperties='Times New Roman', size=16)
    for t in ax1.xaxis.get_ticklines(): t.set_color('w')
    for t in ax1.yaxis.get_ticklines(): t.set_color('w')
    ax1.tick_params(direction='in', length=1, width=2, colors='w',
                    grid_color='r')
    plt.savefig(img, format='png', transparent=True)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url


def imgplot6(signal2):
    wave_result=wavex(signal2)
    plot_url = plot_(wave_result,9,3,)
    return plot_url