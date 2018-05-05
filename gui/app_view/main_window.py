from threading import Thread

from kivy.adapters.listadapter import ListAdapter
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from gui.app_view.abc_alg_view import ABCView
from gui.app_view.loading_popup import LoadingPopup
from gui.app_view.pso_alg_view import PSOView
from gui.app_view.radom_alg_view import RandomView
from kivy.uix.listview import ListItemButton, ListView

from gui.thread_manager import ThreadManager
from sumo.sumo import Simulation
from sumo_io.configuration_io import ConfigurationIO


class MainScreen(GridLayout):
    selected_color = [200, 44, 44, 0.7]
    unselected_color = [1, 1, 1, 1]
    path = "C:/Users/User/Sumo/"
    t_logic = "osm.net.xml"

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.orientation = 'tb-lr'
        self.pressed_button = ""
        self.loading_popup = LoadingPopup()
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
        self.add_simulation_button.bind(on_press=self.add_sim)

        self.run_algorithm_button = Button(text="Run Algorithm")
        self.run_algorithm_button.bind(on_press=self.run_alg)

        self.run_simulation_button = Button(text="Run Simulation")
        self.run_simulation_button.bind(on_press=self.run_sim)

        self.actions.add_widget(self.add_simulation_button)
        self.actions.add_widget(self.run_algorithm_button)
        self.actions.add_widget(self.run_simulation_button)
        self.add_widget(self.actions)

    def add_sim(instance, values):
        ConfigurationIO.add_simulation()
        instance.start_add_simulation_popup()

    def start_add_simulation_popup(self):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="Simulation Name:"))
        name_input = TextInput(multiline=False)
        content.add_widget(name_input)
        button = Button(text="Finish adding!")
        content.add_widget(button)

        popup = Popup(title="Adding Simulation", content=content, auto_dismiss=False)

        # bind the on_press event of the button to the dismiss function
        button.bind(on_press=lambda x: (self.handle_adding_simulation(popup,name_input)))

        # open the popup
        popup.open()

    def handle_adding_simulation(self,popup, name_input):
        new_name = str(name_input.text)
        new_simulation = ConfigurationIO.get_latest_simulation(MainScreen.path, self.list_adapter.data)
        if not new_simulation:
            return
        if new_simulation and not ConfigurationIO.does_path_exist(MainScreen.path + new_name):
            ConfigurationIO.set_simulation_name(MainScreen.path, new_simulation, new_name)
            self.repopulate_list(new_name)
            popup.dismiss()

    def repopulate_list(self, new_name):
        self.list_adapter.data.append(new_name)
        self.list_view._trigger_reset_populate()

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
        location = MainScreen.path + instance.list_adapter.selection[0].text + "/"
        if ConfigurationIO.verify_simulation_files(location, MainScreen.t_logic):
            popup = LoadingPopup()
            ThreadManager.run_thread_with_popup_and_args(instance.algorithm_manager.run_alg, popup,location,MainScreen.t_logic)

    def run_sim(instance, values):
        location = MainScreen.path + instance.get_current_selection()
        if ConfigurationIO.verify_simulation_files(location, MainScreen.t_logic):
                sim = Simulation(location,MainScreen.t_logic)
                popup = LoadingPopup()
                ThreadManager.run_thread_with_popup(sim.run_gui,popup)

    def get_current_selection(self):
        return self.list_adapter.selection[0].text + "/"


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
