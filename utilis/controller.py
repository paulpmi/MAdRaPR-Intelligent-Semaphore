from abc import abstractmethod


class BaseController:
    def __init__(self, simulation, lights):
        self.simulation = simulation
        self.lights = lights

    @abstractmethod
    def run_alg(self):
        pass

    @abstractmethod
    def load_data(self,filename, lights):
        pass

    @abstractmethod
    def iteration(self):
        pass