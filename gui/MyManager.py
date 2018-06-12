from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from gui.app_view.main_window import MainScreen
from gui.results.results_view import ResultsView
from sumo_io.configuration_io import ConfigurationIO


class MyScreenManager(BoxLayout):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.computer_name = ConfigurationIO.get_computer_name()
        self.sim_name = ""

        self.waiting = Popup(text="Loading...",auto_dismiss=False)

        self.main = MainScreen(width=800, cols=2)
        self.main.screen_manager = self

        self.results = ResultsView()
        self.results.screen_manager = self
        self.results.populate()

        self.add_widget(self.main)

    def back_to_main(self):
        self.clear_widgets()
        self.add_widget(self.main)

    def get_selected_sim(self):
        return self.computer_name, self.main.get_current_selection_name()

    def put_start(self):
        self.waiting.open(

        )
    def to_results(self):
        self.clear_widgets()
        self.results.populate()
        self.add_widget(self.results)
