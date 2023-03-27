import traci

class LaneInfo:
    def __init__(self):
        self.vehiclesStopped = 0
        self.totalNumOfVeh = 0
        self.CO2Emission = 0
        self.carInfo = {"Number": 0, "Mean Speed": 0, "Mean Distance from Traffic Light": 0}
        self.busInfo = {"Number": 0, "Mean Speed": 0, "Mean Distance from Traffic Light": 0}
        self.truckInfo = {"Number": 0, "Mean Speed": 0, "Mean Distance from Traffic Light": 0}
        self.motorcycleInfo = {"Number": 0, "Mean Speed": 0, "Mean Distance from Traffic Light": 0}
        self.bicycleInfo = {"Number": 0, "Mean Speed": 0, "Mean Distance from Traffic Light": 0}

def getVehicleInfo(allVehicles, vehicleType):
    vehicles =  [item for item in allVehicles if vehicleType in item]
    vehicleSpeeds = list(map(traci.vehicle.getSpeed, vehicles))
    meanVehicleSpeed = sum(vehicleSpeeds) / len(vehicles) if len(vehicles) != 0 else 0
    nextTLS = list(map(traci.vehicle.getNextTLS, vehicles))                 # nextTLS is of type [((...), (...)), ((...), (...))]

    if len(nextTLS) != 0:
        distanceFromTLS = [item[0][2] for item in nextTLS]
    else:
        distanceFromTLS = []

    meanDistanceFromTLS = sum(distanceFromTLS) / len(distanceFromTLS) if len(distanceFromTLS) != 0 else 0

    return {"Number": len(vehicles), "Mean Speed": meanVehicleSpeed, "Mean Distance from Traffic Light": meanDistanceFromTLS}

def getLaneInfo(edgeID):
    allVehicles = traci.edge.getLastStepVehicleIDs(edgeID)
    laneInfo = LaneInfo()

    laneInfo.vehiclesStopped = traci.edge.getLastStepHaltingNumber(edgeID)
    laneInfo.totalNumOfVeh = traci.edge.getLastStepVehicleNumber(edgeID)
    laneInfo.CO2Emission = traci.edge.getCO2Emission(edgeID)

    carInfo = getVehicleInfo(allVehicles, 'car')
    laneInfo.carInfo.update(carInfo)

    busInfo = getVehicleInfo(allVehicles, 'bus')
    laneInfo.busInfo.update(busInfo)

    truckInfo = getVehicleInfo(allVehicles, 'truck')
    laneInfo.truckInfo.update(truckInfo)

    motorcycleInfo = getVehicleInfo(allVehicles, 'motorcycle')
    laneInfo.motorcycleInfo.update(motorcycleInfo)

    bicycleInfo = getVehicleInfo(allVehicles, 'bicycle')
    laneInfo.bicycleInfo.update(bicycleInfo)

    return laneInfo

def printLaneInfo(laneInfo, title=""):
    print(f'\n{title}')
    print(f'Number of vehicles currently stopped at traffic light= {laneInfo.vehiclesStopped}')
    print(f'Total number of vehicles = {laneInfo.totalNumOfVeh}')
    print(f'Car Info = {laneInfo.carInfo}')
    print(f'Bus Info = {laneInfo.busInfo}')
    print(f'Truck Info = {laneInfo.truckInfo}')
    print(f'Motorcycle Info = {laneInfo.motorcycleInfo}')
    print(f'Bicycle Info = {laneInfo.bicycleInfo}')
    print(f'Carbon Emissions released = {laneInfo.CO2Emission}')