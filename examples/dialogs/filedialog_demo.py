import py_cui
import logging

class App:

    def __init__(self, master):


        # The root py_cui window
        self.master = master


        # Simple button that opens form popup
        self.master.add_button('Open Form', 1, 1, command=self.open_file_dialog)


    def open_file_dialog(self):
        """Callback for button press, opens form popup
        """

        # The name of the form is Demo From
        # The second argument represents individual fields. These must be unique
        # We specify password fields to be ones where characters are replaced with '*'
        # Required fields will need to be populated before submission
        # The callback function is called with a single parameter - a dict of fields -> user inputs
        self.master.show_filedialog_popup(popup_type='openfile', callback=self.show_dialog_results, limit_extensions=['.py', '.txt'])


    def show_dialog_results(self, result):
        """Helper function called on exit. Prints form results
        """

        self.master.show_message_popup('The file dialog returned:',result)


# Create the UI
root = py_cui.PyCUI(3, 3)

# Enable logging
#root.enable_logging(logging_level=logging.ERROR)

# Use unicode box characters for borders
root.toggle_unicode_borders()

# Initialize wrapper class
app = App(root)

# Start the UI
root.start()
