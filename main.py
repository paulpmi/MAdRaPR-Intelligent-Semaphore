import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter

from gui.main_window import MainScreen
from gui.radom_alg_view import RandomView


class MyApp(App):

    def build(self):
        return MainScreen(width=800,cols=2)


if __name__ == '__main__':
    MyApp().run()