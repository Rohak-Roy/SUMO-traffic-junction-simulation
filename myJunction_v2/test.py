import csv 
import pandas as pd
import matplotlib.pyplot as plt
import random
  
header = ['Vehicles Stopped', 'Total Waiting Time', 'CO2 Emissions Released']

data = []
with open('some.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for i in range(10):
        num1 = random.randint(0, 10)
        num2 = random.randint(10, 20)
        num3 = random.randint(20, 30)
        data = [num1, num2, num3]
        writer.writerow(data)


db = pd.read_csv('some.csv')
print(db)

db['Total Waiting Time'].plot()
plt.ylabel("CO2 Emissions")
plt.xlabel("Seconds")
plt.show()