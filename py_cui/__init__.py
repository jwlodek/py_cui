"""
A python library for creating command line based user interfaces.

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""

# Some python core library imports
import sys
import os
import shutil       # We use shutil for getting the terminal dimensions


# py_cui uses the curses library. On windows this does not exist, but
# there is a open source windows_curses module that adds curses support
# for python on windows
import curses


# py_cui imports
import py_cui.cell as cell
import py_cui.grid as grid
import py_cui.statusbar as statusbar
import py_cui.errors
import py_cui.widgets as widgets


# Curses color configuration - curses colors automatically work as pairs, so it was easiest to
# create these values as pairs of the bat to be selected. 
# Format is FOREGROUND_ON_BACKGROUND
WHITE_ON_BLACK      = 1
BLACK_ON_GREEN      = 2
BLACK_ON_WHITE      = 3


# PY_CUI directions. Used for mapping cells to each other. When a cell gets mapped as
# attached, to another cell, these directions will link them together via the arrow keys
LEFT    = 0
RIGHT   = 1
UP      = 2
DOWN    = 3


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

    def __init__(self, num_rows, num_cols, exit_key='q'):

        self.cursor_x = 0
        self.cursor_y = 0
        term_size = shutil.get_terminal_size()

        self.height = term_size.lines
        self.width = term_size.columns
        self.grid = grid.Grid(num_rows, num_cols, self.height, self.width)
        self.widgets = {}
        self.title_bar = None
        self.status_bar = None

        self.selected_widget = None

        self.widget_gotos = {}

        self.keybindings = {}
        self.exit_key = ord(exit_key)


    def set_selected_widget(self, widget_title):
        """
        Function that sets the selected cell for the CUI

        Parameters
        ----------
        cell_title : str
            the title of the cell
        """

        if widget_title in self.widgets.keys():
            self.selected_widget = widget_title
            self.widgets[self.selected_widget].selected = True


    def start(self):
        """ Function that starts the CUI """

        curses.wrapper(self.draw)


    def add_scroll_cell(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0):
        """
        Function that adds a new cell to the CUI grid

        Parameters
        ----------
        title : str
            cell title
        row, column : int
            row and column of cell in the grid
        row_span, column_span : int
            how many rows/columns will the cell take up
        padx, pady : int
            padding size in characters
        """


        new_cell = widgets.ScrollCell(title, self.grid, row, column, row_span, column_span, padx, pady)
        self.widgets[title] = new_cell
        if self.selected_widget is None:
            self.set_selected_widget(title)
        return new_cell


    def add_text_box(self):
        pass


    def add_label(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0):
        new_label = widgets.Label(title, self.grid, row, column, row_span, column_span, padx, pady)
        self.widgets[title] = new_label
        return new_label


    def reverse_direction(self, direction):
        """ Function that takes a direction and finds its reverse """

        if direction == UP:
            return DOWN
        elif direction == DOWN:
            return UP
        elif direction == LEFT:
            return RIGHT
        elif direction == RIGHT:
            return LEFT


    def add_goto_widget(self, from_widget_title, to_widget_title, direction):
        """ Function that links cells accross a particular direction via the arrow keys """

        if from_widget_title not in self.widgets.keys() or to_widget_title not in self.widgets.keys():
            raise py_cui.errors.PyCUIMissingChildError("One or more of the selected widgets couldn't be found.")
        #if not self.widgets[from_widget_title].is_selectable or not self.widgets[to_widget_title].is_selectable:
        #    raise py_cui.errors.PyCUIError("One or more of the widgets is not selectable.")

        if from_widget_title not in self.widget_gotos.keys():
            self.widget_gotos[from_widget_title] = ['', '', '', '']
        if to_widget_title not in self.widget_gotos.keys():
            self.widget_gotos[to_widget_title] = ['', '', '', '']
        self.widget_gotos[from_widget_title][direction] = to_widget_title
        self.widget_gotos[to_widget_title][self.reverse_direction(direction)] = from_widget_title


    def add_status_bar(self, text, color=BLACK_ON_WHITE):
        """ Adds a status bar to the CUI """

        self.status_bar = statusbar.StatusBar(text, BLACK_ON_WHITE)

    def add_title_bar(self, text, color=BLACK_ON_WHITE):
        """ Adds a title bar to the CUI """

        self.title_bar = statusbar.StatusBar(text, BLACK_ON_WHITE)


    def draw_widget(self, widget, stdscr):
        """ Function that calls a widget's draw function """

        widget.draw(stdscr)


    def switch_widgets(self, direction):
        """ Function called to switch between widgets """

        if self.selected_widget in self.widget_gotos.keys():
            if self.widget_gotos[self.selected_widget][direction] in self.widgets.keys():
                self.widgets[self.selected_widget].selected = False
                self.set_selected_widget(self.widget_gotos[self.selected_widget][direction])


    def draw(self, stdscr):
        """ Main CUI draw loop called by start() """

        key_pressed = 0

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.refresh()

        # Start colors in curses
        curses.start_color()
        curses.init_pair(WHITE_ON_BLACK, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(BLACK_ON_GREEN, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(BLACK_ON_WHITE, curses.COLOR_BLACK, curses.COLOR_WHITE)
        stdscr.attron(curses.color_pair(4))

        # Loop where k is the last character pressed
        while key_pressed != self.exit_key:

            # Initialization
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            if self.status_bar is not None:
                height = height - 1
            elif self.title_bar is not None:
                height = height - 1
            if height != self.height or width != self.width:
                self.width = width
                self.height = height
                self.grid.update_grid_height_width(self.height, self.width)


            if key_pressed == curses.KEY_PPAGE:
                if self.selected_widget is not None and self.selected_widget in self.widgets.keys():
                    self.widgets[self.selected_widget].scroll_up()
            if key_pressed == curses.KEY_NPAGE:
                if self.selected_widget is not None and self.selected_widget in self.widgets.keys():
                    self.widgets[self.selected_widget].scroll_down()


            if key_pressed == curses.KEY_UP:
                self.switch_widgets(UP)
            if key_pressed == curses.KEY_DOWN:
                self.switch_widgets(DOWN)
            if key_pressed == curses.KEY_LEFT:
                self.switch_widgets(LEFT)
            if key_pressed == curses.KEY_RIGHT:
                self.switch_widgets(RIGHT)

            #self.reset_cursor()


            # Declaration of strings
            #title = "Curses example"[:width-1]
            #subtitle = "Written by Clay McLeod"[:width-1]
            #keystr = "Last key pressed: {}".format(k)[:width-1]
            #statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
            #if k == 0:
            #    keystr = "No key press detected..."[:width-1]

            # Centering calculations
            #start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
            #start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
            #start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
            #start_y = int((height // 2) - 2)

            # Rendering some text
            #whstr = "Width: {}, Height: {}".format(width, height)
            #stdscr.addstr(0, 0, whstr, curses.color_pair(1))




            if self.status_bar is not None:
                stdscr.attron(curses.color_pair(self.status_bar.color))
                stdscr.addstr(height, 0, self.status_bar.text)
                stdscr.addstr(height, len(self.status_bar.text), " " * (width - len(self.status_bar.text) - 1))
                stdscr.attroff(curses.color_pair(self.status_bar.color))

            if self.title_bar is not None:
                stdscr.attron(curses.color_pair(self.title_bar.color))
                stdscr.addstr(height, 0, self.title_bar.text)
                stdscr.addstr(height, len(self.title_bar.text), " " * (width - len(self.title_bar.text) - 1))
                stdscr.attroff(curses.color_pair(self.title_bar.color))

            for widget_key in self.widgets.keys():
                self.draw_widget(self.widgets[widget_key], stdscr)

            #stdscr.attron(curses.color_pair(3))
            #stdscr.addstr(height-1, 0, statusbarstr)
            #stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
            #stdscr.attroff(curses.color_pair(3))

            # Turning on attributes for title
            #stdscr.attron(curses.color_pair(2))
            #stdscr.attron(curses.A_BOLD)

            # Rendering title
            #stdscr.addstr(start_y, start_x_title, title)

            # Turning off attributes for title
            #stdscr.attroff(curses.color_pair(2))
            #stdscr.attroff(curses.A_BOLD)

            # Print rest of text
            #stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
            #stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
            #stdscr.addstr(start_y + 5, start_x_keystr, keystr)
            #stdscr.move(cursor_y, cursor_x)

            # Refresh the screen
            stdscr.refresh()

            # Wait for next input
            key_pressed = stdscr.getch()