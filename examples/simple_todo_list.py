"""
Example of using py_cui to create a simple Command line TODO list in under 150 lines of code

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""

import py_cui
import os

class SimpleTodoList:

    def __init__(self, master):

        self.master = master

        # The scrolled list cells that will contain our tasks in each of the three categories
        self.todo_scroll_cell =         self.master.add_scroll_menu('TODO',         0, 0, row_span=5, column_span=2)
        self.in_progress_scroll_cell =  self.master.add_scroll_menu('In Progress',  0, 2, row_span=7, column_span=2)
        self.done_scroll_cell =         self.master.add_scroll_menu('Done',         0, 4, row_span=7, column_span=2)

        # Textbox for entering new items
        self.new_todo_textbox = self.master.add_text_box('TODO Item', 5, 0, column_span=2)

        # buttons for rest of control
        self.mark_in_progress = self.master.add_button('Mark in Progress', 7, 0, column_span=2,    command=self.mark_as_in_progress)
        self.mark_in_progress = self.master.add_button('Mark As Done',     7, 2, column_span=2,    command=self.mark_as_done)
        self.remove_todo =      self.master.add_button('Remove TODO Item', 6, 1, pady = 1,         command=self.remove_item)
        self.new_todo_add =     self.master.add_button('Add TODO Item',    6, 0, pady =1,          command=self.add_item)
        self.save_todo_button = self.master.add_button('Save',             7, 4, column_span=2,    command=self.save_todo_file)

        # add some custom keybindings
        self.new_todo_textbox.add_key_command(          py_cui.keys.KEY_ENTER, self.push_and_reset)
        self.todo_scroll_cell.add_key_command(          py_cui.keys.KEY_ENTER, self.mark_as_in_progress)
        self.in_progress_scroll_cell.add_key_command(   py_cui.keys.KEY_ENTER, self.mark_as_done)
        self.read_todo_file()


    def push_and_reset(self):
        """ Adds item and clears textbox. called when textbox is in focus mode and enter is pressed """

        self.add_item()
        self.new_todo_textbox.clear()


    def read_todo_file(self):
        """ Read a saved todo file """

        todo = []
        in_progress = []
        done = []
        if os.path.exists('TODO.txt'):
            todo_fp = open('TODO.txt', 'r')
            state = 0
            line = todo_fp.readline()
            while line:
                line = line.strip()
                if state == 0:
                    if line == '__IN_PROGRESS__':
                        state = 1
                    elif len(line) > 1:
                        todo.append(line)
                elif state == 1:
                    if line == '__DONE__':
                        state = 2
                    elif len(line) > 1:
                        in_progress.append(line)
                elif state == 2:
                    if len(line) > 1:
                        done.append(line)
                line = todo_fp.readline()
            todo_fp.close()
        self.todo_scroll_cell.add_item_list(todo)
        self.in_progress_scroll_cell.add_item_list(in_progress)
        self.done_scroll_cell.add_item_list(done)


    def add_item(self):
        """ Add a todo item """

        self.todo_scroll_cell.add_item('{}'.format(self.new_todo_textbox.get()))


    def remove_item(self):
        """ Remove a todo item """

        self.todo_scroll_cell.remove_selected_item()


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


    def save_todo_file(self):
        """ Save the three lists in a specific format """

        if os.path.exists('TODO.txt'):
            os.remove('TODO.txt')
        todo_fp = open('TODO.txt', 'w')
        todo_items = self.todo_scroll_cell.get_item_list()
        in_progress_items = self.in_progress_scroll_cell.get_item_list()
        done_items = self.done_scroll_cell.get_item_list()
        for item in todo_items:
            todo_fp.write(item + '\n')
        todo_fp.write('__IN_PROGRESS__' + '\n')
        for item in in_progress_items:
            todo_fp.write(item + '\n')
        todo_fp.write('__DONE__' + '\n')
        for item in done_items:
            todo_fp.write(item + '\n')
        todo_fp.close()
        self.master.show_message_popup('Saved', 'Your TODO list has been saved!')


# Create the CUI, pass it to the wrapper object, and start it
root = py_cui.PyCUI(9, 7)
s = SimpleTodoList(root)
root.start()