from numpy import random

def generate_routefile():
    random.seed(42)
    steps = 1000
    
    with open("data\hambrookJunction.rou.xml", "w") as routes:
        print("""<routes>
    <vType id="car" vClass="passenger" color="230,230,250"/>
    <vType id="bus" vClass="bus" color="255, 165, 0"/>
    <vType id="trailer" vClass="trailer" color="255,192,203"/>
    <vType id="motorcycle" vClass="motorcycle" color="red"/>
    <vType id="bicycle" vClass="bicycle" color="yellow"/>
    <vType id="mini-truck" vClass="delivery" color="blue"/>
    <vType id="van" vClass="hov" color="green"/>

    <route id="route_01" edges="BWtoW WtoJ JtoE EtoBE BEtoNE NEtoBN"/>
    <route id="route_02" edges="BEtoE EtoJ JtoW WtoBW BWtoNW NWtoBN"/>
    <route id="route_03" edges="BNtoN NtoJ JtoS StoBS BStoSW SWtoBW"/>
    <route id="route_04" edges="BStoS StoJ JtoN NtoBN BNtoNE NEtoBE"/>
    <route id="route_05" edges="BWtoW WtoJ JtoN NtoBN"/>
    <route id="route_06" edges="BWtoW WtoJ JtoS StoBS"/>
    <route id="route_07" edges="BEtoE EtoJ JtoN NtoBN"/>
    <route id="route_08" edges="BEtoE EtoJ JtoS StoBS"/>
    <route id="route_09" edges="BNtoN NtoJ JtoW WtoBW"/>
    <route id="route_10" edges="BNtoN NtoJ JtoE EtoBE"/>
    <route id="route_11" edges="BStoS StoJ JtoW WtoBW"/>
    <route id="route_12" edges="BStoS StoJ JtoE EtoBE"/>
    """, file=routes)

        carNum, busNum, truckNum, motorcycleNum, bicycleNum = 0, 0, 0, 0, 0
        r1, r2, r3, r4 = 0, 0, 0, 0
        departTime = 0
        departTimeToggle = True
        intervalTime = 10

        for i in range(steps):
            departTimeToggle = True
            carProb = getGaussianDistribution(0.4, 0.1, 1)
            heavyGoodsVehicleProb = getGaussianDistribution(0.23, 0.1, 1)
            lightweightCommercialVehicleProb = getGaussianDistribution(0.36, 0.1, 1)
            twoWheelerProb = getGaussianDistribution(0.1, 0.1, 1)

            uni_dist = getUniformDistribution(0, 1)
            route = getRouteId("route_01", "route_02", "route_03", "route_04", "route_05", "route_06", "route_07", "route_08", "route_09", "route_10", "route_11", "route_12")

            if(carProb >= uni_dist):
                carNum += 1
                if departTimeToggle == True:
                    departTime += intervalTime
                print(f'    <vehicle id="car_{carNum}" type="car" route="{route}" depart="{departTime}" />', file=routes)
                departTimeToggle = False

            if(lightweightCommercialVehicleProb >= uni_dist):
                temp_uni_dist = getUniformDistribution(0, 1)
                if temp_uni_dist < 0.5:
                    truckNum += 1
                    if departTimeToggle == True:
                        departTime += intervalTime
                    print(f'    <vehicle id="truck_{truckNum}" type="mini-truck" route="{route}" depart="{departTime}" />', file=routes)
                    departTimeToggle = False
                else:
                    carNum += 1
                    if departTimeToggle == True:
                        departTime += intervalTime
                    print(f'    <vehicle id="car_{carNum}" type="van" route="{route}" depart="{departTime}" />', file=routes)
                    departTimeToggle = False

            if(heavyGoodsVehicleProb >= uni_dist):
                temp_uni_dist = getUniformDistribution(0, 1)
                if temp_uni_dist <= 0.7:
                    busNum += 1
                    if departTimeToggle == True:
                        departTime += intervalTime
                    print(f'    <vehicle id="bus_{busNum}" type="bus" route="{route}" depart="{departTime}" />', file=routes)
                    departTimeToggle = False
                else:
                    truckNum +=1 
                    if departTimeToggle == True:
                        departTime += intervalTime
                    print(f'    <vehicle id="truck_{truckNum}" type="trailer" route="{route}" depart="{departTime}" />', file=routes)
                    departTimeToggle = False

            if(twoWheelerProb >= uni_dist):
                temp_uni_dist = getUniformDistribution(0, 1)
                if temp_uni_dist < 0.5:
                    bicycleNum += 1
                    if departTimeToggle == True:
                        departTime += intervalTime
                    print(f'    <vehicle id="bicycle_{bicycleNum}" type="bicycle" route="{route}" depart="{departTime}" />', file=routes)
                    departTimeToggle = False
                else:
                    motorcycleNum += 1
                    if departTimeToggle == True:
                        departTime += intervalTime
                    print(f'    <vehicle id="motorcycle_{motorcycleNum}" type="motorcycle" route="{route}" depart="{departTime}" />', file=routes)
                    departTimeToggle = False

        print("</routes>", file=routes)

def getRouteId(route1, route2, route3, route4, route5, route6, route7, route8, route9, route10, route11, route12):
    num = getUniformDistribution(0, 1)
    if num < 0.0833:
        return route1
    if num < 0.1666:
        return route2
    if num < 0.2499:
        return route3
    if num < 0.3332:
        return route4
    if num <  0.4165:
        return route5
    if num < 0.4998:
        return route6
    if num < 0.5831:
        return route7
    if num < 0.6664:
        return route8
    if num < 0.7497:
        return route9
    if num < 0.8330:
        return route10
    if num < 0.9163:
        return route11
    return route12
    
def getGaussianDistribution(mean, std, size):
    return random.normal(loc=mean, scale=std, size=size)

def getUniformDistribution(minVal, maxVal):
    return random.uniform(minVal, maxVal)

generate_routefile()