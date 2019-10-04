"""
A python library for creating command line based user interfaces.

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""

# Some python core library imports
import sys
import os
import time
import shutil       # We use shutil for getting the terminal dimensions
import threading    # Threading isn't currently used, may be removed


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
import py_cui.keybinding as keys
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
    """
    Helper function to fit text within a given width. Used to fix issue with status/title bar text
    being too long and crashing the CUI

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
    """
    Main user interface class for py_cui. To create a user interface, you must first
    create an instance of this class, and then add cells + widgets to it.

    Attributes
    ----------
    cursor_x, cursor_y : int
        absolute position of the cursor in the CUI
    grid : py_cui.grid.Grid
        The main layout manager for the CUI
    cells : list of py_cui.cell.Cell
        list of cells in the grid
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
    start()
        starts the CUI once all of the widgets have been added. Note that you cannot
        add more widgets once this has been run
    add_status_bar(text : str, foreground_color : color, background_color : color)
        function that adds a status bar widget to the CUI
    """

    def __init__(self, num_rows, num_cols, auto_focus_buttons=True, exit_key=keys.KEY_Q_LOWER):

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
        self.init_status_bar_text = 'Press - {} - to exit. Arrow Keys to move between widgets. Enter to enter focus mode.'.format(keys.get_char_from_ascii(exit_key))
        self.status_bar = py_cui.statusbar.StatusBar(self.init_status_bar_text, BLACK_ON_WHITE)

        # Initialize grid, renderer, and widget dict
        self.grid = grid.Grid(num_rows, num_cols, self.height, self.width)
        self.renderer = None
        self.widgets = {}

        # Variables for determining selected widget/focus mode
        self.selected_widget = None
        self.in_focused_mode = False
        self.popup = None
        self.auto_focus_buttons = auto_focus_buttons

        # CUI blocks when loading popup is open
        self.loading = False
        self.stopped = True

        # Top level keybindings. Exit key is 'q' by default
        self.keybindings = {}
        self.exit_key = exit_key

        self.on_stop = None




    # Initialization functions
    # Used to initialzie CUI and its features

    # ----------------------------------------------#
    # Initialization functions                      #
    # Used to initialzie CUI and its features       #
    # ----------------------------------------------#

    def start(self):
        """ Function that starts the CUI """

        self.stopped = False
        curses.wrapper(self.draw)

    def stop(self, callback = None):
        self.stopped = True
        self.on_stop = callback


    def set_title(self, title):
        """ Sets the title bar text """

        self.title = title


    def set_status_bar_text(self, text):
        """ Sets the status bar text when in overview mode """

        self.init_status_bar_text = text
        self.status_bar.set_text(text)


    def initialize_colors(self):
        """ Function for initialzing curses colors. Called when CUI is first created."""

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


    def initialize_widget_renderer(self, stdscr):
        """ Function that creates the renderer object that will draw each widget """

        self.renderer = renderer.Renderer(self, stdscr)
        for widget_id in self.widgets.keys():
            self.widgets[widget_id].assign_renderer(self.renderer)


    # Widget add functions. Each of these adds a particular type of widget to the grid
    # in a specified location.

    def add_scroll_menu(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0):
        """ Function that adds a new scroll menu to the CUI grid """

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


    def set_widget_focus_text(self, widget, text):
        """ Function that sets the text of the status bar when in focus mode for a particular widget """

        if widget is not None and text is not None and isinstance(widget, py_cui.widgets.Widget):
            widget.help_text = text
        else:
            raise py_cui.errors.PyCUIError('Cannot set focus text of non-widget object.')


    # CUI status functions. Used to switch between widgets, set the mode, and 
    # identify neighbors for overview mode

    def check_if_neighbor_exists(self, row, column, row_span, col_span, direction):
        """ Function that checks if widget has neighbor in specified cell. Used for navigating CUI """

        target_row = row
        target_col = column
        if direction == keys.KEY_DOWN_ARROW:
            target_row = target_row + row_span
        elif direction == keys.KEY_UP_ARROW:
            target_row = target_row - 1
        elif direction == keys.KEY_LEFT_ARROW:
            target_col = target_col - 1
        elif direction == keys.KEY_RIGHT_ARROW:
            target_col = target_col + col_span
        if target_row < 0 or target_col < 0 or target_row >= self.grid.num_rows or target_col >= self.grid.num_columns:
            return None
        else:
            for widget_id in self.widgets:
                if self.widgets[widget_id].is_row_col_inside(target_row, target_col):
                    return widget_id
            return None


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


    def lose_focus(self):
        """ Function that forces py_cui out of focus mode. After popup is called, focus is lost """

        if self.in_focused_mode:
            self.in_focused_mode = False
            self.status_bar.set_text(self.init_status_bar_text)
            self.widgets[self.selected_widget].selected = False


    def add_key_binding(self, key, command):
        """ Function that adds a keybinding to the CUI when in overview mode """

        self.keybindings[key] = command


    # Popup functions. Used to display messages, warnings, and errors to the user.

    def show_message_popup(self, title, text):
        """ Shows a message popup """

        color=WHITE_ON_BLACK
        self.popup = py_cui.popups.MessagePopup(self, title, text, color, self.renderer)


    def show_warning_popup(self, title, text):
        """ Shows a warning popup """

        color=YELLOW_ON_BLACK
        self.popup = py_cui.popups.MessagePopup(self, 'WARNING - ' + title, text, color, self.renderer)


    def show_error_popup(self, title, text):
        """ Shows an error popup """

        color=RED_ON_BLACK
        self.popup = py_cui.popups.MessagePopup(self, 'ERROR - ' + title, text, color, self.renderer)


    def show_yes_no_popup(self, title, command):
        """
        Shows a yes/no popup.
        
        The 'command' parameter must be a function with a single boolean parameter
        """

        color=WHITE_ON_BLACK
        self.popup = py_cui.popups.YesNoPopup(self, title + '- (y/n)', 'Yes - (y), No - (n)', color, command, self.renderer)


    def show_text_box_popup(self, title, command):
        """
        Shows a yes/no popup.
        
        The 'command' parameter must be a function with a single boolean parameter
        """

        color=WHITE_ON_BLACK
        self.popup = py_cui.popups.TextBoxPopup(self, title, color, command, self.renderer)
    
    
    def show_menu_popup(self, title, menu_items, command, run_command_if_none=False):
        """
        Shows a yes/no popup.
        
        The 'command' parameter must be a function with a single boolean parameter
        """

        color=WHITE_ON_BLACK
        self.popup = py_cui.popups.MenuPopup(self, menu_items, title, color, command, self.renderer, run_command_if_none)


    def show_loading_icon_popup(self, title, message):
        """ Shows a loading icon popup """
    
        color = WHITE_ON_BLACK
        self.loading = True
        self.popup = py_cui.popups.LoadingIconPopup(self, title, message, color, self.renderer)


    def show_loading_bar_popup(self, title, num_items):
        """ Shows loading bar popup. Use 'increment_loading_bar' to show progress """

        color = WHITE_ON_BLACK
        self.loading = True
        self.popup = py_cui.popups.LoadingBarPopup(self, title, num_items, color, self.renderer)


    def increment_loading_bar(self):
        """ Increments progress bar if loading bar popup is open """

        if self.popup is not None:
            if isinstance(self.popup, py_cui.popups.LoadingBarPopup):
                self.popup.completed_items = self.popup.completed_items + 1


    def stop_loading_popup(self):
        """ Leaves loading state, and closes popup. Must be called by user """

        self.loading = False
        self.close_popup()


    def close_popup(self):
        """ Closes the popup, and resets focus """

        self.lose_focus()
        self.popup = None


    # Draw Functions. Function for drawing widgets, status bars, and popups

    def draw_widgets(self, stdscr):
        """ Function that draws all of the widgets to the screen """

        for widget_key in self.widgets.keys():
            if widget_key != self.selected_widget:
                self.widgets[widget_key].draw()

        # We draw the selected widget last to support cursor location.
        if self.selected_widget is not None:
            #stdscr.attron(curses.A_BOLD)
            self.widgets[self.selected_widget].draw()
            #stdscr.attroff(curses.A_BOLD)


    def draw_status_bars(self, stdscr, height, width):
        """ Draws status bar and title bar """

        if self.status_bar is not None:
            stdscr.attron(curses.color_pair(self.status_bar.color))
            stdscr.addstr(height + 3, 0, fit_text(width, self.status_bar.text))
            stdscr.attroff(curses.color_pair(self.status_bar.color))

        if self.title_bar is not None:
            stdscr.attron(curses.color_pair(self.title_bar.color))
            stdscr.addstr(0, 0, fit_text(width, self.title, center=True))
            stdscr.attroff(curses.color_pair(self.title_bar.color))


    def display_window_warning(self, stdscr, error_info):
            try:
                stdscr.clear()
                stdscr.attron(curses.color_pair(RED_ON_BLACK))
                stdscr.addstr(0, 0, 'Error displaying CUI!!!')
                stdscr.addstr(1, 0, 'Error Type: {}'.format(error_info))
                stdscr.attroff(curses.color_pair(RED_ON_BLACK))
            except KeyboardInterrupt:
                exit()
            except:
                pass

    def handle_key_presses(self, key_pressed):
        """ Function that handles all main loop key presses. """

        # Selected widget represents which widget is being hovered over, though not necessarily in focus mode
        if self.selected_widget is None:
            return
        selected_widget = self.widgets[self.selected_widget]

        # If we are in focus mode, the widget has all of the control of the keyboard except
        # for the escape key, which exits focus mode.
        if self.in_focused_mode and self.popup is None:
            if key_pressed == keys.KEY_ESCAPE:
                self.status_bar.set_text(self.init_status_bar_text)
                self.in_focused_mode = False
                selected_widget.selected = False
            else:
                # widget handles remaining keys
                selected_widget.handle_key_press(key_pressed)

        # Otherwise, barring a popup, we are in overview mode, meaning that arrow keys move between widgets, and Enter key starts focus mode
        elif self.popup is None:
            if key_pressed == keys.KEY_ENTER and self.selected_widget is not None and selected_widget.is_selectable:
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

            # If not in focus mode, use the arrow keys to move around the selectable widgets.
            neighbor = None
            if key_pressed == keys.KEY_UP_ARROW or key_pressed == keys.KEY_DOWN_ARROW or key_pressed == keys.KEY_LEFT_ARROW or key_pressed == keys.KEY_RIGHT_ARROW:
                neighbor = self.check_if_neighbor_exists(selected_widget.row, selected_widget.column, selected_widget.row_span, selected_widget.column_span, key_pressed)
            if neighbor is not None:
                selected_widget.selected = False
                self.set_selected_widget(neighbor)

        # if we have a popup, that takes key control from both overview and focus mode
        elif self.popup is not None:
            self.popup.handle_key_press(key_pressed)


    def draw(self, stdscr):
        """ Main CUI draw loop called by start() """

        key_pressed = 0

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.refresh()

        # Initialization functions. Generates colors and renderer
        self.initialize_colors()
        self.initialize_widget_renderer(stdscr)

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
                    self.width = width
                    self.height = height
                    self.grid.update_grid_height_width(self.height, self.width)
                    for widget_id in self.widgets.keys():
                        self.widgets[widget_id].update_height_width()
                except Exception as e:
                    self.display_window_warning(stdscr, str(e))

            # Handle keypresses
            self.handle_key_presses(key_pressed)

            # Draw status/title bar, and all widgets. Selected widget will be bolded.
            try:
                self.draw_status_bars(stdscr, height, width)
                self.draw_widgets(stdscr)
                # draw the popup if required
                if self.popup is not None:
                    self.popup.draw(stdscr)
            except Exception as e:
                self.display_window_warning(stdscr, str(e))

            # Refresh the screen
            stdscr.refresh()

            # Wait for next input
            if self.loading:
                # When loading, refresh screen every quarter second
                time.sleep(0.25)
                # Need to reset key_pressed, because otherwise the previously pressed key will be used.
                key_pressed = py_cui.keys.KEY_ESCAPE
            elif self.stopped:
                key_pressed = self.exit_key
            else:
                key_pressed = stdscr.getch()

        stdscr.clear()
        stdscr.refresh()
        curses.endwin()
        if self.on_stop is not None:
            self.on_stop()
