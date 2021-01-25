#!/usr/bin/env python3

import py_cui


class App:
    def __init__(self, root_: py_cui.PyCUI):
        self.root = root_

        # Default configuration
        self.default = self.root.add_slider("Default", 0, 0, init_val=15)

        # Borderless titled
        self.named_borderless_slider = self.root.add_slider("Fancy Name", 1, 0, init_val=100)
        self.named_borderless_slider.title_enabled = True

        # Bordered
        self.nameless_bordered_slider = self.root.add_slider("Fancy Frame", 2, 0, init_val=0)
        self.nameless_bordered_slider.border_enabled = True

        # Bordered titled
        self.named_bordered_slider = self.root.add_slider("Even fancier Frame", 3, 0, init_val=25)
        self.named_bordered_slider.border_enabled = True
        self.named_bordered_slider.title_enabled = True

        # Value display disabled, enabled title or set initial value to find out where it is.
        self.clean_slider = self.root.add_slider("Minimalistic", 4, 0, init_val=30)
        self.clean_slider.title_enabled = True
        self.clean_slider.display_value = False

        # changing step size
        self.default.set_slider_step(3)


root = py_cui.PyCUI(5, 2)
root.set_title('Test Slider')
s = App(root)
root.start()
