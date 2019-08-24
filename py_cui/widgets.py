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
        self.renderer = None
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
        self.start_x, self.start_y = self.get_absolute_position()
        self.width, self.height = self.get_absolute_dims()
        self.color = py_cui.WHITE_ON_BLACK
        self.selected_color = py_cui.BLACK_ON_GREEN
        self.selected = False
        self.is_selectable = selectable
        self.key_commands = {}


    def add_key_command(self, key, command):
        """
        Maps a keycode to a function that will be executed when in focus mode

        Parameters
        ----------
        key : py_cui.keys.KEY
            ascii keycode used to map the key
        command : function without args
            a non-argument function or lambda function to execute if in focus mode and key is pressed
        """

        self.key_commands[key] = command


    def set_standard_color(self, color):
        """ Sets the standard color for the widget """

        self.color = color

    def set_selected_color(self, color):
        """ Sets the selected color for the widget """

        self.selected_color = color

    def assign_renderer(self, renderer):
        """ Function that assigns a renderer object to the widget """

        self.renderer = renderer


    def get_absolute_position(self):
        """ Gets the absolute position of the widget in characters """

        x_pos = self.column * self.grid.column_width
        y_pos = self.row * self.grid.row_height
        return x_pos, y_pos


    def get_absolute_dims(self):
        """ Gets the absolute dimensions of the widget in characters """

        self.width = self.grid.column_width * self.column_span + self.overlap_x
        self.height = self.grid.row_height * self.row_span + self.overlap_y
        return self.width, self.height


    def is_row_col_inside(self, row, col):
        """ Checks if a particular row + column is inside the widget area """

        if self.row <= row and row <= (self.row + self.row_span - 1) and self.column <= col and col <= (self.column_span + self.column - 1):
            return True
        else:
            return False

    # BELOW FUNCTIONS SHOULD BE OVERWRITTEN BY SUB-CLASSES

    def get_help_text(self):
        """ Returns help text """

        return 'No help text available.'


    def handle_key_press(self, key_pressed):
        """ Base class function that handles all assigned key presses """

        if key_pressed in self.key_commands.keys():
            command = self.key_commands[key_pressed]
            command()


    def draw(self, stdscr):
        """ Base class draw class that checks if renderer is valid """

        if self.renderer is None:
            return


class Label(Widget):
    """ The most basic subclass of Widget. Simply displays one row of text """

    def __init__(self, id, title,  grid, row, column, row_span, column_span, padx, pady):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady, selectable=False)


    def draw(self):
        """ Override base draw class. Center text and draw it """

        self.renderer.set_color_mode(self.color)
        target_y = self.start_y + int(self.height / 2)
        self.renderer.draw_text(self, self.title, target_y, centered=True, bordered=False)
        self.renderer.unset_color_mode(self.color)


class ScrollMenu(Widget):

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
        if self.selected:
            if self.selected_item < len(self.view_items) - 1:
                self.selected_item = self.selected_item + 1
            if self.selected_item > self.top_view + self.height - (2 * self.pady) - 3:
                self.top_view = self.top_view + 1


    def add_item(self, item_text):
        """
        Adds an item to the cell.

        Parameters
        ----------
        item_text : str
            The text for the item
        """

        self.view_items.append(item_text)


    def add_item_list(self, item_list):
        """
        Adds a list of items to the scroll menu.

        Parameters
        ----------
        item_list : list of str
            list of strings to add as items to the scrollmenu
        """

        for item in item_list:
            self.add_item(item)


    def remove_selected_item(self):
        """ Function that removes the selected item from the scroll menu. """

        del self.view_items[self.selected_item]
        if self.selected_item > len(self.view_items):
            self.selected_item = self.selected_item - 1


    def get_item_list(self):
        """
        Function that gets list of items in a scroll menu

        Returns
        -------
        item_list : list of str
            list of items in the scrollmenu
        """

        return self.view_items

    def get(self):
        """
        Function that gets the selected item from the list

        Returns
        -------
        item : str
            selected item, or None if there are no items in the menu
        """
        
        if self.selected_item < len(self.view_items):
            return self.view_items[self.selected_item]
        return None


    def get_help_text(self):
        return 'Focus mode on ScrollCell. Use up/down to scroll, Enter to trigger command, Esc to exit.'


    def handle_key_press(self, key_pressed):
        """ Override base class function. UP_ARROW scrolls up, DOWN_ARROW scrolls down """

        super().handle_key_press(key_pressed)
        if key_pressed == py_cui.keys.KEY_UP_ARROW:
            self.scroll_up()
        if key_pressed == py_cui.keys.KEY_DOWN_ARROW:
            self.scroll_down()


    def draw(self, stdscr):
        """ Overrides base class draw function """

        stdscr.attron(curses.color_pair(self.color))
        self.draw_border_top(stdscr)
        counter = self.pady + 1
        line_counter = 0
        for line in self.view_items:
            if line_counter < self.top_view:
                line_counter = line_counter + 1
            else:
                if line_counter == self.selected_item:
                    stdscr.attron(curses.color_pair(self.selected_color))
                if counter >= self.height - self.pady - 1:
                    break
                
                counter = counter + 1
                if line_counter == self.selected_item:
                    stdscr.attroff(curses.color_pair(self.selected_color))
                line_counter = line_counter + 1
        while counter < self.height - self.pady - 1:
            self.draw_blank_row(stdscr, self.start_y + counter)
            counter = counter + 1
        self.draw_border_bottom(stdscr)
        stdscr.attroff(curses.color_pair(self.color))


