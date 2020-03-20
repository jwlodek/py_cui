"""File contatining all core widget classes for py_cui.

Widgets are the basic building blocks of a user interface made with py_cui.
This file contains classes for:

* Base Widget class
* Label
* Block Label
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
import py_cui.ui
import py_cui.colors
import py_cui.errors


class Widget(py_cui.ui.UIElement):
    """Top Level Widget Base Class

    Extended by all widgets. Contains base classes for handling key presses, drawing,
    and setting status bar text.

    Attributes
    ----------
    grid : py_cui.grid.Grid
        The parent grid object of the widget
    row, column : int
        row and column position of the widget
    row_span, column_span : int
        number of rows or columns spanned by the widget
    padx, pady : int
        Padding size in terminal characters
    start_x, start_y : int
        The position on the terminal of the top left corner of the widget
    width, height : int
        The width/height of the widget
    selected_color : int
        color code combination for when widget is selected
    is_selectable : bool
        Flag that says if a widget can be selected
    key_commands : dict
        Dictionary mapping key codes to functions
    text_color_rules : list of py_cui.ColorRule
        color rules to load into renderer when drawing widget
    """

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger, selectable = True):
        """Constructor for base widget class
        """

        super().__init__(id, title, None, logger)
        if grid is None:
            raise py_cui.errors.PyCUIMissingParentError("Cannot add widget to NoneType")
        
        self._grid = grid
        grid_rows, grid_cols = self._grid.get_dimensions()
        if (grid_cols < column + column_span) or (grid_rows < row + row_span):
            raise py_cui.errors.PyCUIOutOfBoundsError("Target grid too small for widget {}".format(title))
        
        self._row          = row
        self._column       = column
        self._row_span     = row_span
        self._column_span  = column_span
        self._padx         = padx
        self._pady         = pady
        self._selectable       = selectable
        self._key_commands     = {}
        self._text_color_rules = []
        self.update_height_width()


    def add_key_command(self, key, command):
        """Maps a keycode to a function that will be executed when in focus mode

        Parameters
        ----------
        key : py_cui.keys.KEY
            ascii keycode used to map the key
        command : function without args
            a non-argument function or lambda function to execute if in focus mode and key is pressed
        """

        self._key_commands[key] = command


    def add_text_color_rule(self, regex, color, rule_type, match_type='line', region=[0,1], include_whitespace=False):
        """Forces renderer to draw text using given color if text_condition_function returns True

        Parameters
        ----------
        regex : str
            A string to check against the line for a given rule type
        color : int
            a supported py_cui color value
        rule_type : string
            A supported color rule type
        match_type='line' : str
            sets match type. Can be 'line', 'regex', or 'region'
        region : [int, int]
            A specified region to color if using match_type='region'
        include_whitespace : bool
            if false, strip string before checking for match
        """

        new_color_rule = py_cui.colors.ColorRule(regex, color, rule_type, match_type, region, include_whitespace, self._logger)
        self._text_color_rules.append(new_color_rule)


    def get_absolute_start_pos(self):
        """Gets the absolute position of the widget in characters

        Returns
        -------
        x_pos, y_pos : int
            position of widget in terminal
        """

        x_adjust                = self._column
        y_adjust                = self._row
        offset_x, offset_y      = self._grid.get_offsets()
        row_height, col_width   = self._grid.get_cell_dimensions()
        
        if self._column > offset_x:
            x_adjust = offset_x
        if self._row > offset_y:
            y_adjust = offset_y

        x_pos = self._column * col_width + x_adjust
        # Always add two to the y_pos, because we have a title bar + a pad row
        y_pos = self._row * row_height + 2 + y_adjust
        return x_pos, y_pos


    def get_absolute_stop_pos(self):
        """Gets the absolute dimensions of the widget in characters

        Returns
        -------
        width, height : int
            dimensions of widget in terminal
        """

        offset_x, offset_y      = self._grid.get_offsets()
        row_height, col_width   = self._grid.get_cell_dimensions()

        width   = col_width     * self._column_span
        height  = row_height    * self._row_span
        
        counter = self._row
        while counter < offset_y and (counter - self._row) < self._row_span:
            height  = height    + 1
            counter = counter   + 1
        
        counter = self._column
        while counter < offset_x and (counter - self._column) < self._column_span:
            width   = width     + 1
            counter = counter   + 1
        
        return width + self._start_x, height + self._start_y


    def get_grid_cell(self):
        return self._row, self._column


    def get_grid_cell_spans(self):
        return self._row_span, self._column_span

    def is_selectable(self):
        return self._selectable


    def _is_row_col_inside(self, row, col):
        """Checks if a particular row + column is inside the widget area

        Parameters
        ----------
        row, col : int
            row and column position to check

        Returns
        -------
        is_inside : bool
            True if row, col is within widget bounds, false otherwise
        """

        is_within_rows  = self._row    <= row and row <= (self._row           + self._row_span   - 1)
        is_within_cols  = self._column <= col and col <= (self._column_span   + self._column     - 1)

        if is_within_rows and is_within_cols:
            return True
        else:
            return False


    # BELOW FUNCTIONS SHOULD BE OVERWRITTEN BY SUB-CLASSES


    def _handle_key_press(self, key_pressed):
        """Base class function that handles all assigned key presses.

        When overwriting this function, make sure to add a super().handle_key_press(key_pressed) call,
        as this is required for user defined key command support

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """

        if key_pressed in self._key_commands.keys():
            command = self._key_commands[key_pressed]
            command()


    def _draw(self):
        """Base class draw class that checks if renderer is valid.

        Should be called with super().draw() in overrides
        """

        if self._renderer is None:
            return
        else:
            self._renderer.set_color_rules(self._text_color_rules)


class Label(Widget):
    """The most basic subclass of Widget.

    Simply displays one centered row of text. Has no unique attributes or methods

    Attributes
    ----------
    draw_border : bool
        Toggle for drawing label border
    """

    def __init__(self, id, title,  grid, row, column, row_span, column_span, padx, pady, logger):
        """Constructor for Label
        """

        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady, logger, selectable=False)
        self._draw_border = False


    def toggle_border(self):
        """Function that gives option to draw border around label
        """

        self._draw_border = not self._draw_border


    def _draw(self):
        """Override base draw class.

        Center text and draw it
        """

        super()._draw()
        self._renderer.set_color_mode(self._color)
        if self._draw_border:
            self._renderer.draw_border(self, with_title=False)
        target_y = self._start_y + int(self._height / 2)
        self._renderer.draw_text(self, self._title, target_y, centered=True, bordered=self._draw_border)
        self._renderer.unset_color_mode(self._color)


class BlockLabel(Widget):
    """A Variation of the label widget that renders a block of text.

    Attributes
    ----------
    lines : list of str
        list of lines that make up block text
    center : bool
        Decides whether or not label should be centered
    """

    def __init__(self, id, title,  grid, row, column, row_span, column_span, padx, pady, center, logger):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady, logger, selectable=False)
        self._lines        = title.splitlines()
        self._center       = center
        self._draw_border  = False


    def toggle_border(self):
        """Function that gives option to draw border around label
        """

        self._draw_border = not self._draw_border


    def _draw(self):
        """Override base draw class.

        Center text and draw it
        """

        super()._draw()
        self._renderer.set_color_mode(self._color)
        if self._draw_border:
            self._renderer.draw_border(self, with_title=False)
        counter = self._start_y
        for line in self._lines:
            if counter == self._start_y + self._height - self._pady:
                break
            self._renderer.draw_text(self, line, counter, centered = self._center, bordered=self._draw_border)
            counter = counter + 1
        self._renderer.unset_color_mode(self._color)


class ScrollMenu(Widget, py_cui.ui.MenuImplementation):
    """A scroll menu widget.
    """

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger):
        """Initializer for scroll menu. calls superclass initializers and sets help text
        """

        Widget.__init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger)
        py_cui.ui.MenuImplementation.__init__(self, logger)
        self.set_help_text('Focus mode on ScrollMenu. Use up/down to scroll, Enter to trigger command, Esc to exit.')


    def _handle_key_press(self, key_pressed):
        """Override base class function.

        UP_ARROW scrolls up, DOWN_ARROW scrolls down.

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """

        super()._handle_key_press(key_pressed)
        if key_pressed == py_cui.keys.KEY_UP_ARROW:
            self._scroll_up()
        if key_pressed == py_cui.keys.KEY_DOWN_ARROW:
            
            self._scroll_down(self.get_viewport_height())


    def _draw(self):
        """Overrides base class draw function
        """

        super()._draw()
        self._renderer.set_color_mode(self._color)
        self._renderer.draw_border(self)
        counter = self._pady + 1
        line_counter = 0
        for line in self._view_items:
            if line_counter < self._top_view:
                line_counter = line_counter + 1
            else:
                if counter >= self._height - self._pady - 1:
                    break
                if line_counter == self._selected_item:
                    self._renderer.draw_text(self, line, self._start_y + counter, selected=True)
                else:
                    self._renderer.draw_text(self, line, self._start_y + counter)
                counter = counter + 1
                line_counter = line_counter + 1
        self._renderer.unset_color_mode(self._color)
        self._renderer.reset_cursor(self)


class CheckBoxMenu(ScrollMenu):
    """Extension of ScrollMenu that allows for multiple items to be selected at once.

    Attributes
    ----------
    selected_item_list : list of str
        List of checked items
    checked_char : char
        Character to represent a checked item
    """

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger, checked_char):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady, logger)

        self.selected_item_list = []
        self.checked_char       = checked_char
        self.set_help_text('Focus mode on CheckBoxMenu. Use up/down to scroll, Enter to toggle set, unset, Esc to exit.')


    def add_item(self, item_text):
        """Adds item to Checkbox

        Parameters
        ----------
        item_text : str
            Menu item to add
        """

        item_text = '[ ] - ' + item_text
        super().add_item(item_text)


    def add_item_list(self, item_list):
        """Adds list of items to the checkbox

        Parameters
        ----------
        item_list : list of str
            Menu item list to add
        """

        for item in item_list:
            self.add_item(item)


    def get(self):
        """Gets list of selected items from the checkbox

        Returns
        -------
        selected_items : list of str
            list of checked items
        """

        ret = []
        for item in self.selected_item_list:
            ret.append(item[6:])
        return ret


    def mark_item_as_checked(self, text):
        """Function that marks an item as selected

        Parameters
        ----------
        text : str
            Mark item with text = text as checked
        """

        if '[ ] - {}'.format(text) in self._view_items:
            item_index_of = self._view_items.index('[ ] - {}'.format(text))
            self._view_items[item_index_of] = '[{}] - '.format(self.checked_char) + self._view_items[item_index_of][6:]
            self.selected_item_list.append(text)
        elif '[{}] - {}'.format(self.checked_char, text) in self._view_items:
            item_index_of = self._view_items.index('[{}] - {}'.format(self.checked_char, text))
            self._view_items[item_index_of] = '[ ] - ' + self._view_items[item_index_of][6:]
            self.selected_item_list.remove(text)


    def _handle_key_press(self, key_pressed):
        """Override of key presses.

        First, run the superclass function, scrolling should still work.
        Adds Enter command to toggle selection

        Parameters
        ----------
        key_pressed : int
            key code of pressed key
        """

        super()._handle_key_press(key_pressed)
        if key_pressed == py_cui.keys.KEY_ENTER:
            if super().get() in self.selected_item_list:
                self.selected_item_list.remove(super().get())
                self._view_items[self._selected_item] = '[ ] - ' + self._view_items[self._selected_item][6:]
            else:
                self._view_items[self._selected_item] = '[{}] - '.format(self.checked_char) + self._view_items[self._selected_item][6:]
                self.selected_item_list.append(self._view_items[self._selected_item])



class Button(Widget):
    """Basic button widget.

    Allows for running a command function on Enter

    Attributes
    ----------
    command : function
        A no-args function to run when the button is pressed.
    """

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger, command):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady, logger)
        self.command = command
        self.set_color(py_cui.MAGENTA_ON_BLACK)
        self.set_help_text('Focus mode on Button. Press Enter to press button, Esc to exit focus mode.')


    def _handle_key_press(self, key_pressed):
        """Override of base class, adds ENTER listener that runs the button's command

        Parameters
        ----------
        key_pressed : int
            Key code of pressed key
        """

        super()._handle_key_press(key_pressed)
        if key_pressed == py_cui.keys.KEY_ENTER:
            if self.command is not None:
                ret = self.command()
            return ret


    def _draw(self):
        """Override of base class draw function
        """

        super()._draw()
        self._renderer.set_color_mode(self.get_color())
        self._renderer.draw_border(self, with_title=False)
        button_text_y_pos = self._start_y + int(self._height / 2)
        self._renderer.draw_text(self, self._title, button_text_y_pos, centered=True, selected=self._selected)
        self._renderer.reset_cursor(self)
        self._renderer.unset_color_mode(self.get_color())



class TextBox(Widget, py_cui.ui.TextBoxImplementation):
    """Widget for entering small single lines of text
    """

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger, initial_text, password):
        Widget.__init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger)
        py_cui.ui.TextBoxImplementation.__init__(self, initial_text, password, logger)
        self.update_height_width()
        self.set_help_text('Focus mode on TextBox. Press Esc to exit focus mode.')


    def update_height_width(self):
        """Need to update all cursor positions on resize
        """

        super().update_height_width()
        padx, _          = self.get_padding()
        start_x, start_y    = self.get_start_position()
        height, width       = self.get_absolute_dimensions()
        self._initial_cursor     = start_x + padx + 2
        self._cursor_text_pos    = 0
        self._cursor_x           = start_x + padx + 2
        self._cursor_max_left    = start_x + padx + 2
        self._cursor_max_right   = start_x + width - padx - 1
        self._cursor_y           = start_y + int(height / 2) + 1
        self._viewport_width     = self._cursor_max_right - self._cursor_max_left


    def _handle_key_press(self, key_pressed):
        """Override of base handle key press function

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """

        super()._handle_key_press(key_pressed)
        if key_pressed == py_cui.keys.KEY_LEFT_ARROW:
            self._move_left()
        elif key_pressed == py_cui.keys.KEY_RIGHT_ARROW:
            self._move_right()
        elif key_pressed == py_cui.keys.KEY_BACKSPACE:
            self._erase_char()
        elif key_pressed == py_cui.keys.KEY_DELETE:
            self._delete_char()
        elif key_pressed == py_cui.keys.KEY_HOME:
            self._jump_to_start()
        elif key_pressed == py_cui.keys.KEY_END:
            self._jump_to_end()
        elif key_pressed > 31 and key_pressed < 128:
            self._insert_char(key_pressed)


    def _draw(self):
        """Override of base draw function
        """

        super()._draw()

        self._renderer.set_color_mode(self._color)
        self._renderer.draw_text(self, self._title, self._cursor_y - 2, bordered=False)
        self._renderer.draw_border(self, fill=False, with_title=False)
        render_text = self._text
        if len(self._text) > self._width - 2 * self._padx - 4:
            end = len(self._text) - (self._width - 2 * self._padx - 4)
            if self._cursor_text_pos < end:
                render_text = self._text[self._cursor_text_pos:self._cursor_text_pos + (self._width - 2 * self._padx - 4)]
            else:
                render_text = self._text[end:]
        if self._password:
            temp = '*' * len(render_text)
            render_text = temp
            
        self._renderer.draw_text(self, render_text, self._cursor_y, selected=self._selected)
        if self._selected:
            self._renderer.draw_cursor(self._cursor_y, self._cursor_x)
        else:
            self._renderer.reset_cursor(self, fill=False)
        self._renderer.unset_color_mode(self._color)


class ScrollTextBlock(Widget, py_cui.ui.TextBlockImplementation):
    """Widget for editing large multi-line blocks of text

    Attributes
    ----------
    text_lines : list of str
        The lines of text in the text box
    cursor_x, cursor_y : int
        The absolute positions of the cursor in the terminal window
    cursor_text_pos_x, cursor_text_pos_y : int
        the cursor position relative to the text
    cursor_max_left, cursor_max_right : int
        The cursor bounds of the text box
    cursor_max_up, cursor_max_down : int
        The cursor bounds of the text box
    viewport_x_start, viewport_y_start : int
        upper left corner of the viewport
    viewport_width : int
        The width of the textbox viewport
    """

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger, initial_text):
        Widget.__init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger)
        py_cui.ui.TextBlockImplementation.__init__(self, initial_text, logger)
        self.update_height_width()
        self.set_help_text('Focus mode on TextBlock. Press Esc to exit focus mode.')


    def update_height_width(self):
        """Function that updates the position of the text and cursor on resize
        """

        Widget.update_height_width(self)
        self._viewport_y_start   = 0
        self._viewport_x_start   = 0
        self._cursor_text_pos_x  = 0
        self._cursor_text_pos_y  = 0
        self._cursor_y           = self._start_y + 1
        self._cursor_x           = self._start_x + self._padx + 2
        self._cursor_max_up      = self._cursor_y
        self._cursor_max_down    = self._start_y + self._height - self._pady - 2
        self._cursor_max_left    = self._cursor_x
        self._cursor_max_right   = self._start_x + self._width - self._padx - 1
        self._viewport_width     = self._cursor_max_right - self._cursor_max_left
        self._viewport_height    = self._cursor_max_down  - self._cursor_max_up


    def _handle_key_press(self, key_pressed):
        """Override of base class handle key press function

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """

        super()._handle_key_press(key_pressed)

        if key_pressed == py_cui.keys.KEY_LEFT_ARROW:
            self._move_left()
        elif key_pressed == py_cui.keys.KEY_RIGHT_ARROW:
            self._move_right()
        elif key_pressed == py_cui.keys.KEY_UP_ARROW:
            self._move_up()
        elif key_pressed == py_cui.keys.KEY_DOWN_ARROW and self._cursor_text_pos_y < len(self._text_lines) - 1:
            self._move_down()
        elif key_pressed == py_cui.keys.KEY_BACKSPACE:
            self._handle_backspace()
        elif key_pressed == py_cui.keys.KEY_DELETE:
            self._handle_delete()
        elif key_pressed == py_cui.keys.KEY_ENTER:
            self._handle_newline()
        elif key_pressed == py_cui.keys.KEY_TAB:
            for _ in range(0, 4):
                self._insert_char(py_cui.keys.KEY_SPACE)
        elif key_pressed == py_cui.keys.KEY_HOME:
            self._handle_home()
        elif key_pressed == py_cui.keys.KEY_END:
            self._handle_end()
        elif key_pressed > 31 and key_pressed < 128:
            self._insert_char(key_pressed)


    def _draw(self):
        """Override of base class draw function
        """

        super()._draw()

        self._renderer.set_color_mode(self._color)
        self._renderer.draw_border(self)
        counter = self._cursor_max_up
        for line_counter in range(self._viewport_y_start, self._viewport_y_start + self._viewport_height):
            if line_counter == len(self._text_lines):
                break
            render_text = self._text_lines[line_counter]
            self._renderer.draw_text(self, render_text, counter, start_pos=self._viewport_x_start, selected=self._selected)
            counter = counter + 1
        if self._selected:
            self._renderer.draw_cursor(self._cursor_y, self._cursor_x)
        else:
            self._renderer.reset_cursor(self)
        self._renderer.unset_color_mode(self._color)
