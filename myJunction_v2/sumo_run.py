from generate_routes import generate_routefile
import traci 
import os
import sys
from classes_and_methods import printEdgeInfo, getEdgeInfo, getWeightInfo, printWeightInfo

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

sumoCmd = ["sumo-gui", "-c", "data\myJunction.sumocfg"]
traci.start(sumoCmd)

edgeIDs = ["WtoJ", "EtoJ", "NtoJ", "StoJ"]
weightDifferenceThreshold = 15

stepCounter = 0
while traci.simulation.getMinExpectedNumber() > 0:

    traci.simulationStep()
    stepCounter += 1
    print(f'\nIteration = {stepCounter}')

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

    print(f'\nWeight Difference = {abs(weights_horizontal_flow.totalWeight - weights_vertical_flow.totalWeight)}')

    if abs(weights_horizontal_flow.totalWeight - weights_vertical_flow.totalWeight) > weightDifferenceThreshold:

        if weights_horizontal_flow.totalWeight > weights_vertical_flow.totalWeight:
            if traci.trafficlight.getPhase("Junction") == 0 or traci.trafficlight.getPhase("Junction") == 3:
                traci.trafficlight.setPhase("Junction", 1)

        elif weights_vertical_flow.totalWeight > weights_horizontal_flow.totalWeight:
            if traci.trafficlight.getPhase("Junction") == 2 or traci.trafficlight.getPhase("Junction") == 1:
                traci.trafficlight.setPhase("Junction", 3)
    
traci.close()