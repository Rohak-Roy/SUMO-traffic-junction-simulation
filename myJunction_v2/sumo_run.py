from generate_routes import generate_routefile
import traci 
import os
import sys
from classes_and_methods import LaneInfo, getVehicleInfo, printLaneInfo, getLaneInfo

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

sumoCmd = ["sumo", "-c", "data\myJunction.sumocfg"]
traci.start(sumoCmd)

stepCounter = 0

while traci.simulation.getMinExpectedNumber() > 0:

    traci.simulationStep()
    stepCounter += 1
    print(f'\nIteration = {stepCounter}')

    laneWtoJ = getLaneInfo("WtoJ")
    printLaneInfo(laneWtoJ, "Information about lane West to East:")

    laneEtoJ = getLaneInfo("EtoJ")
    printLaneInfo(laneEtoJ, "Information about lane East to West:")

    laneNtoJ = getLaneInfo("NtoJ")
    printLaneInfo(laneNtoJ, "Information about lane North to South:")

    laneStoJ = getLaneInfo("StoJ")
    printLaneInfo(laneStoJ, "Information about lane South to North:")

traci.close()