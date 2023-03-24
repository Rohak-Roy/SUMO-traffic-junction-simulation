from numpy import random
import matplotlib.pyplot as plt
import seaborn as sns
from pprint import pprint

random.seed(42)
probability_of_car = 0.40
probability_of_heavy_good_vehicle = 0.23
probability_of_lightweight_commercial_vehicle = 0.36
probability_of_bicycle = 0.10
std_deviation = 0.1

def getGaussianDistribution(mean, std, size):
    return random.normal(loc=mean, scale=std, size=size)

def getUniformDistribution(minVal, maxVal):
    return random.uniform(minVal, maxVal)

def displayGraphs(carProb, heavyVehProb, lightweightVehProb, bicycleProb, std_deviation, size):
    carGauss = getGaussianDistribution(carProb, std_deviation, size)
    heavyGoodsVehiclesGauss = getGaussianDistribution(heavyVehProb, std_deviation, size)
    lightweightCommercialVehiclesGauss = getGaussianDistribution(lightweightVehProb, std_deviation, size)
    bicyclesGauss = getGaussianDistribution(bicycleProb, std_deviation, size)

    sns.displot(data=carGauss, kind='kde')
    plt.title('Probability Distribution for Cars.')

    sns.displot(data=heavyGoodsVehiclesGauss, kind='kde')
    plt.title('Probability Distribution for Heavy Goods Vehicles.')

    sns.displot(data=lightweightCommercialVehiclesGauss, kind='kde')
    plt.title('Probability Distribution for Lightweight Commercial Vehicles.')

    sns.displot(data=bicyclesGauss, kind='kde')
    plt.title('Probability Distribution for Bicycles.')

    plt.show()

displayGraphs(probability_of_car, probability_of_heavy_good_vehicle, probability_of_lightweight_commercial_vehicle, probability_of_bicycle, std_deviation, 1000)

steps = 1000
results_list = []
for i in range(steps):
    carProb = getGaussianDistribution(0.4, 0.1, 1)
    heavyGoodsVehicleProb = getGaussianDistribution(0.23, 0.1, 1)
    lightweightCommercialVehicleProb = getGaussianDistribution(0.36, 0.1, 1)
    bicycleProb = getGaussianDistribution(0.1, 0.1, 1)

    array = [carProb, heavyGoodsVehicleProb, lightweightCommercialVehicleProb, bicycleProb]
    results_list.append(array)


pprint(results_list)