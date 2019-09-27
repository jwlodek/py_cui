"""
File contatining all core widget classes for py_cui. Widgets are the basic
building blocks of a user interface made with py_cui. This file contains classes for:

* Base Widget class
* Label
* Scroll Menu
* Checkbox Menu
* Button
* TextBox
* Text Block

Additional widgets should be added in as additional_widgets/$WIDGET_NAME.py, importing this
file and extending the base Widget class, or if appropriate one of the other core widgets.

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""


import curses
import py_cui
import py_cui.colors
import py_cui.errors


class Widget:
    """ Top Level Widget Base Class """

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
        #self.overlap_x = 0
        #self.overlap_y = 0
        #if self.row + self.row_span == self.grid.num_rows:
        #    self.overlap_y = self.grid.height % self.grid.num_rows
        #if self.column + self.column_span == self.grid.num_columns:
        #    self.overlap_x = self.grid.width % self.grid.num_columns - 1
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
        self.text_color_rules = []


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


    def add_text_color_rule(self, regex_list, color, rule_type, match_type='line', region=[0,1], include_whitespace=False):
        """
        Forces renderer to draw text using given color if text_condition_function returns True

        Parameters
        ----------
        rule_type : string
            A supported color rule type
        regex : str
            A string to check against the line for a given rule type
        color : int
            a supported py_cui color value
        match_entire_line : bool
            if true, if regex fits rule type, entire line will be colored. If false, only matching text
        """

        self.text_color_rules.append(py_cui.colors.ColorRule(regex_list, color, rule_type, match_type, region, include_whitespace))



    def set_standard_color(self, color):
        """ Sets the standard color for the widget """

        self.color = color


    def set_selected_color(self, color):
        """ Sets the selected color for the widget """

        self.selected_color = color


    def assign_renderer(self, renderer):
        """ Function that assigns a renderer object to the widget (Meant for internal usage only) """

        if isinstance(renderer, py_cui.renderer.Renderer):
            self.renderer = renderer
        else:
            raise py_cui.errors.PyCUIError('Invalid renderer, must be of type py_cui.renderer.Renderer')


    def get_absolute_position(self):
        """ Gets the absolute position of the widget in characters """

        x_adjust = self.column
        y_adjust = self.row
        if self.column > self.grid.offset_x:
            x_adjust = self.grid.offset_x
        if self.row > self.grid.offset_y:
            y_adjust = self.grid.offset_y

        x_pos = self.column * self.grid.column_width + x_adjust
        # Always add two to the y_pos, because we have a title bar + a pad row
        y_pos = self.row * self.grid.row_height + 2 + y_adjust
        return x_pos, y_pos


    def get_absolute_dims(self):
        """ Gets the absolute dimensions of the widget in characters """

        width = self.grid.column_width * self.column_span
        height = self.grid.row_height * self.row_span
        counter = self.row
        while counter < self.grid.offset_y and (counter - self.row) < self.row_span:
            height = height + 1
            counter = counter + 1
        counter = self.column
        while counter < self.grid.offset_x and (counter - self.column) < self.column_span:
            width = width + 1
            counter = counter + 1
        return width, height


    def is_row_col_inside(self, row, col):
        """ Checks if a particular row + column is inside the widget area """

        if self.row <= row and row <= (self.row + self.row_span - 1) and self.column <= col and col <= (self.column_span + self.column - 1):
            return True
        else:
            return False


    # BELOW FUNCTIONS SHOULD BE OVERWRITTEN BY SUB-CLASSES


    def update_height_width(self):
        """ Function that refreshes position and dimensons on resize. If necessary, make sure required widget attributes updated here as well."""

        self.start_x, self.start_y = self.get_absolute_position()
        self.width, self.height = self.get_absolute_dims()


    def get_help_text(self):
        """ Returns help text """

        return self.help_text


    def handle_key_press(self, key_pressed):
        """
        Base class function that handles all assigned key presses.
        When overwriting this function, make sure to add a super().handle_key_press(key_pressed) call,
        as this is required for user defined key command support
        """

        if key_pressed in self.key_commands.keys():
            command = self.key_commands[key_pressed]
            command()


    def draw(self):
        """ Base class draw class that checks if renderer is valid. Should be called with super().draw() in overrides """

        if self.renderer is None:
            return
        else:
            self.renderer.set_color_rules(self.text_color_rules)


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
    """ A scroll menu widget. Allows for creating a scrollable list of items of which one is selectable. Analogous to a RadioButton """

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)
        self.top_view = 0
        self.selected_item = 0
        self.all_lines = []
        self.view_lines = []
        self.all_items = []
        self.view_items = []
        self.help_text = 'Focus mode on ScrollMenu. Use up/down to scroll, Enter to trigger command, Esc to exit.'


    def clear(self):
        """ Clears all items from the Scroll Menu """

        self.view_items = []
        self.selected_item = 0
        self.top_view = 0


    def scroll_up(self):
        """ Function that scrolls the view up in the scroll menu """

        if self.selected:
            if self.top_view > 0:
                self.top_view = self.top_view - 1
            if self.selected_item > 0:
                self.selected_item = self.selected_item - 1


    def scroll_down(self):
        """ Function that scrolls the view down in the scroll menu """

        if self.selected:
            if self.selected_item < len(self.view_items) - 1:
                self.selected_item = self.selected_item + 1
            if self.selected_item > self.top_view + self.height - (2 * self.pady) - 3:
                self.top_view = self.top_view + 1


    def add_item(self, item_text):
        """
        Adds an item to the menu.

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

        if len(self.view_items) == 0:
            return
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
        Function that gets the selected item from the scroll menu

        Returns
        -------
        item : str
            selected item, or None if there are no items in the menu
        """
        
        if len(self.view_items) > 0:
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
                if counter >= self.height - self.pady - 1:
                    break
                if line_counter == self.selected_item:
                    self.renderer.draw_text(self, line, self.start_y + counter, selected=True)
                else:
                    self.renderer.draw_text(self, line, self.start_y + counter)
                counter = counter + 1
                line_counter = line_counter + 1
        self.renderer.unset_color_mode(self.color)
        self.renderer.reset_cursor(self)


class CheckBoxMenu(ScrollMenu):
    """ Extension of ScrollMenu that allows for multiple items to be selected at once. """

    
    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, checked_char):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)

        self.selected_item_list = []
        self.checked_char = checked_char
        self.help_text = 'Focus mode on CheckBoxMenu. Use up/down to scroll, Enter to toggle set, unset, Esc to exit.'

    def add_item(self, item_text):
        """ Adds item to Checkbox """

        item_text = '[ ] - ' + item_text
        super().add_item(item_text)


    def add_item_list(self, item_list):
        """ Adds list of items to the checkbox """

        for item in item_list:
            self.add_item(item)


    def get(self):
        """ Gets list of selected items from the checkbox """

        ret = []
        for item in self.selected_item_list:
            ret.append(item[6:])
        return ret


    def mark_item_as_checked(self, text):
        """ Function that marks an item as selected """

        self.selected_item_list.append(text)


    def handle_key_press(self, key_pressed):
        """ Override of key presses. First, run the superclass function, scrolling should still work. Adds Enter command to toggle selection """

        super().handle_key_press(key_pressed)
        if key_pressed == py_cui.keys.KEY_ENTER:
            if super().get() in self.selected_item_list:
                self.selected_item_list.remove(super().get())
                self.view_items[self.selected_item] = '[ ] - ' + self.view_items[self.selected_item][6:]
            else:
                self.view_items[self.selected_item] = '[{}] - '.format(self.checked_char) + self.view_items[self.selected_item][6:]
                self.selected_item_list.append(self.view_items[self.selected_item])



class Button(Widget):
    """ Basic button widget. Allows for running a command function on Enter """

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, command):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)
        self.command = command
        self.color = py_cui.MAGENTA_ON_BLACK
        self.help_text = 'Focus mode on Button. Press Enter to press button, Esc to exit focus mode.'


    def handle_key_press(self, key_pressed):
        """ Override of base class, adds ENTER listener that runs the button's command """

        super().handle_key_press(key_pressed)
        if key_pressed == py_cui.keys.KEY_ENTER:
            self.selected_color = py_cui.WHITE_ON_RED
            if self.command is not None:
                ret = self.command()
            self.selected_color = py_cui.BLACK_ON_GREEN
            return ret


    def draw(self):
        """ Override of base class draw function """

        super().draw()
        if self.selected:
            self.renderer.set_color_mode(self.selected_color)
        else:
            self.renderer.set_color_mode(self.color)
        self.renderer.draw_border(self, with_title=False)
        button_text_y_pos = self.start_y + int(self.height / 2)
        self.renderer.draw_text(self, self.title, button_text_y_pos, centered=True, selected=self.selected)
        self.renderer.reset_cursor(self)
        if self.selected:
            self.renderer.unset_color_mode(self.selected_color)
        else:
            self.renderer.unset_color_mode(self.color)



