from abc import abstractmethod


class BaseController:
    def __init__(self, lights, simulation):
        self.simulation = simulation
        self.lights = lights

    @abstractmethod
    def run_alg(self):
        pass

    @abstractmethod
    def load_data(self, lights):
        pass

    @abstractmethod
    def iteration(self):
        pass