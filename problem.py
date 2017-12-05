import xml

from pso.controller import Controller
from sumo.lights import Light
from sumo.sumo import Simulation


class Prooblem:
    def __init__(self):
        self.lights = []
        self.load_data()

    def load_data(self):
        et = xml.etree.ElementTree.parse(Simulation.LogicLocation)
        root = et.getroot()
        for child in root.getchildren():
            tl_id = child.get('id')
            phases = []
            for phase in child.getchildren():
                phases.append(int(phase.get('duration')))
            self.lights.append(Light(tl_id, phases))

    def run_alg(self):
        ctrls = []
        sim = Simulation()
        for light in self.lights:
            ctrls.append(Controller(light,sim))

        sim.run_gui()
        for ctrl in ctrls:
            tl_id, particle = ctrl.run_alg()
            particle.modify_xml()
            print tl_id,particle.position,particle.fitness
        sim.run_gui()
Prooblem().run_alg()
