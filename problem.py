import math
import xml

from pso.controller import Controller
from random.random_search_controller import RandomSearchController
from sumo.lights import Light
from sumo.sumo import Simulation


class Prooblem:
    def __init__(self, path, logic):
        self.lights = []
        self.sim = Simulation(path, logic)
        self.load_data()

    def load_data(self):
        et = xml.etree.ElementTree.parse(self.sim.LogicLocation)
        root = et.getroot()
        for child in root.getchildren():
            if child.tag == "tlLogic":
                tl_id = child.get('id')
                phases = []
                for phase in child.getchildren():
                    val = phase.get('duration')
                    phases.append(int(math.floor(float(val))))
                self.lights.append(Light(tl_id, phases))

    def run_pso_alg(self):
        # path = "C:/Users/ntvid/Sumo/cluj-centru-500/"

        ctrl = Controller(self.lights, self.sim)

        self.sim.run_gui()
        particle = ctrl.run_alg()
        particle.modify_sumo_configuration(self.sim)
        print particle.info, particle.position, particle.fitness
        self.sim.run_gui()

    def run_with_single_start(self):
        # Calculate phases
        self.sim.start_simulation()
        ctrl = Controller(self.lights, self.sim)
        particle = ctrl.run_alg()
        print particle.info
        self.sim.close_simulation()

        # See result
        self.sim.run_gui()
        self.sim.get_arrived_and_departed()
        self.sim.close_simulation()

    def run_gui_only(self):
        self.sim.run_gui()

    def run_solution(self):
        self.sim.run_solution()

    def run_random_search_alg(self):
        ctrl = RandomSearchController(self.lights, self.sim)

        self.sim.run_gui()
        particle = ctrl.run_alg()
        particle.modify_sumo_configuration(self.sim)
        print particle.info, particle.position, particle.fitness
        self.sim.run_gui()

# Prooblem().run_gui_only()
Prooblem("C:/Users/ntvid/Sumo/cluj-centru-500/", "osm.net.xml").run_random_search_alg()
