import xml

from random_search.random_search_population import RandomSearchPopulation

from sumo_io.configuration_io import ConfigurationIO
from utilis.controller import BaseController


class RandomSearchController(BaseController):
    def __init__(self, simulation, lights):
        super(simulation, lights)
        self.no_iterations = 0
        self.population_size = 1000
        self.population = ""
        self.best_solution = ""
        self.best_fitness = -1
        self.load_data("mok file",simulation)

    def run_alg(self):

        for i in range(0, self.no_iterations):
            self.iteration()
        ConfigurationIO.modify_sumo_configuration(self.simulation, self.best_solution.solution)
        return self.best_fitness, self.best_solution.solution

    def load_data(self, filename, lights):
        self.no_iterations = 40
        self.population_size = 1000
        self.population = RandomSearchPopulation(self.population_size, lights, 5, 90)

    def iteration(self):
        for solution in self.population.population:
            solution.evaluate(self.simulation)
            if self.best_fitness < solution.fitness:
                self.best_fitness = solution.fitness
                self.best_solution = solution
