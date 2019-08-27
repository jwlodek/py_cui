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
            raise py_cui.errors.PyCUIMissingParentError("Cannot add widget to NoneType")
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
            self.overlap_x = self.grid.width % self.grid.num_columns - 1
        self.padx = padx
        self.pady = pady
        self.start_x, self.start_y = self.get_absolute_position()
        self.width, self.height = self.get_absolute_dims()
        self.color = py_cui.WHITE_ON_BLACK
        self.selected_color = py_cui.BLACK_ON_GREEN
        self.selected = False
        self.is_selectable = selectable
        self.help_text = 'No help text available.'
        self.key_commands = {}


    def set_focus_text(self, text):
        """ Function that sets the text of the status bar on focus for a particular widget """

        self.help_text = text


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

        if isinstance(renderer, py_cui.renderer.Renderer):
            self.renderer = renderer
        else:
            raise py_cui.errors.PyCUIError('Invalid renderer, must be of type py_cui.renderer.Renderer')


    def get_absolute_position(self):
        """ Gets the absolute position of the widget in characters """

        x_pos = self.column * self.grid.column_width
        # Always add one to the y_pos, because we have a title bar
        y_pos = self.row * self.grid.row_height + 2
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

        return self.help_text


    def handle_key_press(self, key_pressed):
        """ Base class function that handles all assigned key presses """

        if key_pressed in self.key_commands.keys():
            command = self.key_commands[key_pressed]
            command()


    def draw(self):
        """ Base class draw class that checks if renderer is valid """

        if self.renderer is None:
            return


class Label(Widget):
    """ The most basic subclass of Widget. Simply displays one centered row of text """

    def __init__(self, id, title,  grid, row, column, row_span, column_span, padx, pady):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady, selectable=False)


    def draw(self):
        """ Override base draw class. Center text and draw it """

        super().draw()
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
        self.help_text = 'Focus mode on ScrollCell. Use up/down to scroll, Enter to trigger command, Esc to exit.'


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
        if self.selected_item >= len(self.view_items):
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


    def handle_key_press(self, key_pressed):
        """ Override base class function. UP_ARROW scrolls up, DOWN_ARROW scrolls down """

        super().handle_key_press(key_pressed)
        if key_pressed == py_cui.keys.KEY_UP_ARROW:
            self.scroll_up()
        if key_pressed == py_cui.keys.KEY_DOWN_ARROW:
            self.scroll_down()


    def draw(self):
        """ Overrides base class draw function """

        super().draw()
        self.renderer.set_color_mode(self.color)
        self.renderer.draw_border(self)
        counter = self.pady + 1
        line_counter = 0
        for line in self.view_items:
            if line_counter < self.top_view:
                line_counter = line_counter + 1
            else:
                if line_counter == self.selected_item:
                    self.renderer.set_color_mode(self.selected_color)
                if counter >= self.height - self.pady - 1:
                    break
                self.renderer.draw_text(self, line, self.start_y + counter)
                counter = counter + 1
                if line_counter == self.selected_item:
                    self.renderer.unset_color_mode(self.selected_color)
                line_counter = line_counter + 1
        self.renderer.unset_color_mode(self.color)
        self.renderer.reset_cursor(self)


class CheckBoxMenu(ScrollMenu):
    
    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, checked_char):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)

        self.selected_item_list = []
        self.checked_char = checked_char
        self.help_text = 'Focus mode on CheckBoxMenu. Use up/down to scroll, Enter to toggle set, unset, Esc to exit.'

    def add_item(self, item_text):
        item_text = '[ ] - ' + item_text
        super().add_item(item_text)

    def add_item_list(self, item_list):
        for item in item_list:
            self.add_item(item)

    def handle_key_press(self, key_pressed):
        super().handle_key_press(key_pressed)
        if key_pressed == py_cui.keys.KEY_ENTER:
            if super().get() in self.selected_item_list:
                self.selected_item_list.remove(super().get())
                self.view_items[self.selected_item] = '[ ] - ' + self.view_items[self.selected_item][6:]
            else:
                self.view_items[self.selected_item] = '[{}] - '.format(self.checked_char) + self.view_items[self.selected_item][6:]
                self.selected_item_list.append(self.view_items[self.selected_item])

    def get(self):
        ret = []
        for item in self.selected_item_list:
            ret.append(item[6:])
        return ret


