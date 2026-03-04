import numpy as np

def cepstrum(x):
    y = np.fft.fft(x)
    y = np.log(np.abs(y))
    y = np.fft.ifft(y).real
    return y