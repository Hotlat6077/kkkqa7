import numpy as np

def order_analysis(vibration_signal, sampling_frequency, rpm):
    rpm=[float(rpm)]
    rpm=rpm*100
    rps = np.array(rpm)
    t = np.arange(len(vibration_signal)) / sampling_frequency
    rps_interp = np.interp(t, np.linspace(0, t[-1], len(rps)), rps)
    inst_phase = np.cumsum(rps_interp) / sampling_frequency * 2 * np.pi
    resampled_signal = np.interp(np.linspace(0, inst_phase[-1], len(vibration_signal)), inst_phase, vibration_signal)
    freqs = np.fft.fftfreq(len(resampled_signal), d=1 / sampling_frequency)
    fft_values = np.fft.fft(resampled_signal)
    pos_freqs = freqs[:len(freqs) // 2]
    pos_fft_values = np.abs(fft_values[:len(fft_values) // 2])
    return pos_freqs, pos_fft_values

def order_frequency(vibration_signal, sampling_frequency, rpm,faultfrequency):
    # Convert RPM to RPS (Revolutions Per Second)
    rpm=[rpm]*100
    rps = np.array(rpm)
    # Generate time vector based on the length of vibration signal and sampling frequency
    t = np.arange(len(vibration_signal)) / sampling_frequency
    # Interpolate the RPM data to match the vibration signal length
    rps_interp = np.interp(t, np.linspace(0, t[-1], len(rps)), rps)
    # Instantaneous phase calculation
    inst_phase = np.cumsum(rps_interp) / sampling_frequency * 2 * np.pi
    # Resampling the vibration signal based on the instantaneous phase
    resampled_signal = np.interp(np.linspace(0, inst_phase[-1], len(vibration_signal)), inst_phase, vibration_signal)
    # FFT analysis on the resampled signal
    freqs = np.fft.fftfreq(len(resampled_signal), d=1 / sampling_frequency)
    fft_values = np.fft.fft(resampled_signal)
    # Only keep the positive part of the spectrum
    pos_freqs = freqs[:len(freqs) // 2]
    pos_fft_values = np.abs(fft_values[:len(fft_values) // 2])

    # x1 = list(pos_freqs).index(20)
    # x2 = list(pos_freqs).index(40)

    diffs = [abs(xx - faultfrequency) for xx in pos_freqs]
    min_diff_index = diffs.index(min(diffs))
    x1 = list(pos_freqs).index(pos_freqs[min_diff_index])
    x2=2*x1
    if x2>12800:
        x2=x1

    y1=pos_fft_values[x1]
    y2=pos_fft_values[x2]
    result=[y1,y2]
    return result

