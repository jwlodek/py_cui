"""
File containing class that abstracts a collection of widgets. It can be used to swap between collections
of widgets in a py_cui

@Author: Jakub Wlodek
@Created 05-Oct-2019
"""

import shutil
import py_cui.widgets as widgets
import py_cui.grid as grid

class WidgetSet:

    def __init__(self, num_rows, num_cols):
        self.widgets = {}
        self.keybindings = {}
        self.num_rows = num_rows
        self.num_cols = num_cols
        term_size = shutil.get_terminal_size()

        self.height = term_size.lines
        self.width = term_size.columns
        self.height = self.height - 4
        self.grid = grid.Grid(num_rows, num_cols, self.height, self.width)
        self.selected_widget = None

    def set_selected_widget(self, widget_id):
        """
        Function that sets the selected cell for the CUI

        Parameters
        ----------
        cell_title : str
            the title of the cell
        """

        if widget_id in self.widgets.keys():
            self.selected_widget = widget_id


    def add_key_command(self, key, command):
        """ Function that adds a keybinding to the CUI when in overview mode """

        self.keybindings[key] = command


    def add_scroll_menu(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0):

        id = 'Widget{}'.format(len(self.widgets.keys()))
        new_scroll_menu = widgets.ScrollMenu(id, title, self.grid, row, column, row_span, column_span, padx, pady)
        self.widgets[id] = new_scroll_menu
        if self.selected_widget is None:
            self.set_selected_widget(id)
        return new_scroll_menu


    def add_checkbox_menu(self, title, row, column, row_span=1, column_span=1, padx=1, pady=0, checked_char='X'):
        """ Function that adds a new checkbox menu to the CUI grid """

        id = 'Widget{}'.format(len(self.widgets.keys()))
        new_checkbox_menu = widgets.CheckBoxMenu(id, title, self.grid, row, column, row_span, column_span, padx, pady, checked_char)
        self.widgets[id] = new_checkbox_menu
        if self.selected_widget is None:
            self.set_selected_widget(id)
        return new_checkbox_menu


    def add_text_box(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, initial_text = ''):
        """ Function that adds a new text box to the CUI grid """

        id = 'Widget{}'.format(len(self.widgets.keys()))
        new_text_box = widgets.TextBox(id, title,  self.grid, row, column, row_span, column_span, padx, pady, initial_text)
        self.widgets[id] = new_text_box
        if self.selected_widget is None:
            self.set_selected_widget(id)
        return new_text_box


    def add_text_block(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, initial_text = ''):
        """ Function that adds a new text box to the CUI grid """

        id = 'Widget{}'.format(len(self.widgets.keys()))
        new_text_block = widgets.ScrollTextBlock(id, title,  self.grid, row, column, row_span, column_span, padx, pady, initial_text)
        self.widgets[id] = new_text_block
        if self.selected_widget is None:
            self.set_selected_widget(id)
        return new_text_block


    def add_label(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0):
        """ Function that adds a new label to the CUI grid """

        id = 'Widget{}'.format(len(self.widgets.keys()))
        new_label = widgets.Label(id, title, self.grid, row, column, row_span, column_span, padx, pady)
        self.widgets[id] = new_label
        return new_label


    def add_block_label(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0):
        """ Function that adds a new label to the CUI grid """

        id = 'Widget{}'.format(len(self.widgets.keys()))
        new_label = widgets.BlockLabel(id, title, self.grid, row, column, row_span, column_span, padx, pady)
        self.widgets[id] = new_label
        return new_label


    def add_button(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, command=None):
        """ Function that adds a new button to the CUI grid """

        id = 'Widget{}'.format(len(self.widgets.keys()))
        new_button = widgets.Button(id, title, self.grid, row, column, row_span, column_span, padx, pady, command)
        self.widgets[id] = new_button
        if self.selected_widget is None:
            self.set_selected_widget(id)
        return new_button

