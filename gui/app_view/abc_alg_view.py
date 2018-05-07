from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from bees.hive_controller import HiveController
from pso.psocontroller import PSOController
from random_search.random_search_controller import RandomSearchController
from sumo.sumo import Simulation
from sumo_io.configuration_io import ConfigurationIO
from utilis.firebase_handler import ABCSearchRun
from utilis.repository import DataManager


class ABCView(BoxLayout):

    def __init__(self, **kwargs):
        super(ABCView, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.iteration_input = TextInput(text='30', multiline=False)
        self.population_input = TextInput(text='100', multiline=False)
        self.limit_input = TextInput(text='10', multiline=False)

        self.add_widget(Label(text="Generations:", height=10))
        self.add_widget(self.iteration_input)
        self.add_widget(Label(text="Population:"))
        self.add_widget(self.population_input)
        self.add_widget(Label(text="Limit:"))
        self.add_widget(self.limit_input)

    def run_alg(self, path, logic):
        no_generations = 0
        population_size = 0
        limit = 0
        try:
            no_generations = int(self.iteration_input.text)
            population_size = int(self.population_input.text)
            limit = float(self.limit_input.text)

        except ValueError:
            pass
        simulation = Simulation(path, logic)
        lights = ConfigurationIO.load_simulation_data(simulation)
        ctrl = HiveController(lights, simulation, no_generations, population_size, limit)

        fitness, solution = ctrl.run_alg()
        sim_name = path.split('/')[-2]
        run = ABCSearchRun(no_generations, population_size, limit, fitness, solution, sim_name,
                           ConfigurationIO.get_computer_name())
        DataManager.add_abc_run(run)
        # ConfigurationIO.modify_sumo_configuration(simulation, solution)
        # simulation.run_gui()
