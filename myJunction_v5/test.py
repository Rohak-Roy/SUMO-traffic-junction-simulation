import csv 
import pandas as pd
import matplotlib.pyplot as plt
import random
import classes_and_methods as m

lista = [1 , 2, 3, 4, 5]
listb = [10, 20, 30, 40, 50]
listc = [100, 120, 130, 140, 150]

retlist = list(zip(lista, listb, listc))
print(retlist)