"""A python library for intuitively creating CUI/TUI interfaces with pre-built widgets.
"""

#
# Author:   Jakub Wlodek
# Created:  12-Aug-2019
# Docs:     https://jwlodek.github.io/py_cui-docs
# License:  BSD-3-Clause (New/Revised)
#

# Some python core library imports
import sys
import os
import time
import copy
import shutil       # We use shutil for getting the terminal dimensions
import threading    # Threading is used for loading icon popups
import logging      # Use logging library for debug purposes


# py_cui uses the curses library. On windows this does not exist, but
# there is a open source windows-curses module that adds curses support
# for python on windows
import curses


# py_cui imports
import py_cui
import py_cui.keys
import py_cui.statusbar
import py_cui.widgets
import py_cui.control_widgets
import py_cui.widget_set
import py_cui.popups
import py_cui.renderer
import py_cui.debug
import py_cui.errors
from py_cui.colors import *
import py_cui.dialog_widgets
import py_cui.control_widgets


# Version number
__version__ = '0.1.3'


def fit_text(width, text, center=False):
    """Fits text to screen size

    Helper function to fit text within a given width. Used to fix issue with status/title bar text
    being too long

    Parameters
    ----------
    width : int
        width of window in characters
    text : str
        input text
    center : Boolean
        flag to center text

    Returns
    -------
    fitted_text : str
        text fixed depending on width
    """

    if width < 5:
        return '.' * width
    if len(text) >= width:
        return text[:width - 5] + '...'
    else:
        total_num_spaces = (width - len(text) - 1)
        if center:
            left_spaces = int(total_num_spaces / 2)
            right_spaces = int(total_num_spaces / 2)
            if(total_num_spaces % 2 == 1):
                right_spaces = right_spaces + 1
            return ' ' * left_spaces + text + ' ' * right_spaces
        else:
            return text + ' ' * total_num_spaces


