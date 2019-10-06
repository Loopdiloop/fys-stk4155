import numpy as np 
import matplotlib.pyplot as plt 
import sys
import os


from data_generation import data_generate
from fit_matrix import fit
from visualization import plot_3d, plot_bias_var_tradeoff, plot_mse_vs_complexity
import statistical_functions as statistics
from sampling_methods import sampling

"""Running task c) of the project.
Running additional variance-bias tradeoff calculations
for different degrees of polynomials of OLS. 

Q: k-fold??? Or just a single test/training set?
Q: Just a single, "random" run of each?
Hmmmmmm...  
Q: Plotting the bias-variance tradeoff on y-axis? Or just mse etc?

Need to do: 
- Correct sampling
- Bias-var tradeoff correct
- Plot correct thing. """

n = 100                 # no. of x and y coordinates
deg = range(1,20)        # degree of polynomial
noise = 0.1            # if zero, no contribution. Otherwise scaling the noise.

# k batches for k-fold.
k = 10
method = "least squares" # "least squares", "ridge" or "lasso"
#method = "ridge"

best_mse_train = []
best_mse_test = []
average_mse_train = []
average_mse_test = []
best_bias_var_tradeoff = []

for pol_deg in deg:
    #If best of k-fold for the plotting:
    # Generate data
    dataset = data_generate(n, noise)
    liste1 = [dataset] #M: Trenger du denne fremdeles, F?
    dataset.generate_franke()
    dataset.sort_in_k_batches(k)

    #Run k-fold algorithm and fit models.
    sample = sampling(dataset)
    if method == "least squares":
        sample.kfold_cross_validation(k, method, deg = pol_deg)
    else:
        sample.kfold_cross_validation(k, method, deg = pol_deg, lambd = 1e-2)
    
    #best_mse_test.append(np.min(sample.mse[np.argmin(np.abs(np.array(sample.mse)))]))
    #best_mse_train.append(np.min(sample.mse_train[np.argmin(np.abs(np.array(sample.mse)))]))
    best_mse_test.append(np.min(sample.mse))
    best_mse_train.append(sample.mse_train[ np.argmin(sample.mse)])
    average_mse_test.append(np.average(sample.mse))
    average_mse_train.append(np.average(sample.mse_train))
    best_bias_var_tradeoff.append(sample.bias_var_tradeoff[np.argmin(np.abs(np.array(sample.bias_var_tradeoff)))])

    print("\n" + "Run for k = ", k, " and deg = ", pol_deg)
    statistics.print_mse(sample.mse)
    statistics.print_R2(sample.R2)

#plot_bias_var_tradeoff(deg, best_bias_var_tradeoff)
plot_mse_vs_complexity(deg, best_mse_test, best_mse_train)
plot_mse_vs_complexity(deg, average_mse_test, average_mse_train)


try:
    os.remove("backup_data.npz")
except:
    print("Error: backup_data.npz not deleted.")