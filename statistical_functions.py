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


"""def save_statistics(self): #M:Add total avg to statistics file properly.
        y = np.concatenate(self.inst.z_1d)
        #y_tilde = np.concatenate(self.y_tilde)
        y_tilde = self.y_tilde
        self.mse = calc_MSE(y, y_tilde)
        self.R2score = calc_R2_score(y, y_tilde)"""


def calc_statistics(no_datasets, z, z_tilde):
    n = no_datasets
    mse = np.zeros(n)
    calc_r2 = np.zeros(n)

    for i in range(n):
        mse[i] = calc_MSE(z[i], z_tilde[i])
        calc_r2[i] = calc_R2_score(z[i], z_tilde[i])
    return mse, calc_r2


