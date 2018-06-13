from kivy.app import App

from gui.MyManager import MyScreenManager

class MyApp(App):

    def build(self):
        return MyScreenManager()


if __name__ == '__main__':
    MyApp().run()
