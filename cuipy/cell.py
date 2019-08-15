

class ViewItem:

    def __init__(self, text, size_x, size_y):
        self.text = text
        self.size_x = size_x
        self.size_y = size_y


class Cell:

    def __init__(self, title, pycui_grid, row, column, row_span=1, column_span=1, padx=0, pady=0):
        self.title = title
        self.pycui_grid = pycui_grid
        self.column = column
        self.row = row
        self.row_span = row_span
        self.column_span = column_span
        self.overlap_x = 0
        self.overlap_y = 0
        if self.row + self.row_span == self.pycui_grid.num_rows:
            self.overlap_y = self.pycui_grid.height % self.pycui_grid.num_rows
        if self.column + self.column_span == self.pycui_grid.num_columns - 1:
            self.overlap_x = self.pycui_grid.width % self.pycui_grid.num_columns
        self.padx = padx
        self.pady = pady
        self.wrap = True
        self.highlight = True
        self.full_contents = []
        self.view_contents = []

    def get_absolute_position(self):
        x_pos = self.column * self.pycui_grid.column_width
        y_pos = self.row * self.pycui_grid.row_height
        return x_pos, y_pos


    def get_absolute_dims(self):
        width = self.pycui_grid.column_width * self.column_span + self.overlap_x
        height = self.pycui_grid.row_height * self.row_span + self.overlap_y
        return width, height


    def draw(self, stdscr):
        start_x, start_y = self.get_absolute_position()
        width, height = self.get_absolute_dims()

        stdscr.addstr(start_y, width, '+--{}{}+'.format(self.title, '-' * (width - 4 -len(self.title))))
        counter = 1
        for line in self.view_contents:
            stdscr.addstr(start_y + counter, width, '| {}{}|'.format(line, ' ' * (width-3-len(line))))
            counter = counter + 1
        while counter < height - 1:
            stdscr.addstr(start_y + counter, width, '|{}|'.format(' ' *(width-2)))
            counter = counter + 1
        stdscr.addstr(start_y + height - 1, width, '+{}+'.format('-'*(width-2)))
