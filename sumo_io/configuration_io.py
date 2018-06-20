import xml

import math

import os

import subprocess

from sumo.lights import Light


# import imp
#
# osmWizardModule = imp.load_source('osmWebWizard.name', 'C:/Program Files (x86)/DLR/Sumo/tools/osmWebWizard.py')


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
        return ConfigurationIO.get_sim_data(sim.LogicLocation)

    @staticmethod
    def get_sim_data(path):
        lights = []
        et = xml.etree.ElementTree.parse(path)
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
    def add_simulation():
        path = os.environ["SUMO_HOME"]
        path += ConfigurationIO.add_simulation_file_location
        os.startfile(path)

    @staticmethod
    def get_latest_simulation(path, existing_data):
        dirs = ConfigurationIO.get_simulations(path)
        for simulation_name in dirs:
            if simulation_name not in existing_data:
                return simulation_name
        return ""

    @staticmethod
    def does_path_exist(path):
        return os.path.exists(path)

    @staticmethod
    def set_simulation_name(path,old_name,new_name):
        if os.path.exists(path+old_name):
            try:
                os.rename(os.path.join(path, old_name), os.path.join(path, new_name))
            except WindowsError:
                print(WindowsError)
    @staticmethod
    def get_computer_name():
        return os.environ['COMPUTERNAME']


