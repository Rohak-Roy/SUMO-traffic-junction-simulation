import traci
import time
import traci.constants as tc
import pytz
import datetime
from random import randrange
import os
import sys
from sumolib import checkBinary
import optparse

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

def getDateTime():
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    currentDT = utc_now.astimezone(pytz.timezone("GB"))
    DATIME = currentDT.strftime("%Y-%m-%d %H:%M:%S")
    return DATIME

sumoCmd = ["sumo-gui", "-c", "data\experimenting.sumocfg"]
traci.start(sumoCmd)

setTime = 5
counter = 0
while traci.simulation.getMinExpectedNumber() > 0:

    traci.simulationStep()
    counter += 1
    print("\nIteration = ", counter)

    allVehicles = traci.edge.getLastStepVehicleIDs("WtoJ")
    print("VEHICLES ON 'WtoJ' EDGE = ", allVehicles)

    if len(allVehicles) != 0:
        nextTLS = list(map(traci.vehicle.getNextTLS, allVehicles))

        distancesFromTLS = [item[0][2] for item in nextTLS]
        print(f'Distances from TLS are = {distancesFromTLS}')

        vehicleSpeeds = list(map(traci.vehicle.getSpeed, allVehicles))
        print(f'Vehicle speeds are = {vehicleSpeeds}')

        filteredVehicleSpeeds = [item for item in vehicleSpeeds if item > 3]
        print(f'Filtered speed of vehicles are = {filteredVehicleSpeeds}')

        distanceCoveredInGivenTime = [item * 10 for item in filteredVehicleSpeeds]
        print(f'Distance vehicles will cover in 10 secs = {distanceCoveredInGivenTime}')

        predictedDistanceFromTLS = [(x - y) for x,y in zip(distancesFromTLS, distanceCoveredInGivenTime)]
        print(f'Predicted distances of vehicles from TLS after 10 secs = {predictedDistanceFromTLS}')

        numOfPredictedVehiclesAtTLS = len([item for item in predictedDistanceFromTLS if item < 1.1])
        print(f'Number of vehicles predicted to be at the traffic light after 10 secs = {numOfPredictedVehiclesAtTLS}')

    else:
        print(0)
       
traci.close()

#DISTANCE FROM TRAFFIC LIGHT SIGNAL ON SUMO EVEN AFTER CAR HAS REACHED THE TLS = 1.0011215737891064