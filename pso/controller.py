from swarm import Swarm


class Controller:
    def __init__(self, intersection):
        self.c1 = 1
        self.c2 = 2
        self.intersection = ""
        self.max_iterations = 0
        self.population_size = 0
        self.load_data("mock file name")
        self.population = Swarm(self.c1, self.c2, self.population_size, intersection)

    def load_data(self, filename):
        # do a read from file
        self.c1 = 1
        self.c2 = 2
        self.population_size = 40
        self.max_iterations = 40
        self.population = Swarm(self.population_size, self.intersection)

    def iteration(self):
        for particle in self.population.particles:
            particle.update(self.population.get_best_particle())
            particle.evaluate()

    def run_alg(self):
        for i in range(0, self.max_iterations):
            self.iteration()
