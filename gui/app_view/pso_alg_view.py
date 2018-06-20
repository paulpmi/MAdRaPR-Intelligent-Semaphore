from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from pso.psocontroller import PSOController
from random_search.random_search_controller import RandomSearchController
from sumo.sumo import Simulation
from sumo_io.configuration_io import ConfigurationIO
from utilis.firebase_handler import PSOSearchRun
from utilis.repository import DataManager


class PSOView(BoxLayout):

    def __init__(self, **kwargs):
        super(PSOView, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.times_input = TextInput(text='1', multiline=False)
        self.iteration_input = TextInput(text='30', multiline=False)
        self.population_input = TextInput(text='100', multiline=False)
        self.inertia_input = TextInput(text='0.7', multiline=False)
        self.cognitive_input = TextInput(text='2', multiline=False)
        self.social_input = TextInput(text='1', multiline=False)

        self.add_widget(Label(text="Times:", height=10))
        self.add_widget(self.times_input)
        self.add_widget(Label(text="Generations:", height=10))
        self.add_widget(self.iteration_input)
        self.add_widget(Label(text="population:"))
        self.add_widget(self.population_input)
        self.add_widget(Label(text="inertia:"))
        self.add_widget(self.inertia_input)
        self.add_widget(Label(text="cognitive:"))
        self.add_widget(self.cognitive_input)
        self.add_widget(Label(text="social:"))
        self.add_widget(self.social_input)

    def is_valid(self, times, no_g, size_p, w, c, s):
        if times < 0 or no_g < 1 or size_p < 1 or w <= 0 or c <= 0 or s <= 0:
            return False
        return True

    def run_alg(self, path, logic):
        no_generations = 0
        population_size = 0
        inertia = 0
        cognitive = 0
        social = 0
        times = 0
        try:
            times = int(self.times_input.text)
            no_generations = int(self.iteration_input.text)
            population_size = int(self.population_input.text)
            inertia = float(self.inertia_input.text)
            cognitive = float(self.cognitive_input.text)
            social = float(self.social_input.text)
        except ValueError:
            pass
        if not self.is_valid(times, no_generations, population_size, inertia, cognitive, social):
            return
        for i in range(0, times):
            simulation = Simulation(path, logic)
            lights = ConfigurationIO.load_simulation_data(simulation)
            ctrl = PSOController(lights, simulation, no_generations, population_size, inertia, cognitive, social)

            fitness, solution, arrived, waiting, step = ctrl.run_alg()
            sim_name = path.split('/')[-2]
            run = PSOSearchRun(no_generations, population_size, fitness, solution, inertia, cognitive, social, sim_name,
                               ConfigurationIO.get_computer_name(), arrived, waiting, step)
            DataManager.add_pso_run(run)
        # ConfigurationIO.modify_sumo_configuration(simulation, solution)
        # simulation.run_gui()