class PyCUI:
    """Base CUI class

    Main user interface class for py_cui. To create a user interface, you must
    first create an instance of this class, and then add cells + widgets to it.

    Attributes
    ----------
    cursor_x, cursor_y : int
        absolute position of the cursor in the CUI
    grid : py_cui.grid.Grid
        The main layout manager for the CUI
    widgets : dict of str - py_cui.widgets.Widget
        dict of widget in the grid
    title_bar : py_cui.statusbar.StatusBar
        a status bar object that gets drawn at the top of the CUI
    status_bar : py_cui.statusbar.StatusBar
        a status bar object that gets drawn at the bottom of the CUI
    keybindings : list of py_cui.keybinding.KeyBinding
        list of keybindings to check against in the main CUI loop
    height, width : int
        height of the terminal in characters, width of terminal in characters
    exit_key : key_code
        a key code for a key that exits the CUI
    simulated_terminal : List[int]
        Dimensions for an alternative simulated terminal (used for testing)
    """

    def __init__(self, num_rows, num_cols, auto_focus_buttons=True,
                 exit_key=py_cui.keys.KEY_Q_LOWER, simulated_terminal=None):
        """Constructor for PyCUI class
        """

        self._title = 'PyCUI Window'
        # When this is not set, the escape character delay
        # is too long for exiting focus mode
        os.environ.setdefault('ESCDELAY', '25')

        # For unit testing purposes, we want to simulate terminal
        # dimensions so that we don't get errors
        self._simulated_terminal = simulated_terminal

        if self._simulated_terminal is None:
            term_size = shutil.get_terminal_size()
            height  = term_size.lines
            width   = term_size.columns
        else:
            height  = simulated_terminal[0]
            width   = simulated_terminal[1]

        # Init terminal height width. Subtract 4 from height
        # for title/status bar and padding
        self._height                = height
        self._width                 = width
        self._height                = self._height - 4

        # Add status and title bar
        self.title_bar = py_cui.statusbar.StatusBar(self._title, BLACK_ON_WHITE)
        exit_key_char = py_cui.keys.get_char_from_ascii(exit_key)
        self._init_status_bar_text  = 'Press - {} - to exit. Arrow Keys to move ' \
                                       'between widgets. Enter to enter focus ' \
                                       'mode.'.format(exit_key_char)
        self.status_bar = py_cui.statusbar.StatusBar(self._init_status_bar_text,
                                                     BLACK_ON_WHITE)

        # Logging object initialization for py_cui
        self._logger = py_cui.debug._initialize_logger(self,
                                                       name='py_cui')

        # Initialize grid, renderer, and widget dict
        self._grid                  = py_cui.grid.Grid(num_rows, num_cols, self._height, self._width, self._logger)
        self._renderer              = None
        self._border_characters     = None
        self._stdscr                = None
        self._widgets               = {}
        self._refresh_timeout       = -1

        # Variables for determining selected widget/focus mode
        self._selected_widget       = None
        self._in_focused_mode       = False
        self._popup                 = None
        self._auto_focus_buttons    = auto_focus_buttons

        # CUI blocks when loading popup is open
        self._loading               = False
        self._stopped               = False
        self._post_loading_callback = None
        self._on_draw_update_func   = None

        # Top level keybindings. Exit key is 'q' by default
        self._keybindings  = {}
        self._exit_key     = exit_key
        self._forward_cycle_key = py_cui.keys.KEY_CTRL_LEFT
        self._reverse_cycle_key = py_cui.keys.KEY_CTRL_RIGHT

        # Callback to fire when CUI is stopped.
        self._on_stop = None


    def set_refresh_timeout(self, timeout):
        """Sets the CUI auto-refresh timeout to a number of seconds.

        Parameters
        ----------
        timeout : int
            Number of seconds to wait before refreshing the CUI
        """

        # We want the refresh timeout in milliseconds as an integer
        self._refresh_timeout = int(timeout * 1000)


    def set_on_draw_update_func(self, update_function):
        """Adds a function that is fired during each draw call of the CUI

        Parameters
        ----------
        update_function : function
            A no-argument or lambda function that is fired at the start of each draw call
        """

        self._on_draw_update_func = update_function


    def set_widget_cycle_key(self, forward_cycle_key=None, reverse_cycle_key=None):
        """Assigns a key for automatically cycling through widgets in both focus and overview modes

        Parameters
        ----------
        widget_cycle_key : py_cui.keys.KEY
            Key code for key to cycle through widgets
        """

        if forward_cycle_key is not None:
            self._forward_cycle_key = forward_cycle_key
        if reverse_cycle_key is not None:
            self._reverse_cycle_key = reverse_cycle_key


    def enable_logging(self, log_file_path='py_cui_log.txt', logging_level = logging.DEBUG):
        """Function enables logging for py_cui library

        Parameters
        ----------
        log_file_path : str
            The target log filepath. Default 'py_cui_log.txt
        logging_level : int
            Default logging level = logging.DEBUG
        """

        try:
            py_cui.debug._enable_logging(self._logger, filename=log_file_path, logging_level=logging_level)
            self._logger.info('Initialized logger')
        except PermissionError as e:
            print('Failed to initialize logger: {}'.format(str(e)))


    def apply_widget_set(self, new_widget_set):
        """Function that replaces all widgets in a py_cui with those of a different widget set

        Parameters
        ----------
        new_widget_set : WidgetSet
            The new widget set to switch to

        Raises
        ------
        TypeError
            If input is not of type WidgetSet
        """

        if isinstance(new_widget_set, py_cui.widget_set.WidgetSet):
            self.lose_focus()
            self._widgets      = new_widget_set._widgets
            self._grid         = new_widget_set._grid
            self._keybindings  = new_widget_set._keybindings

            if self._simulated_terminal is None:
                if self._stdscr is None:
                    term_size = shutil.get_terminal_size()
                    height  = term_size.lines
                    width   = term_size.columns
                else:
                    # Use curses termsize when possible to fix resize bug on windows.
                    height, width = self._stdscr.getmaxyx()
            else:
                height  = self._simulated_terminal[0]
                width   = self._simulated_terminal[1]

            height  = height - 4

            self._refresh_height_width(height, width)
            if self._stdscr is not None:
                self._initialize_widget_renderer()
            self._selected_widget = new_widget_set._selected_widget
        else:
            raise TypeError('Argument must be of type py_cui.widget_set.WidgetSet')


    def create_new_widget_set(self, num_rows, num_cols):
        """Function that is used to create additional widget sets

        Use this function instead of directly creating widget set object instances, to allow
        for logging support.

        Parameters
        ----------
        num_rows : int
            row count for new widget set
        num_cols : int
            column count for new widget set

        Returns
        -------
        new_widget_set : py_cui.widget_set.WidgetSet
            The new widget set object instance
        """

        # Use current logging object and simulated terminal for sub-widget sets
        return py_cui.widget_set.WidgetSet(num_rows, num_cols, self._logger, 
                                            simulated_terminal=self._simulated_terminal)


    # ----------------------------------------------#
    # Initialization functions                      #
    # Used to initialzie CUI and its features       #
    # ----------------------------------------------#


    def start(self):
        """Function that starts the CUI
        """

        self._logger.info('Starting {} CUI'.format(self._title))
        curses.wrapper(self._draw)


    def stop(self):
        """Function that stops the CUI, and fires the callback function.

        Callback must be a no arg method
        """

        self._logger.info('Stopping CUI')
        self._stopped = True


    def run_on_exit(self, command):
        """Sets callback function on CUI exit. Must be a no-argument function or lambda function

        Parameters
        ----------
        command : function
            A no-argument or lambda function to be fired on exit
        """

        self._on_stop = command


    def set_title(self, title):
        """Sets the title bar text

        Parameters
        ----------
        title : str
            New title for CUI
        """

        self._title = title


    def set_status_bar_text(self, text):
        """Sets the status bar text when in overview mode

        Parameters
        ----------
        text : str
            Status bar text
        """

        self._init_status_bar_text = text
        self.status_bar.set_text(text)


    def _initialize_colors(self):
        """Function for initialzing curses colors. Called when CUI is first created.
        """

        # Start colors in curses.
        # For each color pair in color map, initialize color combination.
        curses.start_color()
        for color_pair in py_cui.colors._COLOR_MAP.keys():
            fg_color, bg_color = py_cui.colors._COLOR_MAP[color_pair]
            curses.init_pair(color_pair, fg_color, bg_color)


    def _initialize_widget_renderer(self):
        """Function that creates the renderer object that will draw each widget
        """

        if self._renderer is None:
            self._renderer = py_cui.renderer.Renderer(self, self._stdscr, self._logger)
        for widget_id in self._widgets.keys():
            self._widgets[widget_id]._assign_renderer(self._renderer)
        if self._popup is not None:
            self._popup._assign_renderer(self._renderer)


    def toggle_unicode_borders(self):
        """Function for toggling unicode based border rendering
        """

        if self._border_characters is None or self._border_characters['UP_LEFT'] == '+':
            self.set_widget_border_characters('\u256d', '\u256e', '\u2570', '\u256f', '\u2500', '\u2502')
        else:
            self.set_widget_border_characters('+', '+', '+', '+', '-', '|')


    def set_widget_border_characters(self, upper_left_corner, upper_right_corner, lower_left_corner, lower_right_corner, horizontal, vertical):
        """Function that can be used to set arbitrary border characters for drawing widget borders by renderer.

        Parameters
        ----------
        upper_left_corner : char
            Upper left corner character
        upper_right_corner : char
            Upper right corner character
        lower_left_corner : char
            Upper left corner character
        lower_right_corner : char
            Lower right corner character
        horizontal : char
            Horizontal border character
        vertical : char
            Vertical border character
        """

        self._border_characters = {
            'UP_LEFT': upper_left_corner,
            'UP_RIGHT': upper_right_corner,
            'DOWN_LEFT': lower_left_corner,
            'DOWN_RIGHT': lower_right_corner,
            'HORIZONTAL': horizontal,
            'VERTICAL': vertical
        }
        self._logger.info('Set border_characters to {}'.format(self._border_characters))


    def get_widgets(self):
        """Function that gets current set of widgets

        Returns
        -------
        widgets : dict of str -> widget
            dictionary mapping widget IDs to object instances
        """

        return self._widgets

    # Widget add functions. Each of these adds a particular type of widget
    # to the grid in a specified location.

    def add_scroll_menu(self, title, row, column, row_span=1, column_span=1, padx=1, pady=0):
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
        new_scroll_menu     = py_cui.widgets.ScrollMenu(id,
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
        new_checkbox_menu   = py_cui.widgets.CheckBoxMenu(id,
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
        new_text_box        = py_cui.widgets.TextBox(id,
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
        new_text_block      = py_cui.widgets.ScrollTextBlock(id,
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
        new_label           = py_cui.widgets.Label(id,
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
        new_label           = py_cui.widgets.BlockLabel(id,
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
        new_button          = py_cui.widgets.Button(id,
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
        new_slider = py_cui.control_widgets.slider.SliderWidget(id,
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

    def get_element_at_position(self, x, y):
        """Returns containing widget for character position

        Parameters
        ----------
        x : int
            Horizontal character position
        y : int
            Vertical character position, top down

        Returns
        -------
        in_widget : UIElement
            Widget or popup that is within the position None if nothing
        """

        if self._popup is not None and self._popup._contains_position(x, y):
            return self._popup
        elif self._popup is None:
            for widget_id in self.get_widgets().keys():
                if self.get_widgets()[widget_id]._contains_position(x, y):
                    return self.get_widgets()[widget_id]
        return None




    def _get_horizontal_neighbors(self, widget, direction):
        """Gets all horizontal (left, right) neighbor widgets

        Parameters
        ----------
        widget : py_cui.widgets.Widget
            The currently selected widget
        direction : py_cui.keys.KEY*
            must be an arrow key value

        Returns
        -------
        id_list : list[]
            A list of the neighbor widget ids
        """

        if not direction in py_cui.keys.ARROW_KEYS:
            return None

        _,          num_cols    = self._grid.get_dimensions()
        row_start,  col_start   = widget.get_grid_cell()
        row_span,   col_span    = widget.get_grid_cell_spans()
        id_list                 = []

        if direction == py_cui.keys.KEY_LEFT_ARROW:
            col_range_start = 0
            col_range_stop = col_start
        else:
            col_range_start = col_start + col_span
            col_range_stop = num_cols

        for col in range(col_range_start, col_range_stop):
            for row in range(row_start, row_start + row_span):
                for widget_id in self.get_widgets().keys():
                    if self.get_widgets()[widget_id]._is_row_col_inside(row, col) and widget_id not in id_list:
                        id_list.append(widget_id)

        if direction == py_cui.keys.KEY_LEFT_ARROW:
            id_list.reverse()

        self._logger.info('Neighbors with ids {} for cell {},{} span {},{}'.format(id_list,
                                                                                   row_start,
                                                                                   col_start,
                                                                                   row_span,
                                                                                   col_span))
        return id_list


    def _get_vertical_neighbors(self, widget, direction):
        """Gets all vertical (up, down) neighbor widgets

        Parameters
        ----------
        widget : py_cui.widgets.Widget
            The currently selected widget
        direction : py_cui.keys.KEY*
            must be an arrow key value

        Returns
        -------
        id_list : list[]
            A list of the neighbor widget ids
        """

        if not direction in py_cui.keys.ARROW_KEYS:
            return None

        num_rows,   _           = self._grid.get_dimensions()
        row_start,  col_start   = widget.get_grid_cell()
        row_span,   col_span    = widget.get_grid_cell_spans()
        id_list                 = []

        if direction == py_cui.keys.KEY_UP_ARROW:
            row_range_start = 0
            row_range_stop = row_start
        else:
            row_range_start = row_start + row_span
            row_range_stop = num_rows

        for row in range(row_range_start, row_range_stop):
            for col in range(col_start, col_start + col_span):
                for widget_id in self.get_widgets().keys():
                    if self.get_widgets()[widget_id]._is_row_col_inside(row, col) and widget_id not in id_list:
                        id_list.append(widget_id)

        if direction == py_cui.keys.KEY_UP_ARROW:
            id_list.reverse()

        self._logger.info('Neighbors with ids {} for cell {},{} span {},{}'.format(id_list,
                                                                                   row_start,
                                                                                   col_start,
                                                                                   row_span,
                                                                                   col_span))
        return id_list

    # CUI status functions. Used to switch between widgets, set the mode, and
    # identify neighbors for overview mode

    def _check_if_neighbor_exists(self, direction):
        """Function that checks if widget has neighbor in specified cell.

        Used for navigating CUI, as arrow keys find the immediate neighbor

        Parameters
        ----------
        direction : py_cui.keys.KEY_*
            The direction in which to search

        Returns
        -------
        widget_id : str
            The widget neighbor ID if found, None otherwise
        """

        start_widget                = self.get_widgets()[self._selected_widget]

        # Find all the widgets in the given row or column
        neighbors = []
        if direction in [py_cui.keys.KEY_DOWN_ARROW, py_cui.keys.KEY_UP_ARROW]:
            neighbors = self._get_vertical_neighbors(start_widget, direction)
        elif direction in [py_cui.keys.KEY_RIGHT_ARROW, py_cui.keys.KEY_LEFT_ARROW]:
            neighbors = self._get_horizontal_neighbors(start_widget, direction)

        if len(neighbors) == 0:
            return None

        # We select the best match to jump to (first neighbor)
        return neighbors[0]


    def get_selected_widget(self):
        """Function that gets currently selected widget

        Returns
        -------
        selected_widget : py_cui.widgets.Widget
            Reference to currently selected widget object
        """

        if self._selected_widget is not None and self._selected_widget in self.get_widgets().keys():
            return self.get_widgets()[self._selected_widget]
        else:
            self._logger.warn('Selected widget ID is None or invalid')
            return None


    def set_selected_widget(self, widget_id):
        """Function that sets the selected widget for the CUI

        Parameters
        ----------
        widget_id : str
            the id of the widget to select
        """

        if widget_id in self.get_widgets().keys():
            self._logger.info('Setting selected widget to ID {}'.format(widget_id))
            self._selected_widget = widget_id
        else:
            self._logger.warn('Widget w/ ID {} does not exist among current widgets.'.format(widget_id))


    def lose_focus(self):
        """Function that forces py_cui out of focus mode.

        After popup is called, focus is lost
        """

        if self._in_focused_mode:
            self._in_focused_mode = False
            self.status_bar.set_text(self._init_status_bar_text)
            self.get_widgets()[self._selected_widget].set_selected(False)
        else:
            self._logger.info('lose_focus: Not currently in focus mode')


    def move_focus(self, widget, auto_press_buttons=True):
        """Moves focus mode to different widget

        Parameters
        ----------
        widget : Widget
            The widget object we want to move focus to.
        """

        self.lose_focus()
        self.set_selected_widget(widget.get_id())
        # If autofocus buttons is selected, we automatically process the button command and reset to overview mode
        if self._auto_focus_buttons and auto_press_buttons and isinstance(widget, py_cui.widgets.Button):
            widget.command()
            self._logger.info('Moved focus to button {} - ran autofocus command'.format(widget.get_title()))
        elif self._auto_focus_buttons and isinstance(widget, py_cui.widgets.Button):
            self.status_bar.set_text(self._init_status_bar_text)
        else:
            widget.set_selected(True)
            self._in_focused_mode = True
            self.status_bar.set_text(widget.get_help_text())
        self._logger.info('Moved focus to widget {}'.format(widget.get_title()))


    def _cycle_widgets(self, reverse=False):
        """Function that is fired if cycle key is pressed to move to next widget

        Parameters
        ----------
        reverse : bool
            Default false. If true, cycle widgets in reverse order.
        """

        num_widgets = len(self.get_widgets().keys())
        current_widget_num = int(self._selected_widget.split('Widget')[1])

        if not reverse:
            next_widget_num = current_widget_num + 1
            if next_widget_num == num_widgets:
                next_widget_num = 0
            cycle_key = self._forward_cycle_key
        else:
            next_widget_num = current_widget_num - 1
            if next_widget_num < 0:
                next_widget_num = num_widgets - 1
            cycle_key = self._reverse_cycle_key

        current_widget_id = 'Widget{}'.format(current_widget_num)
        next_widget_id = 'Widget{}'.format(next_widget_num)
        if self._in_focused_mode and cycle_key in self.get_widgets()[current_widget_id]._key_commands.keys():
            # In the event that we are focusing on a widget with that key defined, we do not cycle.
            pass
        else:
            self.move_focus(self.get_widgets()[next_widget_id], auto_press_buttons=False)


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

    # Popup functions. Used to display messages, warnings, and errors to the user.

    def show_message_popup(self, title, text):
        """Shows a message popup

        Parameters
        ----------
        title : str
            Message title
        text : str
            Message text
        """

        color       = WHITE_ON_BLACK
        self._popup = py_cui.popups.MessagePopup(self, title, text, color, self._renderer, self._logger)
        self._logger.info('Opened {} popup with title {}'.format(str(type(self._popup)), self._popup.get_title()))


    def show_warning_popup(self, title, text):
        """Shows a warning popup

        Parameters
        ----------
        title : str
            Warning title
        text : str
            Warning text
        """

        color       = YELLOW_ON_BLACK
        self._popup = py_cui.popups.MessagePopup(self, 'WARNING - ' + title, text, color, self._renderer, self._logger)
        self._logger.info('Opened {} popup with title {}'.format(str(type(self._popup)), self._popup.get_title()))


    def show_error_popup(self, title, text):
        """Shows an error popup

        Parameters
        ----------
        title : str
            Error title
        text : str
            Error text
        """

        color       = RED_ON_BLACK
        self._popup = py_cui.popups.MessagePopup(self, 'ERROR - ' + title, text, color, self._renderer, self._logger)
        self._logger.info('Opened {} popup with title {}'.format(str(type(self._popup)), self._popup.get_title()))


    def show_yes_no_popup(self, title, command):
        """Shows a yes/no popup.

        The 'command' parameter must be a function with a single boolean parameter

        Parameters
        ----------
        title : str
            Message title
        command : function
            A function taking in a single boolean parameter. Will be fired with True if yes selected, false otherwise
        """

        color       = WHITE_ON_BLACK
        self._popup = py_cui.popups.YesNoPopup(self, title + '- (y/n)', 'Yes - (y), No - (n)', color, command, self._renderer, self._logger)
        self._logger.info('Opened {} popup with title {}'.format(str(type(self._popup)), self._popup.get_title()))


    def show_text_box_popup(self, title, command, password=False):
        """Shows a textbox popup.

        The 'command' parameter must be a function with a single string parameter

        Parameters
        ----------
        title : str
            Message title
        command : Function
            A function with a single string parameter, fired with contents of textbox when enter key pressed
        password=False : bool
            If true, write characters as '*'
        """

        color       = WHITE_ON_BLACK
        self._popup = py_cui.popups.TextBoxPopup(self, title, color, command, self._renderer, password, self._logger)
        self._logger.info('Opened {} popup with title {}'.format(str(type(self._popup)), self._popup.get_title()))


    def show_menu_popup(self, title, menu_items, command, run_command_if_none=False):
        """Shows a menu popup.

        The 'command' parameter must be a function with a single string parameter

        Parameters
        ----------
        title : str
            menu title
        menu_items : list of str
            A list of menu items
        command : Function
            A function taking in a single string argument. Fired with selected menu item when ENTER pressed.
        run_command_if_none=False : bool
            If True, will run command passing in None if no menu item selected.
        """

        color       = WHITE_ON_BLACK
        self._popup = py_cui.popups.MenuPopup(self, menu_items, title, color, command, self._renderer, self._logger, run_command_if_none)
        self._logger.info('Opened {} popup with title {}'.format(str(type(self._popup)), self._popup.get_title()))


    def show_loading_icon_popup(self, title, message, callback=None):
        """Shows a loading icon popup

        Parameters
        ----------
        title : str
            Message title
        message : str
            Message text. Will show as '$message...'
        callback=None : Function
            If not none, fired after loading is completed. Must be a no-arg function
        """

        if callback is not None:
            self._post_loading_callback = callback

        color         = WHITE_ON_BLACK
        self._loading = True
        self._popup   = py_cui.popups.LoadingIconPopup(self, title, message, color, self._renderer, self._logger)
        self._logger.info('Opened {} popup with title {}'.format(str(type(self._popup)), self._popup.get_title()))


    def show_loading_bar_popup(self, title, num_items, callback=None):
        """Shows loading bar popup.

        Use 'increment_loading_bar' to show progress

        Parameters
        ----------
        title : str
            Message title
        num_items : int
            Number of items to iterate through for loading
        callback=None : Function
            If not none, fired after loading is completed. Must be a no-arg function
        """

        if callback is not None:
            self._post_loading_callback = callback

        color         = WHITE_ON_BLACK
        self._loading = True
        self._popup   = py_cui.popups.LoadingBarPopup(self, title, num_items, color, self._renderer, self._logger)
        self._logger.info('Opened {} popup with title {}'.format(str(type(self._popup)), self._popup.get_title()))


    def show_form_popup(self, title, fields, passwd_fields=[], required=[], callback=None):
        """Shows form popup.

        Used for inputting several fields worth of values

        Paramters
        ---------
        title : str
            Message title
        fields : List[str]
            Names of each individual field
        passwd_fields : List[str]
            Field names that should have characters hidden
        required : List[str]
            Fields that are required before submission
        callback=None : Function
            If not none, fired after loading is completed. Must be a no-arg function
        """

        self._popup = py_cui.dialog_widgets.form.FormPopup(self, fields, passwd_fields, required, {}, title, py_cui.WHITE_ON_BLACK, self._renderer, self._logger)
        if callback is not None:
            self._popup.set_on_submit_action(callback)


    def show_filedialog_popup(self, popup_type='file', initial_dir='.', callback=None, ascii_icons=False, limit_extensions=[]):
        """Shows form popup.

        Used for inputting several fields worth of values

        Paramters
        ---------
        title : str
            Message title
        fields : List[str]
            Names of each individual field
        passwd_fields : List[str]
            Field names that should have characters hidden
        required : List[str]
            Fields that are required before submission
        callback=None : Function
            If not none, fired after loading is completed. Must be a no-arg function
        """

        self._popup = py_cui.dialog_widgets.explorer.FileDialogPopup(self, callback, initial_dir, popup_type, ascii_icons, limit_extensions, py_cui.WHITE_ON_BLACK, self._renderer, self._logger)


    def increment_loading_bar(self):
        """Increments progress bar if loading bar popup is open
        """

        if self._popup is not None:
            self._popup._increment_counter()
        else:
            self._logger.warn('No popup is currently opened.')


    def stop_loading_popup(self):
        """Leaves loading state, and closes popup.

        Must be called by user to escape loading.
        """

        self._loading = False
        self.close_popup()
        self._logger.info('Stopping open loading popup')


    def close_popup(self):
        """Closes the popup, and resets focus
        """

        self.lose_focus()
        self._popup = None


    def _refresh_height_width(self, height, width):
        """Function that updates the height and width of the CUI based on terminal window size

        Parameters
        ----------
        height : int
            Window height in terminal characters
        width : int
            Window width in terminal characters
        """

        self._height = height
        self._width  = width
        self._grid.update_grid_height_width(self._height, self._width)
        for widget_id in self._widgets.keys():
            self._widgets[widget_id].update_height_width()
        if self._popup is not None:
            self._popup.update_height_width()


    def get_absolute_size(self):
        """Returns dimensions of CUI

        Returns
        -------
        height, width : int
            The dimensions of drawable CUI space in characters
        """

        return self._height, self._width

    # Draw Functions. Function for drawing widgets, status bars, and popups

    def _draw_widgets(self):
        """Function that draws all of the widgets to the screen
        """

        for widget_key in self.get_widgets().keys():
            if widget_key != self._selected_widget:
                self.get_widgets()[widget_key]._draw()

        # We draw the selected widget last to support cursor location.
        if self._selected_widget is not None:
            self.get_widgets()[self._selected_widget]._draw()

        self._logger.info('Drew widgets')



    def _draw_status_bars(self, stdscr, height, width):
        """Draws status bar and title bar

        Parameters
        ----------
        stdscr : curses Standard cursor
            The cursor used to draw the status bar
        height : int
            Window height in terminal characters
        width : int
            Window width in terminal characters
        """

        if self.status_bar is not None:
            stdscr.attron(curses.color_pair(self.status_bar.get_color()))
            stdscr.addstr(height + 3, 0, fit_text(width, self.status_bar.get_text()))
            stdscr.attroff(curses.color_pair(self.status_bar.get_color()))

        if self.title_bar is not None:
            stdscr.attron(curses.color_pair(self.title_bar.get_color()))
            stdscr.addstr(0, 0, fit_text(width, self._title, center=True))
            stdscr.attroff(curses.color_pair(self.title_bar.get_color()))


    def _display_window_warning(self, stdscr, error_info):
        """Function that prints some basic error info if there is an error with the CUI

        Parameters
        ----------
        stdscr : curses Standard cursor
            The cursor used to draw the warning
        error_info : str
            The information regarding the error.
        """

        stdscr.clear()
        stdscr.attron(curses.color_pair(RED_ON_BLACK))
        stdscr.addstr(0, 0, 'Error displaying CUI!!!')
        stdscr.addstr(1, 0, 'Error Type: {}'.format(error_info))
        stdscr.addstr(2, 0, 'Most likely terminal dimensions are too small.')
        stdscr.attroff(curses.color_pair(RED_ON_BLACK))
        stdscr.refresh()
        self._logger.info('Encountered error -> {}'.format(error_info))


    def _handle_key_presses(self, key_pressed):
        """Function that handles all main loop key presses.

        Parameters
        ----------
        key_pressed : py_cui.keys.KEY_*
            The key being pressed
        """

        # Selected widget represents which widget is being hovered over, though not necessarily in focus mode
        if self._selected_widget is None:
            return

        selected_widget = self.get_widgets()[self._selected_widget]

        # If we are in focus mode, the widget has all of the control of the keyboard except
        # for the escape key, which exits focus mode.
        if self._in_focused_mode and self._popup is None:
            if key_pressed == py_cui.keys.KEY_ESCAPE:
                self.status_bar.set_text(self._init_status_bar_text)
                self._in_focused_mode = False
                selected_widget.set_selected(False)
                self._logger.info('Exiting focus mode on widget {}'.format(selected_widget.get_title()))
            else:
                # widget handles remaining py_cui.keys
                self._logger.info('Widget {} handling {} key'.format(selected_widget.get_title(), key_pressed))
                selected_widget._handle_key_press(key_pressed)

        # Otherwise, barring a popup, we are in overview mode, meaning that arrow py_cui.keys move between widgets, and Enter key starts focus mode
        elif self._popup is None:
            if key_pressed == py_cui.keys.KEY_ENTER and self._selected_widget is not None and selected_widget.is_selectable():
                self.move_focus(selected_widget)

            for key in self._keybindings.keys():
                if key_pressed == key:
                    command = self._keybindings[key]
                    self._logger.info('Detected binding for key {}, running command {}'.format(key_pressed, command.__name__))
                    command()

            # If not in focus mode, use the arrow py_cui.keys to move around the selectable widgets.
            neighbor = None
            if key_pressed in py_cui.keys.ARROW_KEYS:
                neighbor = self._check_if_neighbor_exists(key_pressed)
            if neighbor is not None:
                self.set_selected_widget(neighbor)
                self._logger.info('Navigated to neighbor widget {}'.format(self.get_widgets()[self._selected_widget].get_title()))

        # if we have a popup, that takes key control from both overview and focus mode
        elif self._popup is not None:
            self._logger.info('Popup {} handling key {}'.format(self._popup.get_title(), key_pressed))
            self._popup._handle_key_press(key_pressed)


    def _draw(self, stdscr):
        """Main CUI draw loop called by start()

        Parameters
        ----------
        stdscr : curses Standard cursor
            The cursor used to draw the CUI
        """

        self._stdscr = stdscr
        key_pressed = 0

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.refresh()
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        # stdscr.nodelay(False)
        stdscr.keypad(True)

        # Initialization functions. Generates colors and renderer
        self._initialize_colors()
        self._initialize_widget_renderer()
        
        # If user specified a refresh timeout, apply it here
        if self._refresh_timeout > 0:
            self._stdscr.timeout(self._refresh_timeout)
        #self._stdscr.timeout(1000)

        # If user sets non-default border characters, update them here
        if self._border_characters is not None:
            self._renderer._set_border_renderer_chars(self._border_characters)

        # Loop where key_pressed is the last character pressed. Wait for exit key while no popup or focus mode
        while key_pressed != self._exit_key or self._in_focused_mode or self._popup is not None:

            try:
                # If we call stop, we want to break out of the main draw loop
                if self._stopped:
                    break

                # Initialization and size adjustment
                stdscr.erase()

                # find height width, adjust if status/title bar added. We decrement the height by 4 to account for status/title bar and padding
                if self._simulated_terminal is None:
                    height, width   = stdscr.getmaxyx()
                else:
                    height  = self._simulated_terminal[0]
                    width   = self._simulated_terminal[1]

                height          = height - 4

                # If the user defined an update function to fire on each draw call,
                # Run it here. This can of course be also handled user-side
                # through a separate thread.
                if self._on_draw_update_func is not None:
                    self._on_draw_update_func()

                # This is what allows the CUI to be responsive. Adjust grid size based on current terminal size
                # Resize the grid and the widgets if there was a resize operation
                if key_pressed == curses.KEY_RESIZE:
                    self._logger.info('Resizing CUI to new dimensions {} by {}'.format(height, width))
                    try:
                        self._refresh_height_width(height, width)
                    except py_cui.errors.PyCUIOutOfBoundsError as e:
                        self._logger.info('Resized terminal too small')
                        self._display_window_warning(stdscr, str(e))

                # Here we handle mouse click events globally, or pass them to the UI element to handle
                elif key_pressed == curses.KEY_MOUSE:
                    self._logger.info('Detected mouse click')
                    _, x, y, _, _ = curses.getmouse()
                    in_element = self.get_element_at_position(x, y)

                    # In first case, we click inside already selected widget, pass click for processing
                    if in_element is not None and in_element.is_selected():
                        in_element._handle_mouse_press(x, y)
                    # Otherwise, if not a popup, select the clicked on widget
                    elif in_element is not None and not isinstance(in_element, py_cui.popups.Popup):
                        self.move_focus(in_element)
                        in_element._handle_mouse_press(x, y)

                # If we have a post_loading_callback, fire it here
                if self._post_loading_callback is not None and not self._loading:
                    self._logger.info('Firing post-loading callback function {}'.format(self._post_loading_callback.__name__))
                    self._post_loading_callback()
                    self._post_loading_callback = None

                # Handle widget cycling
                if key_pressed == self._forward_cycle_key:
                    self._cycle_widgets()
                elif key_pressed == self._reverse_cycle_key:
                    self._cycle_widgets(reverse=True)

                # Handle keypresses
                self._handle_key_presses(key_pressed)

                try:
                    # Draw status/title bar, and all widgets. Selected widget will be bolded.
                    self._draw_status_bars(stdscr, height, width)
                    self._draw_widgets()
                    # draw the popup if required
                    if self._popup is not None:
                        self._popup._draw()
                except curses.error as e:
                    self._logger.error('Curses error while drawing TUI')
                    self._display_window_warning(stdscr, str(e))
                except py_cui.errors.PyCUIOutOfBoundsError as e:
                    self._logger.error('Resized terminal too small')
                    self._display_window_warning(stdscr, str(e))

                # Refresh the screen
                stdscr.refresh()

                # Wait for next input
                if self._loading or self._post_loading_callback is not None:
                    # When loading, refresh screen every quarter second
                    time.sleep(0.25)
                    # Need to reset key_pressed, because otherwise the previously pressed key will be used.
                    key_pressed = 0
                elif self._stopped:
                    key_pressed = self._exit_key
                else:
                    self._logger.info('Waiting for next keypress')
                    key_pressed = stdscr.getch()

            except KeyboardInterrupt:
                self._logger.info('Detect Keyboard Interrupt, Exiting...')
                self._stopped = True


        stdscr.erase()
        stdscr.refresh()
        curses.endwin()
        if self._on_stop is not None:
            self._logger.info('Firing onstop function {}'.format(self._on_stop.__name__))
            self._on_stop()


    def __format__(self, fmt):
        """Override of base format function. Prints list of current widgets.

        Parameters
        ----------
        fmt : Format
            The format to override
        """

        out = ''
        for widget in self.get_widgets().keys():
            out += '{}\n'.format(self.get_widgets()[widget].get_title())
        return out
