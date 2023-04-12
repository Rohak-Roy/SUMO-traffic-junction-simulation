import csv 
import pandas as pd
import matplotlib.pyplot as plt
import random
import classes_and_methods as m
import numpy as np
import math

def exponential(x, vertical_stretch=1/2, horizontal_stretch=1/2.88539008178, coefficient=1):
    y = coefficient * (vertical_stretch * np.exp(horizontal_stretch * x))
    return y

y = 1/1.39 * np.exp(-1/15 * (0 - 5))

print (m.exponential(24, horizontal_stretch=1/10))