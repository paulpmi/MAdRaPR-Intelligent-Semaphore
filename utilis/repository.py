from sumo_io.configuration_io import ConfigurationIO
from utilis.firebase_handler import SimulationBlueprint, Firebasehandler


class DataManager:

    @staticmethod
    def add_simulation_blueprint(full_path, name):
        initial_data = ConfigurationIO.get_sim_data(full_path)
        computer_name = ConfigurationIO.get_computer_name()
        blueprint = SimulationBlueprint(name,initial_data,computer_name)
        Firebasehandler.save_simulation_blueprint(blueprint)