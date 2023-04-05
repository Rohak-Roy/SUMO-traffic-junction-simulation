import math
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# def exponential(x, vertical_stretch=1/2, coefficient=1):
#     y = coefficient * (vertical_stretch * np.exp(1/2.88539008178 * x))
#     return y

# def logarithm(x):
#     y = np.log2(x + 1)
#     return y

# print(logarithm(0))

def exponentialDecayForTrafficPhaseChange(x):
    y = 30 * (np.exp(-1/3.69269373069 * x))
    return y

inf = float('inf') + 10
print(exponentialDecayForTrafficPhaseChange(inf))