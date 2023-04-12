from generate_routes import generate_routefile
import traci 
import os
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
from classes_and_methods import printEdgeInfo, getEdgeInfo, getWeightInfo, printWeightInfo, exponential

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

sumoCmd = ["sumo-gui", "-c", "data\myJunction.sumocfg"]
traci.start(sumoCmd)

edges = ['WtoJ', 'EtoJ', 'NtoJ', 'StoJ']
weightDifferenceThresholdList = []
allVehicleNumList = []
header = ['Number of Vehicles Stopped', 'Total Waiting Time of All Vehicles', 'Total CO2 Emissions Released']
stepCounter = 0
signalChangeCounter = 0

with open('after.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    while traci.simulation.getMinExpectedNumber() > 0:

        traci.simulationStep()
        stepCounter += 1
        signalChangeCounter += 1
        print(f'\nIteration = {stepCounter}')

        allVehicleNum = sum(list(map(traci.edge.getLastStepVehicleNumber, edges)))
        print(f'Total Number of Vehicles = {allVehicleNum}')
        weightDifferenceThreshold = exponential(allVehicleNum, horizontal_stretch=1/6)
        signalChangeWeight = exponential(signalChangeCounter, vertical_stretch=100, horizontal_stretch=-1/1.3)

        horizontal_numOfVehs = traci.edge.getLastStepVehicleNumber('WtoJ') + traci.edge.getLastStepVehicleNumber('EtoJ')
        vertical_numOfVehs = traci.edge.getLastStepVehicleNumber('NtoJ') + traci.edge.getLastStepVehicleNumber('StoJ')
        differece = abs(horizontal_numOfVehs - vertical_numOfVehs)
        differenceWeight = 1/1.85 * np.exp(-1/8 * (differece - 5))
        weightDifferenceThreshold = (differenceWeight * weightDifferenceThreshold) + signalChangeWeight

        if weightDifferenceThreshold < 5:
            weightDifferenceThreshold = 5

        allVehicleNumList.append(allVehicleNum)
        weightDifferenceThresholdList.append(weightDifferenceThreshold)

        edge_WtoJ = getEdgeInfo("WtoJ")
        printEdgeInfo(edge_WtoJ, "Information about Road in direction West to East:")

        edge_EtoJ = getEdgeInfo("EtoJ")
        printEdgeInfo(edge_EtoJ, "Information about Road in direction East to West:")

        edge_NtoJ = getEdgeInfo("NtoJ")
        printEdgeInfo(edge_NtoJ, "Information about Road in direction North to South:")

        edge_StoJ = getEdgeInfo("StoJ")
        printEdgeInfo(edge_StoJ, "Information about Road in direction South to North:")

        weights_horizontal_flow = getWeightInfo(edge_WtoJ, edge_EtoJ)
        printWeightInfo(weights_horizontal_flow, "Information about weights about Road in direction West to East")

        weights_vertical_flow = getWeightInfo(edge_NtoJ, edge_StoJ)
        printWeightInfo(weights_vertical_flow, "Information about weights about Road in direction North to South")

        print(f'\nWeight Difference = {abs(weights_horizontal_flow.totalWeight - weights_vertical_flow.totalWeight)} and threshold is {weightDifferenceThreshold}')

        if abs(weights_horizontal_flow.totalWeight - weights_vertical_flow.totalWeight) > weightDifferenceThreshold:

            if weights_horizontal_flow.totalWeight > weights_vertical_flow.totalWeight:
                if traci.trafficlight.getPhase("Junction") == 0 or traci.trafficlight.getPhase("Junction") == 3:
                    traci.trafficlight.setPhase("Junction", 1)
                    signalChangeCounter = 0

            elif weights_vertical_flow.totalWeight > weights_horizontal_flow.totalWeight:
                if traci.trafficlight.getPhase("Junction") == 2 or traci.trafficlight.getPhase("Junction") == 1:
                    traci.trafficlight.setPhase("Junction", 3)
                    signalChangeCounter = 0

        writer.writerow([edge_WtoJ.vehiclesStopped + edge_EtoJ.vehiclesStopped + edge_NtoJ.vehiclesStopped + edge_StoJ.vehiclesStopped, 
                            edge_WtoJ.waitingTime + edge_EtoJ.waitingTime + edge_NtoJ.waitingTime + edge_StoJ.waitingTime, 
                            edge_WtoJ.CO2Emission + edge_EtoJ.CO2Emission + edge_NtoJ.CO2Emission + edge_StoJ.CO2Emission])

    fig = plt.figure()
    fig.add_subplot(1, 2, 1)
    arr = np.arange(0, len(weightDifferenceThresholdList))
    plt.title('Weight Difference Threshold v Time')
    plt.plot(arr, weightDifferenceThresholdList)

    fig.add_subplot(1, 2, 2)
    arr2 = np.arange(0, len(allVehicleNumList))
    plt.plot(arr2, allVehicleNumList)
    plt.title('Number of Vehicles in Simulation v Time')
    plt.show()

traci.close()