class TextBox(Widget):
    """ Widget for entering small single lines of text """

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


    def update_height_width(self):
        """ Need to update all cursor positions on resize """

        super().update_height_width()
        self.cursor_y = self.start_y + int(self.height / 2) + 1
        self.cursor_x = self.start_x + self.padx + 2
        self.cursor_text_pos = 0
        self.cursor_max_right = self.start_x + self.width - self.padx - 1
        self.cursor_max_left = self.cursor_x
        self.viewport_width = self.cursor_max_right - self.cursor_max_left


    def set_text(self, text):
        """ Sets the value of the text. Overwrites existing text """

        self.text = text
        if self.cursor_text_pos > len(self.text):
            diff = self.cursor_text_pos - len(self.text)
            self.cursor_text_pos = len(self.text)
            self.cursor_x = self.cursor_x - diff

    def get(self):
        """ Gets value of the text in the textbox """

        return self.text


    def clear(self):
        """ Clears the text in the textbox """

        self.cursor_x = self.cursor_max_left
        self.cursor_text_pos = 0
        self.text = ''


    def move_left(self):
        """ Shifts the cursor the the left. Internal use only """

        if  self.cursor_text_pos > 0:
            if self.cursor_x > self.cursor_max_left:
                self.cursor_x = self.cursor_x - 1
            self.cursor_text_pos = self.cursor_text_pos - 1


    def move_right(self):
        """ Shifts the cursor the the right. Internal use only """
        if self.cursor_text_pos < len(self.text):
            if self.cursor_x < self.cursor_max_right:
                self.cursor_x = self.cursor_x + 1
            self.cursor_text_pos = self.cursor_text_pos + 1

    def insert_char(self, key_pressed):
        """ Inserts char at cursor position. Internal use only """
        self.text = self.text[:self.cursor_text_pos] + chr(key_pressed) + self.text[self.cursor_text_pos:]
        if len(self.text) < self.viewport_width:
            self.cursor_x = self.cursor_x + 1
        self.cursor_text_pos = self.cursor_text_pos + 1


    def jump_to_start(self):
        """ Jumps to the start of the textbox """

        self.cursor_x = self.start_x + self.padx + 2
        self.cursor_text_pos = 0


    def jump_to_end(self):
        """ Jumps to the end to the textbox """

        self.cursor_text_pos = len(self.text)
        self.cursor_x = self.start_x + self.padx + 2 + self.cursor_text_pos


    def erase_char(self):
        """ Erases character at textbox cursor """

        if self.cursor_text_pos > 0:
            self.text = self.text[:self.cursor_text_pos - 1] + self.text[self.cursor_text_pos:]
            if len(self.text) < self.width - 2 * self.padx - 4:
                self.cursor_x = self.cursor_x - 1
            self.cursor_text_pos = self.cursor_text_pos - 1



    def handle_key_press(self, key_pressed):
        """ Override of base handle key press function """

        super().handle_key_press(key_pressed)
        if key_pressed == py_cui.keys.KEY_LEFT_ARROW:
            self.move_left()
        elif key_pressed == py_cui.keys.KEY_RIGHT_ARROW:
            self.move_right()
        elif key_pressed == py_cui.keys.KEY_BACKSPACE:
            self.erase_char()
        elif key_pressed == py_cui.keys.KEY_HOME:
            self.jump_to_start()
        elif key_pressed == py_cui.keys.KEY_END:
            self.jump_to_end()
        elif key_pressed > 31 and key_pressed < 128:
            self.insert_char(key_pressed)


    def draw(self):
        """ Override of base draw function """
        
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
        self.renderer.draw_text(self, render_text, self.cursor_y, selected=self.selected)

        if self.selected:
            self.renderer.draw_cursor(self.cursor_y, self.cursor_x)
        else:
            self.renderer.reset_cursor(self, fill=False)
        self.renderer.unset_color_mode(self.color)


