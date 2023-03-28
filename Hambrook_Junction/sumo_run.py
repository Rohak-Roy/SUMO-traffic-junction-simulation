from generate_routes import generate_routefile
import traci 
import os
import sys
from classes_and_methods import EdgeInfo, getVehicleInfo, printEdgeInfo, getEdgeInfo, getLaneInfo, printSingleLaneInfo, getLaneIDsFromEdgeID, printAllLanesInfo

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

sumoCmd = ["sumo", "-c", "data\hambrookJunction.sumocfg"]
traci.start(sumoCmd)

edgeIDs = ["WtoJ", "EtoJ", "NtoJ", "StoJ"]

stepCounter = 0

while traci.simulation.getMinExpectedNumber() > 0:

    traci.simulationStep()
    stepCounter += 1
    print(f'\nIteration = {stepCounter}')

    edge_WtoJ = getEdgeInfo("WtoJ")
    printEdgeInfo(edge_WtoJ, "Information about Road in direction West to East:")
    laneIDs_WtoJ = getLaneIDsFromEdgeID("WtoJ")
    printAllLanesInfo(laneIDs_WtoJ, "West to East")

    edge_EtoJ = getEdgeInfo("EtoJ")
    printEdgeInfo(edge_EtoJ, "Information about Road in direction East to West:")
    laneIDs_EtoJ = getLaneIDsFromEdgeID("EtoJ")
    printAllLanesInfo(laneIDs_EtoJ, "East to West")

    edge_NtoJ = getEdgeInfo("NtoJ")
    printEdgeInfo(edge_NtoJ, "Information about Road in direction North to South:")
    laneIDs_NtoJ = getLaneIDsFromEdgeID("NtoJ")
    printAllLanesInfo(laneIDs_NtoJ, "North to South")

    edge_StoJ = getEdgeInfo("StoJ")
    printEdgeInfo(edge_StoJ, "Information about Road in direction South to North:")
    laneIDs_StoJ = getLaneIDsFromEdgeID("StoJ")
    printAllLanesInfo(laneIDs_StoJ, "South to North")

traci.close()