import xml

from random_search.random_search_population import RandomSearchPopulation
from utilis.controller import BaseController


class RandomSearchController(BaseController):
    def __init__(self, simulation, lights):
        super(simulation, lights)
        self.no_iterations = 0
        self.population_size = 1000
        self.population = ""
        self.load_data()

    def run_alg(self):
        best_solution = ""
        best_fitness = -1
        for i in range(0, self.no_iterations):
            for solution in self.population.population:
                solution.evaluate(self.simulation)
                if best_fitness < solution.fitness:
                    best_fitness = solution.fitness
                    best_solution = solution
        return

    def load_data(self, filename, lights):
        self.no_iterations = 40
        self.population_size = 1000
        self.population = RandomSearchPopulation(self.population_size, lights, 5, 90)

    def iteration(self):
        pass

    #move it to an input output xml file
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
