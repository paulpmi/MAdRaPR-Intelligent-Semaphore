import copy
import random
import xml
from math import exp
import random

from sumo.sumo import Simulation


class Particle:
    def __init__(self, intersection):
        self.position = []  # list of integers representing the time duration for each state
        self.velocity = []
        self.intersection = intersection
        self.fitness = 0
        self.best_position = []
        self.best_fitness = 0
        self.initialize(intersection)

    def initialize(self, intersection):
        for i in range(0, len(intersection.phases)):
            self.position.append(random.randint(3, 90))
        self.intersection.phases = self.position[:]
        self.best_position = self.position[:]
        self.velocity = self.position[:]

    # the numbers of cars that had reached their destination in a simulation time of t squared minus the number of those
    #  who haven't
    def evaluate(self, simulation):
        self.modify_xml()
        fitness = simulation.run_simulation()
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
            s = 1 / (1 + exp(self.velocity[i]))
            if random.random() < s:
                # formula from some lab I made
                #    self.position[i], self.position[self.position.index(best_particle.position[i])] =\
                #        self.position[self.position.index(best_particle.position[i])], self.position[i]
                self.position[i] = self.position[i] + self.velocity[i]
                if self.position[i] < 3:
                    self.position[i] = 3
                if self.position[i] > 90:
                    self.position[i] = 90

    def modify_xml(self):
        et = xml.etree.ElementTree.parse(Simulation.LogicLocation)
        root = et.getroot()
        for child in root.getchildren():
            tl_id = child.get('id')
            k = 0
            if tl_id == self.intersection.id:
                for phase in child.getchildren():
                    phase.set('duration', str(self.position[k]))
                    k += 1
        et.write(Simulation.LogicLocation)
