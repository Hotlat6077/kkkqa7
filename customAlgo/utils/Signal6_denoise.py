# 六、降噪的算法放这里
# 降噪denoise
import math
import numpy as np
import pywt
from vmdpy import VMD as vmd

from utils import *  #


class denoisex():
    """
    降噪算法
    降噪6
    """
    def __init__(self,RawSignal=None, RawSignal2=None, SampleFraquency=None, M=None, mu=None, N=None):
        self.RawSignal=RawSignal
        self.RawSignal2 = RawSignal2
        self.SampleFraquency=SampleFraquency
        self.M = M
        self.mu = mu
        self.N=N

    # 1.小波降噪
    def waveletdx(self):
        data = self.RawSignal
        data = data.T.tolist()  # 将np.ndarray()转为列表
        w = pywt.Wavelet('sym8')  # 选择sym8小波基
        [ca5, cd5, cd4, cd3, cd2, cd1] = pywt.wavedec(data, w, level=5)  # 5层小波分解
        length1 = len(cd1)
        length0 = len(data)
        Cd1 = np.array(cd1)
        abs_cd1 = np.abs(Cd1)
        median_cd1 = np.median(abs_cd1)
        sigma = (1.0 / 0.6745) * median_cd1
        lamda = 20 * sigma * math.sqrt(2.0 * math.log(float(length0), math.e))  # 固定阈值计算
        usecoeffs = []
        usecoeffs.append(ca5)  # 向列表末尾添加对象
        # 软硬阈值折中的方法
        a = 0.5
        for k in range(length1):
            if (abs(cd1[k]) >= lamda).all():
                cd1[k] = sgn(cd1[k]) * (abs(cd1[k]) - a * lamda)
            else:
                cd1[k] = 0.0

        length2 = len(cd2)
        for k in range(length2):
            if (abs(cd2[k]) >= lamda).all():
                cd2[k] = sgn(cd2[k]) * (abs(cd2[k]) - a * lamda)
            else:
                cd2[k] = 0.0

        length3 = len(cd3)
        for k in range(length3):
            if (abs(cd3[k]) >= lamda).all():
                cd3[k] = sgn(cd3[k]) * (abs(cd3[k]) - a * lamda)
            else:
                cd3[k] = 0.0

        length4 = len(cd4)
        for k in range(length4):
            if (abs(cd4[k]) >= lamda).all():
                cd4[k] = sgn(cd4[k]) * (abs(cd4[k]) - a * lamda)
            else:
                cd4[k] = 0.0

        length5 = len(cd5)
        for k in range(length5):
            if (abs(cd5[k]) >= lamda).all():
                cd5[k] = sgn(cd5[k]) * (abs(cd5[k]) - a * lamda)
            else:
                cd5[k] = 0.0
        usecoeffs.append(cd5)
        usecoeffs.append(cd4)
        usecoeffs.append(cd3)
        usecoeffs.append(cd2) 
        usecoeffs.append(cd1)
        recoeffs = pywt.waverec(usecoeffs, w)  # 信号重构
        return recoeffs
    # 2.软阈值降噪
    def softx(self):
        data = self.RawSignal
        w = pywt.Wavelet('dB10')#选择dB10小波基
        ca3, cd3, cd2, cd1 = pywt.wavedec(data, w, level=3)  # 3层小波分解
        ca3 = ca3.squeeze(axis=0) #ndarray数组减维：(1，a)->(a,)
        cd3 = cd3.squeeze(axis=0)
        cd2 = cd2.squeeze(axis=0)
        cd1 = cd1.squeeze(axis=0)
        length1 = len(cd1)
        length0 = len(data[0])

        abs_cd1 = np.abs(np.array(cd1))
        median_cd1 = np.median(abs_cd1)

        sigma = (1.0 / 0.6745) * median_cd1
        lamda = sigma * math.sqrt(2.0 * math.log(float(length0 ), math.e))
        usecoeffs = []
        usecoeffs.append(ca3)

        #软阈值方法
        for k in range(length1):
            if (abs(cd1[k]) >= lamda/np.log2(2)):
                cd1[k] = sgn(cd1[k]) * (abs(cd1[k]) - lamda/np.log2(2))
            else:
                cd1[k] = 0.0

        length2 = len(cd2)
        for k in range(length2):
            if (abs(cd2[k]) >= lamda/np.log2(3)):
                cd2[k] = sgn(cd2[k]) * (abs(cd2[k]) - lamda/np.log2(3))
            else:
                cd2[k] = 0.0

        length3 = len(cd3)
        for k in range(length3):
            if (abs(cd3[k]) >= lamda/np.log2(4)):
                cd3[k] = sgn(cd3[k]) * (abs(cd3[k]) - lamda/np.log2(4))
            else:
                cd3[k] = 0.0

        usecoeffs.append(cd3)
        usecoeffs.append(cd2)
        usecoeffs.append(cd1)
        recoeffs = pywt.waverec(usecoeffs, w)#信号重构
        return recoeffs

    # 3.主成分分析降噪
    def pcax(self):
        from sklearn.decomposition import PCA
        _sig_soure = self.RawSignal - np.mean(self.RawSignal)
        # 构造矩阵X
        m = 500
        X = []
        for i in range(len(self.RawSignal)-m):
            X.append(self.RawSignal[i:i+m])
        X = np.array(X).reshape(-1,m).T
        # 构造协方差矩阵
        C = np.matmul(X, X.T)
        # 求取特征值
        vals, vec = np.linalg.eig(C)
        vals = np.sort(vals)/np.sum(vals)
        vals = vals[::-1]
        # 计算PCA分解后主成分分量个数（按照保留90%能量计算）
        for _component in range(1, len(vals)):
            energy = np.sum(vals[:_component])
            if energy >= 0.80:
                break
        # 对矩阵X进行PCA分解
        estimator = PCA(_component)
        # 获取PCA结果
        X_trans = estimator.fit_transform(X)
        # 获取特征矩阵
        _vec = estimator.components_
        # 恢复原信号向量矩阵
        X_zip = np.matmul(_vec.T, X_trans.T)
        # 恢复原信号
        sig_zip = list(X_zip.T[0])
        for i in range(1, m):
            sig_zip.append(X_zip.T[i, -1])
        return sig_zip

    # 4.自适应滤波
    def lmsx(self):
        # 输入：
        # x - 输入信号向量
        # M - 滤波器长度
        # mu - 步长因子
        N = len(self.RawSignal)
        w = np.zeros((self.M, 1))
        y = np.zeros((N, 1))
        e = np.zeros((N, 1))
        x_delay = np.zeros((self.M, 1))
        # 自适应滤波主体循环
        for n in range(N):
            x_delay[1:] = x_delay[:-1]
            x_delay[0] = self.RawSignal[n]
            y[n] = np.dot(w.T, x_delay)
            e[n] = self.RawSignal[n] - y[n]
            k = 0.1* x_delay / (self.mu + np.dot(x_delay.T, x_delay))
            w = w + k * e[n]
        return y

    # 5.谱峭度
    def Spectrum_kurtosis(self):
        from scipy import signal
        TKUR = []
        N = [5, 10, 20, 50, 100, 200, 500, 1000]  # 可以根据实际需求修改
        for i in N:
            f, t, Zxx = signal.stft(self.RawSignal, self.SampleFraquency, nperseg=i)
            a = np.abs(Zxx)
            # print(len(a))
            KUR = []
            len_ = a.shape[1]
            for j in range(len(f)):
                K = 0
                mean_ = a[j].mean(axis=0)  # 均值
                std_ = a[j].std(axis=0)  # 标准差
                for k in range(len_):
                    K += (a[j].tolist()[k] - mean_) ** 4
                kur = K / ((len_ - 1) * std_ ** 4)  # 峭度
                KUR.append(kur)
            TKUR.append(KUR)
        result = []
        for i in range(len(TKUR)):
            m = max(TKUR[i])
            result.append(m)
        index_result = result.index(max(result))
        f, t, Zxx = signal.stft(self.RawSignal, self.SampleFraquency, nperseg=N[index_result])
        a = np.abs(Zxx)
        result_KUR = []
        len_ = a.shape[1]
        for j in range(len(f)):
            K = 0
            mean_ = a[j].mean(axis=0)  # 均值
            std_ = a[j].std(axis=0)  # 标准差

            for k in range(len_):
                K += (a[j].tolist()[k] - mean_) ** 4
            kur = K / ((len_ - 1) * std_ ** 4)  # 峭度
            result_KUR.append(kur)
        # print(result_KUR)
        return result_KUR

    #6.稀疏表示
    def sr(self):
        from ksvd import ApproximateKSVD
        X = self.RawSignal

        aksvd = ApproximateKSVD(n_components=120)
        dictionary = aksvd.fit(X).components_
        gamma = aksvd.transform(X)
        y = gamma.dot(dictionary)
        return y

    # 7.相关系数分析
    def corrx(self):
        # 计算信号1和信号2的相关系数
        corr = np.corrcoef(self.RawSignal, self.RawSignal2)[0, 1]
        return corr

    # 6.共振解调
    def resonancex(self):
        # 引包
        from scipy.fftpack import hilbert, fft,ifft
        # 最小
        fmin = 200  # 选取频率范围：最小
        fmax = 1000  # 选取频率范围：最大
        # 最大
        n = 1  # 选择分析列数
        m = len(self.RawSignal)  # 信号长度
        f = np.arange(0, m) * self.SampleFraquency / m  # 频域波形很坐标 ：频率 fs
        f_half = f[0:int(np.round(m / 2))]  # 取一半 频率坐标
        fmin_number = int(np.round(fmin * m / self.SampleFraquency))  # 获取点数 对应的下标
        fmax_number = int(np.round(fmax * m / self.SampleFraquency)) # 获取点数 对应的下标
        y_new = [0 * i for i in range(m)]  # 快速创建一个元素为0的列表 y_new
        y = np.array(self.RawSignal) # 转为数组
        y_fft = fft(y)  # fft # 傅里叶变换
        y_new[fmin_number:fmax_number] = y_fft[fmin_number:fmax_number]  # 替换元素 # 取频率范围内的值
        y_new[m - fmax_number:m - fmin_number] = y_fft[m - fmax_number:m - fmin_number]  # 替换元素 # 取频率范围内的值
        y_ifft = ifft(y_new).real  # 逆变换并取复数的实部 #ifft
        H = np.abs(hilbert(y_ifft) - np.mean(y_ifft))  # 包络 # hilbert
        HP = np.abs(fft(H - np.mean(H))) * 2 / m  # 包络谱 # fft
        HP_half = HP[0:int(np.round(m / 2))]  # #   取一半 包络谱
        return f_half, HP_half  # 返回 频率坐标 和 包络谱

    # 10.重采样
    def reconstruction(self,q):
        from scipy.signal import decimate
        samples_new=int(len(self.RawSignal)/q)
        xnew=np.linspace(0,len(self.RawSignal),samples_new)
        ynew=decimate(self.RawSignal.reshape(1,-1),q)
        return xnew,ynew

    # 11.相关系数分析
    def cztx(self):
        from czt import czt, czt_points
        fs=self.SampleFraquency
        f1 = 8
        M = fs // 2  # Just positive frequencies, like rfft
        a = np.exp(-f1 / fs)  # Starting point of the circle, radius < 1
        w = np.exp(-1j * np.pi / M)  # "Step size" of circle
        points = czt_points(M + 1, w, a)  # M + 1 to include Nyquist
        z_vals = czt(self.RawSignal, M + 1, w, a)  # Include Nyquist for comparison to rfft
        freqs = np.angle(points) * fs / (2 * np.pi)  # angle = omega, radius = sigma
        xx = freqs
        yy = abs(z_vals)
        return xx,yy

    #12.Teager 能量算子解调
    def teod(self):
        x = self.RawSignal
        y = np.zeros(len(x))
        w = np.zeros(len(x))
        a = np.zeros(len(x))
        for i in range(1, len(x) - 1):
            y[i] = x[i] - x[i - 1]

        ey = Teager_power_function(y)
        ex = Teager_power_function(x)
        for i in range(1, len(x) - 1):
            arccos_value = 1 - (ey[i] + ey[i + 1]) / (4 * ex[i])
            if 1.0 < arccos_value:
                arccos_value = 1.0
            elif arccos_value < -1.0:
                arccos_value = -1.0

            w[i] = np.arccos(round(arccos_value, 3))
            a[i] = np.sqrt(np.abs(ex[i] / (1 - (1 - (ey[i] + ey[i + 1]) / (4 * ex[i])) ** 2)))
        return  w,a

    #13.迭代阈值收缩算法

    def ista(self):
        from scipy.linalg import orth
        x=self.RawSignal
        Z = x[0:1000]
        Z=np.array(Z)
        Z = Z.reshape(1, 1000)
        X = np.zeros((1, 128))   #X维度可修改
        Psi = np.eye(1000)
        Phi = np.random.randn(128, 1000)
        Phi = np.transpose(orth(np.transpose(Phi)))
        W_d = np.dot(Phi, Psi)
        W_d=np.mat(W_d)
        for i in range(1):
            X[i] = np.dot(W_d, Z[i, :])
        X = np.mat(X).T
        eig, eig_vector = np.linalg.eig(W_d.T * W_d)
        assert 2 > np.max(eig)
        del eig, eig_vector

        W_e = W_d.T / 2

        recon_errors = []
        Z_old = np.zeros((W_d.shape[1], 1))
        for i in range(1000):
            temp = W_d * Z_old - X
            Z_new = shrinkage(Z_old - W_e * temp, 0.1 / 2)
            if np.sum(np.abs(Z_new - Z_old)) <= 0.00001: break
            Z_old = Z_new
            recon_error = np.linalg.norm(X - W_d * Z_new, 2) ** 2
            recon_errors.append(recon_error)
        Z_new = Z_new.A
        result = []
        for i in Z_new:
            for y in i:
                result.append(y)
        return result

    # 13.VMD_CVM(variational mode decomposition (VMD) algorithm and Cramer Von Misses (CVM) statistic)
    def VMD_CVM(self, NIMF=10, Np=36):

        # Check noisy is a 1D array_like object
        Pf = np.exp(-np.arange(0, NIMF - 1))

        pts = len(self.RawSignal)  # data length

        # Some sample parameters for VMD
        alpha = 2000  # moderate badwidth constraint
        tau = 0  # noise-tolerance (no strict fidelity enforcement)
        DC = 0  # no DC part imposed
        init = 1  # initialize omegas uniformly
        tol = 1e-7

        # Variational mode decomposition of the noisy signal
        imf, _, _ = vmd(self.RawSignal, alpha, tau, NIMF, DC, init, tol)

        if imf.shape[0] < NIMF:
            NIMF = imf.shape[0] - 1
            print('NIMF found to be less than the size of actual imf')

        rec = np.zeros(shape=imf.shape, dtype=np.float64)

        # Determining k'_2 index
        # ----------------------

        # Compute distance between each mode and the estimated noisy ECD
        Dist = np.empty(shape=NIMF, dtype=np.float64)
        tempx = np.empty(shape=imf.shape[1], dtype=np.float64)
        nEdf, nInd = ecdf(self.RawSignal)
        for imfcnt in range(NIMF):
            tempx = imf[imfcnt, :]
            z = cdfcalc(np.sort(tempx), nEdf, nInd)
            Dist[imfcnt] = cvm(z, pts)

        D = np.abs(np.diff(Dist))
        n = np.argmax(D)
        while n <= NIMF / 2:
            D[n] = 0
            n = np.argmax(D)

        ni = NIMF - n
        if ni < 3:
            ni = 3

        # Compute thresholds
        # ------------------
        imfvec = np.empty(shape=(imf.shape[0] - (NIMF - ni - 1)) * imf.shape[1], dtype=np.float64)
        imfvec = imf[NIMF - ni - 1:, :].flatten()

        PfvThvec, disn_m, ind_m = threshvspfa(imfvec, self.N)

        # Detection of signal/noisy coefficients in modes containing signal
        # -----------------------------------------------------------------
        TH = PfvThvec[0, :]
        PF = PfvThvec[1, :]
        for imfcnt in range(NIMF - ni + 1):
            temp = imf[imfcnt, :]  # Current IMF values
            indpf = np.argmin(
                np.abs(Pf[imfcnt] - PF))  # Matches the optimal Pfa calulated for current IMF with available PFAs
            thresh = TH[indpf]  # Extract the threshold value for current IMF

            # Signal/noise discrimination in each window
            booln = np.zeros(shape=temp.shape[0], dtype=np.int_)
            for jj in range(self.N, pts - self.N):  # range(N//2, pts-N//2):
                x = temp[(jj - self.N // 2):(jj + self.N // 2)]
                z = cdfcalc(np.sort(x), disn_m, ind_m)

                test = cvm(z, self.N)  # CVM statistic
                if test > thresh:  # statistic > threshold: signal present
                    booln[jj] = 1

            # Consider detection only if it happens at least for length N; removes impulse-like noise!
            D = np.diff(np.pad(booln, (1, 1), 'constant', constant_values=(0, 0)))  # Find "edges"
            bg = np.nonzero(D == 1)[0]  # Beginning of clustes of 1's (supossedly signal)
            ed = np.nonzero(D == -1)[0] - 1  # End of clusters
            for ii in range(len(bg)):
                if ((ed[ii] - bg[
                    ii]) < Np):  # If the length of cluster is too small we attribute detection to noise peak
                    booln[bg[ii]:ed[ii]] = 0  # No detection of signal there

            # Effectively eliminate detected noise peaks
            rec[imfcnt, :] = temp * booln

        rec[0] = imf[0]
        sigrec = np.sum(rec, axis=0)

        return imf, rec, sigrec

    # 14.Autoregressive Model
    def AR(self, lag):
        from statsmodels.tsa.ar_model import AutoReg
        model = AutoReg(self.RawSignal, lags=lag)
        result = model.fit()
        fitted_values = model.predict(result.params, start=0, end=len(self.RawSignal) - 1)
        return np.nan_to_num(fitted_values)

    # 15.Total Variation Denoising
    def TVD(self):
        N = len(self.RawSignal)
        lamda = np.sqrt(0.0001 * N) / 20
        X = np.zeros(N)

        k, k0, kz, kf = 0, 0, 0, 0
        vmin = self.RawSignal[0] - lamda
        vmax = self.RawSignal[0] + lamda
        umin = lamda
        umax = -lamda

        while k < N:

            if k == N - 1:
                X[k] = vmin + umin
                break

            if self.RawSignal[k + 1] < vmin - lamda - umin:
                for i in range(k0, kf + 1):
                    X[i] = vmin
                k, k0, kz, kf = kf + 1, kf + 1, kf + 1, kf + 1
                vmin = self.RawSignal[k]
                vmax = self.RawSignal[k] + 2 * lamda
                umin = lamda
                umax = -lamda

            elif self.RawSignal[k + 1] > vmax + lamda - umax:
                for i in range(k0, kz + 1):
                    X[i] = vmax
                k, k0, kz, kf = kz + 1, kz + 1, kz + 1, kz + 1
                vmin = self.RawSignal[k] - 2 * lamda
                vmax = self.RawSignal[k]
                umin = lamda
                umax = -lamda

            else:
                k += 1
                umin = umin + self.RawSignal[k] - vmin
                umax = umax + self.RawSignal[k] - vmax
                if umin >= lamda:
                    vmin = vmin + (umin - lamda) * 1.0 / (k - k0 + 1)
                    umin = lamda
                    kf = k
                if umax <= -lamda:
                    vmax = vmax + (umax + lamda) * 1.0 / (k - k0 + 1)
                    umax = -lamda
                    kz = k

            if k == N - 1:
                if umin < 0:
                    for i in range(k0, kf + 1):
                        X[i] = vmin
                    k, k0, kf = kf + 1, kf + 1, kf + 1
                    vmin = self.RawSignal[k]
                    umin = lamda
                    umax = self.RawSignal[k] + lamda - vmax

                elif umax > 0:
                    for i in range(k0, kz + 1):
                        X[i] = vmax
                    k, k0, kz = kz + 1, kz + 1, kz + 1
                    vmax = self.RawSignal[k]
                    umax = -lamda
                    umin = self.RawSignal[k] - lamda - vmin

                else:
                    for i in range(k0, N):
                        X[i] = vmin + umin * 1.0 / (k - k0 + 1)
                    break

        return X

    # 16.Total Variation Denoising via the Moreau Envelope
    def METV(self, num):
        from utils import denoising_1D_TV  # 这里是不是少给了一个utils的 数据处理的工具包
        N = len(self.RawSignal)
        lamda = np.sqrt(0.0001 * N) / 10
        err = 0.001
        alpha = 0.3 / lamda

        K, N = 0, len(self.RawSignal)
        X = np.zeros(N)
        U = np.ones(N)

        while K <= num and np.linalg.norm(U - X) > err:
            Z = self.RawSignal + lamda * alpha * (X - denoising_1D_TV(self.RawSignal, 1 / alpha))
            U = X
            X = denoising_1D_TV(Z, lamda)
            K += 1

        return X

    # 17.Minmax-concave Total Variation Denoising
    def MCTV(self, num):
        from utils import denoising_1D_TV, shrink, Dx, Dxt
        K, N = 0, len(self.RawSignal)
        X = np.zeros(N)
        U = np.ones(N)
        lamda = np.sqrt(0.0001 * N) / 10
        err = 0.001
        alpha = 0.3 / lamda

        while K <= num and np.linalg.norm(U - X) > err:
            C = Dxt(Dx(X)) - Dxt(shrink(Dx(X), 1 / alpha))
            Z = self.RawSignal + lamda * alpha * C
            U = X
            X = denoising_1D_TV(Z, lamda)
            K += 1

        return X

    #变窗fft
    def addwindow_fftx(self,name):
        from middle.SignalProcessing6_8add_fft import choose_windows
        import numpy.fft as fft
        fs = self.SampleFraquency  # 采样频率
        Sampling_points = len(self.RawSignal)  # 采样点数，fft后的点数就是这个数
        df = 1 / fs  # 采样间隔时间
        y = self.RawSignal[:]
        window,Amplitude_correction_factor=choose_windows(name=name, N=len(y))#加窗
        y=y*window
        y = list(map(float, y))
        y = np.array(y)
        f_values = np.linspace(0.0, fs / 2.0, Sampling_points // 2)
        fft_values_ = fft.fft(y)
        fft_values = (2.0 / Sampling_points * np.abs(fft_values_[0:Sampling_points // 2]))*Amplitude_correction_factor
        return f_values,fft_values
    # 带阻滤波 2024年6月8号####################
    def BRF(self,lowcut,highcut,N):
        import numpy as np
        import scipy.signal as signal
        fs = self.SampleFraquency  # 采样频率
        len_ = len(self.RawSignal)
        df = 1 / fs
        t = np.linspace(0.0, len_ * df, len_)
        x =  self.RawSignal   # 原始信号
        # 确定带阻滤波器的参数
        lowcut = float(lowcut) # 阻带的下截止频率
        highcut = float(highcut)  # 阻带的上截止频率
        # 设计带阻滤波器
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = signal.butter(int(N), [low, high], btype='bandstop')
        # 应用滤波器到时域信号
        filtered_signal = signal.lfilter(b, a, x)
        return t, filtered_signal


# #################################
def sgn(num):
    if(num.all() > 0.0):
        return 1.0
    elif(num.all() == 0.0):
        return 0.0
    else:
        return -1.0

def Teager_power_function(Signal):
    Teager_power=np.zeros(len(Signal))
#离散Teager能量算子的公式=S（n）*S（n）-S(n+1)*S*(n-1)
    for i in range(1,len(Signal)-1):
        Teager_power[i]=Signal[i]*Signal[i]-Signal[i+1]*Signal[i-1]
    return Teager_power

def shrinkage(x, theta):
    return np.multiply(np.sign(x), np.maximum(np.abs(x) - theta, 0))


