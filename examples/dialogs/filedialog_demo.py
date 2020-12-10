import py_cui
import logging

class App:

    def __init__(self, master):

        # The root py_cui window
        self.master = master


        # Simple button that opens filedialog popup
        self.master.add_button('Open Demo File Dialog', 1, 1, command=self.open_file_dialog)


    def open_file_dialog(self):
        """Callback for button press, opens form popup
        """

        # Here we open our file dialog. There are three valid popup_type kwargs:
        #
        # 1. openfile -> which will return the currently selected file
        # 2. opendir -> which will return the currently entered directory
        # 3. saveas -> which will return the currently entered directory joined with the specified new name
        #
        # Your assigned callback function will be called with the appropriate return value as the only argument.
        # You can also specify an initial directory with kwarg initial_dir, whether or not to use ascii icons
        # for folders and files with ascii_icons=True, and you can limit visible file extensions for saveas or 
        # openfile popup types.
        #
        # Feel free to experiment with the available dialogs by editing the below.
        self.master.show_filedialog_popup(popup_type='openfile', 
                                            callback=self.show_dialog_results, 
                                            initial_dir='.', 
                                            ascii_icons=False, 
                                            limit_extensions=[])


    def show_dialog_results(self, result):
        """Utility function that simply shows the result of the filedialog in a popup.
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
