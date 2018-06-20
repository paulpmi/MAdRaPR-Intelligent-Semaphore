import random

import copy

from bees.bee import Bee


class Hive:
    def __init__(self, bee_size, hive_size, limit, min, max):
        self.min = min
        self.max = max
        self.limit = limit
        self.bee_size = bee_size
        self.hive_size = hive_size
        self.hive = [Bee(bee_size, min, max) for i in range(0, hive_size)]

    def evaluate_population(self, simulation):
        for bee in self.hive:
            bee.evaluate(simulation)

    def get_random_index(self, exception):
        index = copy.deepcopy(exception)
        while index == exception:
            index = random.randint(0, len(self.hive)-1)
        return index

    def get_bee_from_neighbour(self, bee):
        current_bee_index = -1
        for i in range(0, len(self.hive)):
            if self.hive[i] == bee:
                current_bee_index = i
        neighbour_bee_index = self.get_random_index(current_bee_index)
        new_bee = Bee(self.bee_size, self.min, self.max)
        new_bee.initialize_from_neighbor(self.hive[current_bee_index], self.hive[neighbour_bee_index])

        return new_bee

    def sort(self):
        self.hive.sort(key=lambda x: x.fitness)

    def get_best_bee(self):
        self.sort()
        return self.hive[0]

    def do_work(self, bee, new_bees, simulation):
        new_bee = self.get_bee_from_neighbour(bee)
        new_bee.evaluate(simulation)
        if new_bee.fitness < bee.fitness:
            new_bees.append(new_bee)
        else:
            bee.trials += 1
            new_bees.append(bee)

    def send_employed_bees(self, simulation):
        new_bees = []
        for bee in self.hive:
            self.do_work(bee, new_bees, simulation)
        self.hive = new_bees[:]
        self.sort()

    def send_onlookers_bees(self, simulation):
        new_bees = []
        for bee in self.hive:
            if random.random() < bee.probability:
                self.do_work(bee, new_bees, simulation)
            else:
                new_bees.append(bee)
        self.hive = new_bees[:]
        self.sort()

    def send_scout_bees(self, simulation):
        new_bees = []
        for bee in self.hive:
            if bee.trials > self.limit:
                self.scout_food_source(bee, new_bees, simulation)
            else:
                new_bees.append(bee)
        self.hive = new_bees[:]
        self.sort()

    def calculate_probabilities(self):
        max_fitness = self.get_best_bee().fitness
        for bee in self.hive:
            bee.calculate_probability(max_fitness)

    def scout_food_source(self, bee, new_bees, simulation):
        new_bee = Bee(self.bee_size, self.min, self.max)
        new_bee.initialize_with_scouting(bee)
        new_bee.evaluate(simulation)
        new_bees.append(new_bee)
