from Canvas import Rectangle

from kivy.uix.button import Button

from kivy.adapters.listadapter import ListAdapter
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.listview import ListView, ListItemButton

from gui.app_view.main_window import MainScreen
from sumo.sumo import Simulation
from sumo_io.configuration_io import ConfigurationIO
from utilis.repository import DataManager
from utilis.thread_manager import ThreadManager


class HeaderLabel(Label):
    def __init__(self, **kwargs):
        super(HeaderLabel, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = 80


class DataItem(object):
    def __init__(self, is_selected=False, fitness=-1, solution=[], args={}, per_step=[], type="none", population=0,
                 generations=0, arrived=0, waiting=0):
        self.text = str(fitness) + " " + type
        self.is_selected = is_selected
        self.fitness = fitness
        self.population = population
        self.generations = generations
        self.solution = solution[:]
        self.args = args.copy()
        self.per_step = per_step[:]
        self.type = type


class ResultsView(BoxLayout):

    def __init__(self, **kwargs):
        super(ResultsView, self).__init__(**kwargs)
        self.screen_manager = ""
        self.width = 800
        self.orientation = 'vertical'
        self.action_bar = BoxLayout(orientation="horizontal", height=100, size_hint_y=None)
        self.sim_name = ""
        self.comp_name = ""
        self.init()

    def init(self):

        self.clear_widgets()
        self.action_bar.clear_widgets()

        self.back_button = Button(on_press=self.back_clicked, text="Back")
        self.run_button = Button(on_press=self.run_clicked, text="Run")
        self.view_button = Button(on_press=self.view_clicked, text="View")
        self.action_bar.add_widget(self.back_button)
        self.action_bar.add_widget(self.run_button)
        self.action_bar.add_widget(self.view_button)
        data = []
        self.add_widget(HeaderLabel(text='Solutions'))
        self.args_converter = lambda row_index, rec: {'text': rec.text,
                                                      'size_hint_y': None,
                                                      'height': 25}
        self.list_adapter = ListAdapter(data=data,
                                        args_converter=self.args_converter,
                                        cls=ListItemButton,
                                        selection_mode='single',
                                        allow_empty_selection=False)
        self.list_view = ListView(adapter=self.list_adapter, scrolling='true')
        self.add_widget(self.list_view)
        self.add_widget(self.action_bar)

    def populate(self):
        self.comp_name, self.sim_name = self.screen_manager.get_selected_sim()
        pso_runs = DataManager.get_pso_runs(self.comp_name, self.sim_name)
        abc_runs = DataManager.get_abc_runs(self.comp_name, self.sim_name)
        rand_runs = DataManager.get_rand_runs(self.comp_name, self.sim_name)

        data = []
        for run in pso_runs:
            data.append(DataItem(fitness=run.v, population=run.population, generations=run.generations,
                                 solution=run.best_solution, arrived=run.arrived, waiting=run.departed,
                                 per_step=run.per_step, type="PSO",
                                 args={"inertia": run.inertia, "cognitive": run.cognitive, "social": run.social}))
        for run in abc_runs:
            data.append(DataItem(fitness=run.v, population=run.population, generations=run.generations,
                                 solution=run.best_solution, arrived=run.arrived, waiting=run.departed,
                                 per_step=run.per_step, type="ABC",
                                 args={"limit": run.limit}))
        for run in rand_runs:
            data.append(DataItem(fitness=run.v, population=run.population, generations=run.generations,
                                 solution=run.best_solution, arrived=run.arrived, waiting=run.departed,
                                 per_step=run.per_step, type="RAND",
                                 ))
        data = sorted(data, key=lambda key: key.fitness)

        del self.list_adapter.data[:]
        for d in data:
            self.list_adapter.data.append(d)
        self.list_view._trigger_reset_populate()

    def run_clicked(instance, values):
        location = MainScreen.path + instance.sim_name + "/"
        if ConfigurationIO.verify_simulation_files(location, MainScreen.t_logic) and len(
                instance.list_adapter.data) > 0:
            sim = Simulation(location, MainScreen.t_logic)
            ThreadManager.run_thread_without_popup(sim.run_gui, [
                instance.list_adapter.data[instance.list_adapter.selection[0].index].solution,instance.screen_manager.waiting])

    def view_clicked(instance, values):
        pass

    def back_clicked(instance, values):
        instance.screen_manager.back_to_main()
