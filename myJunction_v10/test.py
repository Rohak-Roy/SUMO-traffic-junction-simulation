import pandas as pd
import numpy as np

df = pd.read_csv('mean_and_std.csv')
mean_and_std = df.to_numpy()

train_mean = mean_and_std[0]
train_std = mean_and_std[1]

arr = np.random.rand(1, 19)
print(f'Original array is = {arr}')

arr_norm = (arr - train_mean) / train_std
print(f'Normalized array is = {arr_norm}')

print((arr[0][5] - train_mean[5]) / train_std[5])

print(f'Normalized array shape = {arr_norm.shape}')