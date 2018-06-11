from abc import abstractmethod

from firebase import firebase
import json


class Firebasehandler:
    firebase = firebase.FirebaseApplication('https://lights-d20c1.firebaseio.com/')

    @staticmethod
    def save_simulation_blueprint(blueprint):
        Firebasehandler.firebase.post('/blueprints', blueprint.to_json())

    @staticmethod
    def get_simulations_blueprint():
        dic = Firebasehandler.firebase.get('/blueprints', None)
        blueprint_list = []
        if dic is None:
            return blueprint_list
        for items in dic.values():
            blueprint = SimulationBlueprint.from_json(items)
            blueprint_list.append(blueprint)
        return blueprint_list

    @staticmethod
    def get_simulation_blueprint(name, computer_name):
        blueprints = Firebasehandler.get_simulations_blueprint()
        for blueprint in blueprints:
            if blueprint.name == name and blueprint.computer_name == computer_name:
                return SimulationBlueprint.from_json(blueprint)
        return None

    @staticmethod
    def simulation_is_present_blueprint(name, computer_name):
        blueprints = Firebasehandler.get_simulations_blueprint()
        for blueprint in blueprints:
            if blueprint.name == name and blueprint.computer_name == computer_name:
                return True
        return False

    @staticmethod
    def get_runs(run_type, computer_name, name):
        result = []
        dic = Firebasehandler.firebase.get(run_type, None)
        if dic is None:
            return result

        for item in dic.values():
            if str(item[u'simulation_name']) == name and str(item[u'computer_name']) == computer_name:
                result.append(item)
        return result

    @staticmethod
    def get_random_runs(computer_name, name):
        runs = Firebasehandler.get_runs("/random", computer_name, name)
        random_runs = []
        for run in runs:
            random_runs.append(RandomSearchRun.from_json(run))
        return random_runs

    @staticmethod
    def get_pso_runs(computer_name, name):
        runs = Firebasehandler.get_runs("/pso", computer_name, name)
        pso_runs = []
        for run in runs:
            pso_runs.append(PSOSearchRun.from_json(run))
        return pso_runs

    @staticmethod
    def get_abc_runs(computer_name, name):
        runs = Firebasehandler.get_runs("/abc", computer_name, name)
        abc_runs = []
        for run in runs:
            abc_runs.append(ABCSearchRun.from_json(run))
        return abc_runs

    @staticmethod
    def save_run(run_type, run):
        Firebasehandler.firebase.post(run_type, run.to_json())


class SimulationBlueprint():
    def __init__(self, name, initial_data, computer_name):
        self.name = name
        self.initial_data = initial_data
        self.computer_name = computer_name

    def to_json(self):
        return {"name": self.name, "initial_data": self.initial_data, "computer_name": self.computer_name}

    @staticmethod
    def from_json(dic):
        name = str(dic[u'name'])
        computer_name = str(dic[u'computer_name'])
        initial_data = dic[u'initial_data']
        return SimulationBlueprint(name, initial_data, computer_name)


class SearchRun:
    def __init__(self, generations, population, best_fitness, best_solution, simulation_name, computer_name, arrived,
                 departed, per_step):
        self.generations = int(generations)
        self.population = population
        self.best_fitness = best_fitness
        self.best_solution = best_solution
        self.simulation_name = simulation_name
        self.computer_name = computer_name
        self.arrived = arrived
        self.departed = departed
        self.per_step = per_step

    @abstractmethod
    def to_json(self):
        pass


class RandomSearchRun(SearchRun):
    def __init__(self, generations, population, best_fitness, best_solution, simulation_name, computer_name, arrived,
                 departed, per_step):
        SearchRun.__init__(self, generations, population, best_fitness, best_solution, simulation_name, computer_name,
                           arrived, departed, per_step)

    def to_json(self):
        return {"generations": self.generations, "population": self.population, "best_fitness": self.best_fitness,
                "best_solution": self.best_solution, "simulation_name": self.simulation_name,
                "computer_name": self.computer_name, "version": 2, "arrived": self.arrived, "waiting": self.departed,
                "per_step": self.per_step}

    @staticmethod
    def from_json(dic):
        generations = str(dic[u'generations'])
        population = str(dic[u'population'])
        best_fitness = dic[u'best_fitness']
        best_solution = dic[u'best_solution']
        simulation_name = dic[u'simulation_name']
        computer_name = dic[u'computer_name']
        arrived = dic[u'arrived']
        waiting = dic[u'waiting']
        per_step = dic[u'per_step']
        return RandomSearchRun(generations, population, best_fitness, best_solution, simulation_name, computer_name,
                               arrived, waiting, per_step)


class PSOSearchRun(SearchRun):
    def __init__(self, generations, population, best_fitness, best_solution, inertia, cognitive, social,
                 simulation_name, computer_name, arrived, departed, per_step):
        SearchRun.__init__(self, generations, population, best_fitness, best_solution, simulation_name, computer_name,
                           arrived,
                           departed, per_step)
        self.inertia = float(inertia)
        self.cognitive = float(cognitive)
        self.social = float(social)

    def to_json(self):
        return {"generations": self.generations, "population": self.population, "inertia": self.inertia,
                "cognitive": self.cognitive, "social": self.social, "best_fitness": self.best_fitness,
                "best_solution": self.best_solution, "simulation_name": self.simulation_name,
                "computer_name": self.computer_name, "version": 2, "arrived": self.arrived,
                "waiting": self.departed, "per_step": self.per_step}

    @staticmethod
    def from_json(dic):
        generations = str(dic[u'generations'])
        population = str(dic[u'population'])
        inertia = str(dic[u'inertia'])
        cognitive = str(dic[u'cognitive'])
        social = str(dic[u'social'])
        best_fitness = dic[u'best_fitness']
        best_solution = dic[u'best_solution']
        simulation_name = dic[u'simulation_name']
        computer_name = dic[u'computer_name']
        arrived = dic[u'arrived']
        waiting = dic[u'waiting']
        per_step = dic[u'per_step']
        return PSOSearchRun(generations, population, best_fitness,best_solution,inertia, cognitive, social,
                            simulation_name, computer_name, arrived, waiting, per_step)


class ABCSearchRun(SearchRun):
    def __init__(self, generations, population, limit, best_fitness, best_solution,
                 simulation_name, computer_name, arrived,
                 departed, per_step):
        SearchRun.__init__(self, generations, population, best_fitness, best_solution, simulation_name, computer_name,
                           arrived, departed, per_step)
        self.limit = limit

    def to_json(self):
        return {"generations": self.generations, "population": self.population, "limit": self.limit,
                "best_fitness": self.best_fitness,
                "best_solution": self.best_solution, "simulation_name": self.simulation_name,
                "computer_name": self.computer_name, "version": 2, "arrived": self.arrived,
                "waiting": self.departed, "per_step": self.per_step}

    @staticmethod
    def from_json(dic):
        generations = str(dic[u'generations'])
        population = str(dic[u'population'])
        limit = int(dic[u'limit'])
        best_fitness = dic[u'best_fitness']
        best_solution = dic[u'best_solution']
        simulation_name = dic[u'simulation_name']
        computer_name = dic[u'computer_name']
        arrived = dic[u'arrived']
        waiting = dic[u'waiting']
        per_step = dic[u'per_step']
        return ABCSearchRun(generations, population, limit, best_fitness, best_solution,
                            simulation_name, computer_name, arrived, waiting, per_step)
