from kivy.app import App

from gui.app_view.main_window import MainScreen


class MyApp(App):

    def build(self):
        return MainScreen(width=800,cols=2)


if __name__ == '__main__':
    MyApp().run()