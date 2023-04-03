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

    # weightNumOfVehStopped_horizontal = exponential(edge_WtoJ.vehiclesStopped + edge_EtoJ.vehiclesStopped)
    # weightNumOfVehStopped_vertical = exponential(edge_NtoJ.vehiclesStopped + edge_StoJ.vehiclesStopped)
    
    # weightWaitingTime_horizontal = exponential(edge_WtoJ.waitingTime + edge_EtoJ.waitingTime)
    # weightWaitingTime_vertical = exponential(edge_NtoJ.waitingTime + edge_StoJ.waitingTime)

    # weightCarbonEmissions_horizontal = logarithm(edge_WtoJ.CO2Emission + edge_EtoJ.CO2Emission)
    # weightCarbonEmissions_vertical = logarithm(edge_NtoJ.CO2Emission + edge_StoJ.CO2Emission)

    # weightNumOfTrucks_horizontal = exponential(edge_WtoJ.truckInfo["Number"] + edge_EtoJ.truckInfo["Number"])
    # weightNumOfTrucks_vertical = exponential(edge_NtoJ.truckInfo["Number"] + edge_StoJ.truckInfo["Number"])

    # print(f"\nweight due to number of vehicles stopped in the horizontal direction = {weightNumOfVehStopped_horizontal}")
    # print(f"weight due to number of vehicles stopped in the vertical direction = {weightNumOfVehStopped_vertical}")
    
    # print(f"\nweight due to waiting time of vehicles stopped in the horizontal direction = {weightWaitingTime_horizontal}")
    # print(f"weight due to waiting time of vehicles stopped in the vertical direction = {weightWaitingTime_vertical}")

    # print(f"\nweight due to carbon emissions  of vehicles  in the horizontal direction = {weightCarbonEmissions_horizontal}")
    # print(f"weight due to carbon emissions  of vehicles  in the vertical direction = {weightCarbonEmissions_vertical}")

    # print(f"\nweight due to number of trucks in the horizontal direction = {weightNumOfTrucks_horizontal}")
    # print(f"weight due to number of trucks in the vertical direction = {weightNumOfTrucks_vertical}")
    
traci.close()