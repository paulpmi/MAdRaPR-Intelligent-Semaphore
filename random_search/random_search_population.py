from random_search.random_search_solution import RandomSearchSolution


class RandomSearchPopulation:
    def __init__(self, size,lights, min, max):
        self.size = size
        self.min = min
        self.max = max
        self.population = [RandomSearchSolution(lights, min, max) for i in range(0, self.size)]
