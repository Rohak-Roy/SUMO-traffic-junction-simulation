from numpy import random
import matplotlib.pyplot as plt
import seaborn as sns
from pprint import pprint
import numpy as np

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

def getRouteId(route1, route2, route3, route4):
    num = getUniformDistribution(0, 1)
    if num < 0.25:
        return route1
    if num < 0.50:
        return route2
    if num < 0.75:
        return route3
    if num < 1.00:
        return route4

#displayGraphs(probability_of_car, probability_of_heavy_good_vehicle, probability_of_lightweight_commercial_vehicle, probability_of_bicycle, std_deviation, 1000)

steps = 1000
uniform_distribution_list = []
carNum, heavyGoodsVehNum, miniTruckNum, vanNum, lightweightVehNum, busNum, trailerNum, bicycleNum, twoWheelerNum, motorcycleNum = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
r1, r2, r3, r4 = 0, 0, 0, 0
routes = {"route_01": 0, "route_02": 0, "route_03": 0, "route_04": 0}

for i in range(steps):
    carProb = getGaussianDistribution(0.4, 0.1, 1)
    heavyGoodsVehicleProb = getGaussianDistribution(0.23, 0.1, 1)
    lightweightCommercialVehicleProb = getGaussianDistribution(0.36, 0.1, 1)
    twoWheelerProb = getGaussianDistribution(0.1, 0.1, 1)

    uni_dist = getUniformDistribution(0, 1)
    uniform_distribution_list.append(uni_dist)

    route = getRouteId("route_01", "route_02", "route_03", "route_04")
  
    if route == "route_01":
        r1 += 1
    if route == "route_02":
        r2 += 1
    if route == "route_03":
        r3 += 1
    if route == "route_04":
        r4 += 1

    if(carProb >= uni_dist):
        routes[route] += 1
        carNum += 1

    if(lightweightCommercialVehicleProb >= uni_dist):
        lightweightVehNum += 1
        temp_uni_dist = getUniformDistribution(0, 1)
        if temp_uni_dist < 0.5:
            routes[route] += 1
            miniTruckNum += 1
        else:
            routes[route] += 1
            vanNum += 1

    if(heavyGoodsVehicleProb >= uni_dist):
        heavyGoodsVehNum += 1
        temp_uni_dist = getUniformDistribution(0, 1)
        if temp_uni_dist <= 0.7:
            routes[route] += 1
            busNum += 1
        else:
            routes[route] += 1
            trailerNum +=1 

    if(twoWheelerProb >= uni_dist):
        twoWheelerNum += 1
        temp_uni_dist = getUniformDistribution(0, 1)
        if temp_uni_dist < 0.5:
            routes[route] += 1
            bicycleNum += 1
        else:
            routes[route] += 1
            motorcycleNum += 1

print(f'\nThere are {carNum/10}% cars, {heavyGoodsVehNum/10}% heavy good vehicles, {lightweightVehNum/10}% lightweight vehicles, and {twoWheelerNum/10}% two-wheelers \n')
print(f'Out of the lightweight commercial vehicles, there are {miniTruckNum/10}% of mini-trucks and {vanNum/10}% of vans. \n')
print(f'Out of the heavy good vehicles, there are {busNum/10}% of buses and {trailerNum/10}% of trailers. \n')
print(f'Out of the two-wheeler vehicles, there are {bicycleNum/10}% of bicycles and {motorcycleNum/10}% of motorcycles. \n')

print(f'Route 1 was selected {r1/10}% of the times, Route 2 was selected {r2/10}% of the times, Route 3 was selected {r3/10}% of the times, and Route 4 was selected {r4/10}% of times. \n')

print(routes, '\n')

# sns.displot(data=uniform_distribution_list, kind='hist')
# plt.title("Uniform Distribution Samples Histogram")
# plt.show()