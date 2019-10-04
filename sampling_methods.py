import numpy as np 

import statistical_functions as statistics
from fit_matrix import fit
from functions import franke_function

class sampling():
    def __init__(self, inst):
        self.inst = inst

    def kfold_cross_validation(self, k, method, deg=5, lambd=1):
        """Method that implements the k-fold cross-validation algorithm. It takes
        as input the method we want to use. if "least squares" an ordinary OLS will be evaulated.
        if "ridge" then the ridge method will be used, and respectively the same for "lasso"."""

        inst = self.inst
        lowest_mse = 1e2

        self.mse = []
        self.R2 = []
        design_matrix = fit(inst)
        
        for i in range(self.inst.k):
            #pick the i-th set as test
            inst.sort_training_test_kfold(i)
            inst.fill_array_test_training()

            design_matrix.create_design_matrix(deg = deg)
            if method == "least squares":
                z_pred, beta_pred = design_matrix.fit_design_matrix_numpy()
            elif method == "ridge":
                z_pred, beta_pred = design_matrix.fit_design_matrix_ridge(lambd)
            elif method == "lasso":
                z_pred, beta_pred = design_matrix.fit_design_matrix_lasso()
            else:
                sys.exit("Wrongly designated method: ", method)


            #Find out which values get predicted by the training set
            X_test = design_matrix.create_design_matrix(x=inst.test_x_1d, y=inst.test_y_1d, z=inst.test_z_1d, N=inst.N_testing, deg=deg)
            z_test = design_matrix.test_design_matrix(beta_pred)

            # Generate analytical solution for statistics
            z_analytical = franke_function(inst.test_x_1d, inst.test_y_1d)

            # Statistically evaluate the training set with test and analytical solution.
            mse, calc_r2 = statistics.calc_statistics(z_analytical, z_test)
            self.mse.append(mse)
            self.R2.append(calc_r2)
            # If needed/wanted?: 
            if abs(mse) < lowest_mse:
                lowest_mse = mse
                self.best_predicting_beta = beta_pred
            
