import random


class RandomSearch:
    def __init__(self, minimum, maximum):
        self.min = minimum
        self.max = maximum

    def get_random_solution(self, vector):
        return [random.randint(self.min, self.max) for i in range(0, len(vector))]

