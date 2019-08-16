import curses
import py_cui
import py_cui.errors


class Widget:
    """ Top Level Widget Class """

    def __init__(self, title, grid, row, column, row_span, column_span, padx, pady):
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
        self.selected = False
        #self.is_selectable = is_selectable


    def set_standard_color(self, color):
        self.color = color


    def set_selected_color(self, color):
        self.selected_color = color

    def get_absolute_position(self):
        x_pos = self.column * self.grid.column_width
        y_pos = self.row * self.grid.row_height
        return x_pos, y_pos


    def get_absolute_dims(self):
        width = self.grid.column_width * self.column_span + self.overlap_x
        height = self.grid.row_height * self.row_span + self.overlap_y
        return width, height


    def draw(self, stdscr):
        pass


class Label(Widget):

    def __init__(self, title, grid, row, column, row_span, column_span, padx, pady):
        super().__init__(title, grid, row, column, row_span, column_span, padx, pady)
        #self.with_border = with_border

    def draw_with_border(self, stdscr):
        pass

    def draw(self, stdscr):
        stdscr.attron(curses.color_pair(self.color))
        start_x, start_y = self.get_absolute_position()
        width, height = self.get_absolute_dims()
        if False:
            self.draw_w_border(self, stdscr, start_x, start_y, height, width)
        else:
            target_y = start_y + int(height / 2)
            stdscr.addstr(target_y, start_x, self.title.center(width - (2 * self.padx), ' '))
        stdscr.attroff(curses.color_pair(self.color))


class ScrollCell(Widget):

    def __init__(self, title, grid, row, column, row_span, column_span, padx, pady):
        super().__init__(title, grid, row, column, row_span, column_span, padx, pady)
        self.top_view = 0
        self.selected_item = 0
        self.all_lines = []
        self.view_lines = []
        self.all_items = []
        self.view_items = []



    def scroll_up(self):
        if self.selected:
            if self.top_view > 0:
                self.top_view = self.top_view - 1
            if self.selected_item > 0:
                self.selected_item = self.selected_item - 1


    def scroll_down(self):
        _, height = self.get_absolute_dims()
        if self.selected:
            if self.selected_item < len(self.view_items) - 1:
                self.selected_item = self.selected_item + 1
            if self.selected_item > self.top_view + height - (2 * self.pady) - 3:
                self.top_view = self.top_view + 1

    def add_item_to_scroll_cell(self, item_text):
        """
        Adds an item to the cell.

        Parameters
        ----------
        cell_title : str
            The cell title
        item_text : str
            The text for the item
        """

        self.view_items.append(item_text)


    def draw(self, stdscr):
        start_x, start_y = self.get_absolute_position()
        width, height = self.get_absolute_dims()
        stdscr.attron(curses.color_pair(self.color))
        stdscr.addstr(start_y + self.pady, start_x + self.padx, '+--{}{}+'.format(self.title, '-' * (width - 4 - self.padx -len(self.title))))
        counter = self.pady + 1
        line_counter = 0
        for line in self.view_items:
            if line_counter < self.top_view:
                line_counter = line_counter + 1
            else:
                if line_counter == self.selected_item and self.selected:
                    stdscr.attron(curses.color_pair(self.selected_color))
                if counter >= height - self.pady - 1:
                    break
                stdscr.addstr(start_y + counter, start_x + self.padx, '| {}{}|'.format(line, ' ' * (width-3 - self.padx -len(line))))
                counter = counter + 1
                if line_counter == self.selected_item and self.selected:
                    stdscr.attroff(curses.color_pair(self.selected_color))
                line_counter = line_counter + 1
        while counter < height - self.pady - 1:
            stdscr.addstr(start_y + counter, start_x + self.padx, '|{}|'.format(' ' *(width-2 - self.padx)))
            counter = counter + 1
        stdscr.addstr(start_y + height - self.pady - 1, start_x + self.padx, '+{}+'.format('-'*(width-2 - self.padx)))
        stdscr.attroff(curses.color_pair(self.color))


