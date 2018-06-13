import operator

import numpy
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from utilis.statistics import Statistics


class StatisticsView(BoxLayout):
    def __init__(self, **kwargs):
        super(StatisticsView, self).__init__(**kwargs)
        self.screen_manager = ""
        self.orientation = "horizontal"
        self.pso_scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        self.add_widget(self.pso_scroll_view)
        self.pos_grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.pso_scroll_view.add_widget(self.pos_grid)

        self.abc_scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        self.add_widget(self.abc_scroll_view)
        self.abc_grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.abc_scroll_view.add_widget(self.abc_grid)

        self.rand_scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        self.add_widget(self.rand_scroll_view)
        self.rand_grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.rand_scroll_view.add_widget(self.rand_grid)

        self.add_widget(Button(text="Back", size_hint=(None, None), width=40, height=20, on_press=self.go_back))

    def go_back(instance, values):
        instance.screen_manager.to_results()

    def populate(self, pso, abc, rand):
        self.pos_grid.clear_widgets()
        self.abc_grid.clear_widgets()
        self.rand_grid.clear_widgets()
        
        pso_data = Statistics.map_to_mean_and_std_dev(Statistics.separate_pso_runs(pso))
        pso_data = sorted(pso_data.items(), key=lambda x: x[1][0])
        for item in pso_data:
            g, w, c, s = item[0]
            mean, std_dev, no = item[1]

            # graph = Graph(ylabel='Fitness mean',
            #               y_ticks_minor=0.1,
            #               y_ticks_major=1,
            #               x_ticks_minor=0.1,
            #               x_ticks_major=1,
            #               y_grid_label=True,
            #               x_grid_label=False,
            #               padding=1,
            #               y_grid=True,
            #               x_grid=True,
            #               ymin=0,
            #               ymax=7,
            #               xmin=0,
            #               xmax=1,
            #               # height=100,
            #               # hint_size_y=None,
            #               # hint_size_x=None,
            #               # width=100
            #               )
            # plot = BarPlot(color=[1, 1, 0, 1])
            # plot.points = [(0.5,y) for y in numpy.arange(0.0, mean + 0.1, 0.1).tolist()]
            # graph.add_plot(plot)

            self.pos_grid.add_widget(
                Label(text="E: " + str(g) + " W: " + str(w) + " C: " + str(c) + " S: " + str(c), size_hint_y=None,
                      height=20))

            # self.pos_grid.add_widget(graph)

            self.pos_grid.add_widget(
                Label(text="Mean: " + str(round(mean, 2)) + " Std dev: " + str(round(std_dev, 2)) + " No: " + str(no),
                      size_hint_y=None,
                      height=20))

        abc_data = Statistics.map_to_mean_and_std_dev(Statistics.separate_abc_runs(abc))
        abc_data = sorted(abc_data.items(), key=lambda x: x[1][0])
        for item in abc_data:
            g, l = item[0]
            mean, std_dev, no = item[1]
            self.abc_grid.add_widget(
                Label(text="E: " + str(g) + " L: " + str(l), size_hint_y=None, height=20))
            self.abc_grid.add_widget(
                Label(text="Mean: " + str(round(mean, 2)) + " Std dev: " + str(round(std_dev, 2)) + " No: " + str(no),
                      size_hint_y=None, height=20))

        rand_data = Statistics.map_to_mean_and_std_dev(Statistics.separate_random_runs(rand))
        rand_data = sorted(rand_data.items(), key=lambda x: x[1][0])
        for item in rand_data:
            g = item[0]
            mean, std_dev, no = item[1]
            self.rand_grid.add_widget(
                Label(text="E: " + str(g), size_hint_y=None, height=20))
            self.rand_grid.add_widget(
                Label(text="Mean: " + str(round(mean, 2)) + " Std dev: " + str(round(std_dev, 2)) + " No: " + str(no),
                      size_hint_y=None, height=20))
