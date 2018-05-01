from kivy.adapters.listadapter import ListAdapter
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from gui.abc_alg_view import ABCView
from gui.pso_alg_view import PSOView
from gui.radom_alg_view import RandomView
from kivy.uix.listview import ListItemButton, ListView

from sumo_io.configuration_io import ConfigurationIO


class MainScreen(GridLayout):
    selected_color = [200, 44, 44, 0.7]
    unselected_color = [1, 1, 1, 1]
    path = "C:\Users\User\Sumo"

    def __init__(self, **kwargs):

        super(MainScreen, self).__init__(**kwargs)
        self.orientation = 'tb-lr'
        self.pressed_button = ""
        # handle upper layout
        self.side_bar = BoxLayout(orientation='vertical')
        self.add_widget(self.side_bar)

        # handle list

        data = ConfigurationIO.get_simulations(MainScreen.path)

        self.args_converter = lambda row_index, rec: {'text': rec,
                                                      'size_hint_y': None,
                                                      'height': 25}

        self.list_adapter = ListAdapter(data=data,
                                        args_converter=self.args_converter,
                                        cls=ListItemButton,
                                        selection_mode='single',
                                        allow_empty_selection=False)

        self.list_view = ListView(adapter=self.list_adapter, scrolling='true')

        self.add_widget(self.list_view)

        # # handle side bar
        self.random_button = Button(text="Random")
        self.pressed_button = self.random_button
        self.random_button.color = MainScreen.selected_color[:]
        self.pso_button = Button(text="PSO")
        self.abc_button = Button(text="ABC")
        self.side_bar.add_widget(self.random_button)
        self.random_button.bind(on_press=self.random_press_action)
        self.side_bar.add_widget(self.pso_button)
        self.pso_button.bind(on_press=self.pso_press_action)
        self.side_bar.add_widget(self.abc_button)
        self.abc_button.bind(on_press=self.abc_press_action)

        # algorithm view
        self.algorithm_manager = AlgorithmManager()
        self.algorithm_manager.set_view(RandomView())
        self.add_widget(self.algorithm_manager)

        # actions
        self.actions = BoxLayout(orientation='vertical')
        self.add_simulation_button = Button(text="Add Simulation", )

        self.run_simulation_button = Button(text="Run Simulation")
        self.run_simulation_button.bind(on_press=self.run_alg)

        self.actions.add_widget(self.add_simulation_button)
        self.actions.add_widget(self.run_simulation_button)
        self.add_widget(self.actions)

    def pso_press_action(instance, values):
        instance.pressed_button.color = MainScreen.unselected_color[:]
        instance.pso_button.color = MainScreen.selected_color[:]
        instance.pressed_button = instance.pso_button
        instance.algorithm_manager.set_view(PSOView())

    def abc_press_action(instance, values):
        instance.pressed_button.color = MainScreen.unselected_color[:]
        instance.abc_button.color = MainScreen.selected_color[:]
        instance.pressed_button = instance.abc_button
        instance.algorithm_manager.set_view(ABCView())

    def random_press_action(instance, values):
        instance.pressed_button.color = MainScreen.unselected_color[:]
        instance.random_button.color = MainScreen.selected_color[:]
        instance.pressed_button = instance.random_button
        instance.algorithm_manager.set_view(RandomView())

    def run_alg(instance, values):
        instance.algorithm_manager.run_alg("", "")


class AlgorithmManager(BoxLayout):
    def __init__(self, **kwargs):
        super(AlgorithmManager, self).__init__(**kwargs)
        self.view = ""

    def set_view(self, view):
        self.clear_widgets()
        self.view = view
        self.add_widget(self.view)

    def run_alg(self, location, t_logic_file):
        if self.view:
            self.view.run_alg(location, t_logic_file)
