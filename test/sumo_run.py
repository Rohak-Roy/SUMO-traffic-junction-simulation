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

    vehicles = traci.edge.getLastStepVehicleIDs("WtoJ")
    print("VEHICLES ON 'WtoJ' EDGE = ", vehicles)

    nextTLS = list(map(traci.vehicle.getNextTLS, vehicles))

    if len(vehicles) != 0:

        distanceFromTLS = [item[0][2] for item in nextTLS]
        print(f"Distances from traffic light = {distanceFromTLS}")

        vehicleSpeeds = list(map(traci.vehicle.getSpeed, vehicles))
        print(f"Speed of vehicles = {vehicleSpeeds}")

        distanceCovered = [item * setTime for item in vehicleSpeeds]
        print(f"Distance Covered after 5 seconds = {distanceCovered}")

        currentAndFutureDistances = list(zip(distanceFromTLS, distanceCovered))

        predictedDistanceFromTLS = [(x - y) for x,y in currentAndFutureDistances]
        print(f"Predicted Distance from traffic light after {setTime}s is = {predictedDistanceFromTLS}")

        numOfPredictedVehAtTLS = len([item for item in predictedDistanceFromTLS if item < 1.1])
        print(f"Number vehicles predicted to be at traffic light after {setTime}s is = {numOfPredictedVehAtTLS}")

    else:
        print(0)
       
traci.close()

#DISTANCE FROM TRAFFIC LIGHT SIGNAL ON SUMO EVEN AFTER CAR HAS REACHED THE TLS = 1.0011215737891064