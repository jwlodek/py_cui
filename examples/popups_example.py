"""
A simple example of using all py_cui popup types

@author:    Jakub Wlodek
@created:   27-Sep-2019
"""

import py_cui
import time
import os
import threading

class PopupExample:

    def __init__(self, master):

        self.master = master


        # buttons for rest of control
        self.show_message_popup = self.master.add_button('Show Message Popup', 0, 0, command=self.show_message)
        self.show_yes_no_popup  = self.master.add_button('Show Yes No Popup',  1, 0, command=self.show_yes_no)
        self.show_loading_icon_popup = self.master.add_button('Show Loading Icon Popup', 2, 0, command=self.show_loading_icon)
        self.show_loading_bar_popup = self.master.add_button('Show Loading Bar Popup', 0,1, command = self.show_loading_bar)

    def show_message(self):
        self.master.show_message_popup('Hello!', 'This is a message popup. You can also spawn warnings and errors.')

    def show_yes_no(self):
        # For the yes/no popup, the 'command' parameter must take a function that requires a single boolean parameter
        self.master.show_yes_no_popup('Are you sure you want to quit?', self.quit_cui)


    def quit_cui(self, to_quit):
        # THis is the function given to the yes no popup. The to_quit parameter will be true if y is pressed, or False if n is pressed
        if to_quit:
            exit()
        else:
            self.master.show_message_popup('Cancelled', 'The quit operation was cancelled.')

    def show_loading_icon(self):
        # The loading popup will remain onscreen until the stop loading function is called. Call this before a large operation, and call
        # stop after the operation is finished. Note that for these long operations, you must use a different thread
        # to not block the draw calls.
        self.master.show_loading_icon_popup('Please Wait', 'Loading')
        operation_thread = threading.Thread(target=self.long_operation)
        operation_thread.start()
    
    def show_loading_bar(self):
        self.master.show_loading_bar_popup('Incrementing a counter...', 20)
        operation_thread = threading.Thread(target=self.long_operation)
        operation_thread.start()


    def long_operation(self):
        counter = 0
        for i in range(0, 20):
            time.sleep(0.3)
            counter= counter +1
            self.master.status_bar.set_text(str(counter))
            # When using a bar indicator, we will increment the completed counter
            self.master.increment_loading_bar()
        self.master.stop_loading_popup()


# Create the CUI, pass it to the wrapper object, and start it
root = py_cui.PyCUI(3, 3)
root.set_title('CUI Popups Example')
s = PopupExample(root)
root.start()