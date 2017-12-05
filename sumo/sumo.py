import os
import sys

import traci


class Simulation:
    sumoBinary = "C:/Program Files (x86)/DLR/Sumo/bin/sumo"
    sumoBinaryGui = "C:/Program Files (x86)/DLR/Sumo/bin/sumo-gui"
    LogicLocation = "C:/Users/ntvid/Sumo/test/rilsa1_tls.add.xml"

    def __init__(self):

        self.sumo_cmd = [Simulation.sumoBinary, "-c", "C:/Users/ntvid/Sumo/test/run.sumo.cfg"]
        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit("please declare environment variable 'SUMO_HOME'")

    def run_gui(self):
        sumo_cmd = [Simulation.sumoBinaryGui, "-c", "C:/Users/ntvid/Sumo/test/run.sumo.cfg"]
        traci.start(sumo_cmd)
        step = 0
        arrived = 0
        deaparted = 0
        while step < 1000:
            traci.simulationStep()
            step += 1
            arrived += traci.simulation.getArrivedNumber()
            deaparted += traci.simulation.getDepartedNumber()
        traci.close()
        print arrived, deaparted

    def run_simulation(self):
        traci.start(self.sumo_cmd)
        step = 0
        arrived = 0
        deaparted = 0
        while step < 1000:
            traci.simulationStep()
            step += 1
            arrived += traci.simulation.getArrivedNumber()
            deaparted += traci.simulation.getDepartedNumber()
        print arrived,deaparted
        traci.close()
        return pow(arrived,2) - (deaparted - arrived)


