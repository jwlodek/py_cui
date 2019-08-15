"""
A python library for creating command line based user interfaces.

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""


# Some python core library imports
import sys
import os
import shutil


# py_cui uses the curses library. On windows this does not exist, but
# there is a open source windows_curses module that adds curses support
# for python on windows
try:
    import curses
except ImportError:
    import windows_curses as curses


# py_cui imports
import py_cui.cell as cell
import py_cui.grid as grid
import py_cui.statusbar as statusbar


# Curses color configuration - rename to use with py_cui
RED     = curses.COLOR_RED
BLACK   = curses.COLOR_BLACK
WHITE   = curses.COLOR_WHITE
BLUE    = curses.COLOR_BLUE
CYAN    = curses.COLOR_CYAN
GREEN   = curses.COLOR_GREEN
YELLOW  = curses.COLOR_YELLOW


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
        self.cells = []
        self.title_bar = None
        self.status_bar = None

        self.keybindings = []
        self.cells.append(cell.Cell('Test', self.grid, 0, 0))
        self.cells[0].view_contents.append('Hello World')
        self.exit_key = ord(exit_key)


    def start(self):

        curses.wrapper(self.draw)

    def add_status_bar(self, text, foreground_color=BLACK, background_color=WHITE):
        self.status_bar = statusbar.StatusBar(text, )


    def reset_cursor(self):
        self.cursor_x = max(0, self.cursor_x)
        self.cursor_x = min(width-1, self.cursor_x)

        self.cursor_y = max(0, self.cursor_y)
        self.cursor_y = min(height-1, self.cursor_y)


    def draw_cell_contents(self, cell, stdscr):
        cell.draw(stdscr)


    def draw(self, stdscr):
        key_pressed = 0

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.refresh()

        # Start colors in curses
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        stdscr.attron(curses.color_pair(4))

        # Loop where k is the last character pressed
        while key_pressed != self.exit_key:

            # Initialization
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            if height != self.height or width != self.width:
                self.width = width
                self.height = height
                self.grid.update_grid_height_width(self.height, self.width)


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

            for cell in self.cells:
                self.draw_cell_contents(cell, stdscr)


            if self.status_bar is not None:
                stdscr.attron(curses.color_pair(3))
                stdscr.addstr(height-1, 0, self.status_bar.text)
                stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
                stdscr.attroff(curses.color_pair(3))

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