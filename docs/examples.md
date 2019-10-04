# py_cui Examples

There are several examples of simple `py_cui` programs you can find in the `examples` directory of the github repository. In addition, a larger python module `pyautogit` was written with `py_cui`, and is available for download using `pip` or from github. In this section of the documentation we will explain the source code for some of the supplied examples in more detail.

### Hello py_cui!

As is tradition with programming, we start with our Hello World example. Here we simply create a `PyCUI` object with a grid size of 3 x 3, and we add a Label into the center grid space. This is the most basic `py_cui` you can create.

```Python
# Import the lib
import py_cui

# create the CUI object. Will have a 3 by 3 grid with indexes from 0,0 to 2,2
root = py_cui.PyCUI(3,3)

# Add a label to the center of the CUI in the 1,1 grid position
root.add_label('Hello py_cui!!!', 1, 1)

# Start/Render the CUI
root.start()
```

### Simple Todo List

A simple usage of `py_cui` for creating a terminal todo list. We use keybindings to get control of each of our lists as well as our text entry

```Python
import py_cui

class SimpleTodoList:

    def __init__(self, master):

        self.master = master

        # The scrolled list cells that will contain our tasks in each of the three categories
        self.todo_scroll_cell =         self.master.add_scroll_menu('TODO',         0, 0, row_span=6, column_span=2)
        self.in_progress_scroll_cell =  self.master.add_scroll_menu('In Progress',  0, 2, row_span=7, column_span=2)
        self.done_scroll_cell =         self.master.add_scroll_menu('Done',         0, 4, row_span=7, column_span=2)

        # Textbox for entering new items
        self.new_todo_textbox = self.master.add_text_box('TODO Item', 6, 0, column_span=2)

        # Keybindings for controlling our CUI.
        # We bind the enter key for each of the widgets
        self.new_todo_textbox.add_key_command(          py_cui.keys.KEY_ENTER, self.add_item)
        self.todo_scroll_cell.add_key_command(          py_cui.keys.KEY_ENTER, self.mark_as_in_progress)
        self.in_progress_scroll_cell.add_key_command(   py_cui.keys.KEY_ENTER, self.mark_as_done)
        self.done_scroll_cell.add_key_command(          py_cui.keys.KEY_ENTER, self.remove_item)

    def add_item(self):
        """ Add a todo item """

        self.todo_scroll_cell.add_item('{}'.format(self.new_todo_textbox.get()))
        self.new_todo_textbox.clear()

    def mark_as_in_progress(self):
        """ Mark a todo item as inprogress. Remove it from todo scroll list, add it to in progress list, or show error popup if no tasks """

        in_prog = self.todo_scroll_cell.get()
        if in_prog is None:
            self.master.show_error_popup('No Item', 'There is no item in the list to mark as in progress')
            return
        self.todo_scroll_cell.remove_selected_item()
        self.in_progress_scroll_cell.add_item(in_prog)

    def mark_as_done(self):
        """ Mark a inprogress item as done. Remove it from inprogress scroll list, add it to done list, or show error popup if no tasks """

        done = self.in_progress_scroll_cell.get()
        if done is None:
            self.master.show_error_popup('No Item', 'There is no item in the list to mark as done')
            return
        self.in_progress_scroll_cell.remove_selected_item()
        self.done_scroll_cell.add_item(done)

    def remove_item(self):
        """ Remove a todo item """

        self.done_scroll_cell.remove_selected_item()

# Create the CUI with 7 rows 6 columns, pass it to the wrapper object, and start it
root = py_cui.PyCUI(7, 6)
root.set_title('CUI TODO List')
s = SimpleTodoList(root)
root.start()
```

### Popups Example

This example will demonstrate the usage for using all supported popups.

```Python
# imports
import py_cui
import time
import os
import threading    # We will need the threading library when we want to use the loading popups

class PopupExample:

    def __init__(self, master):

        # This is a reference to our top level CUI object
        self.master = master

        # buttons for control - each simply spawns the linked popup
        self.show_message_popup = self.master.add_button('Show Message Popup', 0, 0,            command=self.show_message)
        self.show_yes_no_popup  = self.master.add_button('Show Yes No Popup',  1, 0,            command=self.show_yes_no)
        self.show_loading_icon_popup = self.master.add_button('Show Loading Icon Popup', 2, 0,  command=self.show_loading_icon)
        self.show_loading_bar_popup = self.master.add_button('Show Loading Bar Popup', 0,1,     command = self.show_loading_bar)
        self.show_text_box_popup = self.master.add_button('Show Text Box Popup', 1,1,           command = self.show_text_box)
        self.show_menu_popup = self.master.add_button('Show Scroll Menu Popup', 2,1,            command = self.show_menu_popup_fun)


    def show_message(self):
        """ Displays a simple message popup """

        self.master.show_message_popup('Hello!', 'This is a message popup. You can also spawn warnings and errors.')

    ################################################
    # YES NO POPUP

    def quit_cui(self, to_quit):
        # THis is the function given to the yes no popup. The to_quit parameter will be true if y is pressed, or False if n is pressed
        if to_quit:
            exit()
        else:
            self.master.show_message_popup('Cancelled', 'The quit operation was cancelled.')


    def show_yes_no(self):
        """ Displays a yes no popup asking if the user would like to quit """

        # For the yes/no popup, the 'command' parameter must take a function that requires a single boolean parameter
        self.master.show_yes_no_popup('Are you sure you want to quit?', self.quit_cui)

    ################################################

    ################################################
    # TEXTBOX POPUP

    def reset_title(self, new_title):
        self.master.title = new_title


    def show_text_box(self):
        """ Displays a textbox popup asking the user for a new window title """

        # A textbox popup requires a prompt and a function reference. The function must take a single string parameter that will return
        # whatever is within the text box when the ENTER key is pressed
        self.master.show_text_box_popup('Please enter a new window title', self.reset_title)

    ################################################

    ################################################
    # SCROLL MENU POPUP

    def change_button_color(self, new_color):
        """ Function called when ENTER pressed in menu popup. Takes string as parameter """

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

    def show_menu_popup_fun(self):
        """ Opens scroll menu for selecting button colors """

        # Spawning a menu popup must recieve a list of strings as menu options, and a function reference that takes a string parameter
        menu_choices = ['RED', 'CYAN', 'MAGENTA']
        self.master.show_menu_popup('Please select a new button color', menu_choices, self.change_button_color)

    ################################################

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
            # When using a bar indicator, we will increment the completed counter. Will be ignored for loading icon popup
            self.master.increment_loading_bar()
        # This is what stops the loading popup and reenters overview mode
        self.master.stop_loading_popup()


# Create the CUI, pass it to the wrapper object, and start it
root = py_cui.PyCUI(3, 2)
root.set_title('CUI Popups Example')
s = PopupExample(root)
root.start()
```

### Other examples

Other examples are available in the `examples` directory in the repository on github. For a larger example of a project using `py_cui`, see [pyautogit](https://github.com/jwlodek/pyautogit).