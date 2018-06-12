from Canvas import Rectangle

from kivy.adapters.listadapter import ListAdapter
from kivy.graphics.context_instructions import Color
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.listview import ListView, ListItemButton

from utilis.repository import DataManager


class HeaderLabel(Label):
    def __init__(self, **kwargs):
        super(HeaderLabel, self).__init__(**kwargs)
        self.size_hint_x = None
        self.width = 250
        self.height = 80


class DataItem(object):
    def __init__(self, text='', is_selected=False):
        self.text = text
        self.is_selected = is_selected


class RunListView(ListView):
    def __init__(self, **kwargs):
        super(ListView, self).__init__(**kwargs)
        self.height = 500
        list_item_args_converter = lambda row_index, obj: {'text': obj.best_fitness,
                                                           'size_hint_y': None,
                                                           'height': 30}
        self.adapter = ListAdapter(data=self.parent[:],
                                                  args_converter=list_item_args_converter,
                                                  propagate_selection_to_data=True,
                                                  cls=ListItemButton)


class ResultsView(GridLayout):
    def __init__(self, **kwargs):
        super(ResultsView, self).__init__(**kwargs)
        self.width = 800
        self.canvas.clear()
        self.row_force_default = True
        self.row_default_height = 40
        self.cols = 3
        self.rows = 3
        self.pso_runs = DataManager.get_pso_runs("DESKTOP-7T3FAU8", "RiLSA_example1")
        self.abc_runs = DataManager.get_abc_runs("DESKTOP-7T3FAU8", "RiLSA_example1")
        self.rand_runs = DataManager.get_rand_runs("DESKTOP-7T3FAU8", "RiLSA_example1")
        self.add_widget(HeaderLabel(text='PSO'))
        self.add_widget(HeaderLabel(text='ABC'))
        self.add_widget(HeaderLabel(text='RANDOM'))
        self.add_widget(RunListView(parent=self.pso_runs))
        self.add_widget(RunListView(parent=self.abc_runs))
        self.add_widget(RunListView(parent=self.rand_runs))
