import os
import sys

import traci


def toMillis(seconds):
    return seconds * 1000


def toSeconds(millis):
    return millis / 1000


class Simulation:
    sumoBinary = "C:/Program Files (x86)/DLR/Sumo/bin/sumo"
    sumoBinaryGui = "C:/Program Files (x86)/DLR/Sumo/bin/sumo-gui"

    def __init__(self, path,logic):
        self.stated = False
        self.path = path
        self.LogicLocation = self.path + logic
        self.time = 1000
        self.sumo_cmd = [Simulation.sumoBinary, "-c", self.path + "osm.sumocfg"]
        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit("please declare environment variable 'SUMO_HOME'")

    def run_gui(self):
        self.start_gui_simulation()
        arrived, departed = self.get_arrived_and_departed()
        self.close_simulation()

        print arrived, departed

    def run_simulation(self):
        self.start_simulation()
        f = self.get_fitness()

        self.close_simulation()
        return f

    def get_fitness(self):
        if not self.stated:
            return -1, 0, 0
        arrived, departed = self.get_arrived_and_departed()
        return (pow(arrived, 2) - (departed - arrived)), departed, arrived

    def close_simulation(self):
        traci.close()
        self.stated = False

    def get_arrived_and_departed(self):
        step = 0
        arrived = 0
        departed = 0
        while step < self.time:
            traci.simulationStep()
            step += 1
            arrived += traci.simulation.getArrivedNumber()
            departed += traci.simulation.getDepartedNumber()
        return arrived, departed

    def run_simul_until_no_more_cars(self):
        while step < self.time:
            traci.simulationStep()
            step += 1
            arrived += traci.simulation.getArrivedNumber()
            departed += traci.simulation.getDepartedNumber()

    def start_simulation(self):
        traci.start(self.sumo_cmd)
        self.stated = True

    def start_gui_simulation(self):
        sumo_cmd = [Simulation.sumoBinaryGui, "-c", self.path + "osm.sumocfg"]
        traci.start(sumo_cmd)
        self.stated = True

    def get_traffic_lights(self):
        return traci.trafficlights.getIDList()

    def set_all_phases(self, solution):
        programs = []
        ids = self.get_traffic_lights()
        k = 0
        for tid in ids:
            t_logic = traci.trafficlights.getCompleteRedYellowGreenDefinition(tid)
            for i in range(len(t_logic[0]._phases)):
                t_logic[0]._phases[i]._duration = toMillis(solution[i])
                t_logic[0]._phases[i]._duration1 = toMillis(5)
                t_logic[0]._phases[i]._duration2 = toMillis(50)
                k += 1
            traci.trafficlights.setCompleteRedYellowGreenDefinition(tid, t_logic[0])
            programs.append(t_logic)
            # for p in programs:
            #     print p

    def run_solution(self):
        self.start_simulation()
        arrived, departed = self.get_arrived_and_departed()
        print arrived, departed
        self.close_simulation()

