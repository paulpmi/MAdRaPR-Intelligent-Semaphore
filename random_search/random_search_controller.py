import sys

import copy

from random_search.random_search_generator import RandomSearch
from random_search.random_search_population import RandomSearchPopulation

from sumo_io.configuration_io import ConfigurationIO
from utilis.controller import BaseController


class RandomSearchController(BaseController):
    def __init__(self, lights, simulation, no_iterations, population_siez):
        BaseController.__init__(self, lights, simulation)
        self.no_iterations = no_iterations
        self.population_size = population_siez
        self.population = ""
        self.best_solution = ""
        self.best_fitness = sys.maxint
        self.arrived = 0
        self.waiting = 0
        self.per_step = {}
        self.load_data(lights)

    def run_alg(self):

        for i in range(0, self.no_iterations):
            self.iteration()
        if self.no_iterations > 0:
            ConfigurationIO.modify_sumo_configuration(self.simulation, self.best_solution)
            return self.best_fitness, self.best_solution, self.arrived, self.waiting, self.per_step
        return -1, []

    def load_data(self, lights):
        self.population = RandomSearchPopulation(self.population_size, lights, 5, 50)

    def iteration(self):
        for solution in self.population.population:
            solution.solution = RandomSearch(5, 50).get_random_solution(solution.solution)
            solution.evaluate(self.simulation)
            if self.best_fitness > solution.fitness:
                self.best_fitness = copy.deepcopy(solution.fitness)
                self.best_solution = solution.solution[:]
                self.arrived = copy.deepcopy(solution.info["arrived"])
                self.waiting = copy.deepcopy(solution.info["waiting"])
                self.per_step = solution.info["arrived_per_step"][:]
