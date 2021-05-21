# Writing a py_cui, Step by Step

Once you have installed `py_cui`, you can continue on to create an application.

On this page, we will create a simple `py_cui` program, step by step. We will create something similar to the todo list example that can be seen in the [`examples`](https://github.com/jwlodek/py_cui/blob/master/examples/simple_todo_list.py) directory in the repository.

To get started, you can either use the `py_cui_cookiecutter` template, or start the project from scratch.

**Step 0 - Full Project Setup (Optional)**

If you are developing a mid to large scale project that is meant to be distributed via PyPi, you may want to use the available `cookiecutter` template to generate some boilerplate setup code for you. First, install the `cookiecutter` tool:

```
pip install cookiecutter
```

Once it is installed, navigate to the directory in which you would like your projects to live, and run:

```
cookiecutter https://github.com/jwlodek/py_cui_cookiecutter
```

This will clone the template, and ask several questions about your application, including project name and description, as well as some developer information. It will then create a basic `py_cui` style project with some pre-done functionality like a working `setup.py` file etc.

The entrypoint for the created program will be in `myproject/__init__.py`, in the `main` method.

To run the interface created with `cookiecutter`, enter your project's top-level directory, install with `pip` (you may want to set up a virtual environment first), and use the project's name to run the program. If you do this without making any changes to the template, you should be able to see a `Hello World` example:

```
cd myproject
pip install .
myproject
```

You are now ready to extend this template for your own application!

Alternatively, of course, you may always create your project structure from scratch, depending on your needs. 


**Step 1 - Create PyCUI and Wrapper Class**

Once you have the project template set up, or have created your own project structure, you can start developing the application itself.

The recommended way to create `py_cui` programs is to create a wrapper class that takes the `PyCUI` object as an argument, similar to how `Tk` objects are often passed as an argument to a wrapper class.

```Python
import py_cui

class SimpleTodoList:

    # We add type annotations to our master PyCUI objects for improved intellisense
    def __init__(self, master : py_cui.PyCUI):

        self.master = master

# Create the CUI with 7 rows 6 columns, pass it to the wrapper object, and start it
root = py_cui.PyCUI(7, 6)

# If we want to use unicode box characters, we toggle them on here.
# Alternatively, you can define your own border characters using
# root.set_border_characters(...)
root.toggle_unicode_borders()
root.set_title('CUI TODO List')
s = SimpleTodoList(root)
root.start()
```

**Step 2 - Add Your Widgets**

Next, we want to add widgets to the CUI. We will add 3 scroll menus to represent our lists of TODO, In Progress, and Done, a text field for adding new items for now.
In more complex programs, you may use any object with an implemented `__str__` function to pass to a scroll menu, but in this example, we will simply input strings representing 
the different tasks in our list.

```Python
import py_cui

class SimpleTodoList:

    # We add type annotations to our master PyCUI objects for improved intellisense
    def __init__(self, master: py_cui.PyCUI):

        self.master = master

        # The scrolled list cells that will contain our tasks in each of the three categories
        self.todo_scroll_cell = self.master.add_scroll_menu('TODO', 0, 0, row_span=6, column_span=2)
        self.in_progress_scroll_cell = self.master.add_scroll_menu('In Progress', 0, 2, row_span=7, column_span=2)
        self.done_scroll_cell = self.master.add_scroll_menu('Done', 0, 4, row_span=7, column_span=2)

        # Textbox for entering new items
        self.new_todo_textbox = self.master.add_text_box('TODO Item', 6, 0, column_span=2)

# Create the CUI with 7 rows 6 columns, pass it to the wrapper object, and start it
root = py_cui.PyCUI(7, 6)
root.set_title('CUI TODO List')
s = SimpleTodoList(root)
root.start()
```

Note how we set the `row_span` and `column_span` values, so that even though the grid is 7x6, our widgets will actually be larger than any individual cell. The reason we define these sizes is becaue we wish to have the text field fill a narrow row, meaning that we must subdivide the window into many rows.

**Step 3 - Add Key Commands**

Next, add keybindings to your widgets. We want buttons that send items into the next list, and the items get removed if theyre in the "Done" list. Also, we need to make the text field send its contents into the "TODO" list.

```Python
import py_cui

class SimpleTodoList:

    # We add type annotations to our master PyCUI objects for improved intellisense
    def __init__(self, master: py_cui.PyCUI):

        self.master = master

        # The scrolled list cells that will contain our tasks in each of the three categories
        self.todo_scroll_cell = self.master.add_scroll_menu('TODO', 0, 0, row_span=6, column_span=2)
        self.in_progress_scroll_cell = self.master.add_scroll_menu('In Progress', 0, 2, row_span=7, column_span=2)
        self.done_scroll_cell = self.master.add_scroll_menu('Done',  0, 4, row_span=7, column_span=2)

        # Textbox for entering new items
        self.new_todo_textbox = self.master.add_text_box('TODO Item', 6, 0, column_span=2)

        self.new_todo_textbox.add_key_command(py_cui.keys.KEY_ENTER, self.add_item)
        self.todo_scroll_cell.add_key_command(py_cui.keys.KEY_ENTER, self.mark_as_in_progress)
        self.in_progress_scroll_cell.add_key_command(py_cui.keys.KEY_ENTER, self.mark_as_done)
        self.done_scroll_cell.add_key_command(py_cui.keys.KEY_ENTER, self.remove_item)

    def add_item(self):
        """ Add a todo item """

        self.todo_scroll_cell.add_item(f'{self.new_todo_textbox.get()}')
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

Note that in the `mark_as_in_progress` and `mark_as_done` functions spawn an error popup if the lists are empty.

**Step 4 - You're done!**

That's it! our simple example is complete, and you can test it with:

```
python3 simple_todo.py
```

if you created your own file, or with:

```
cd myproject
pip install --upgrade .
myproject
```

if you used the `cookiecutter` project template.

Feel free to play around with this CUI, and note how the keybindings we assigned perform the tasks we wanted them to.

### Advanced Features

There are several features supported by `py_cui` that allow for more complex interfaces to be created. Below is a quick rundown of some of these, and how to implement them in you application. If there is something not listed 

**Live Updates to Widgets**

By default, `py_cui` only refreshes the screen when an event is registered, like a key or mouse press. If you would like to change this behavior, you simply must set the screen refresh timeout (in seconds) with:

```Python
root.set_refresh_timeout(1)
```

Note that that this will simply have the UI refresh every set number of seconds, and processing any updates to widgets must be performed in a parallel thread outside of the main draw/IO thread.

**Multiple "Windows"**

If your UI requires multiple UI screens, you should not creat multiple `PyCUI` instances, but rather by using multiple `WidgetSet` objects. You should use the original root instance to create the widget sets, and then apply the one you would like to currently display. For a basic example of this principle, see below:

```Python
import py_cui

class MultiWindowDemo:

    def __init__(self, root: py_cui.PyCUI):

        # Root PyCUI window
        self.root = root

        # Collect current CUI configuration as a widget set object
        self.widget_set_A = self.root.create_new_widget_set(3,3)

        # Add a button the the CUI
        self.widget_set_A.add_button('Open 2nd Window', 1, 1, command = self.open_set_B)

        # apply the initial widget set
        self.root.apply_widget_set(self.widget_set_A)

        # Create a second widget set (window). This one will have a 5x5 grid, not 3x3 like the original CUI
        self.widget_set_B = self.root.create_new_widget_set(5, 5)

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
```

In addition, it may be worthwhile to create additional wrapper classes for the individual screens in order to better separate the logic for each. An example of this approach would be the [`ScreenManager`](https://github.com/jwlodek/pyautogit/blob/master/pyautogit/screen_manager.py) and various [sub-classes](https://github.com/jwlodek/pyautogit/blob/master/pyautogit/settings_screen.py) for `pyautogit`.
