from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from random_search.random_search_controller import RandomSearchController
from sumo.sumo import Simulation
from sumo_io.configuration_io import ConfigurationIO
from utilis.firebase_handler import RandomSearchRun
from utilis.repository import DataManager


class RandomView(BoxLayout):

    def __init__(self, **kwargs):
        super(RandomView, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.times_input = TextInput(text='1', multiline=False)
        self.iteration_input = TextInput(text='2', multiline=False)
        self.iteration_input.bind(on_text_validate=self.on_enter)

        self.population_input = TextInput(text='20', multiline=False)

        self.add_widget(Label(text="Times:", height=10))
        self.add_widget(self.times_input)
        self.add_widget(Label(text="Generations:", height=10))
        self.add_widget(self.iteration_input)
        self.add_widget(Label(text="population:"))
        self.add_widget(self.population_input)

    def on_enter(instance, value):
        print('User pressed enter in', value)

    def run_alg(self, path, logic):
        no_generations = 0
        population_size = 0
        times = 0
        try:
            times = int(self.times_input.text)
            no_generations = int(self.iteration_input.text)
            population_size = int(self.population_input.text)
        except ValueError:
            pass
        for i in range(0,times):
            simulation = Simulation(path, logic)
            lights = ConfigurationIO.load_simulation_data(simulation)
            ctrl = RandomSearchController(lights, simulation, no_generations, population_size)

            fitness, solution = ctrl.run_alg()
            sim_name = path.split('/')[-2]
            run = RandomSearchRun(no_generations,population_size,fitness,solution,sim_name,ConfigurationIO.get_computer_name())
            DataManager.add_random_run(run)

        # ConfigurationIO.modify_sumo_configuration(simulation, solution)
        # simulation.run_gui()
