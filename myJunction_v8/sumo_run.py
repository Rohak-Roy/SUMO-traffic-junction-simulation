from generate_routes import generate_routefile
import traci 
import os
import sys
import csv
import tensorflow as tf
import keras
import numpy as np
from classes_and_methods import printEdgeInfo, getEdgeInfo, getWeightInfo, printWeightInfo, getData

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

header = ['Number of Vehicles Stopped', 'Total Waiting Time of All Vehicles', 'Total CO2 Emissions Released']
sumoCmd = ["sumo-gui", "-c", "data\myJunction.sumocfg"]
traci.start(sumoCmd)

stepCounter = 0
timeSinceTLSChange = 0
weightDifferenceThreshold = 15

# with open('after_ML.csv', 'w') as f:
#     writer = csv.writer(f)
#     writer.writerow(header)

while traci.simulation.getMinExpectedNumber() > 0:

    traci.simulationStep()
    stepCounter += 1
    print(f'\nIteration = {stepCounter}')

    timeSinceTLSChange += 1

    edge_WtoJ = getEdgeInfo("WtoJ")
    printEdgeInfo(edge_WtoJ, "Information about Road in direction West to East:")

    edge_EtoJ = getEdgeInfo("EtoJ")
    printEdgeInfo(edge_EtoJ, "Information about Road in direction East to West:")

    edge_NtoJ = getEdgeInfo("NtoJ")
    printEdgeInfo(edge_NtoJ, "Information about Road in direction North to South:")

    edge_StoJ = getEdgeInfo("StoJ")
    printEdgeInfo(edge_StoJ, "Information about Road in direction South to North:")

    # weights_horizontal_flow = getWeightInfo(edge_WtoJ, edge_EtoJ)
    # printWeightInfo(weights_horizontal_flow, "Information about weights about Road in direction West to East")

    # weights_vertical_flow = getWeightInfo(edge_NtoJ, edge_StoJ)
    # printWeightInfo(weights_vertical_flow, "Information about weights about Road in direction North to South")

    # print(f'\nWeight Difference = {abs(weights_horizontal_flow.totalWeight - weights_vertical_flow.totalWeight)}')

    # if abs(weights_horizontal_flow.totalWeight - weights_vertical_flow.totalWeight) > weightDifferenceThreshold:

    #     if weights_horizontal_flow.totalWeight > weights_vertical_flow.totalWeight:
    #         if traci.trafficlight.getPhase("Junction") == 0 or traci.trafficlight.getPhase("Junction") == 3:
    #             traci.trafficlight.setPhase("Junction", 1)

    #     elif weights_vertical_flow.totalWeight > weights_horizontal_flow.totalWeight:
    #         if traci.trafficlight.getPhase("Junction") == 2 or traci.trafficlight.getPhase("Junction") == 1:
    #             traci.trafficlight.setPhase("Junction", 3)

    model_path = "my_best_model_v4.hdf5"
    model = keras.models.load_model(model_path)
    
    data = getData(edge_WtoJ, edge_EtoJ, edge_NtoJ, edge_StoJ)
    data.append(timeSinceTLSChange)
    data = np.array([data])

    prediction = tf.round(model.predict(data))
    print(f'MODEL LAYERS =  {model.layers}')

    currentPhase = traci.trafficlight.getPhase("Junction")
    if currentPhase == 0 or currentPhase == 3:
        if prediction == 1:
            traci.trafficlight.setPhase("Junction", 1)
            timeSinceTLSChange = 0
    elif currentPhase == 1 or currentPhase == 2:
        if prediction == 0:
            traci.trafficlight.setPhase("Junction", 0)
            timeSinceTLSChange = 0

    # writer.writerow([edge_WtoJ.vehiclesStopped + edge_EtoJ.vehiclesStopped + edge_NtoJ.vehiclesStopped + edge_StoJ.vehiclesStopped, 
    #                 edge_WtoJ.waitingTime + edge_EtoJ.waitingTime + edge_NtoJ.waitingTime + edge_StoJ.waitingTime, 
    #                 edge_WtoJ.CO2Emission + edge_EtoJ.CO2Emission + edge_NtoJ.CO2Emission + edge_StoJ.CO2Emission])

traci.close()