class TextBox(Widget):

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, initial_text):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)
        self.text = initial_text
        self.cursor_x = self.start_x + padx + 2
        self.cursor_text_pos = 0
        self.cursor_max_left = self.cursor_x
        self.cursor_max_right = self.start_x + self.width - padx - 1
        self.cursor_y = self.start_y + int(self.height / 2) + 1

    def set_text(self, text):
        self.text = text


    def get(self):
        return self.text


    def get_help_text(self):
        return 'Focus mode on TextBox. Press Esc to exit focus mode.'

    def clear(self):
        self.cursor_x = self.start_x + self.padx + 2
        self.cursor_text_pos = 0
        self.text = ''


    def handle_key_press(self, key_pressed):
        super().handle_key_press(key_pressed)
        if key_pressed == py_cui.keys.KEY_LEFT_ARROW and self.cursor_text_pos > 0:
            if self.cursor_x > self.cursor_max_left:
                self.cursor_x = self.cursor_x - 1
            self.cursor_text_pos = self.cursor_text_pos - 1
        elif key_pressed == py_cui.keys.KEY_RIGHT_ARROW and self.cursor_text_pos < len(self.text):
            if self.cursor_x < self.cursor_max_right:
                self.cursor_x = self.cursor_x + 1
            self.cursor_text_pos = self.cursor_text_pos + 1
        elif key_pressed == 8 and self.cursor_text_pos > 0:
            self.set_text(self.text[:self.cursor_text_pos - 1] + self.text[self.cursor_text_pos:])
            if len(self.text) <= self.width - 2 * self.padx - 4:
                self.cursor_x = self.cursor_x - 1
            self.cursor_text_pos = self.cursor_text_pos - 1
        elif key_pressed == py_cui.keys.KEY_HOME:
            loc_x, loc_y = self.get_absolute_position()
            self.cursor_x = loc_x + self.padx + 2
            self.cursor_text_pos = 0
        elif key_pressed == py_cui.keys.KEY_END:
            self.cursor_text_pos = len(self.text)
            loc_x, loc_y = self.get_absolute_position()
            self.cursor_x = loc_x + self.padx + 2 + self.cursor_text_pos
        
        elif key_pressed > 31 and key_pressed < 128:
            self.set_text(self.text[:self.cursor_text_pos] + chr(key_pressed) + self.text[self.cursor_text_pos:])
            if len(self.text) <= self.width - 2 * self.padx - 4:
                self.cursor_x = self.cursor_x + 1
            self.cursor_text_pos = self.cursor_text_pos + 1


    def draw(self, stdscr):
        stdscr.attron(curses.color_pair(self.color))
        stdscr.addstr(self.cursor_y - 2, self.start_x + self.padx, '{}'.format(self.title))
        stdscr.addstr(self.cursor_y - 1, self.start_x + self.padx, '+-{}-+'.format('-' * (self.width - 4 - self.padx)))
        render_text = self.text
        if len(self.text) > self.width - 2 * self.padx - 4:
            end = len(self.text) - (self.width - 2 * self.padx - 4)
            if self.cursor_text_pos < end:
                render_text = self.text[self.cursor_text_pos:self.cursor_text_pos + (self.width - 2 * self.padx - 4)]
            else:
                render_text = self.text[end:]
        stdscr.addstr(self.cursor_y, self.start_x + self.padx, '| {}{} |'.format(render_text, ' ' * (self.width - 4 - self.padx - len(self.text))))
        stdscr.addstr(self.cursor_y + 1, self.start_x + self.padx, '+-{}-+'.format('-' * (self.width - 4 - self.padx)))
        if self.selected:
            stdscr.move(self.cursor_y, self.cursor_x)
        stdscr.attroff(curses.color_pair(self.color))


class Button(Widget):

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, command):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)
        self.command = command
        self.color = py_cui.MAGENTA_ON_BLACK


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
        self.start_x, self.start_y = self.get_absolute_position()
        self.width, self.height = self.get_absolute_dims()
        target_y = self.start_y + int(self.height / 2)
        stdscr.addstr(self.start_y + self.pady, self.start_x + self.padx, '+-{}-+'.format('-' * (self.width - 4 - self.padx)))
        if self.selected:
            stdscr.attron(curses.color_pair(self.selected_color))
        for i in range(self.start_y + self.pady + 1, target_y):
            stdscr.addstr(i, self.start_x + self.padx, '|{}|'.format(' ' * (self.width - 2 - self.padx)))
        stdscr.addstr(target_y, self.start_x + self.padx, '|{}|'.format(self.title.center(self.width - self.padx - 2, ' ')))
        for i in range(target_y + 1, self.start_y + self.height - self.pady):
            stdscr.addstr(i, self.start_x + self.padx, '|{}|'.format(' ' * (self.width - 2 - self.padx)))
        if self.selected:
            stdscr.attroff(curses.color_pair(self.selected_color))
        stdscr.addstr(self.start_y + self.height - self.pady, self.start_x + self.padx, '+-{}-+'.format('-' * (self.width - 4 - self.padx)))
        stdscr.attroff(curses.color_pair(self.color))


class ScrollTextBlock(Widget):
    pass