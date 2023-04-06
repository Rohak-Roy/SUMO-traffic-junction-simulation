import pandas as pd
import matplotlib.pyplot as plt

df_after = pd.read_csv('after.csv')
df_before = pd.read_csv('before.csv')

figure = plt.figure()

# figure.add_subplot(1, 2, 1)
# df_before['Number of Vehicles Stopped'].plot()
# plt.ylabel('Number of Vehicles Stopped - Before')
# plt.xlabel('Seconds Elapsed')

# figure.add_subplot(1, 2, 2)
# df_after['Number of Vehicles Stopped'].plot()
# plt.ylabel('Number of Vehicles Stopped - After')
# plt.xlabel('Seconds Elapsed')

# plt.show()

# figure.add_subplot(1, 2, 1)
# df_before['Total Waiting Time of All Vehicles'].plot()
# plt.ylabel('Total Waiting Time of All Vehicles (s) - Before')
# plt.xlabel('Seconds Elapsed')

# figure.add_subplot(1, 2, 2)
# df_after['Total Waiting Time of All Vehicles'].plot()
# plt.ylabel('Total Waiting Time of All Vehicles (s) - After')
# plt.xlabel('Seconds Elapsed')

# plt.show()

figure.add_subplot(1, 2, 1)
df_before['Total CO2 Emissions Released'].plot()
plt.ylabel('Total CO2 Emissions Released (mg/s) - Before')
plt.xlabel('Seconds Elapsed')

figure.add_subplot(1, 2, 2)
df_after['Total CO2 Emissions Released'].plot()
plt.ylabel('Total CO2 Emissions Released (mg/s) - After')
plt.xlabel('Seconds Elapsed')

plt.show()
