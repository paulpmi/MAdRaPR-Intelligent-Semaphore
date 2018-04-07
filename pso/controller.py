from sumo_io.configuration_io import ConfigurationIO
from utilis.controller import BaseController
from swarm import Swarm


class Controller(BaseController):
    def __init__(self, lights, simulation):
        super(lights,simulation)
        self.w = 1
        self.c1 = 2
        self.c2 = 1
        self.lights = lights
        self.max_iterations = 0
        self.population_size = 0
        self.population = ""
        self.simulation = simulation
        self.load_data("mock file name", lights)

    def load_data(self, filename, lights):
        # do a read from file
        self.c1 = 2
        self.c2 = 2
        self.population_size = 100
        self.max_iterations = 30
        self.population = Swarm(self.population_size, lights)

    def iteration(self):
        for particle in self.population.particles:
            particle.update(self.w, self.c1, self.c2, self.population.get_best_particle())
            particle.evaluate(self.simulation)

    def run_alg(self):
        for i in range(0, self.max_iterations):
            self.iteration()
        pBest = self.population.particles[0]
        for p in self.population.particles:
            if p.fitness > pBest.fitness:
                pBest = p
        ConfigurationIO.modify_sumo_configuration(self.simulation,pBest.position)
        return pBest