class TextBox(Widget):

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, initial_text):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)
        self.text = initial_text
        self.cursor_x = self.start_x + padx + 2
        self.cursor_text_pos = 0
        self.cursor_max_left = self.cursor_x
        self.cursor_max_right = self.start_x + self.width - padx - 1
        self.cursor_y = self.start_y + int(self.height / 2) + 1
        self.help_text = 'Focus mode on TextBox. Press Esc to exit focus mode.'
        self.viewport_width = self.cursor_max_right - self.cursor_max_left

    def set_text(self, text):
        self.text = text
        if len(self.text) < self.cursor_text_pos:
            diff = self.cursor_text_pos - len(self.text)
            self.cursor_text_pos = len(self.text)
            self.cursor_x = self.cursor_x - diff


    def get(self):
        return self.text


    def clear(self):
        self.cursor_x = self.start_x + self.padx + 2
        self.cursor_text_pos = 0
        self.text = ''


    def move_left(self):
        if  self.cursor_text_pos > 0:
            if self.cursor_x > self.cursor_max_left:
                self.cursor_x = self.cursor_x - 1
            self.cursor_text_pos = self.cursor_text_pos - 1

    def move_right(self):
        if self.cursor_text_pos < len(self.text):
            if self.cursor_x < self.cursor_max_right:
                self.cursor_x = self.cursor_x + 1
            self.cursor_text_pos = self.cursor_text_pos + 1

    def insert_char(self, key_pressed):
        self.set_text(self.text[:self.cursor_text_pos] + chr(key_pressed) + self.text[self.cursor_text_pos:])
        if len(self.text) <= self.width - 2 * self.padx - 4:
            self.cursor_x = self.cursor_x + 1
        self.cursor_text_pos = self.cursor_text_pos + 1

    def jump_to_start(self):
        self.cursor_x = self.start_x + self.padx + 2
        self.cursor_text_pos = 0

    def jump_to_end(self):
        self.cursor_text_pos = len(self.text)
        self.cursor_x = self.start_x + self.padx + 2 + self.cursor_text_pos
    
    def erase_char(self):
        self.set_text(self.text[:self.cursor_text_pos - 1] + self.text[self.cursor_text_pos:])
        if len(self.text) <= self.width - 2 * self.padx - 4:
            self.cursor_x = self.cursor_x - 1
        self.cursor_text_pos = self.cursor_text_pos - 1


    def handle_key_press(self, key_pressed):
        super().handle_key_press(key_pressed)
        if key_pressed == py_cui.keys.KEY_LEFT_ARROW:
            self.move_left()
        elif key_pressed == py_cui.keys.KEY_RIGHT_ARROW:
            self.move_right()
        elif key_pressed == py_cui.keys.KEY_BACKSPACE and self.cursor_text_pos > 0:
            self.erase_char()
        elif key_pressed == py_cui.keys.KEY_HOME:
            self.jump_to_start()
        elif key_pressed == py_cui.keys.KEY_END:
            self.jump_to_end()
        elif key_pressed > 31 and key_pressed < 128:
            self.insert_char(key_pressed)


    def draw(self):
        super().draw()

        self.renderer.set_color_mode(self.color)
        self.renderer.draw_text(self, self.title, self.cursor_y - 2, bordered=False)
        self.renderer.draw_border(self, fill=False, with_title=False)
        render_text = self.text
        if len(self.text) > self.width - 2 * self.padx - 4:
            end = len(self.text) - (self.width - 2 * self.padx - 4)
            if self.cursor_text_pos < end:
                render_text = self.text[self.cursor_text_pos:self.cursor_text_pos + (self.width - 2 * self.padx - 4)]
            else:
                render_text = self.text[end:]
        self.renderer.draw_text(self, render_text, self.cursor_y)

        if self.selected:
            self.renderer.draw_cursor(self.cursor_y, self.cursor_x)
        else:
            self.renderer.reset_cursor(self, fill=False)
        self.renderer.unset_color_mode(self.color)


