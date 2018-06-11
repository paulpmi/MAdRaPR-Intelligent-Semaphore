from Canvas import Rectangle

from kivy.graphics.context_instructions import Color
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class HeaderLabel(Label):
    def __init__(self, **kwargs):
        super(HeaderLabel, self).__init__(**kwargs)
        self.size_hint_x = None
        self.width = 250
        self.height = 80


class ResultsView(GridLayout):
    def __init__(self, **kwargs):
        super(ResultsView, self).__init__(**kwargs)
        self.width = 800
        self.canvas.clear()
        self.row_force_default = True
        self.row_default_height = 40
        self.cols = 3
        self.rows = 3
        self.add_widget(HeaderLabel(text='PSO'))
        self.add_widget(HeaderLabel(text='ABC'))
        self.add_widget(HeaderLabel(text='RANDOM'))
