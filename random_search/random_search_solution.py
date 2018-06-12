import random

from sumo_io.configuration_io import ConfigurationIO


class RandomSearchSolution:
    def __init__(self, lights, min, max):
        self.info = {}
        self.solution = []
        self.fitness = -1
        self.initialize(lights, min, max)

    # the numbers of cars that had reached their destination in a simulation time of t squared minus the number of those
    #  who haven't
    def evaluate(self, simulation):
        ConfigurationIO.modify_sumo_configuration(simulation, self.solution)
        fitness, arrived, waiting, arrived_per_step = simulation.get_fitness()
        self.info['arrived'] = arrived
        self.info['waiting'] = waiting
        self.info['arrived_per_step'] = arrived_per_step
        self.fitness = fitness

    def initialize(self, lights, min, max):
        for light in lights:
            for i in range(0, len(light.phases)):
                self.solution.append(random.randint(min, max))
