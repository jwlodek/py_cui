import py_cui
import os

class SimpleTodoList:

    def __init__(self, master):

        self.master = master
        self.todo_scroll_cell = self.master.add_scroll_cell('Scroll1', 'TODO', 0, 0, row_span=5, column_span=2)
        self.new_todo_textbox = self.master.add_text_box('Text1', 'TODO Item', 5, 0, column_span=2)



        self.in_progress_scroll_cell = self.master.add_scroll_cell('Scroll2', 'In Progress', 0, 2, row_span=7, column_span=2)

        self.done_scroll_cell = self.master.add_scroll_cell('Scroll3', 'Done', 0, 4, row_span=7, column_span=2)

        self.mark_in_progress = self.master.add_button('Button3', 'Mark in Progress', 7, 0, column_span=2, command=self.mark_as_in_progress)
        self.mark_in_progress = self.master.add_button('Button4', 'Mark As Done', 7, 2, column_span=2, command=self.mark_as_done)
        self.remove_todo = self.master.add_button('Button2', 'Remove TODO Item', 6, 1, pady = 1, command=self.remove_item)
        self.new_todo_add = self.master.add_button('Button1', 'Add TODO Item', 6, 0, command=self.add_item, pady =1)
        self.save_todo_button = self.master.add_button('Button5', 'Save', 7, 4, column_span=2, command=self.save_todo_file)

        self.new_todo_textbox.add_key_command('\n', self.push_and_reset)
        self.todo_scroll_cell.add_key_command('\n', self.mark_as_in_progress)
        self.in_progress_scroll_cell.add_key_command('\n', self.mark_as_done)
        self.read_todo_file()


    def push_and_reset(self):
        self.add_item()
        self.new_todo_textbox.clear()


    def read_todo_file(self):
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

        self.todo_scroll_cell.add_item('{}'.format(self.new_todo_textbox.get()))

    def remove_item(self):
        self.todo_scroll_cell.remove_selected_item()

    def mark_as_in_progress(self):
        in_prog = self.todo_scroll_cell.get()
        if in_prog is None:
            self.master.show_error_popup('No Item', 'There is no item in the list to mark as in progress')
            return
        self.todo_scroll_cell.remove_selected_item()
        self.in_progress_scroll_cell.add_item(in_prog)

    def mark_as_done(self):
        done = self.in_progress_scroll_cell.get()
        if done is None:
            self.master.show_error_popup('No Item', 'There is no item in the list to mark as in done')
            return
        self.in_progress_scroll_cell.remove_selected_item()
        self.done_scroll_cell.add_item(done)


    def save_todo_file(self):
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


root = py_cui.PyCUI(9, 7)
s = SimpleTodoList(root)
root.start()