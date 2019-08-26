import py_cui
import os


__version__ = '0.0.1'


class SuperNano:

    def __init__(self, root):
        self.root = root
        self.file_menu = self.root.add_scroll_menu('Directory Files', 0, 0, row_span=5, column_span=2)
        files = []
        dir_contents = os.listdir('.')
        for elem in dir_contents:
            if os.path.isfile(elem):
                files.append(elem)

        self.file_menu.add_item_list(files)
        self.file_menu.add_key_command(py_cui.keys.KEY_ENTER, self.open_file)

        self.save_button = self.root.add_button('Save', 6, 0, command=self.save_opened_file)
        self.delete_button = self.root.add_button('Delete', 6, 1, command=self.delete_selected_file)
        self.new_file_textbox = self.root.add_text_box('Add New File', 5, 0, column_span=2)

        self.edit_text_block = self.root.add_text_block('Open file', 0, 2, row_span=7, column_span=6)
        self.new_file_textbox.add_key_command(py_cui.keys.KEY_ENTER, self.add_new_file)


    def add_new_file(self):
        self.file_menu.add_item(self.new_file_textbox.get())
        self.file_menu.selected_item = len(self.file_menu.get_item_list()) - 1
        self.root.set_selected_widget(self.edit_text_block.id)
        self.edit_text_block.title = self.new_file_textbox.get()
        self.new_file_textbox.clear()

    def open_file(self):
        filename = self.file_menu.get()
        fp = open(filename, 'r')
        text = fp.read()
        fp.close()
        self.edit_text_block.set_text(text)
        self.edit_text_block.title = filename


    def save_opened_file(self):
        if self.edit_text_block.title != 'Open file':
            fp = open(self.edit_text_block.title, 'w')
            fp.write(self.edit_text_block.get())
            fp.close()
            self.root.show_message_popup('Saved', 'Your file has been saved as {}'.format(self.edit_text_block.title))
        else:
            self.root.show_error_popup('No File Opened', 'Please open a file before saving it.')


    def delete_selected_file(self):
        if self.edit_text_block.title != 'Open file':
            self.os.remove(edit_text_block.title)
            self.edit_text_block.set_text('')
            self.edit_text_block.title = 'Open file'
            file_menu.remove_selected_item()
        else:
            self.root.show_error_popup('No File Opened', 'Please open a file before saving it.')



root = py_cui.PyCUI(7, 8)
root.set_title('Super Nano v{}'.format(__version__))
frame = SuperNano(root)
root.start()
