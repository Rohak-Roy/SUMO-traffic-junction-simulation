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

sumoCmd = ["sumo", "-c", "data\myJunction.sumocfg"]
traci.start(sumoCmd)

counter = 0
while traci.simulation.getMinExpectedNumber() > 0:

    traci.simulationStep()
    counter += 1

    vehicles = traci.vehicle.getIDList()

    print("Iteration", counter, " = ", vehicles)

traci.close()