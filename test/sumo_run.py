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
import matplotlib.pyplot as plt

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

sumoCmd = ["sumo", "-c", "data\experimenting.sumocfg"]
traci.start(sumoCmd)

setTime = 5
counter = 0
counterList = []
CO2List = []
speedList = []

while traci.simulation.getMinExpectedNumber() > 0:

    traci.simulationStep()
    
    counter += 1
    print("\nIteration = ", counter)

    allVehicles = traci.edge.getLastStepVehicleIDs("WtoJ")
    print("VEHICLES ON 'WtoJ' EDGE = ", allVehicles)

    if len(allVehicles) == 0:
        break

    CO2 = traci.edge.getCO2Emission("WtoJ")
    print("Carbon Emissions = ", CO2)

    speed = traci.vehicle.getSpeed(allVehicles[0])
    print("Speed = ", speed)
    
    CO2List.append(CO2)
    counterList.append(counter)
    speedList.append(speed)

fig = plt.figure()

fig.add_subplot(1, 2, 1)
plt.plot(counterList, CO2List)
plt.title("CO2 vs Time")

fig.add_subplot(1, 2, 2)
plt.title("Speed vs Time")
plt.plot(counterList, speedList)

plt.show()

traci.close()

#DISTANCE FROM TRAFFIC LIGHT SIGNAL ON SUMO EVEN AFTER CAR HAS REACHED THE TLS = 1.0011215737891064