class Button(Widget):

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, command):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)
        self.command = command
        self.color = py_cui.MAGENTA_ON_BLACK
        self.help_text = 'Focus mode on Button. Press Enter to press button, Esc to exit focus mode.'


    def handle_key_press(self, key_pressed):
        super().handle_key_press(key_pressed)
        if key_pressed == 10:
            self.selected_color = py_cui.WHITE_ON_RED
            if self.command is not None:
                ret = self.command()
            self.selected_color = py_cui.BLACK_ON_GREEN
            return ret


    def draw(self):

        super().draw()
        if self.selected:
            self.renderer.set_color_mode(self.selected_color)
        else:
            self.renderer.set_color_mode(self.color)
        self.renderer.draw_border(self, with_title=False)
        button_text_y_pos = self.start_y + int(self.height / 2)
        self.renderer.draw_text(self, self.title, button_text_y_pos, centered=True)
        self.renderer.reset_cursor(self)
        if self.selected:
            self.renderer.unset_color_mode(self.selected_color)
        else:
            self.renderer.unset_color_mode(self.color)


class ScrollTextBlock(Widget):
    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, initial_text):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)
        self.text_lines = initial_text.splitlines()
        if len(self.text_lines) == 0:
            self.text_lines.append('')
        self.cursor_y = self.start_y + 1
        self.cursor_x = self.start_x + padx + 2
        self.viewport_y_start = 0
        self.cursor_text_pos_x = 0
        self.cursor_text_pos_y = 0
        self.cursor_max_up = self.cursor_y
        self.cursor_max_down = self.start_y + self.height - pady - 2
        self.cursor_max_left = self.cursor_x
        self.cursor_max_right = self.start_x + self.width - padx - 1
        self.help_text = 'Focus mode on TextBlock. Press Esc to exit focus mode.'


    def set_text(self, text):
        self.text_lines = text.splitlines()
        if len(self.text_lines) == 0:
            self.text_lines.append('')
        self.cursor_text_pos_y = 0
        self.cursor_y = self.cursor_max_up


    def set_text_line(self, text):
        self.text_lines[self.cursor_text_pos_y] = text

    def get(self):
        text = ''
        for line in self.text_lines:
            text = '{}{}\n'.format(text, line)
        return text

    def clear(self):
        self.cursor_x = self.cursor_max_left
        self.cursor_y = self.cursor_max_up
        self.cursor_text_pos_x = 0
        self.cursor_text_pos_y = 0
        self.text_lines = []
        self.text_lines.append('')


    def handle_key_press(self, key_pressed):
        super().handle_key_press(key_pressed)
        current_line = self.text_lines[self.cursor_text_pos_y]

        if key_pressed == py_cui.keys.KEY_LEFT_ARROW and self.cursor_text_pos_x > 0:
            if self.cursor_x > self.cursor_max_left:
                self.cursor_x = self.cursor_x - 1
            self.cursor_text_pos_x = self.cursor_text_pos_x - 1

        elif key_pressed == py_cui.keys.KEY_RIGHT_ARROW and self.cursor_text_pos_x < len(current_line):
            if self.cursor_x < self.cursor_max_right:
                self.cursor_x = self.cursor_x + 1
            self.cursor_text_pos_x = self.cursor_text_pos_x + 1

        elif key_pressed == py_cui.keys.KEY_UP_ARROW and self.cursor_text_pos_y > 0:
            if self.cursor_y > self.cursor_max_up:
                self.cursor_y = self.cursor_y - 1
            self.cursor_text_pos_y = self.cursor_text_pos_y - 1
            if self.cursor_text_pos_x > len(self.text_lines[self.cursor_text_pos_y]):
                temp = len(self.text_lines[self.cursor_text_pos_y])
                self.cursor_x = self.cursor_x - (self.cursor_text_pos_x - temp)
                self.cursor_text_pos_x = temp

        elif key_pressed == py_cui.keys.KEY_DOWN_ARROW and self.cursor_text_pos_y < len(self.text_lines) - 1:
            if self.cursor_y < self.cursor_max_down:
                self.cursor_y = self.cursor_y + 1
            else:
                self.viewport_y_start = self.viewport_y_start + 1
            self.cursor_text_pos_y = self.cursor_text_pos_y + 1
            if self.cursor_text_pos_x > len(self.text_lines[self.cursor_text_pos_y]):
                temp = len(self.text_lines[self.cursor_text_pos_y])
                self.cursor_x = self.cursor_x - (self.cursor_text_pos_x - temp)
                self.cursor_text_pos_x = temp


        elif key_pressed == py_cui.keys.KEY_BACKSPACE and self.cursor_text_pos_x > 0:
            if current_line == '':
                self.text_lines = self.text_lines[:self.cursor_text_pos_y] + self.text_lines[self.cursor_text_pos_y + 1:]
                self.cursor_text_pos_y = self.cursor_text_pos_y - 1
                self.cursor_y = self.cursor_y - 1
                self.cursor_text_pos_x = len(self.text_lines[self.cursor_text_pos_y]) - 1
                self.cursor_x = self.cursor_max_left + self.cursor_text_pos_x
            else:
                self.set_text_line(current_line[:self.cursor_text_pos_x - 1] + current_line[self.cursor_text_pos_x:])
                if len(current_line) <= self.width - 2 * self.padx - 4:
                    self.cursor_x = self.cursor_x - 1
                self.cursor_text_pos_x = self.cursor_text_pos_x - 1
        
        elif key_pressed == py_cui.keys.KEY_ENTER:
            current_line = self.text_lines[self.cursor_text_pos_y]
            new_line_1 = current_line[:self.cursor_text_pos_x]
            new_line_2 = current_line[self.cursor_text_pos_x:]
            self.text_lines[self.cursor_text_pos_y] = new_line_1
            self.text_lines.insert(self.cursor_text_pos_y + 1, new_line_2)
            self.cursor_text_pos_y = self.cursor_text_pos_y + 1
            self.cursor_text_pos_x = 0
            self.cursor_x = self.cursor_max_left
            self.cursor_y = self.cursor_y + 1

        elif key_pressed == py_cui.keys.KEY_HOME:
            loc_x, _ = self.get_absolute_position()
            self.cursor_x = self.cursor_max_left
            self.cursor_text_pos_x = 0

        elif key_pressed == py_cui.keys.KEY_END:
            self.cursor_text_pos_x = len(current_line)
            loc_x, _ = self.get_absolute_position()
            self.cursor_x = loc_x + self.padx + 2 + self.cursor_text_pos_x
        
        elif key_pressed > 31 and key_pressed < 128:
            self.set_text_line(current_line[:self.cursor_text_pos_x] + chr(key_pressed) + current_line[self.cursor_text_pos_x:])
            if len(current_line) <= self.width - 2 * self.padx - 4:
                self.cursor_x = self.cursor_x + 1
            self.cursor_text_pos_x = self.cursor_text_pos_x + 1


    def draw(self):
        super().draw()

        self.renderer.set_color_mode(self.color)
        self.renderer.draw_border(self)
        counter = self.cursor_max_up
        for line_counter in range(self.viewport_y_start, self.viewport_y_start + self.height - 2):
            if line_counter == len(self.text_lines):
                break
            render_text = self.text_lines[line_counter]
            self.renderer.draw_text(self, render_text, counter)
            counter = counter + 1
        if self.selected:
            self.renderer.draw_cursor(self.cursor_y, self.cursor_x)
        else:
            self.renderer.reset_cursor(self, fill=False)
        self.renderer.unset_color_mode(self.color)
