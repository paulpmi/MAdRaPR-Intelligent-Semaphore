from kivy.app import App

from gui.app_view.main_window import MainScreen
from gui.results.results_view import ResultsView


class MyApp(App):

    def build(self):
        return MainScreen(width=800,cols=2)
        #return ResultsView()


if __name__ == '__main__':
    MyApp().run()