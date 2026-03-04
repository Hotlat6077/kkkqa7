import numpy as np
from sklearn.decomposition import PCA


def pca(data):
    _sig_soure = data - np.mean(data)
    # 构造矩阵X
    m = 500
    X = []
    for i in range(len(data)-m):
        X.append(data[i:i+m])
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
    # 展示去噪效果
    # plt.figure()
    # plt.plot(sig_zip)
    # plt.show()
    return sig_zip