"""
This example demonstrates how you would handle having multiple "windows" for one py_cui application.

@Author: Jakub Wlodek
@Created 05-Oct-2019
"""

import py_cui

class MultiWindowDemo:

    def __init__(self, root):

        # Root PyCUI window
        self.root = root

        # Add a button the the CUI
        self.root.add_button('Open 2nd Window', 1, 1, command = self.open_set_B)

        # Collect current CUI configuration as a widget set object
        self.widget_set_A = self.root.get_widget_set()

        # Create a second widget set (window). This one will have a 5x5 grid, not 3x3 like the original CUI
        self.widget_set_B = py_cui.widget_set.WidgetSet(5, 5)

        # Add a text box to the second widget set
        self.text_box_B = self.widget_set_B.add_text_box('Enter something', 0, 0, column_span=2)
        self.text_box_B.add_key_command(py_cui.keys.KEY_ENTER, self.open_set_A)


    def open_set_A(self):
        # Fired on the ENTER key in the textbox. Use apply_widget_set to switch between "windows"
        self.root.apply_widget_set(self.widget_set_A)


    def open_set_B(self):
        # Fired on button press. Use apply_widget_set to switch between "windows"
        self.root.apply_widget_set(self.widget_set_B)


# Create CUI object, pass to wrapper class, and start the CUI
root = py_cui.PyCUI(3, 3)
wrapper = MultiWindowDemo(root)
root.start()