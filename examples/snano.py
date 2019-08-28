"""
Example of using py_cui to create a simple text editor for editing All files in directory at once.

"Super Nano"

@author:    Jakub Wlodek
@created:   27-Aug-2019
"""

import py_cui
import os
import argparse


__version__ = '0.0.1'


class SuperNano:

    def __init__(self, root, dir):
        self.root = root
        self.dir = dir
        self.file_menu = self.root.add_scroll_menu('Directory Files', 0, 0, row_span=4, column_span=2)
        self.new_dir_box = self.root.add_text_box('Current Directory', 6, 0, column_span=2)
        self.new_dir_box.set_text(self.dir)
        self.open_new_directory()

        self.file_menu.add_key_command(py_cui.keys.KEY_ENTER, self.open_file_dir)

        self.save_button = self.root.add_button('Save', 4, 0, command=self.save_opened_file)
        self.delete_button = self.root.add_button('Delete', 4, 1, command=self.delete_selected_file)
        self.new_file_textbox = self.root.add_text_box('Add New File', 5, 0, column_span=2)


        self.edit_text_block = self.root.add_text_block('Open file', 0, 2, row_span=7, column_span=6)
        self.new_dir_box.add_key_command(py_cui.keys.KEY_ENTER, self.open_new_directory)
        self.new_file_textbox.add_key_command(py_cui.keys.KEY_ENTER, self.add_new_file)

    def open_new_directory(self):
        target = self.new_dir_box.get()
        if len(target) == 0:
            target = '.'
        elif not os.path.exists(target):
            self.root.show_error_popup('Does not exist', 'ERROR - {} path does not exist'.format(target))
            return
        elif not os.path.isdir(target):
            self.root.show_error_popup('Not a Dir', 'ERROR - {} is not a directory'.format(target))
            return
        target = os.path.abspath(target)
        self.new_dir_box.set_text(target)
        self.dir = target

        files = []
        files.append('<DIR> ..')
        dir_contents = os.listdir(self.dir)
        for elem in dir_contents:
            if os.path.isfile(os.path.join(self.dir, elem)):
                files.append(elem)
            else:
                files.append('<DIR> ' + elem)

        self.file_menu.clear()
        self.file_menu.add_item_list(files)
        

    def add_new_file(self):
        self.file_menu.add_item(self.new_file_textbox.get())
        self.file_menu.selected_item = len(self.file_menu.get_item_list()) - 1
        self.root.set_selected_widget(self.edit_text_block.id)
        self.edit_text_block.title = self.new_file_textbox.get()
        self.edit_text_block.clear()
        self.new_file_textbox.clear()

    def open_file_dir(self):
        filename = self.file_menu.get()
        if filename.startswith('<DIR>'):
            self.new_dir_box.set_text(os.path.join(self.dir, filename[6:]))
            self.open_new_directory()
        else:
            try:
                fp = open(os.path.join(self.dir, filename), 'r')
                text = fp.read()
                fp.close()
                self.edit_text_block.set_text(text)
                self.edit_text_block.title = filename
            except:
                self.root.show_warning_popup('Not a text file', 'The selected file could not be opened - not a text file')


    def save_opened_file(self):
        if self.edit_text_block.title != 'Open file':
            fp = open(os.path.join(self.dir, self.edit_text_block.title), 'w')
            fp.write(self.edit_text_block.get())
            fp.close()
            self.root.show_message_popup('Saved', 'Your file has been saved as {}'.format(self.edit_text_block.title))
        else:
            self.root.show_error_popup('No File Opened', 'Please open a file before saving it.')


    def delete_selected_file(self):
        if self.edit_text_block.title != 'Open file':
            try:
                os.remove(os.path.join(self.dir, self.edit_text_block.title))
                self.edit_text_block.clear()
                self.edit_text_block.title = 'Open file'
                self.file_menu.remove_selected_item()
            except OSError:
                self.root.show_error_popup('OS Error', 'Operation could not be completed due to an OS error.')
        else:
            self.root.show_error_popup('No File Opened', 'Please open a file before saving it.')


def parse_args():
    parser = argparse.ArgumentParser(description='An extension on nano for editing directories in CLI.')
    parser.add_argument('directory', help='Target directory to edit.')
    args = vars(parser.parse_args())
    if 'directory' not in args.keys():
        return '.' 
    elif not os.path.exists(args['directory']):
        print('ERROR - {} path does not exist'.format(args['directory']))
        exit()
    elif not os.path.isdir(args['directory']):
        print('ERROR - {} is not a directory'.format(args['directory']))
        exit()
    return args['directory']


dir = parse_args()
root = py_cui.PyCUI(7, 8)
root.set_title('Super Nano v{}'.format(__version__))
frame = SuperNano(root, dir)
root.start()
