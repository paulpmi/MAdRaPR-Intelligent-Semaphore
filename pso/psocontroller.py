import copy

import sys

from utilis.controller import BaseController
from swarm import Swarm


class PSOController(BaseController):
    def __init__(self, lights, simulation, no_iterations, population_size, inertia_c, cognitive_l_c, social_l_c):
        BaseController.__init__(self, lights, simulation)
        self.max_w = float(inertia_c)
        self.w = float(inertia_c)
        self.c1 = cognitive_l_c
        self.c2 = social_l_c
        self.lights = lights
        self.max_iterations = no_iterations
        self.population_size = population_size
        self.population = ""
        self.simulation = simulation
        self.load_data(lights)
        self.best_position = []
        self.best_fitness = sys.maxint
        self.info = {}

    def load_data(self, lights):
        self.population = Swarm(self.population_size, lights)

    def iteration(self, generation):
        self.update_velocity_and_position(generation)
        self.evaluate_particles()
        self.update_best_particle()

    def update_velocity_and_position(self, generation):
        for particle in self.population.particles:
            self.update_inertia(generation)
            particle.update(self.w, self.c1, self.c2, self.population.get_best_particle())

    def evaluate_particles(self):
        for particle in self.population.particles:
            particle.evaluate(self.simulation)

    def update_inertia(self, generation):
        self.w = self.w - float((self.max_w - 0.2) * generation / self.max_iterations)

    def run_alg(self):
        self.evaluate_particles()
        self.update_best_particle()
        for i in range(0, self.max_iterations):
            self.iteration(i)

        self.simulation.close_simulation()
        return self.best_fitness, self.best_position, self.info["arrived"],self.info["waiting"],self.info["step"]

    def update_best_particle(self):
        for p in self.population.particles:
            if p.fitness < self.best_fitness:
                self.best_fitness = copy.deepcopy(p.fitness)
                self.best_position = p.position[:]
                self.info = p.info.copy()