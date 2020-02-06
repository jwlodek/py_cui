"""A python library for creating command line based user interfaces.

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""

# Some python core library imports
import sys
import os
import time
import shutil       # We use shutil for getting the terminal dimensions
import threading    # Threading is used for loading icon popups


# py_cui uses the curses library. On windows this does not exist, but
# there is a open source windows-curses module that adds curses support
# for python on windows
import curses


# py_cui imports
import py_cui.grid as grid
import py_cui.statusbar as statusbar
import py_cui.renderer as renderer
import py_cui.errors
import py_cui.widgets as widgets
import py_cui.widget_set as widget_set
import py_cui.keys
import py_cui.popups


# Curses color configuration - curses colors automatically work as pairs, so it was easiest to
# create these values as pairs of the bat to be selected. 
# Format is FOREGROUND_ON_BACKGROUND
# TODO add more color options
WHITE_ON_BLACK      = 1
BLACK_ON_GREEN      = 2
BLACK_ON_WHITE      = 3
WHITE_ON_RED        = 4
YELLOW_ON_BLACK     = 5
RED_ON_BLACK        = 6
CYAN_ON_BLACK       = 7
MAGENTA_ON_BLACK    = 8
GREEN_ON_BLACK      = 9
BLUE_ON_BLACK       = 10


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
        return text[:width-5] + '...'
    else:
        total_num_spaces = (width - len(text) - 1)
        if center:
            left_spaces = int(total_num_spaces/2)
            right_spaces = int(total_num_spaces/2)
            if(total_num_spaces % 2 == 1):
                right_spaces = right_spaces+1
            return ' ' * left_spaces + text + ' ' * right_spaces
        else:
            return text + ' ' * total_num_spaces


class PyCUI:
    """Base CUI class

    Main user interface class for py_cui. To create a user interface, you must first
    create an instance of this class, and then add cells + widgets to it.

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

    Methods
    -------
    get_widget_set()
        Gets widget set object from current widgets.
    apply_widget_set()
        Function that replaces all widgets in a py_cui with those of a different widget set
    start()
        starts the CUI once all of the widgets have been added
    stop()
        Function that stops CUI and runs the run_on_exit function if set.
    run_on_exit()
        Sets callback function on CUI exit. Must be a no-argument function or lambda function
    add_scroll_menu()
        Function that adds a new scroll menu to the CUI grid
    add_checkbox_menu()
        Function that adds a new checkbox menu to the CUI grid
    add_text_box()
        Function that adds a new text box to the CUI grid
    add_text_block()
        Function that adds a new text block to the CUI grid
    add_label()
        Function that adds a new label to the CUI grid
    add_block_label()
        Function that adds a new block label to the CUI grid
    add_button()
        Function that adds a new button to the CUI grid
    add_key_command()
        Function that adds a keybinding to the CUI when in overview mode
    show_message_popup()
        Shows a message popup
    show_warning_popup()
        Shows a warning popup
    show_error_popup()
        Shows an error popup
    show_yes_no_popup()
        Shows a yes/no popup.
    show_text_box_popup()
        Shows a textbox popup.
    show_menu_popup()
        Shows a menu popup.
    show_loading_icon_popup()
        Shows a loading icon popup
    show_loading_bar_popup()
        Shows loading bar popup.
    increment_loading_bar()
        Increments progress bar if loading bar popup is open
    stop_loading_popup()
        Leaves loading state, and closes popup.
    close_popup()
        Closes the popup, and resets focus
    refresh_height_width()
        Function that updates the height and width of the CUI based on terminal window size
    draw_widgets()
        Function that draws all of the widgets to the screen
    draw_status_bars()
        Draws status bar and title bar
    display_window_warning()
        Function that prints some basic error info if there is an error with the CUI
    handle_key_presses()
        Function that handles all main loop key presses.
    draw()
        Main CUI draw loop called by start()
    set_title()
        Sets the title bar text
    set_status_bar_text()
        Sets the status bar text when in overview mode
    initialize_colors()
        Function for initialzing curses colors. Called when CUI is first created.
    initialize_widget_renderer()
        Function that creates the renderer object that will draw each widget
    check_if_neighbor_exists()
        Function that checks if widget has neighbor in specified cell.
    set_selected_widget()
        Function that sets the selected cell for the CUI
    get_widget_id()
        Function for grabbing widget ID
    lose_focus()
        Function that forces py_cui out of focus mode.
    move_focus()
        Moves focus mode to different widget
    add_status_bar()
        function that adds a status bar widget to the CUI
    """

    def __init__(self, num_rows, num_cols, auto_focus_buttons=True, exit_key=py_cui.keys.KEY_Q_LOWER):
        """Constructor for PyCUI class
        """

        self.title = 'PyCUI Window'
        # When this is not set, the escape character delay is too long for exiting focus mode
        os.environ.setdefault('ESCDELAY', '25')
        self.cursor_x = 0
        self.cursor_y = 0
        term_size = shutil.get_terminal_size()

        self.height = term_size.lines
        self.width = term_size.columns
        self.height = self.height - 4

        # Add status and title bar
        self.title_bar = py_cui.statusbar.StatusBar(self.title, BLACK_ON_WHITE)
        self.init_status_bar_text = 'Press - {} - to exit. Arrow Keys to move between widgets. Enter to enter focus mode.'.format(py_cui.keys.get_char_from_ascii(exit_key))
        self.status_bar = py_cui.statusbar.StatusBar(self.init_status_bar_text, BLACK_ON_WHITE)

        # Initialize grid, renderer, and widget dict
        self.grid = grid.Grid(num_rows, num_cols, self.height, self.width)
        self.renderer = None
        self.stdscr = None
        self.widgets = {}

        # Variables for determining selected widget/focus mode
        self.selected_widget = None
        self.in_focused_mode = False
        self.popup = None
        self.auto_focus_buttons = auto_focus_buttons

        # CUI blocks when loading popup is open
        self.loading = False
        self.stopped = True
        self.post_loading_callback = None

        # Top level keybindings. Exit key is 'q' by default
        self.keybindings = {}
        self.exit_key = exit_key

        # Callback to fire when CUI is stopped.
        self.on_stop = None


    def get_widget_set(self):
        """Gets widget set object from current widgets.

        Returns
        -------
        new_widget_set : py_cui.widget_set.WidgetSet
            Widget set collected from widgets currently added to the py_cui
        """

        new_widget_set = widget_set.WidgetSet(self.grid.num_rows, self.grid.num_columns)
        new_widget_set.grid = self.grid
        new_widget_set.widgets = self.widgets
        new_widget_set.keybindings = self.keybindings
        return new_widget_set


    def apply_widget_set(self, new_widget_set):
        """Function that replaces all widgets in a py_cui with those of a different widget set

        Parameters
        ----------
        new_widget_set : WidgetSet
            The new widget set to switch to

        Raises
        ------
        TypeError
            If input is not of type widget set
        """

        if isinstance(new_widget_set, widget_set.WidgetSet):
            self.lose_focus()
            self.widgets = new_widget_set.widgets
            self.grid = new_widget_set.grid
            self.keybindings = new_widget_set.keybindings
            term_size = shutil.get_terminal_size()
            height = term_size.lines
            width = term_size.columns
            height = height - 4
            self.refresh_height_width(height, width)
            self.initialize_widget_renderer()
            self.selected_widget = new_widget_set.selected_widget
        else:
            raise TypeError("Argument must be of type py_cui.widget_set.WidgetSet")


    # ----------------------------------------------#
    # Initialization functions                      #
    # Used to initialzie CUI and its features       #
    # ----------------------------------------------#


    def start(self):
        """Function that starts the CUI
        """

        self.stopped = False
        curses.wrapper(self.draw)


    def stop(self):
        """Function that stops the CUI, and fires the callback function. 
        
        Callback must be a no arg method
        """

        self.stopped = True


    def run_on_exit(self, command):
        """Sets callback function on CUI exit. Must be a no-argument function or lambda function

        Parameters
        ----------
        command : function
            A no-argument or lambda function to be fired on exit
        """

        self.on_stop = command


    def set_title(self, title):
        """Sets the title bar text

        Parameters
        ----------
        title : str
            New title for CUI
        """

        self.title = title


    def set_status_bar_text(self, text):
        """Sets the status bar text when in overview mode

        Parameters
        ----------
        text : str
            Status bar text
        """

        self.init_status_bar_text = text
        self.status_bar.set_text(text)


    def initialize_colors(self):
        """Function for initialzing curses colors. Called when CUI is first created.
        """

        # Start colors in curses
        curses.start_color()
        curses.init_pair(WHITE_ON_BLACK,    curses.COLOR_WHITE,     curses.COLOR_BLACK)
        curses.init_pair(BLACK_ON_GREEN,    curses.COLOR_BLACK,     curses.COLOR_GREEN)
        curses.init_pair(BLACK_ON_WHITE,    curses.COLOR_BLACK,     curses.COLOR_WHITE)
        curses.init_pair(WHITE_ON_RED,      curses.COLOR_WHITE,     curses.COLOR_RED)
        curses.init_pair(YELLOW_ON_BLACK,   curses.COLOR_YELLOW,    curses.COLOR_BLACK)
        curses.init_pair(RED_ON_BLACK,      curses.COLOR_RED,       curses.COLOR_BLACK)
        curses.init_pair(CYAN_ON_BLACK,     curses.COLOR_CYAN,      curses.COLOR_BLACK)
        curses.init_pair(MAGENTA_ON_BLACK,  curses.COLOR_MAGENTA,   curses.COLOR_BLACK)
        curses.init_pair(GREEN_ON_BLACK,    curses.COLOR_GREEN,     curses.COLOR_BLACK)
        curses.init_pair(BLUE_ON_BLACK,     curses.COLOR_BLUE,      curses.COLOR_BLACK)


    def initialize_widget_renderer(self):
        """Function that creates the renderer object that will draw each widget
        """

        self.renderer = renderer.Renderer(self, self.stdscr)
        for widget_id in self.widgets.keys():
            self.widgets[widget_id].assign_renderer(self.renderer)
        if self.popup is not None:
            self.popup.renderer = self.renderer


    # Widget add functions. Each of these adds a particular type of widget to the grid
    # in a specified location.

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

        id = 'Widget{}'.format(len(self.widgets.keys()))
        new_scroll_menu = widgets.ScrollMenu(id, title, self.grid, row, column, row_span, column_span, padx, pady)
        self.widgets[id] = new_scroll_menu
        if self.selected_widget is None:
            self.set_selected_widget(id)
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

        id = 'Widget{}'.format(len(self.widgets.keys()))
        new_checkbox_menu = widgets.CheckBoxMenu(id, title, self.grid, row, column, row_span, column_span, padx, pady, checked_char)
        self.widgets[id] = new_checkbox_menu
        if self.selected_widget is None:
            self.set_selected_widget(id)
        return new_checkbox_menu


    def add_text_box(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, initial_text = ''):
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

        Returns
        -------
        new_text_box : TextBox
            A reference to the created textbox object.
        """

        id = 'Widget{}'.format(len(self.widgets.keys()))
        new_text_box = widgets.TextBox(id, title,  self.grid, row, column, row_span, column_span, padx, pady, initial_text)
        self.widgets[id] = new_text_box
        if self.selected_widget is None:
            self.set_selected_widget(id)
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

        id = 'Widget{}'.format(len(self.widgets.keys()))
        new_text_block = widgets.ScrollTextBlock(id, title,  self.grid, row, column, row_span, column_span, padx, pady, initial_text)
        self.widgets[id] = new_text_block
        if self.selected_widget is None:
            self.set_selected_widget(id)
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

        id = 'Widget{}'.format(len(self.widgets.keys()))
        new_label = widgets.Label(id, title, self.grid, row, column, row_span, column_span, padx, pady)
        self.widgets[id] = new_label
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

        id = 'Widget{}'.format(len(self.widgets.keys()))
        new_label = widgets.BlockLabel(id, title, self.grid, row, column, row_span, column_span, padx, pady, center)
        self.widgets[id] = new_label
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

        id = 'Widget{}'.format(len(self.widgets.keys()))
        new_button = widgets.Button(id, title, self.grid, row, column, row_span, column_span, padx, pady, command)
        self.widgets[id] = new_button
        if self.selected_widget is None:
            self.set_selected_widget(id)
        return new_button


    # CUI status functions. Used to switch between widgets, set the mode, and 
    # identify neighbors for overview mode

    def check_if_neighbor_exists(self, row, column, row_span, col_span, direction):
        """Function that checks if widget has neighbor in specified cell. 
        
        Used for navigating CUI, as arrow keys find the immediate neighbor

        Parameters
        ----------
        row : int
            row of current widget
        column : int
            column of current widget
        row_span : int
            row span of current widget
        col_span : int
            column span of current widget
        direction : py_cui.keys.KEY_*
            The direction in which to search

        Returns
        -------
        widget_id : str
            The widget neighbor ID if found, None otherwise
        """

        target_row = row
        target_col = column
        if direction == py_cui.keys.KEY_DOWN_ARROW:
            target_row = target_row + row_span
        elif direction == py_cui.keys.KEY_UP_ARROW:
            target_row = target_row - 1
        elif direction == py_cui.keys.KEY_LEFT_ARROW:
            target_col = target_col - 1
        elif direction == py_cui.keys.KEY_RIGHT_ARROW:
            target_col = target_col + col_span
        if target_row < 0 or target_col < 0 or target_row >= self.grid.num_rows or target_col >= self.grid.num_columns:
            return None
        else:
            for widget_id in self.widgets:
                if self.widgets[widget_id].is_row_col_inside(target_row, target_col):
                    return widget_id
            return None


    def set_selected_widget(self, widget_id):
        """Function that sets the selected cell for the CUI

        Parameters
        ----------
        widget_id : str
            the id of the widget
        """

        if widget_id in self.widgets.keys():
            self.selected_widget = widget_id


    def get_widget_id(self, widget):
        """Function for grabbing widget ID

        Parameters
        ----------
        widget : Widget
            The widget object we wish to get an ID from
        
        Returns
        -------
        widget_id : str
            The id if found, None otherwise
        """

        return widget.id


    def lose_focus(self):
        """Function that forces py_cui out of focus mode.
        
        After popup is called, focus is lost
        """

        if self.in_focused_mode:
            self.in_focused_mode = False
            self.status_bar.set_text(self.init_status_bar_text)
            self.widgets[self.selected_widget].selected = False


    def move_focus(self, widget):
        """Moves focus mode to different widget

        Parameters
        ----------
        widget : Widget
            The widget object we want to move focus to.
        """

        self.lose_focus()
        self.set_selected_widget(self.get_widget_id(widget))
        widget.selected = True
        self.in_focused_mode = True
        self.set_status_bar_text(widget.get_help_text())


    def add_key_command(self, key, command):
        """Function that adds a keybinding to the CUI when in overview mode

        Parameters
        ----------
        key : py_cui.keys.KEY_*
            The key bound to the command
        command : Function
            A no-arg or lambda function to fire on keypress
        """

        self.keybindings[key] = command


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

        color=WHITE_ON_BLACK
        self.popup = py_cui.popups.MessagePopup(self, title, text, color, self.renderer)


    def show_warning_popup(self, title, text):
        """Shows a warning popup

        Parameters
        ----------
        title : str
            Warning title
        text : str
            Warning text
        """

        color=YELLOW_ON_BLACK
        self.popup = py_cui.popups.MessagePopup(self, 'WARNING - ' + title, text, color, self.renderer)


    def show_error_popup(self, title, text):
        """Shows an error popup

        Parameters
        ----------
        title : str
            Error title
        text : str
            Error text
        """

        color=RED_ON_BLACK
        self.popup = py_cui.popups.MessagePopup(self, 'ERROR - ' + title, text, color, self.renderer)


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

        color=WHITE_ON_BLACK
        self.popup = py_cui.popups.YesNoPopup(self, title + '- (y/n)', 'Yes - (y), No - (n)', color, command, self.renderer)


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

        color=WHITE_ON_BLACK
        self.popup = py_cui.popups.TextBoxPopup(self, title, color, command, self.renderer, password)
    
    
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

        color=WHITE_ON_BLACK
        self.popup = py_cui.popups.MenuPopup(self, menu_items, title, color, command, self.renderer, run_command_if_none)


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
            self.post_loading_callback = callback
        color = WHITE_ON_BLACK
        self.loading = True
        self.popup = py_cui.popups.LoadingIconPopup(self, title, message, color, self.renderer)


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
            self.post_loading_callback = callback
        color = WHITE_ON_BLACK
        self.loading = True
        self.popup = py_cui.popups.LoadingBarPopup(self, title, num_items, color, self.renderer)


    def increment_loading_bar(self):
        """Increments progress bar if loading bar popup is open
        """

        if self.popup is not None:
            if isinstance(self.popup, py_cui.popups.LoadingBarPopup):
                self.popup.completed_items = self.popup.completed_items + 1


    def stop_loading_popup(self):
        """Leaves loading state, and closes popup.
        
        Must be called by user to escape loading.
        """

        self.loading = False
        self.close_popup()


    def close_popup(self):
        """Closes the popup, and resets focus
        """

        self.lose_focus()
        self.popup = None


    def refresh_height_width(self, height, width):
        """Function that updates the height and width of the CUI based on terminal window size

        Parameters
        ----------
        height : int
            Window height in terminal characters
        width : int
            Window width in terminal characters
        """

        self.width = width
        self.height = height
        self.grid.update_grid_height_width(self.height, self.width)
        for widget_id in self.widgets.keys():
            self.widgets[widget_id].update_height_width()

    # Draw Functions. Function for drawing widgets, status bars, and popups

    def draw_widgets(self):
        """Function that draws all of the widgets to the screen
        """

        for widget_key in self.widgets.keys():
            if widget_key != self.selected_widget:
                self.widgets[widget_key].draw()

        # We draw the selected widget last to support cursor location.
        if self.selected_widget is not None:
            #stdscr.attron(curses.A_BOLD)
            self.widgets[self.selected_widget].draw()
            #stdscr.attroff(curses.A_BOLD)


    def draw_status_bars(self, stdscr, height, width):
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
            stdscr.attron(curses.color_pair(self.status_bar.color))
            stdscr.addstr(height + 3, 0, fit_text(width, self.status_bar.text))
            stdscr.attroff(curses.color_pair(self.status_bar.color))

        if self.title_bar is not None:
            stdscr.attron(curses.color_pair(self.title_bar.color))
            stdscr.addstr(0, 0, fit_text(width, self.title, center=True))
            stdscr.attroff(curses.color_pair(self.title_bar.color))


    def display_window_warning(self, stdscr, error_info):
        """Function that prints some basic error info if there is an error with the CUI

        Parameters
        ----------
        stdscr : curses Standard cursor
            The cursor used to draw the warning
        error_info : str
            The information regarding the error.
        """

        try:
            stdscr.clear()
            stdscr.attron(curses.color_pair(RED_ON_BLACK))
            stdscr.addstr(0, 0, 'Error displaying CUI!!!')
            stdscr.addstr(1, 0, 'Error Type: {}'.format(error_info))
            stdscr.attroff(curses.color_pair(RED_ON_BLACK))
        except KeyboardInterrupt:
            exit()


    def handle_key_presses(self, key_pressed):
        """Function that handles all main loop key presses.

        Parameters
        ----------
        key_pressed : py_cui.keys.KEY_*
            The key being pressed
        """

        # Selected widget represents which widget is being hovered over, though not necessarily in focus mode
        if self.selected_widget is None:
            return
        selected_widget = self.widgets[self.selected_widget]

        # If we are in focus mode, the widget has all of the control of the keyboard except
        # for the escape key, which exits focus mode.
        if self.in_focused_mode and self.popup is None:
            if key_pressed == py_cui.keys.KEY_ESCAPE:
                self.status_bar.set_text(self.init_status_bar_text)
                self.in_focused_mode = False
                selected_widget.selected = False
            else:
                # widget handles remaining py_cui.keys
                selected_widget.handle_key_press(key_pressed)

        # Otherwise, barring a popup, we are in overview mode, meaning that arrow py_cui.keys move between widgets, and Enter key starts focus mode
        elif self.popup is None:
            if key_pressed == py_cui.keys.KEY_ENTER and self.selected_widget is not None and selected_widget.is_selectable:
                self.in_focused_mode = True
                selected_widget.selected = True
                # If autofocus buttons is selected, we automatically process the button command and reset to overview mode
                if self.auto_focus_buttons and isinstance(selected_widget, widgets.Button):
                    self.in_focused_mode = False
                    selected_widget.selected = False
                    if selected_widget.command is not None:
                        selected_widget.command()
                else:
                    self.status_bar.set_text(selected_widget.get_help_text())
            for key in self.keybindings.keys():
                if key_pressed == key:
                    command = self.keybindings[key]
                    command()

            # If not in focus mode, use the arrow py_cui.keys to move around the selectable widgets.
            neighbor = None
            if key_pressed == py_cui.keys.KEY_UP_ARROW or key_pressed == py_cui.keys.KEY_DOWN_ARROW or key_pressed == py_cui.keys.KEY_LEFT_ARROW or key_pressed == py_cui.keys.KEY_RIGHT_ARROW:
                neighbor = self.check_if_neighbor_exists(selected_widget.row, selected_widget.column, selected_widget.row_span, selected_widget.column_span, key_pressed)
            if neighbor is not None:
                selected_widget.selected = False
                self.set_selected_widget(neighbor)

        # if we have a popup, that takes key control from both overview and focus mode
        elif self.popup is not None:
            self.popup.handle_key_press(key_pressed)


    def draw(self, stdscr):
        """Main CUI draw loop called by start()

        Parameters
        ----------
        stdscr : curses Standard cursor
            The cursor used to draw the CUI
        """

        self.stdscr = stdscr
        key_pressed = 0

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.refresh()

        # Initialization functions. Generates colors and renderer
        self.initialize_colors()
        self.initialize_widget_renderer()

        # Loop where key_pressed is the last character pressed. Wait for exit key while no popup or focus mode
        while key_pressed != self.exit_key or self.in_focused_mode or self.popup is not None:

            if self.stopped:
                break

            # Initialization and size adjustment
            stdscr.clear()
            # find height width, adjust if status/title bar added. We decrement the height by 4 to account for status/title bar and padding
            height, width = stdscr.getmaxyx()
            height = height - 4
            width = width
            # This is what allows the CUI to be responsive. Adjust grid size based on current terminal size
            # Resize the grid and the widgets if there was a resize operation
            if key_pressed == curses.KEY_RESIZE:
                try:
                    self.refresh_height_width(height, width)
                except Exception as e:
                    self.display_window_warning(stdscr, str(e))

            # If we have a post_loading_callback, fire it here
            if self.post_loading_callback is not None and not self.loading:
                self.post_loading_callback()
                self.post_loading_callback = None

            # Handle keypresses
            self.handle_key_presses(key_pressed)

            # Draw status/title bar, and all widgets. Selected widget will be bolded.
            self.draw_status_bars(stdscr, height, width)
            self.draw_widgets()
            # draw the popup if required
            if self.popup is not None:
                self.popup.draw()

            # Refresh the screen
            stdscr.refresh()

            # Wait for next input
            if self.loading or self.post_loading_callback is not None:
                # When loading, refresh screen every quarter second
                time.sleep(0.25)
                # Need to reset key_pressed, because otherwise the previously pressed key will be used.
                key_pressed = 0
            elif self.stopped:
                key_pressed = self.exit_key
            else:
                key_pressed = stdscr.getch()

        stdscr.clear()
        stdscr.refresh()
        curses.endwin()
        if self.on_stop is not None:
            self.on_stop()


    def __format__(self, fmt):
        """Override of base format function. Prints list of current widgets.

        Parameters
        ----------
        fmt : Format
            The format to override
        """

        out = ''
        for widget in self.widgets.keys():
            out += '{}\n'.format(self.widgets[widget].title)
        return out