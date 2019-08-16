"""
File contatining all widget classes for py_cui. Widgets are the basic
building blocks of a user interface made with py_cui

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""


import curses
import py_cui
import py_cui.errors


class Widget:
    """ Top Level Widget Class """

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, selectable = True):
        if grid is None:
            raise py_cui.errors.PyCUIMissingParentError("Cannot add cell to NoneType")
        self.id = id
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
        self.is_selectable = selectable
        self.key_commands = {}


    def add_key_command(self, key, command):
        self.key_commands[ord(key)] = command

    def set_standard_color(self, color):
        self.color = color


    def set_selected_color(self, color):
        self.selected_color = color

    def get_absolute_position(self):
        x_pos = self.column * self.grid.column_width
        y_pos = self.row * self.grid.row_height
        if self.grid.has_title_bar:
            y_pos = y_pos + 1
        return x_pos, y_pos


    def get_absolute_dims(self):
        width = self.grid.column_width * self.column_span + self.overlap_x
        height = self.grid.row_height * self.row_span + self.overlap_y
        return width, height

    def is_row_col_inside(self, row, col):
        if self.row <= row and row <= (self.row + self.row_span - 1) and self.column <= col and col <= (self.column_span + self.column - 1):
            return True
        else:
            return False

    def get_help_text(self):
        return 'No help text available.'


    def handle_key_press(self, key_pressed):
        if key_pressed in self.key_commands.keys():
            temp = self.key_commands[key_pressed]
            temp()


    def draw(self, stdscr):
        pass


class Label(Widget):

    def __init__(self, id, title,  grid, row, column, row_span, column_span, padx, pady):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady, selectable=False)

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

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)
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

    def add_item(self, item_text):
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


    def add_item_list(self, item_list):
        for item in item_list:
            self.add_item(item)


    def remove_selected_item(self):
        del self.view_items[self.selected_item]
        if self.selected_item > len(self.view_items):
            self.selected_item = self.selected_item - 1

    def get_item_list(self):
        return self.view_items

    def get(self):
        
        if self.selected_item < len(self.view_items):
            return self.view_items[self.selected_item]
        return None


    def get_help_text(self):
        return 'Focus mode on ScrollCell. Use up/down to scroll, Enter to trigger command, Esc to exit.'


    def handle_key_press(self, key_pressed):
        super().handle_key_press(key_pressed)
        if key_pressed == curses.KEY_UP:
            self.scroll_up()
        if key_pressed == curses.KEY_DOWN:
            self.scroll_down()


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
                if line_counter == self.selected_item:
                    stdscr.attron(curses.color_pair(self.selected_color))
                if counter >= height - self.pady - 1:
                    break
                stdscr.addstr(start_y + counter, start_x + self.padx, '| {}{}|'.format(line, ' ' * (width-3 - self.padx -len(line))))
                counter = counter + 1
                if line_counter == self.selected_item:
                    stdscr.attroff(curses.color_pair(self.selected_color))
                line_counter = line_counter + 1
        while counter < height - self.pady - 1:
            stdscr.addstr(start_y + counter, start_x + self.padx, '|{}|'.format(' ' *(width-2 - self.padx)))
            counter = counter + 1
        stdscr.addstr(start_y + height - self.pady - 1, start_x + self.padx, '+{}+'.format('-'*(width-2 - self.padx)))
        stdscr.attroff(curses.color_pair(self.color))


class TextBox(Widget):

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, initial_text):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)
        self.text = initial_text
        width, height = self.get_absolute_dims()
        loc_x, loc_y = self.get_absolute_position()
        self.cursor_x = loc_x + padx + 2
        self.cursor_text_pos = 0
        self.cursor_max_left = self.cursor_x
        self.cursor_max_right = loc_x + width - padx - 1
        self.cursor_y = loc_y + int(height / 2) + 1

    def set_text(self, text):
        self.text = text


    def get(self):
        return self.text


    def get_help_text(self):
        return 'Focus mode on TextBox. Press Esc to exit focus mode.'

    def clear(self):
        loc_x, loc_y = self.get_absolute_position()
        self.cursor_x = loc_x + self.padx + 2
        self.cursor_text_pos = 0
        self.text = ''


    def handle_key_press(self, key_pressed):
        super().handle_key_press(key_pressed)
        if key_pressed == curses.KEY_LEFT and self.cursor_x > self.cursor_max_left:
            self.cursor_x = self.cursor_x - 1
            self.cursor_text_pos = self.cursor_text_pos - 1
        elif key_pressed == curses.KEY_RIGHT and self.cursor_x < self.cursor_max_right and self.cursor_text_pos < len(self.text):
            self.cursor_x = self.cursor_x + 1
            self.cursor_text_pos = self.cursor_text_pos + 1
        elif key_pressed == curses.KEY_BACKSPACE and self.cursor_text_pos > 0:
            self.set_text(self.text[:self.cursor_text_pos - 1] + self.text[self.cursor_text_pos:])
            self.cursor_x = self.cursor_x - 1
            self.cursor_text_pos = self.cursor_text_pos - 1
        elif key_pressed == curses.KEY_HOME:
            loc_x, loc_y = self.get_absolute_position()
            self.cursor_x = loc_x + self.padx + 2
            self.cursor_text_pos = 0
        elif key_pressed == curses.KEY_END:
            self.cursor_text_pos = len(self.text)
            loc_x, loc_y = self.get_absolute_position()
            self.cursor_x = loc_x + self.padx + 2 + self.cursor_text_pos
        
        elif key_pressed > 31 and key_pressed < 128:
            self.set_text(self.text[:self.cursor_text_pos] + chr(key_pressed) + self.text[self.cursor_text_pos:])
            self.cursor_x = self.cursor_x + 1
            self.cursor_text_pos = self.cursor_text_pos + 1


    def draw(self, stdscr):
        start_x, start_y = self.get_absolute_position()
        width, height = self.get_absolute_dims()
        stdscr.attron(curses.color_pair(self.color))
        stdscr.addstr(self.cursor_y - 2, start_x + self.padx, '{}'.format(self.title))
        stdscr.addstr(self.cursor_y - 1, start_x + self.padx, '+-{}-+'.format('-' * (width - 4 - self.padx)))
        stdscr.addstr(self.cursor_y, start_x + self.padx, '| {}{} |'.format(self.text, ' ' * (width - 4 - self.padx - len(self.text))))
        stdscr.addstr(self.cursor_y + 1, start_x + self.padx, '+-{}-+'.format('-' * (width - 4 - self.padx)))
        if self.selected:
            stdscr.move(self.cursor_y, self.cursor_x)
        stdscr.attroff(curses.color_pair(self.color))


class Button(Widget):

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, command):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)
        self.command = command
        self.color = py_cui.CYAN_ON_BLACK


    def get_help_text(self):
        return 'Focus mode on Button. Press Enter to press button, Esc to exit focus mode.'


    def handle_key_press(self, key_pressed):
        super().handle_key_press(key_pressed)
        if key_pressed == 10:
            self.selected_color = py_cui.WHITE_ON_RED
            if self.command is not None:
                ret = self.command()
            self.selected_color = py_cui.BLACK_ON_GREEN
            return ret


    def draw(self, stdscr):
        stdscr.attron(curses.color_pair(self.color))
        start_x, start_y = self.get_absolute_position()
        width, height = self.get_absolute_dims()
        target_y = start_y + int(height / 2)
        stdscr.addstr(start_y + self.pady, start_x + self.padx, '+-{}-+'.format('-' * (width - 4 - self.padx)))
        if self.selected:
            stdscr.attron(curses.color_pair(self.selected_color))
        for i in range(start_y + self.pady + 1, target_y):
            stdscr.addstr(i, start_x + self.padx, '|{}|'.format(' ' * (width - 2 - self.padx)))
        stdscr.addstr(target_y, start_x + self.padx, '|{}|'.format(self.title.center(width - self.padx - 2, ' ')))
        for i in range(target_y + 1, start_y + height - self.pady):
            stdscr.addstr(i, start_x + self.padx, '|{}|'.format(' ' * (width - 2 - self.padx)))
        if self.selected:
            stdscr.attroff(curses.color_pair(self.selected_color))
        stdscr.addstr(start_y + height - self.pady, start_x + self.padx, '+-{}-+'.format('-' * (width - 4 - self.padx)))
        stdscr.attroff(curses.color_pair(self.color))