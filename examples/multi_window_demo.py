"""
This example demonstrates how you would handle having multiple "windows" for one py_cui application.

@Author: Jakub Wlodek
@Created 05-Oct-2019
"""

import py_cui

class MultiWindowDemo:

    def __init__(self, root):

        self.root = root
        self.root.add_button('Open 2nd Window', 1, 1, command = self.open_set_B)
        self.widget_set_A = self.root.get_widget_set()
        self.widget_set_B = py_cui.widget_set.WidgetSet(5, 5)
        self.text_box_B = self.widget_set_B.add_text_box('Enter something', 0, 0, column_span=2)
        self.text_box_B.add_key_command(py_cui.keys.KEY_ENTER, self.open_set_A)


    def open_set_A(self):
        self.root.apply_widget_set(self.widget_set_A)


    def open_set_B(self):
        self.root.apply_widget_set(self.widget_set_B)


root = py_cui.PyCUI(3, 3)
wrapper = MultiWindowDemo(root)
root.start()