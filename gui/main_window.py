from kivy.adapters.listadapter import ListAdapter
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from kivy.uix.stacklayout import StackLayout

from gui.abc_alg_view import ABCView
from gui.pso_alg_view import PSOView
from gui.radom_alg_view import RandomView


class MainScreen(GridLayout):
    selected_color = [200, 44, 44, 0.7]
    unselected_color = [1, 1, 1, 1]

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.orientation = 'tb-lr'

        # handle upper layout
        self.side_bar = BoxLayout(orientation='vertical')
        self.add_widget(self.side_bar)

        # handle list
        from kivy.uix.listview import ListItemButton, ListView

        data = [{'text': str(i), 'is_selected': False} for i in range(100)]

        self.args_converter = lambda row_index, rec: {'text': rec['text'],
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
        self.random_button = Button(text="Random", colour='red')
        self.random_button.background_color = MainScreen.selected_color[:]
        self.pso_button = Button(text="PSO")
        self.abc_button = Button(text="ABC")
        self.side_bar.add_widget(self.random_button)
        self.side_bar.add_widget(self.pso_button)
        self.side_bar.add_widget(self.abc_button)

        # algorithm view
        self.algorithm_view = ABCView()
        self.add_widget(self.algorithm_view)

        # actions
        self.actions = BoxLayout(orientation='vertical')
        self.add_simulation_button = Button(text="Add Simulation", )

        self.run_simulation_button = Button(text="Run Simulation")
        self.run_simulation_button.bind(on_press=self.run_alg)

        self.actions.add_widget(self.add_simulation_button)
        self.actions.add_widget(self.run_simulation_button)
        self.add_widget(self.actions)

    def run_alg(instance, values):
        instance.algorithm_view.run_alg("", "")
