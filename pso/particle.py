import copy
import random

import sys

import random_search
import xml
from math import exp

from sumo_io.configuration_io import ConfigurationIO


class Particle:
    def __init__(self, intersections):
        self.info = {}
        self.position = []  # list of integers representing the time duration for each state
        self.velocity = []
        self.intersections = intersections
        self.fitness = sys.maxint
        self.best_position = []
        self.best_fitness = sys.maxint
        self.initialize(intersections)

    def initialize(self, intersections):
        self.position = []
        self.velocity = []
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
        ConfigurationIO.modify_sumo_configuration(simulation, self.position)
        fitness, departed, waiting, per_step = simulation.get_fitness()
        self.info['arrived'] = departed
        self.info['waiting'] = waiting
        self.info['step'] = per_step
        self.fitness = fitness
        if self.fitness < self.best_fitness:
            self.best_fitness = self.fitness
            self.best_position = copy.copy(self.position)

    def update(self, w, c1, c2, best_position):
        # best global particle
        # update velocity
        # update position
        for i in range(len(self.position)):
            self.velocity[i] = w * self.velocity[i] + int(c1 * random.random() *
                                                          (self.best_position[i] - self.position[i])) + int(
                c2 * random.random() * (best_position[i] - self.position[i]))
            if self.velocity[i] > 45:
                self.velocity[i] = 45

            self.position[i] = self.position[i] + self.velocity[i]
            if self.position[i] < 5:
                self.position[i] = 5
            if self.position[i] > 50:
                self.position[i] = 50
