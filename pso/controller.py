from swarm import Swarm

class Controller:
    def __init__(self, intersection):
        self.intersection = 0
        self.max_iterations = 0
        self.population = Swarm()
        self.populationSize = ""

    def load_data(self, filename):
        # do a read from file
        self.populationSize = 40
        self.max_iterations = 40
        self.population = Swarm(self.population_size, self.intersection)

    def iteration(self):
        for particle in self.population.particles:
            particle.update(self.population.get_best_neighbour(particle))
            particle.evaluate()


    def run_alg(self):
        for i in range(0, self.max_iterations):
            self.iteration()
