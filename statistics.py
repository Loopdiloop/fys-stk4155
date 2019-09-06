import numpy as np
from sklearn.metrics import r2_score as r2


def calc_MSE(z, z_tilde):
    mse = 0
    n=len(z)
    for i in range(n):
        mse += (z[i] - z_tilde[i])**2
    return mse/n


def calc_R2_score(z, z_tilde):
    mse = 0
    ms_avg = 0
    n=len(z)
    for i in range(n):
        mse += (z[i] - z_tilde[i])**2
        ms_avg += (z[i] - np.mean(z))**2
    return 1-mse/ms_avg

def calc_R2_score_sklearn(z, z_tilde):
    return r2(z, z_tilde)