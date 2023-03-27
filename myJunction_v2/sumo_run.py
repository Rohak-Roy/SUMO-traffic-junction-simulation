from generate_routes import generate_routefile
import traci 
import os
import sys
from classes_and_methods import LaneInfo, getVehicleInfo, printLaneInfo

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

sumoCmd = ["sumo", "-c", "data\myJunction.sumocfg"]
traci.start(sumoCmd)

stepCounter = 0
laneWtoJ = LaneInfo()

while traci.simulation.getMinExpectedNumber() > 0:

    traci.simulationStep()
    stepCounter += 1
    print('\nIteration = ', stepCounter)

    allVehicles = traci.edge.getLastStepVehicleIDs("WtoJ")
    laneWtoJ.vehiclesStopped = traci.edge.getLastStepHaltingNumber("WtoJ")
    laneWtoJ.totalNumOfVeh = traci.edge.getLastStepVehicleNumber("WtoJ")

    carInfo = getVehicleInfo(allVehicles, 'car')
    laneWtoJ.carInfo.update(carInfo)

    busInfo = getVehicleInfo(allVehicles, 'bus')
    laneWtoJ.busInfo.update(busInfo)

    truckInfo = getVehicleInfo(allVehicles, 'truck')
    laneWtoJ.truckInfo.update(truckInfo)

    motorcycleInfo = getVehicleInfo(allVehicles, 'motorcycle')
    laneWtoJ.motorcycleInfo.update(motorcycleInfo)

    bicycleInfo = getVehicleInfo(allVehicles, 'bicycle')
    laneWtoJ.bicycleInfo.update(bicycleInfo)

    printLaneInfo(laneWtoJ)

traci.close()