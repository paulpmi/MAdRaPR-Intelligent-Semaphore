from bees.bee import Bee
from bees.hive import Hive
from utilis.controller import BaseController


class HiveController(BaseController):
    def __init__(self, lights, simulation):
        BaseController.__init__(self, lights, simulation)
        self.min = 5
        self.max = 50
        self.n = -1  # number of scout bees
        self.m = -1  # number of sites selected out of n visited sites
        self.e = -1  # number of best sites out of m selected sites (e)
        self.nep = -1  # number of bees recruited for best e sites (nep)
        self.nsp = -1  # number of bees recruited for the other (m-e) selected sites (nsp)
        self.ngh = -1  # initial size of patches (ngh) which includes site and its neighbourhood
        self.limit = -1
        self.max_generations = -1  # stopping criterion
        self.load_data("mocked file name", lights)
        self.hive = ""
        self.best = Bee(1, 0, 0)

    def run_alg(self):
        bee_size = 0
        for light in self.lights:
            bee_size += len(light.phases)

        self.hive = Hive(bee_size, self.n / 2, self.limit, self.min, self.max)
        self.hive.evaluate_population(self.simulation)
        for i in range(0, self.max_generations):
            self.iteration()
        return self.best

    def load_data(self, filename, lights):
        self.n = 10
        self.m = 10
        self.limit = 5
        self.max_generations = 10
        pass

    def iteration(self):
        self.hive.send_employed_bees(self.simulation)
        self.hive.calculate_probabilities()
        self.hive.send_onlookers_bees(self.simulation)
        self.hive.send_scout_bees(self.simulation)
        best_generation_bee = self.hive.get_best_bee()
        if best_generation_bee.fitness > self.best.fitness:
            self.best = best_generation_bee.clone()