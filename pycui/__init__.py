import sys, os, shutil

try:
    import curses
except ImportError:
    import windows_curses as curses

# pycui imports
import pycui.cell as cell
import pycui.grid as grid
import pycui.statusbar as statusbar


# Curses color configuration
RED     = curses.COLOR_RED
BLACK   = curses.COLOR_BLACK
WHITE   = curses.COLOR_WHITE
BLUE    = curses.COLOR_BLUE
CYAN    = curses.COLOR_CYAN
GREEN   = curses.COLOR_GREEN
YELLOW  = curses.COLOR_YELLOW


class PyCUI:

    def __init__(self, exit_key='q'):

        self.cursor_x = 0
        self.cursor_y = 0
        term_size = shutil.get_terminal_size()
        self.grid = grid.Grid(3,3, term_size.lines, term_size.columns)
        self.cells = []
        self.title_bar = None
        self.status_bar = None

        self.keybindings = []
        self.cells.append(cell.Cell('Test', self.grid, 1, 1, row_span=2))
        self.cells[0].view_contents.append('Hello World')

        self.height = 0
        self.width = 0
        self.exit_key = ord(exit_key)


    def pycui_start(self):

        curses.wrapper(self.draw)

    def add_status_bar(self, text, foreground_color=BLACK, background_color=WHITE):
        self.status_bar = statusbar.StatusBar(text, )


    def reset_cursor(self):
        self.cursor_x = max(0, self.cursor_x)
        self.cursor_x = min(width-1, self.cursor_x)

        self.cursor_y = max(0, self.cursor_y)
        self.cursor_y = min(height-1, self.cursor_y)


    def draw_cell_contents(self, cell, stdscr):
        start_x, start_y = cell.get_absolute_position()
        width, height = cell.get_absolute_dims()
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(start_y, width, '+--{}{}+'.format(cell.title, '-' * (width - 4 -len(cell.title))))
        counter = 1
        for line in cell.view_contents:
            stdscr.addstr(start_y + counter, width, '| {}{}|'.format(line, ' ' * (width-3-len(line))))
            counter = counter + 1
        while counter < height - 1:
            stdscr.addstr(start_y + counter, width, '|{}|'.format(' ' *(width-2)))
            counter = counter + 1
        stdscr.addstr(start_y + height - 1, width, '+{}+'.format('-'*(width-2)))
        stdscr.attroff(curses.color_pair(3))


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

        # Loop where k is the last character pressed
        while key_pressed != self.exit_key:

            # Initialization
            stdscr.clear()
            self.height, self.width = stdscr.getmaxyx()


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