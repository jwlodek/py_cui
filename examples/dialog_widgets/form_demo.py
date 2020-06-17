import py_cui
import logging

class App:

    def __init__(self, master):

        self.form_results = None
        self.master = master
        self.master.run_on_exit(self.show_form_results)
        self.master.add_button('Open Form', 1, 1, command=self.open_form)

    def save_form_results(self, form_output):
        self.form_results = form_output

    def open_form(self):
        self.master.show_form_popup('Demo Form', ['First Name', 'Last Name', 'Email'], passwd_fields=['Last Name'], required=['Email'], callback=self.save_form_results)

    def show_form_results(self):
        print(str(self.form_results))


root = py_cui.PyCUI(3, 3)
root.enable_logging(logging_level=logging.ERROR)
root.toggle_unicode_borders()
app = App(root)
root.start()
