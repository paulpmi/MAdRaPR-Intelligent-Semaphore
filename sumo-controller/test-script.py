import os
import sys
import traci


sumoBinary = "C:/Program Files (x86)/DLR/Sumo/bin/sumo-gui"

sumoCmd = [sumoBinary, "-c", "C:/Users/ntvid/Sumo/test/hello.sumocfg"]
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

traci.start(sumoCmd)
step = 0
while step < 1000:
    traci.simulationStep()
    if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
        continue
        #traci.trafficlight.setRedYellowGreenState("0", "GrGr")
    step += 1

traci.close()


