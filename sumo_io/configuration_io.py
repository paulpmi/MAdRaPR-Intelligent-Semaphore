import xml

import math

import os

from sumo.lights import Light


class ConfigurationIO:
    add_simulation_file_location = "tools\\osmWebWizard.py"
    def __init__(self):
        pass

    @staticmethod
    def modify_sumo_configuration(simulation, solution):
        et = xml.etree.ElementTree.parse(simulation.LogicLocation)
        root = et.getroot()
        for child in root.getchildren():
            k = 0
            if child.tag == "tlLogic":
                for phase in child.getchildren():
                    phase.set('duration', str(solution[k]))
                    k += 1
        et.write(simulation.LogicLocation)

    @staticmethod
    def load_simulation_data(sim):
        lights = []
        et = xml.etree.ElementTree.parse(sim.LogicLocation)
        root = et.getroot()
        for child in root.getchildren():
            if child.tag == "tlLogic":
                tl_id = child.get('id')
                phases = []
                for phase in child.getchildren():
                    val = phase.get('duration')
                    phases.append(int(math.floor(float(val))))
                lights.append(Light(tl_id, phases))
        return lights

    @staticmethod
    def get_simulations(path):
        dirs = []
        if os.path.exists(path):
            dirs = os.listdir(path)
        return dirs

    @staticmethod
    def verify_simulation_files(location, t_logic):
        return location and t_logic and os.path.exists(location + t_logic)

    @staticmethod
    def add_simulation(self):
        path = os.environ["SUMO_HOME"]
        if path:
            path += ConfigurationIO.add_simulation_file_location
            os.startfile(path)
