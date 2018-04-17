from sumo_io.configuration_io import ConfigurationIO
from utilis.controller import BaseController
from swarm import Swarm


class PSOController(BaseController):
    def __init__(self, lights, simulation, no_iterations, population_size, inertia_c, cognitive_l_c, social_l_c):
        BaseController.__init__(self, lights, simulation)
        self.w = inertia_c
        self.c1 = cognitive_l_c
        self.c2 = social_l_c
        self.lights = lights
        self.max_iterations = no_iterations
        self.population_size = population_size
        self.population = ""
        self.simulation = simulation
        self.load_data(lights)

    def load_data(self, lights):
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
        return pBest.fitness, pBest.position
