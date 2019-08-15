import curses
import py_cui
import py_cui.errors

class ViewItem:

    def __init__(self, text, size_x, size_y):
        self.text = text
        self.size_x = size_x
        self.size_y = size_y
        self.selected = False


class Cell:

    def __init__(self, title, grid, row, column, row_span=1, column_span=1, padx=0, pady=0):
        if grid is None:
            raise py_cui.errors.PyCUIMissingParentError("Cannot add cell to NoneType")
        self.title = title
        self.grid = grid
        if (self.grid.num_columns < column + column_span) or (self.grid.num_rows < row + row_span):
            raise py_cui.errors.PyCUIOutOfBoundsError("Target grid too small")
        self.column = column
        self.row = row
        self.row_span = row_span
        self.column_span = column_span
        self.overlap_x = 0
        self.overlap_y = 0
        if self.row + self.row_span == self.grid.num_rows:
            self.overlap_y = self.grid.height % self.grid.num_rows
        if self.column + self.column_span == self.grid.num_columns:
            self.overlap_x = self.grid.width % self.grid.num_columns
        self.padx = padx
        self.pady = pady
        self.color = py_cui.WHITE_ON_BLACK
        self.selected_color = py_cui.BLACK_ON_GREEN
        self.view_x = 0
        self.view_y = 0
        self.auto_scroll = False
        self.wrap = True
        self.highlight = True
        self.selected = False
        self.all_lines = []
        self.all_items = []
        self.view_lines = []
        self.view_items = []


    def get_absolute_position(self):
        x_pos = self.column * self.grid.column_width
        y_pos = self.row * self.grid.row_height
        return x_pos, y_pos


    def get_absolute_dims(self):
        width = self.grid.column_width * self.column_span + self.overlap_x
        height = self.grid.row_height * self.row_span + self.overlap_y
        return width, height


    def draw(self, stdscr):
        start_x, start_y = self.get_absolute_position()
        width, height = self.get_absolute_dims()
        stdscr.attron(curses.color_pair(self.color))
        stdscr.addstr(start_y + self.pady, start_x + self.padx, '+--{}{}+'.format(self.title, '-' * (width - 4 - self.padx -len(self.title))))
        counter = self.pady + 1
        for line in self.view_lines:
            if counter >= height - self.pady - 1:
                break
            stdscr.addstr(start_y + counter, start_x + self.padx, '| {}{}|'.format(line, ' ' * (width-3 - self.padx -len(line))))
            counter = counter + 1
        while counter < height - self.pady - 1:
            stdscr.addstr(start_y + counter, start_x + self.padx, '|{}|'.format(' ' *(width-2 - self.padx)))
            counter = counter + 1
        stdscr.addstr(start_y + height - self.pady - 1, start_x + self.padx, '+{}+'.format('-'*(width-2 - self.padx)))
        stdscr.attroff(curses.color_pair(self.color))