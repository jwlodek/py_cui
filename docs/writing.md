# Writing a py_cui, step by step

On this page, we will create a simple `py_cui` program, step by step. We will create something similar to the todo list example that can be seen in the `examples` directory in the repository.

**Step 1 - Create PyCUI and wrapper class**

The recommended way to create `py_cui` programs is to create a wrapper class that takes the `PyCUI` object as an argument, similar to how `Tk` objects are often passed as an argument to a wrapper class.

```Python
import py_cui

class SimpleTodoList:

    def __init__(self, master):

        self.master = master

# Create the CUI with 7 rows 6 columns, pass it to the wrapper object, and start it
root = py_cui.PyCUI(7, 6)
root.set_title('CUI TODO List')
s = SimpleTodoList(root)
root.start()
```

**Step 2 - Add your widgets**

Next, we want to add widgets to the CUI. We will add 3 scroll menus to represent our lists of TODO, In Progress, and Done, a text field for adding new items for now.
In more complex programs, you may use any object with an implemented `__str__` function to pass to a scroll menu, but in this example, we will simply input strings representing 
the different tasks in our list.

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

# Create the CUI with 7 rows 6 columns, pass it to the wrapper object, and start it
root = py_cui.PyCUI(7, 6)
root.set_title('CUI TODO List')
s = SimpleTodoList(root)
root.start()
```
Note how we set the `row_span` and `column_span` values, so that even though the grid is 7x6, our widgets will actually be larger than that size. The reason we define these sizes is becaue we wish to have the text field fill a narrow row, meaning that we must subdivide the window into many rows.

**Step 3 - Add key commands**

Next, add keybindings to your widgets. We want buttons that send items into the next list, and the items get removed if theyre in the "Done" list. Also, we need to make the text field send its contents into the "TODO" list.

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

Note that in the `mark_as_in_progress` and `mark_as_done` functions spawn an error popup if the lists are empty.

**Step 4 - You're done!**

That's it! our simple example is complete, and you can test it with:
```
python3 simple_todo.py
```
You should see something similar to this:

Feel free to play around with this CUI, and note how the keybindings we assigned perform the tasks we wanted them to.