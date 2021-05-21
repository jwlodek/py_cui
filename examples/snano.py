"""
Example of using py_cui to create a simple text editor for editing All files in directory at once.

"Super Nano"

@author:    Jakub Wlodek
@created:   27-Aug-2019
"""

import py_cui
import os
import argparse
import py_cui.colors

__version__ = "0.0.1"


class SuperNano:
    def __init__(self, root: py_cui.PyCUI, dir):

        # Wrapper class takes its parent PyCUI object
        self.root = root

        # Currently opened directory
        self.dir = dir

        # If we press 's' we want to save the opened file
        self.root.add_key_command(py_cui.keys.KEY_S_LOWER, self.save_opened_file)

        # Add a file selection menu
        self.file_menu = self.root.add_scroll_menu("Directory Files", 0, 0, row_span=5, column_span=2)

        # With ENTER key press, we open the selected file or directory, DELETE will delete the selected file or directory
        # See the callback functions for how these operations are performed
        self.file_menu.add_key_command(py_cui.keys.KEY_ENTER, self.open_file_dir)
        self.file_menu.add_key_command(py_cui.keys.KEY_DELETE, self.delete_selected_file)

        # To better distingusish directories, add a color rule that is used to color directory names green
        # First parameter is a regex, second is color, third is how the rule should check the regex against the line.
        # A region match type means to color only the specified region.
        self.file_menu.add_text_color_rule(
            "<DIR>", py_cui.GREEN_ON_BLACK, "startswith", match_type="region", region=[5, 1000]
        )

        # Add a textbox for listing the current directory, set initial text to current directory
        self.current_dir_box = self.root.add_text_box("Current Directory", 6, 0, column_span=2)
        self.current_dir_box.set_text(self.dir)

        # You can manually enter directory path, and ENTER will try to open it
        self.current_dir_box.add_key_command(py_cui.keys.KEY_ENTER, self.open_new_directory)

        # Function that opens initial directory
        self.open_new_directory()

        # Add main text block for edition text.
        self.edit_text_block = self.root.add_text_block("Open file", 0, 2, row_span=7, column_span=6)

        # Add a textbox for adding new files on ENTER key
        self.new_file_textbox = self.root.add_text_box("Add New File", 5, 0, column_span=2)
        self.new_file_textbox.add_key_command(py_cui.keys.KEY_ENTER, self.add_new_file)

    def open_new_directory(self):

        # Get the text in the current directory textbox, check if it exists
        target = self.current_dir_box.get()
        if len(target) == 0:
            target = "."
        elif not os.path.exists(target):
            self.root.show_error_popup("Does not exist", f"ERROR - {target} path does not exist")
            return
        elif not os.path.isdir(target):
            self.root.show_error_popup("Not a Dir", f"ERROR - {target} is not a directory")
            return
        target = os.path.abspath(target)
        self.current_dir_box.set_text(target)
        self.dir = target

        # If it does exist, list contents, and create list of files/dirs for file menu
        files = []
        files.append("<DIR> ..")
        dir_contents = os.listdir(self.dir)
        for elem in dir_contents:
            if os.path.isfile(os.path.join(self.dir, elem)):
                files.append(elem)
            else:
                files.append("<DIR> " + elem)

        self.file_menu.clear()
        self.file_menu.add_item_list(files)

    def add_new_file(self):

        # Add item to file menu, and refresh. File not saved to disk until 's' pressed.
        self.file_menu.add_item(self.new_file_textbox.get())
        self.file_menu.selected_item = len(self.file_menu.get_item_list()) - 1
        self.new_file_textbox.set_selected(False)
        self.root.set_selected_widget(self.edit_text_block.get_id())
        self.edit_text_block.title = self.new_file_textbox.get()
        self.edit_text_block.clear()
        self.new_file_textbox.clear()

    def open_file_dir(self):
        # Open file or directory by checking selected item in file menu.
        filename = self.file_menu.get()
        if filename.startswith("<DIR>"):
            # if directory, set the current dir box to selected one, and refresh
            self.current_dir_box.set_text(os.path.join(self.dir, filename[6:]))
            self.open_new_directory()
        else:
            try:
                # Otherwise, if it is a file, put it in the text block
                self.edit_text_block.text_color_rules = []
                fp = open(os.path.join(self.dir, filename), "r")
                text = fp.read()
                fp.close()
                self.edit_text_block.set_text(text)
                self.edit_text_block.set_title(filename)
            except:
                # if we get an error, it wasn't a text file, so show warning poup
                self.root.show_warning_popup(
                    "Not a text file", "The selected file could not be opened - not a text file"
                )

    def save_opened_file(self):
        # If we have an opened file, save it to the disk
        if self.edit_text_block.get_title() != "Open file":
            fp = open(os.path.join(self.dir, self.edit_text_block.get_title()), "w")
            fp.write(self.edit_text_block.get())
            fp.close()
            self.root.show_message_popup("Saved", f"Your file has been saved as {self.edit_text_block.get_title()}")
        else:
            self.root.show_error_popup("No File Opened", "Please open a file before saving it.")

    def delete_selected_file(self):
        # If we have an opened file, delete it from the disk
        if self.edit_text_block.get_title() != "Open file":
            try:
                os.remove(os.path.join(self.dir, self.edit_text_block.get_title()))
                self.edit_text_block.clear()
                self.edit_text_block.set_title("Open file")
                self.file_menu.remove_selected_item()
            except OSError:
                self.root.show_error_popup("OS Error", "Operation could not be completed due to an OS error.")
        else:
            self.root.show_error_popup("No File Opened", "Please open a file before deleting it.")


def parse_args():

    # Parse some basic arguments (requires target directory)
    parser = argparse.ArgumentParser(description="An extension on nano for editing directories in CLI.")
    parser.add_argument("directory", help="Target directory to edit.")
    args = vars(parser.parse_args())
    if "directory" not in args.keys():
        return "."
    elif not os.path.exists(args["directory"]):
        print(f"ERROR - {args['directory']} path does not exist")
        exit()
    elif not os.path.isdir(args["directory"]):
        print(f"ERROR - {args['directory']} is not a directory")
        exit()
    return args["directory"]


# Collect some argument information
dir = parse_args()

# Initialize the PyCUI object, and set the title
root = py_cui.PyCUI(7, 8)
root.set_title(f"Super Nano v{__version__}")

# Create the wrapper instance object.
frame = SuperNano(root, dir)

# Start the CUI
root.start()
