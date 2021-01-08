#!/usr/bin/env python3

import py_cui


class App:
    def __init__(self, master: py_cui.PyCUI):
        self.master = master

        self.g1 = self.master.add_scroll_menu('GRID1',
                                              0, 0, row_span=6, column_span=2)

        self.g4 = self.master.add_slider('slider', 6, 0, row_span=1,
                                         column_span=6, padx=1, pady=0,
                                         min_val=8, max_val=100, step=5,
                                         init_val=20)
        # update slider
        self.g4.set_slider_step(3)


root = py_cui.PyCUI(9, 6)
root.set_title('Test Slider')
s = App(root)
root.start()
