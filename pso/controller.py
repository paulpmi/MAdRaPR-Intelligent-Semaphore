import threading

from swarm import Swarm


class Controller:
    def __init__(self, intersections, simulation):
        self.w = 1
        self.c1 = 2
        self.c2 = 1
        self.intersections = intersections
        self.max_iterations = 0
        self.population_size = 0
        self.population = ""
        self.simulation = simulation
        self.load_data("mock file name", intersections)

    def load_data(self, filename, intersection):
        # do a read from file
        self.c1 = 2
        self.c2 = 2
        self.population_size = 100
        self.max_iterations = 30
        self.population = Swarm(self.population_size, intersection)

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
        pBest.modify_xml(self.simulation)
        return pBest
