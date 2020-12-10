"""File containing class that abstracts a collection of widgets.

It can be used to swap between collections of widgets (screens) in a py_cui
"""

# Author:    Jakub Wlodek
# Created:   12-Aug-2019

# TODO: Should create an initial widget set in PyCUI class that widgets are added to by default.

import shutil
import py_cui.widgets as widgets
import py_cui.grid as grid
import py_cui.controls as controls


class WidgetSet:
    """Class that represents a collection of widgets.

    Use PyCUI.apply_widget_set() to set a given widget set for display

    Attributes
    ----------
    grid : py_cui.grid.Grid
        The main layout manager for the CUI
    widgets : dict of str - py_cui.widgets.Widget
        dict of widget in the grid
    keybindings : list of py_cui.keybinding.KeyBinding
        list of keybindings to check against in the main CUI loop
    height, width : int
        height of the terminal in characters, width of terminal in characters
    """

    def __init__(self, num_rows, num_cols, logger, simulated_terminal=None):
        """Constructor for WidgetSet
        """

        self._widgets      = {}
        self._keybindings  = {}

        self._simulated_terminal = simulated_terminal

        if self._simulated_terminal is None:
            term_size = shutil.get_terminal_size()
            height = term_size.lines
            width = term_size.columns
        else:
            height  = self._simulated_terminal[0]
            width   = self._simulated_terminal[1]

        self._height = height
        self._width = width
        self._height = self._height - 4

        self._grid = grid.Grid(num_rows, num_cols, self._height, self._width, logger)

        self._selected_widget = None
        self._logger = logger


    def set_selected_widget(self, widget_id):
        """Function that sets the selected cell for the CUI

        Parameters
        ----------
        cell_title : str
            the title of the cell
        """

        if widget_id in self._widgets.keys():
            self._selected_widget = widget_id


    def get_widgets(self):
        """Function that gets current set of widgets

        Returns
        -------
        widgets : dict of str -> widget
            dictionary mapping widget IDs to object instances
        """

        return self._widgets


    def add_key_command(self, key, command):
        """Function that adds a keybinding to the CUI when in overview mode

        Parameters
        ----------
        key : py_cui.keys.KEY_*
            The key bound to the command
        command : Function
            A no-arg or lambda function to fire on keypress
        """

        self._keybindings[key] = command


    def add_scroll_menu(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0):
        """Function that adds a new scroll menu to the CUI grid

        Parameters
        ----------
        title : str
            The title of the scroll menu
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction

        Returns
        -------
        new_scroll_menu : ScrollMenu
            A reference to the created scroll menu object.
        """

        id = 'Widget{}'.format(len(self._widgets.keys()))
        new_scroll_menu     = widgets.ScrollMenu(id,
                                                 title,
                                                 self._grid,
                                                 row,
                                                 column,
                                                 row_span,
                                                 column_span,
                                                 padx,
                                                 pady,
                                                 self._logger)
        self._widgets[id]  = new_scroll_menu
        if self._selected_widget is None:
            self.set_selected_widget(id)
        self._logger.info('Adding widget {} w/ ID {} of type {}'.format(title, id, str(type(new_scroll_menu))))
        return new_scroll_menu


    def add_checkbox_menu(self, title, row, column, row_span=1, column_span=1, padx=1, pady=0, checked_char='X'):
        """Function that adds a new checkbox menu to the CUI grid

        Parameters
        ----------
        title : str
            The title of the checkbox
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction
        checked_char='X' : char
            The character used to mark 'Checked' items

        Returns
        -------
        new_checkbox_menu : CheckBoxMenu
            A reference to the created checkbox object.
        """

        id = 'Widget{}'.format(len(self._widgets.keys()))
        new_checkbox_menu   = widgets.CheckBoxMenu(id,
                                                   title,
                                                   self._grid,
                                                   row,
                                                   column,
                                                   row_span,
                                                   column_span,
                                                   padx,
                                                   pady,
                                                   self._logger,
                                                   checked_char)
        self._widgets[id]  = new_checkbox_menu
        if self._selected_widget is None:
            self.set_selected_widget(id)
        self._logger.info('Adding widget {} w/ ID {} of type {}'.format(title, id, str(type(new_checkbox_menu))))
        return new_checkbox_menu


    def add_text_box(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, initial_text = '', password = False):
        """Function that adds a new text box to the CUI grid

        Parameters
        ----------
        title : str
            The title of the textbox
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction
        initial_text='' : str
            Initial text for the textbox
        password=False : bool
            Toggle to show '*' instead of characters.

        Returns
        -------
        new_text_box : TextBox
            A reference to the created textbox object.
        """

        id = 'Widget{}'.format(len(self._widgets.keys()))
        new_text_box        = widgets.TextBox(id,
                                              title,
                                              self._grid,
                                              row, column,
                                              row_span,
                                              column_span,
                                              padx, pady,
                                              self._logger,
                                              initial_text,
                                              password)
        self._widgets[id]    = new_text_box
        if self._selected_widget is None:
            self.set_selected_widget(id)
        self._logger.info('Adding widget {} w/ ID {} of type {}'.format(title, id, str(type(new_text_box))))
        return new_text_box


    def add_text_block(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, initial_text = ''):
        """Function that adds a new text block to the CUI grid

        Parameters
        ----------
        title : str
            The title of the text block
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction
        initial_text='' : str
            Initial text for the text block

        Returns
        -------
        new_text_block : ScrollTextBlock
            A reference to the created textblock object.
        """

        id = 'Widget{}'.format(len(self._widgets.keys()))
        new_text_block      = widgets.ScrollTextBlock(id,
                                                      title,
                                                      self._grid,
                                                      row,
                                                      column,
                                                      row_span,
                                                      column_span,
                                                      padx,
                                                      pady,
                                                      self._logger,
                                                      initial_text)
        self._widgets[id]  = new_text_block
        if self._selected_widget is None:
            self.set_selected_widget(id)
        self._logger.info('Adding widget {} w/ ID {} of type {}'.format(title, id, str(type(new_text_block))))
        return new_text_block


    def add_label(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0):
        """Function that adds a new label to the CUI grid

        Parameters
        ----------
        title : str
            The title of the label
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction

        Returns
        -------
        new_label : Label
            A reference to the created label object.
        """

        id = 'Widget{}'.format(len(self._widgets.keys()))
        new_label           = widgets.Label(id,
                                            title,
                                            self._grid,
                                            row,
                                            column,
                                            row_span,
                                            column_span,
                                            padx,
                                            pady,
                                            self._logger)
        self._widgets[id]  = new_label
        self._logger.info('Adding widget {} w/ ID {} of type {}'.format(title, id, str(type(new_label))))
        return new_label


    def add_block_label(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, center=True):
        """Function that adds a new block label to the CUI grid

        Parameters
        ----------
        title : str
            The title of the block label
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction
        center : bool
            flag to tell label to be centered or left-aligned.

        Returns
        -------
        new_label : BlockLabel
            A reference to the created block label object.
        """

        id = 'Widget{}'.format(len(self._widgets.keys()))
        new_label           = widgets.BlockLabel(id,
                                                 title,
                                                 self._grid,
                                                 row,
                                                 column,
                                                 row_span,
                                                 column_span,
                                                 padx,
                                                 pady,
                                                 center,
                                                 self._logger)
        self._widgets[id]  = new_label
        self._logger.info('Adding widget {} w/ ID {} of type {}'.format(title, id, str(type(new_label))))
        return new_label


    def add_button(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, command=None):
        """Function that adds a new button to the CUI grid

        Parameters
        ----------
        title : str
            The title of the button
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction
        command=None : Function
            A no-argument or lambda function to fire on button press.

        Returns
        -------
        new_button : Button
            A reference to the created button object.
        """

        id = 'Widget{}'.format(len(self._widgets.keys()))
        new_button          = widgets.Button(id,
                                             title,
                                             self._grid,
                                             row,
                                             column,
                                             row_span,
                                             column_span,
                                             padx,
                                             pady,
                                             self._logger,
                                             command)
        self._widgets[id]  = new_button
        if self._selected_widget is None:
            self.set_selected_widget(id)
        self._logger.info('Adding widget {} w/ ID {} of type {}'.format(title, id, str(type(new_button))))
        return new_button


    def add_slider(self, title, row, column, row_span=1,
                   column_span=1, padx=1, pady=0,
                   min_val=0, max_val=100, step=1, init_val=0):
        """Function that adds a new label to the CUI grid

        Parameters
        ----------
        title : str
            The title of the label
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction
        min_val = 0 int
            min value of the slider
        max_val = 0 int
            max value of the slider
        step = 0 int
            step to incremento or decrement
        init_val = 0 int
            initial value of the slider


        Returns
        -------
        new_slider : Slider
            A reference to the created slider object.
        """

        id = 'Widget{}'.format(len(self._widgets.keys()))
        new_slider = controls.slider.SliderWidget(id,
                                                  title,
                                                  self._grid,
                                                  row,
                                                  column,
                                                  row_span,
                                                  column_span,
                                                  padx,
                                                  pady,
                                                  self._logger,
                                                  min_val,
                                                  max_val,
                                                  step,
                                                  init_val)
        self._widgets[id] = new_slider
        self._logger.info('Adding widget {} w/ ID {} of type {}'
                           .format(title, id, str(type(new_slider))))
        return new_slider
