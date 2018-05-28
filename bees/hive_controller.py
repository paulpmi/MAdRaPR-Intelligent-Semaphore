from bees.bee import Bee
from bees.hive import Hive
from utilis.controller import BaseController


class HiveController(BaseController):
    def __init__(self, lights, simulation, no_generations, population_size, limit):
        BaseController.__init__(self, lights, simulation)
        self.min = 5
        self.max = 50
        self.population_size = population_size  # number of scout bees
        self.limit = limit
        self.no_generations = no_generations  # stopping criterion
        self.hive = ""
        self.load_data(lights)
        self.best = Bee(1, 0, 0)

    def load_data(self, lights):
        bee_size = 0
        for light in self.lights:
            bee_size += len(light.phases)
        self.hive = Hive(bee_size, self.population_size / 2, self.limit, self.min, self.max)

    def run_alg(self):
        self.hive.evaluate_population(self.simulation)
        for i in range(0, self.no_generations):
            self.iteration()
        self.simulation.close_simulation()
        return self.best.fitness,self.best.solution

    def iteration(self):
        self.hive.send_employed_bees(self.simulation)
        self.hive.calculate_probabilities()
        self.hive.send_onlookers_bees(self.simulation)
        self.hive.send_scout_bees(self.simulation)
        best_generation_bee = self.hive.get_best_bee()
        if best_generation_bee.fitness < self.best.fitness:
            self.best = best_generation_bee.clone()
