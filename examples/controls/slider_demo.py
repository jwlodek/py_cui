#!/usr/bin/env python3
from inspect import cleandoc
import itertools
import py_cui


class App:
    character_gen = itertools.cycle(("X", "-", "█", "[", "#"))

    def __init__(self, root_: py_cui.PyCUI):
        self.root = root_

        # Default configuration
        self.default = self.root.add_slider("Default", 0, 0, column_span=2, min_val=-50, max_val=50)

        # controls
        self.title_button = self.root.add_button("Toggle title", 1, 0, command=self.default.toggle_title)
        self.border_button = self.root.add_button("Toggle border", 1, 1, command=self.default.toggle_border)
        self.value_button = self.root.add_button("Toggle value", 1, 2, command=self.default.toggle_value)
        self.character_button = self.root.add_button("Cycle char", 2, 0, command=self.cycle_characters)
        self.align_button = self.root.add_button("Change alignment", 2, 1, command=self.cycle_height)
        self.step_slider = self.root.add_slider("Step size", 2, 2, min_val=1, init_val=2, max_val=10)
        self.spacer = self.root.add_text_block("Spacer", 0, 2)

        # setups
        self.root.set_on_draw_update_func(self.set_step)
        self.height_cycle = itertools.cycle(
            (
                self.default.align_to_top,
                self.default.align_to_middle,
                self.default.align_to_bottom,
            )
        )

        help_text = """
                    Press a button to make a change.
                    You can change character freely,
                    but for demonstration purpose,
                    I've set it to cycle it here.
                    """

        help_text = cleandoc(help_text)
        self.spacer.set_text(help_text)

    def cycle_characters(self):
        self.default.set_bar_char(next(self.character_gen))

    def cycle_height(self):
        next(self.height_cycle)()

    def set_step(self):
        self.default.set_slider_step(self.step_slider.get_slider_value())


if __name__ == '__main__':
    root = py_cui.PyCUI(3, 3)
    root.set_title("Slider playground")
    s = App(root)
    root.start()
