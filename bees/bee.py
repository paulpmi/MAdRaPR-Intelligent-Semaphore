import random

import copy

from sumo_io.configuration_io import ConfigurationIO


class Bee:
    def __init__(self, size, min, max):
        self.min = min
        self.max = max
        self.solution = [random.randint(min, max) for i in range(0, size)]
        self.fitness = -1
        self.info = {}
        self.probability = -1
        self.trials = 0

    def clone(self):
        cloned_bee = Bee(len(self.solution), self.min, self.max)
        cloned_bee.solution = self.solution[:]
        cloned_bee.probability = copy.deepcopy(self.probability)
        cloned_bee.fitness = copy.deepcopy(self.fitness)
        cloned_bee.trials = copy.deepcopy(self.trials)
        cloned_bee.info = self.info.copy()
        return cloned_bee

    def initialize_from_neighbor(self, current, neighbour):
        for i in range(0, len(self.solution)):
            new_value = int(
                current.get_solution_at(i) + (current.get_solution_at(i) - neighbour.get_solution_at(i)) * (
                        random.random() - 0.5) * 2)

            if new_value < self.min:
                new_value = self.min
            if new_value > self.max:
                new_value = self.max

            self.solution[i] = new_value

    def initialize_with_scouting(self, bee):
        max_value = max(bee.solution)
        min_value = min(bee.solution)
        for i in range(0, len(bee.solution)):
            new_value = int(min_value + random.random() * (max_value - min_value))

            if new_value < self.min:
                new_value = self.min
            if new_value > self.max:
                new_value = self.max

            self.solution[i] = new_value

    def get_solution_at(self, index):
        return self.solution[index]

    def calculate_probability(self, max_fitness):
        self.probability = 0.9 * self.fitness / max_fitness + 0.1

    def evaluate(self, simulation):
        ConfigurationIO.modify_sumo_configuration(simulation, self.solution)
        simulation.start_simulation()
        fitness, departed, arrived = simulation.get_fitness()
        self.info['departed'] = departed
        self.info['arrived'] = arrived
        simulation.close_simulation()
        self.fitness = fitness
