import numpy as np
from scipy.integrate import quad
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd

def Ze(z):
    value= z**5 / ((np.exp(z) - 1) * (1 - np.exp(-z)))
    return value

def I(T, d):
    upper_limit = d / T
    integral, _ = quad(Ze, 0, upper_limit)
    return integral

def p_T(T, p0, R, A, d,D,u):
    P_ph_T = np.array([R * (T_i / d)**5 * I(T_i, d) for T_i in T])
    return p0 + P_ph_T + A * T**3 + D*np.log(u/T)

df = pd.read_csv('data-for-fit.csv')
T_data = df['T']
p_data = df['rho 0.5']

MIN_MSE = float('inf')
def USE_PROGRAM(T_data,p_data,initial_guesses):
  global MIN_MSE
  popt, pcov = curve_fit(p_T, T_data, p_data, p0=initial_guesses)
  p0_fitted, R_fitted, A_fitted, d_fitted , D_fitted, u_fitted= popt

  p_predicted = p_T(T_data, *popt)

  mse = np.mean((p_data - p_predicted) ** 2)
  if mse < MIN_MSE:
    MIN_MSE = mse
    print(initial_guesses,mse)

    print(f"Fitted p0: {p0_fitted}")
    print(f"Fitted R: {R_fitted}")
    print(f"Fitted A: {A_fitted}")
    print(f"Fitted d: {d_fitted}")
    print(f"Fitted D: {D_fitted}")
    print(f"Fitted u: {u_fitted}")
    print(f"Mean Squared Error: {mse}")

    T_fit = T_data
    p_fit = p_T(T_fit, *popt)

    plt.figure()
    plt.scatter(T_data, p_data, label='Data')
    plt.scatter(T_fit, p_fit, label='Fitted')
    plt.xlabel('T')
    plt.ylabel('p(T)')
    plt.legend()
    plt.show()

# p0, R, A, d,D,u
guess = [4,-10,0,10,0,10]
USE_PROGRAM(T_data,p_data,guess)

# from itertools import product
# # Define the set of values to choose from
# values = [1e-3,1e-2,1e-1,1e0,1e1,1e2,1e3]

# # Define the length of the permutations (e.g., 4 positions)
# length = 4

# # Generate all permutations with repetition
# perms = product(values, repeat=length)
# initial_guesses_list = list(perms)


# SAVE = 740
# for i,guess in enumerate(initial_guesses_list[SAVE:]):
#     ind = i + SAVE
#     print(f"Guess : {ind}/{len(initial_guesses_list)} = {(ind/len(initial_guesses_list)) * 100} %")
#     try:
#         USE_PROGRAM(T_data,p_data,guess)
#     except:
#         continue

  


# Lowest - 2.1e-7
# New lowest - 4e-8
# Extreme lowest - 1.3e-9

# 740
# LOWEST SO FAR : (0.001, 1.0, 1.0, 0.01) 0.3439282962449831