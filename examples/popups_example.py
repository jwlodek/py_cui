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

        # This is a reference to our top level CUI object
        self.master = master

        # buttons that will open each type of popup
        self.show_message_popup         = self.master.add_button('Show Message Popup',      0, 0, command=self.show_message)
        self.show_yes_no_popup          = self.master.add_button('Show Yes No Popup',       1, 0, command=self.show_yes_no)
        self.show_loading_icon_popup    = self.master.add_button('Show Loading Icon Popup', 2, 0, command=self.show_loading_icon)
        self.show_loading_bar_popup     = self.master.add_button('Show Loading Bar Popup',  0, 1, command=self.show_loading_bar)
        self.show_text_box_popup        = self.master.add_button('Show Text Box Popup',     1, 1, command=self.show_text_box)
        self.show_menu_popup            = self.master.add_button('Show Scroll Menu Popup',  2, 1, command=self.show_menu_popup_fun)

    # -------------------------------------------------------------------------------
    # First, the most simple popup, the message popup.
    # This will simply display a message, and is closed with enter, escape or space. 
    # -------------------------------------------------------------------------------

    def show_message(self):
        """ Displays a simple message popup """

        self.master.show_message_popup('Hello!', 'This is a message popup. You can also spawn warnings and errors.')
        # Below is the syntax for warning and error popups. Feel free to experiment with these
        #self.master.show_warning_popup('Warning!', 'This is a warning popup. You can also spawn messages and errors.')
        #self.master.show_error_popup('Error!', 'This is an error popup. You can also spawn warnings and messages.')


    # -------------------------------------------------------------------------------
    # Next, we take a look at the yes-no popup. It is spawned in a similar way to the message popup,
    # but its second argument is a function that takes a single boolean parameter.
    # If the user selects 'y' the funtion is run with True, otherwise with False
    # -------------------------------------------------------------------------------

    def show_yes_no(self):
        """ Displays a yes no popup asking if the user would like to quit """

        # For the yes/no popup, the 'command' parameter must take a function that requires a single boolean parameter
        self.master.show_yes_no_popup('Are you sure you want to quit?', self.quit_cui)


    def quit_cui(self, to_quit):
        # THis is the function given to the yes no popup. The to_quit parameter will be True if y is pressed, or False if n is pressed
        if to_quit:
            exit()
        else:
            self.master.show_message_popup('Cancelled', 'The quit operation was cancelled.')


    # -------------------------------------------------------------------------------
    # Next, the textbox popup. This works similar to the yes-no popup, but passes the 
    # entered string into the callback function
    # -------------------------------------------------------------------------------

    def show_text_box(self):
        # Here, reset title is a function that takes a string parameter, which will be the user entered string
        self.master.show_text_box_popup('Please enter a new window title', self.reset_title)

    def reset_title(self, new_title):
        self.master.title = new_title


    # -------------------------------------------------------------------------------
    # The menu popup requires a list of strings, which will serve as menu items.
    # The callback function must take a single string parameter, same as the text box,
    # and this will simply be the selected menu item
    # -------------------------------------------------------------------------------

    def show_menu_popup_fun(self):
        # List of menu items
        menu_choices = ['RED', 'CYAN', 'MAGENTA']
        # Change button color function takes string, and depending on menu choices performs specific action
        self.master.show_menu_popup('Please select a new button color', menu_choices, self.change_button_color)

    def change_button_color(self, new_color):

        # Note how this menu callback function essentially "switches" on possible menu items
        color = py_cui.WHITE_ON_BLACK
        if new_color == "RED":
            color = py_cui.RED_ON_BLACK
        elif new_color == "CYAN":
            color = py_cui.CYAN_ON_BLACK
        elif new_color == "MAGENTA":
            color = py_cui.MAGENTA_ON_BLACK
        for key in self.master.widgets.keys():
            if isinstance(self.master.widgets[key], py_cui.widgets.Button):
                self.master.widgets[key].color = color


    # -------------------------------------------------------------------------------
    # Finally, for loading popups, you are required to use some form of async/threading
    # Start the loading popup, and then the thread to perform the long operation in the same function.
    # Then, in your long operation function, at the end, close the loading popup. In the case of the loading bar
    # you can also increment the loading bar in the long operation.
    # -------------------------------------------------------------------------------

    def show_loading_icon(self):
        """ Function that shows the usage for spwaning a loading icon popup """

        # The loading popup will remain onscreen until the stop loading function is called. Call this before a large operation, and call
        # stop after the operation is finished. Note that for these long operations, you must use a different thread
        # to not block the draw calls.
        self.master.show_loading_icon_popup('Please Wait', 'Loading')
        operation_thread = threading.Thread(target=self.long_operation)
        operation_thread.start()

    def show_loading_bar(self):
        """ Function that shows the usage for spawning a loading bar popup """

        self.master.show_loading_bar_popup('Incrementing a counter...', 100)
        operation_thread = threading.Thread(target=self.long_operation)
        operation_thread.start()

    def long_operation(self):
        """ A simple function that demonstrates a long callback operation performed while loading popup is open """

        counter = 0
        for i in range(0, 100):
            time.sleep(0.1)
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
