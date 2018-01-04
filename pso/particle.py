import copy
from math import exp
from random import random


class Particle:
    def __init__(self, intersection):
        self.position = []  # list of integers representing the time duration for each state
        self.velocity = []
        self.fitness = 0
        self.best_position = []
        self.best_fitness = 0
        self.initialize(intersection)

    def initialize(self, intersection):
        # ToDo initialize position based on intersection
        self.best_position = self.position[:]
        self.velocity = self.position[:]

    # the numbers of cars that had reached their destination in a simulation time of t squared minus the number of those
    #  who haven't
    def evaluate(self, simulation, intersection, network):
        network.schedule_intersection(intersection, self.position)
        simulation.run(network)
        fitness = pow(simulation.no_cars_reached_destination, 2) - simulation.no_cars_en_route
        self.fitness = fitness
        if self.fitness > self.best_fitness:
            self.best_fitness = self.fitness
            self.best_position = copy.copy(self.position)

    def update(self, w, c1, c2, best_particle):
        # best global particle
        # update velocity
        # update position
        for i in range(len(self.position)):
            self.velocity[i] = w * self.velocity[i] + int(c1 * random() *
                                                          (self.best_position[i] - self.position[i])) + int(
                c2 * random() * (best_particle.position[i] - self.position[i]))
            s = 1 / (1 + exp(self.velocity[i]))
            if random() < s:
                # formula from some lab I made
                #    self.position[i], self.position[self.position.index(best_particle.position[i])] =\
                #        self.position[self.position.index(best_particle.position[i])], self.position[i]
                self.position[i] = self.position[i] + self.velocity[i]
