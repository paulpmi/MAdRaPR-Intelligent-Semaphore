from sumo_io.configuration_io import ConfigurationIO
from utilis.firebase_handler import SimulationBlueprint, Firebasehandler


class DataManager:

    @staticmethod
    def add_simulation_blueprint(full_path, name):
        initial_data_raw = ConfigurationIO.get_sim_data(full_path)
        initial_data = [x.phases for x in initial_data_raw]
        computer_name = ConfigurationIO.get_computer_name()
        blueprint = SimulationBlueprint(name, initial_data, computer_name)
        Firebasehandler.save_simulation_blueprint(blueprint)

    @staticmethod
    def add_pso_run(run):
        Firebasehandler.save_run("/pso", run)

    @staticmethod
    def add_abc_run(run):
        Firebasehandler.save_run("/abc", run)

    @staticmethod
    def add_random_run(run):
        Firebasehandler.save_run("/random", run)

    @staticmethod
    def get_pso_runs(computer_name, sim_name):
        return Firebasehandler.get_pso_runs(computer_name, sim_name)

    @staticmethod
    def get_abc_runs(computer_name, sim_name):
        return Firebasehandler.get_abc_runs(computer_name, sim_name)

    @staticmethod
    def get_rand_runs(computer_name, sim_name):
        return Firebasehandler.get_random_runs(computer_name, sim_name)

DataManager.get_abc_runs("DESKTOP-7T3FAU8","RiLSA_example1")