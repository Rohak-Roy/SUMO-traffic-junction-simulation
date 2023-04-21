from generate_routes import generate_routefile
import traci 
import os
import sys
import csv
import numpy as np
import tensorflow as tf
import keras
from classes_and_methods import printEdgeInfo, getEdgeInfo, getWeightInfo, printWeightInfo, getData

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

sumoCmd = ["sumo", "-c", "data\myJunction.sumocfg"]
traci.start(sumoCmd)

weightDifferenceThreshold = 15
header = ['Number of Vehicles Stopped', 'Total Waiting Time of All Vehicles', 'Total CO2 Emissions Released']
header_2 = ['Number Of Vehicles Stopped - Horizontal', 'Total Waiting Time - Horizontal', 'Carbon Emissions Released - Horizontal', 'Number of Vehicles Predicted at Traffic Light - Horizontal', 'Number of Cars - Horizontal', 'Number of Buses - Horizontal', 'Number of Trucks - Horizontal', 'Number of Motorcycles - Horizontal', 'Number of Bicycles - Horizontal',
            'Number Of Vehicles Stopped - Vertical', 'Total Waiting Time - Vertical', 'Carbon Emissions Released - Vertical', 'Number of Vehicles Predicted at Traffic Light - Vertical', 'Number of Cars - Vertical', 'Number of Buses - Vertical', 'Number of Trucks - Vertical', 'Number of Motorcycles - Vertical', 'Number of Bicycles - Vertical', 'Time Since Signal Change', 'Traffic Phase']
stepCounter = 0
timeSinceTLSChange = 0
trafficPhase = 0

with open('after_ML.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    # data_writer = csv.writer(f2)
    # data_writer.writerow(header_2)
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
        #             timeSinceTLSChange = 0

        #     elif weights_vertical_flow.totalWeight > weights_horizontal_flow.totalWeight:
        #         if traci.trafficlight.getPhase("Junction") == 2 or traci.trafficlight.getPhase("Junction") == 1:
        #             traci.trafficlight.setPhase("Junction", 3)
        #             timeSinceTLSChange = 0

        # currentTrafficPhase = traci.trafficlight.getPhase("Junction")
        # if currentTrafficPhase == 0 or currentTrafficPhase == 3:
        #     trafficPhase = 0
        # if currentTrafficPhase == 1 or currentTrafficPhase == 2:
        #     trafficPhase = 1

        data = getData(edge_WtoJ, edge_EtoJ, edge_NtoJ, edge_StoJ)
        # data.append(timeSinceTLSChange)
        # data.append(trafficPhase)
        # writer.writerow(data)

        data = np.array([data])
        
        model = keras.models.load_model('my_best_model.hdf5')
        prediction = tf.round(model.predict(data))

        # print(f"Prediction is = {'West to East' if prediction == 1 else 'North to South'}, time since TLS change is {timeSinceTLSChange}")

        if prediction == 1:
            if traci.trafficlight.getPhase("Junction") == 0 or traci.trafficlight.getPhase("Junction") == 3:
                if timeSinceTLSChange > 15:
                    traci.trafficlight.setPhase("Junction", 1)
                    timeSinceTLSChange = 0

        elif prediction == 0:
            if traci.trafficlight.getPhase("Junction") == 1 or traci.trafficlight.getPhase("Junction") == 2:
                if timeSinceTLSChange > 15:
                    traci.trafficlight.setPhase("Junction", 3)
                    timeSinceTLSChange = 0
            
        writer.writerow([edge_WtoJ.vehiclesStopped + edge_EtoJ.vehiclesStopped + edge_NtoJ.vehiclesStopped + edge_StoJ.vehiclesStopped, 
                        edge_WtoJ.waitingTime + edge_EtoJ.waitingTime + edge_NtoJ.waitingTime + edge_StoJ.waitingTime, 
                        edge_WtoJ.CO2Emission + edge_EtoJ.CO2Emission + edge_NtoJ.CO2Emission + edge_StoJ.CO2Emission])

traci.close()