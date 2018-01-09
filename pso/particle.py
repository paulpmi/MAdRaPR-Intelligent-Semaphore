import copy
import random
import xml
from math import exp


class Particle:
    def __init__(self, intersections):
        self.info = {}
        self.position = []  # list of integers representing the time duration for each state
        self.velocity = []
        self.intersections = intersections
        self.fitness = 0
        self.best_position = []
        self.best_fitness = 0
        self.initialize(intersections)

    def initialize(self, intersections):
        for light in intersections:
            for i in range(0, len(light.phases)):
                self.position.append(random.randint(5, 50))
        self.best_position = self.position[:]
        self.velocity = self.position[:]
        for k in range(0, len(self.position)):
            self.velocity[k] = 4.5

    # the numbers of cars that had reached their destination in a simulation time of t squared minus the number of those
    #  who haven't
    def evaluate(self, simulation):

        # self.modify_xml(simulation)
        # simulation.set_all_phases(self.position)
        simulation.start_simulation()
        fitness, departed, arrived = simulation.get_fitness()
        self.info['departed'] = departed
        self.info['arrived'] = arrived
        simulation.close_simulation()
        self.fitness = fitness
        if self.fitness > self.best_fitness:
            self.best_fitness = self.fitness
            self.best_position = copy.copy(self.position)

    def update(self, w, c1, c2, best_particle):
        # best global particle
        # update velocity
        # update position
        for i in range(len(self.position)):
            self.velocity[i] = w * self.velocity[i] + int(c1 * random.random() *
                                                          (self.best_position[i] - self.position[i])) + int(
                c2 * random.random() * (best_particle.position[i] - self.position[i]))
            if self.velocity[i] > 45:
                self.velocity[i] = 45

            try:
                s = 1 / (1 + exp(self.velocity[i]))
            except:
                s = 1 / 1.7976931348623157e+308
            if random.random() < s:

                self.position[i] = self.position[i] + self.velocity[i]
                if self.position[i] < 5:
                    self.position[i] = 5
                if self.position[i] > 50:
                    self.position[i] = 50

    def modify_xml(self, simulation):
        et = xml.etree.ElementTree.parse(simulation.LogicLocation)
        root = et.getroot()
        for child in root.getchildren():
            k = 0
            if child.tag == "tlLogic":
                for phase in child.getchildren():
                    phase.set('duration', str(self.position[k]))
                    k += 1
        et.write(simulation.LogicLocation)