class ScrollTextBlock(Widget):
    """ Widget for editing large multi-line blocks of text """

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, initial_text):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)
        self.text_lines = initial_text.splitlines()
        if len(self.text_lines) == 0:
            self.text_lines.append('')
        self.cursor_y = self.start_y + 1
        self.cursor_x = self.start_x + padx + 2
        self.viewport_y_start = 0
        self.viewport_x_start = 0
        self.cursor_text_pos_x = 0
        self.cursor_text_pos_y = 0
        self.cursor_max_up = self.cursor_y
        self.cursor_max_down = self.start_y + self.height - pady - 2
        self.cursor_max_left = self.cursor_x
        self.cursor_max_right = self.start_x + self.width - padx - 1
        self.viewport_width = self.cursor_max_right - self.cursor_max_left
        self.help_text = 'Focus mode on TextBlock. Press Esc to exit focus mode.'


    def update_height_width(self):

        super().update_height_width()
        self.viewport_y_start = 0
        self.viewport_x_start = 0
        self.cursor_text_pos_x = 0
        self.cursor_text_pos_y = 0
        self.cursor_y = self.start_y + 1
        self.cursor_x = self.start_x + self.padx + 2
        self.cursor_max_up = self.cursor_y
        self.cursor_max_down = self.start_y + self.height - self.pady - 2
        self.cursor_max_left = self.cursor_x
        self.cursor_max_right = self.start_x + self.width - self.padx - 1
        self.viewport_width = self.cursor_max_right - self.cursor_max_left


    def get(self):
        """ Gets all of the text in the textblock and returns it """

        text = ''
        for line in self.text_lines:
            text = '{}{}\n'.format(text, line)
        return text


    def write(self, text):
        """ Function used for writing text to the text block """

        lines = text.splitlines()
        if len(self.text_lines) == 1 and self.text_lines[0] == '':
            self.set_text(text)
        else:
            self.text_lines.append(lines)


    def clear(self):
        """ Function that clears the text block """

        self.cursor_x = self.cursor_max_left
        self.cursor_y = self.cursor_max_up
        self.cursor_text_pos_x = 0
        self.cursor_text_pos_y = 0
        self.text_lines = []
        self.text_lines.append('')



    def set_text(self, text):
        """
        Function that sets the text for the textblock. Note that this will overwrite any existing text 

        Parameters
        ----------
        text : str
            text to write into text block
        """

        self.text_lines = text.splitlines()
        if len(self.text_lines) == 0:
            self.text_lines.append('')
        self.cursor_text_pos_y = 0
        self.cursor_y = self.cursor_max_up
        self.viewport_y_start = 0
        self.cursor_x = self.cursor_max_left
        self.cursor_text_pos_x = 0


    def set_text_line(self, text):
        """ Function that sets the current line's text. Meant only for internal use """

        self.text_lines[self.cursor_text_pos_y] = text


    def move_left(self, current_line):
        """ Function that moves the cursor/text position one location to the left """

        if self.cursor_text_pos_x > 0:
            if self.cursor_x > self.cursor_max_left:
                self.cursor_x = self.cursor_x - 1
            elif self.viewport_x_start > 0:
                self.viewport_x_start = self.viewport_x_start - 1
            self.cursor_text_pos_x = self.cursor_text_pos_x - 1

    def move_right(self, current_line):
        """ Function that moves the cursor/text position one location to the right """

        if self.cursor_text_pos_x < len(current_line):
            if self.cursor_x < self.cursor_max_right:
                self.cursor_x = self.cursor_x + 1
            elif self.viewport_x_start + self.width - 2 * self.padx - 4 < len(current_line):
                self.viewport_x_start = self.viewport_x_start + 1
            self.cursor_text_pos_x = self.cursor_text_pos_x + 1


    def move_up(self, current_line):
        """ Function that moves the cursor/text position one location up """

        if self.cursor_text_pos_y > 0:
            if self.cursor_y > self.cursor_max_up:
                self.cursor_y = self.cursor_y - 1
            elif self.viewport_y_start > 0:
                self.viewport_y_start = self.viewport_y_start - 1
            self.cursor_text_pos_y = self.cursor_text_pos_y - 1
            if self.cursor_text_pos_x > len(self.text_lines[self.cursor_text_pos_y]):
                temp = len(self.text_lines[self.cursor_text_pos_y])
                self.cursor_x = self.cursor_x - (self.cursor_text_pos_x - temp)
                self.cursor_text_pos_x = temp


    def move_down(self, current_line):
        """ Function that moves the cursor/text position one location down """

        if self.cursor_text_pos_y < len(self.text_lines) - 1:
            if self.cursor_y < self.cursor_max_down:
                self.cursor_y = self.cursor_y + 1
            elif self.viewport_y_start + self.height - 2 < len(self.text_lines):
                self.viewport_y_start = self.viewport_y_start + 1
            self.cursor_text_pos_y = self.cursor_text_pos_y + 1
            if self.cursor_text_pos_x > len(self.text_lines[self.cursor_text_pos_y]):
                temp = len(self.text_lines[self.cursor_text_pos_y])
                self.cursor_x = self.cursor_x - (self.cursor_text_pos_x - temp)
                self.cursor_text_pos_x = temp


    def handle_newline(self, current_line):
        """ Function that handles recieving newline characters in the text """

        current_line = self.text_lines[self.cursor_text_pos_y]
        new_line_1 = current_line[:self.cursor_text_pos_x]
        new_line_2 = current_line[self.cursor_text_pos_x:]
        self.text_lines[self.cursor_text_pos_y] = new_line_1
        self.text_lines.insert(self.cursor_text_pos_y + 1, new_line_2)
        self.cursor_text_pos_y = self.cursor_text_pos_y + 1
        self.cursor_text_pos_x = 0
        self.cursor_x = self.cursor_max_left
        if self.cursor_y < self.cursor_max_down:
            self.cursor_y = self.cursor_y + 1
        elif self.viewport_y_start + self.height - 2 < len(self.text_lines):
            self.viewport_y_start = self.viewport_y_start + 1


    def handle_backspace(self, current_line):
        """ Function that handles recieving backspace characters in the text """

        if self.cursor_text_pos_x == 0 and self.cursor_text_pos_y != 0:
            self.cursor_text_pos_x = len(self.text_lines[self.cursor_text_pos_y - 1])
            self.text_lines[self.cursor_text_pos_y - 1] = self.text_lines[self.cursor_text_pos_y - 1] + self.text_lines[self.cursor_text_pos_y]
            self.text_lines = self.text_lines[:self.cursor_text_pos_y] + self.text_lines[self.cursor_text_pos_y + 1:]
            self.cursor_text_pos_y = self.cursor_text_pos_y - 1
            self.cursor_x = self.cursor_max_left + self.cursor_text_pos_x
            if self.cursor_y > self.cursor_max_up:
                self.cursor_y = self.cursor_y - 1
            elif self.viewport_y_start > 0:
                self.viewport_y_start = self.viewport_y_start - 1
        elif self.cursor_text_pos_x > 0:
            self.set_text_line(current_line[:self.cursor_text_pos_x - 1] + current_line[self.cursor_text_pos_x:])
            if len(current_line) <= self.width - 2 * self.padx - 4:
                self.cursor_x = self.cursor_x - 1
            self.cursor_text_pos_x = self.cursor_text_pos_x - 1


    def handle_home(self, current_line):
        """ Function that handles recieving a home keypress """

        self.cursor_x = self.cursor_max_left
        self.cursor_text_pos_x = 0
        self.viewport_x_start = 0


    def handle_end(self, current_line):
        """ Function that handles recieving an end keypress """

        self.cursor_text_pos_x = len(current_line)
        if len(current_line) > self.viewport_width:
            self.cursor_x = self.cursor_max_right
            self.viewport_x_start = self.cursor_text_pos_x - self.viewport_width
        else:
            self.cursor_x = self.cursor_max_left + len(current_line)


    def handle_delete(self, current_line):
        """ Function that handles recieving a delete keypress """

        if self.cursor_text_pos_x == len(current_line) and self.cursor_text_pos_y < len(self.text_lines):
            self.text_lines[self.cursor_text_pos_y] = self.text_lines[self.cursor_text_pos_y] + self.text_lines[self.cursor_text_pos_y + 1]
            self.text_lines = self.text_lines[:self.cursor_text_pos_y+1] + self.text_lines[self.cursor_text_pos_y + 2:]
        elif self.cursor_text_pos_x < len(current_line):
            self.set_text_line(current_line[:self.cursor_text_pos_x] + current_line[self.cursor_text_pos_x+1:])


    def insert_char(self, current_line, key_pressed):
        """ Function that handles recieving a character """

        self.set_text_line(current_line[:self.cursor_text_pos_x] + chr(key_pressed) + current_line[self.cursor_text_pos_x:])
        if len(current_line) <= self.width - 2 * self.padx - 4:
            self.cursor_x = self.cursor_x + 1
        elif self.viewport_x_start + self.width - 2 * self.padx - 4 < len(current_line):
            self.viewport_x_start = self.viewport_x_start + 1
        self.cursor_text_pos_x = self.cursor_text_pos_x + 1


    def handle_key_press(self, key_pressed):
        """ Override of base class handle key press function """

        super().handle_key_press(key_pressed)

        # The current line on which the user's cursor is located
        current_line = self.text_lines[self.cursor_text_pos_y]

        if key_pressed == py_cui.keys.KEY_LEFT_ARROW:
            self.move_left(current_line)
        elif key_pressed == py_cui.keys.KEY_RIGHT_ARROW:
            self.move_right(current_line)
        elif key_pressed == py_cui.keys.KEY_UP_ARROW:
            self.move_up(current_line)
        elif key_pressed == py_cui.keys.KEY_DOWN_ARROW and self.cursor_text_pos_y < len(self.text_lines) - 1:
            self.move_down(current_line)
        elif key_pressed == py_cui.keys.KEY_BACKSPACE:
            self.handle_backspace(current_line)
        elif key_pressed == py_cui.keys.KEY_DELETE:
            self.handle_delete(current_line)
        elif key_pressed == py_cui.keys.KEY_ENTER:
            self.handle_newline(current_line)
        elif key_pressed == py_cui.keys.KEY_TAB:
            for i in range(0, 4):
                self.insert_char(current_line, py_cui.keys.KEY_SPACE)
        elif key_pressed == py_cui.keys.KEY_HOME:
            self.handle_home(current_line)
        elif key_pressed == py_cui.keys.KEY_END:
            self.handle_end(current_line)
        elif key_pressed > 31 and key_pressed < 128:
            self.insert_char(current_line, key_pressed)


    def draw(self):
        """ Override of base class draw function """

        super().draw()

        self.renderer.set_color_mode(self.color)
        self.renderer.draw_border(self)
        counter = self.cursor_max_up
        for line_counter in range(self.viewport_y_start, self.viewport_y_start + self.height - 2):
            if line_counter == len(self.text_lines):
                break
            render_text = self.text_lines[line_counter]
            self.renderer.draw_text(self, render_text, counter, start_pos=self.viewport_x_start, selected=self.selected)
            counter = counter + 1
        if self.selected:
            self.renderer.draw_cursor(self.cursor_y, self.cursor_x)
        else:
            self.renderer.reset_cursor(self)
        self.renderer.unset_color_mode(self.color)
