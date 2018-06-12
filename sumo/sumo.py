import os
import sys

import re
import sumolib
import subprocess

import copy
from cStringIO import StringIO

import traci

DLR_SUMO_BIN_SUMO_GUI = "C:/Program Files (x86)/DLR/Sumo/bin/sumo-gui"

DLR_SUMO_BIN_SUMO = "C:/Program Files (x86)/DLR/Sumo/bin/sumo"

NET_STATS = "C:/Program Files (x86)/DLR/Sumo/tools/assign/networkStatistics.py"


def toMillis(seconds):
    return seconds * 1000


def toSeconds(millis):
    return millis / 1000


class Simulation:
    sumoBinary = DLR_SUMO_BIN_SUMO
    sumoBinaryGui = DLR_SUMO_BIN_SUMO_GUI

    def __init__(self, path, logic):
        self.stated = False
        self.path = path
        self.LogicLocation = self.path + logic
        self.time = 500

        self.map = path + "/osm.net.xml"
        self.route = path + "/osm.passenger.rou.xml"
        self.trips = path + "/osm.passenger.trips.net.xml"

        self.statistics = path + "/osm.stats.xml"

        self.sumo_cmd = [Simulation.sumoBinary, "-c", self.path + "osm.sumocfg",
                         "-n", self.map,
                         "-r", self.route,
                         "--tripinfo-output", self.trips]

        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit("please declare environment variable 'SUMO_HOME'")

    def run_gui(self):
        self.start_gui_simulation()
        fitness, arrived, waiting, per_step = self.get_simulation_data()

        return arrived, arrived, waiting, per_step

    def run_simulation(self):
        return self.get_fitness()

    def get_fitness(self):

        arrived, waiting, total_journey_time, total_waiting_time, self.time, green_red_ratio_sum, arrived_per_step = self.get_simulation_data()
        return (total_journey_time + total_waiting_time + waiting * self.time) / (
                arrived * arrived + green_red_ratio_sum), arrived, waiting, arrived_per_step

    def get_simulation_data(self):

        step = 0
        arrived = 0
        waiting = 0

        green_red_ratio_sum = 0
        lanes_waiting_times = {}
        vehicles_start_times = {}
        vehicles_end_times = {}
        arrived_per_step = []

        traci.start(self.sumo_cmd)

        lane_ids = traci.lane.getIDList()
        for lane_id in lane_ids:
            lanes_waiting_times[lane_id] = 0

        for light_id in traci.trafficlight.getIDList():
            a = traci.trafficlight.getCompleteRedYellowGreenDefinition(light_id)
            phases = a[-1]._phases

        while step < self.time:
            departed_ids = traci.simulation.getDepartedIDList()
            arrived_ids = traci.simulation.getArrivedIDList()

            for vehicle_id in departed_ids:
                vehicles_start_times[vehicle_id] = copy.deepcopy(step)
                vehicles_end_times[vehicle_id] = copy.deepcopy(step)

            for vehicle_id in arrived_ids:
                vehicles_end_times[vehicle_id] = copy.deepcopy(step)

            arrived += len(arrived_ids)
            arrived_per_step.append(arrived)
            traci.simulationStep()
            step += 1

        traci.close()

        total_waiting_time, total_journey_time = self.generate_statistics()

        for vehicle_id in vehicles_start_times:
            if vehicles_end_times[vehicle_id] - vehicles_start_times[vehicle_id] == 0:
                waiting += 1

            for phase in phases:
                reds = 0
                greens = 0
                duration = phase._duration / 1000.0
                state = phase._phaseDef
                reds += state.count('r')
                reds += state.count('R')
                greens += state.count('g')
                greens += state.count('G')
                reds = max(reds, 1)
                green_red_ratio_sum += duration * greens / reds

        return arrived, waiting, total_journey_time, total_waiting_time, self.time, green_red_ratio_sum, arrived_per_step

    def run_simul_until_no_more_cars(self):
        step = 0
        arrived = 0
        departed = 0
        while step < self.time:
            traci.simulationStep()
            step += 1
            arrived += traci.simulation.getArrivedNumber()
            departed += traci.simulation.getDepartedNumber()

    def start_gui_simulation(self):
        sumo_cmd = [Simulation.sumoBinaryGui, "-c", self.path + "osm.sumocfg"]
        traci.start(sumo_cmd)
        self.stated = True

    def get_traffic_lights(self):
        return traci.trafficlight.getIDList()

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
        arrived, departed = self.get_simulation_data()
        print arrived, departed

    def generate_statistics(self):
        subprocess.call(['python', NET_STATS, '-t', self.trips, '-o', self.statistics])

        file = open(self.statistics, "r")
        waiting_time = 0
        travel_time = 0
        for line in file:
            try:
                line.index("total waiting time")
                values = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                waiting_time = float(values[0])
            except ValueError:
                pass
            try:
                line.index("total travel time")
                values = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                travel_time = float(values[0])
            except ValueError:
                pass

        return waiting_time, travel_time
