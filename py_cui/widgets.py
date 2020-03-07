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
import py_cui.colors
import py_cui.errors
import py_cui.keys


class Widget:
    """Top Level Widget Base Class

    Extended by all widgets. Contains base classes for handling key presses, drawing,
    and setting status bar text.

    Attributes
    ----------
    id : int
        Id of the widget
    title : str
        Widget title
    grid : py_cui.grid.Grid
        The parent grid object of the widget
    renderer : py_cui.renderer.Renderer
        The renderer object that draws the widget
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
    color : int
        Color code combination
    selected_color : int
        color code combination for when widget is selected
    selected : bool
        Flag that says if widget is selected
    is_selectable : bool
        Flag that says if a widget can be selected
    help_text : str
        text displayed in status bar when selected
    key_commands : dict
        Dictionary mapping key codes to functions
    text_color_rules : list of py_cui.ColorRule
        color rules to load into renderer when drawing widget
    on_lose_focus : Callable
        called when this widget loses focus
    """

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, selectable = True):
        """Constructor for base widget class
        """
        self.on_lose_focus = None
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
        self.padx = padx
        self.pady = pady
        self.start_x, self.start_y = self.get_absolute_position()
        self.width, self.height = self.get_absolute_dims()
        self.color = py_cui.WHITE_ON_BLACK
        self.selected_color = py_cui.BLACK_ON_GREEN
        self.selected = False
        self.is_selectable = selectable
        self.help_text = 'No help text available.'
        self.text_color_rules = []
        self.key_map = py_cui.keys.KeyMap()
        self.key_map.bind_key(key=py_cui.keys.Key.ESCAPE, definition=self._on_lose_focus)
        self.raw_key_map = py_cui.keys.RawKeyMap(range(32, 128))

    def _on_lose_focus(self, key: py_cui.keys.Key):
        if self.on_lose_focus:
            self.on_lose_focus()

    def set_focus_text(self, text):
        """Function that sets the text of the status bar on focus for a particular widget

        Parameters
        ----------
        text : str
            text to write to status bar when in focus mode.
        """

        self.help_text = text

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

        self.text_color_rules.append(py_cui.colors.ColorRule(regex, color, rule_type, match_type, region, include_whitespace))


    def set_standard_color(self, color):
        """Sets the standard color for the widget

        Parameters
        ----------
        color : int
            Color code for widegt
        """

        self.color = color


    def set_selected_color(self, color):
        """Sets the selected color for the widget

        Parameters
        ----------
        color : int
            Color code for widegt when selected
        """

        self.selected_color = color


    def assign_renderer(self, renderer):
        """Function that assigns a renderer object to the widget

        (Meant for internal usage only)

        Parameters
        ----------
        renderer : py_cui.renderer.Renderer
            Renderer for drawing widget

        Raises
        ------
        error : PyCUIError
            If parameter is not a initialized renderer.
        """

        if isinstance(renderer, py_cui.renderer.Renderer):
            self.renderer = renderer
        else:
            raise py_cui.errors.PyCUIError('Invalid renderer, must be of type py_cui.renderer.Renderer')


    def get_absolute_position(self):
        """Gets the absolute position of the widget in characters

        Returns
        -------
        x_pos, y_pos : int
            position of widget in terminal
        """

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
        """Gets the absolute dimensions of the widget in characters

        Returns
        -------
        width, height : int
            dimensions of widget in terminal
        """

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

        if self.row <= row and row <= (self.row + self.row_span - 1) and self.column <= col and col <= (self.column_span + self.column - 1):
            return True
        else:
            return False


    # BELOW FUNCTIONS SHOULD BE OVERWRITTEN BY SUB-CLASSES


    def update_height_width(self):
        """Function that refreshes position and dimensons on resize.

        If necessary, make sure required widget attributes updated here as well.
        """

        self.start_x, self.start_y = self.get_absolute_position()
        self.width, self.height = self.get_absolute_dims()


    def get_help_text(self):
        """Returns help text

        Returns
        -------
        help_text : str
            Status bar text
        """

        return self.help_text


    def handle_key_press(self, key_pressed):
        """Base class function that handles all assigned key presses.

        When overwriting this function, make sure to add a super().handle_key_press(key_pressed) call,
        as this is required for user defined key command support

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """
        try:
            self.raw_key_map.execute(key_pressed)
            key = py_cui.keys.Key(key_pressed)
            self.key_map.execute(key)
        except ValueError:
            return

    def draw(self):
        """Base class draw class that checks if renderer is valid.

        Should be called with super().draw() in overrides
        """

        if self.renderer is None:
            return
        else:
            self.renderer.set_color_rules(self.text_color_rules)


class Label(Widget):
    """The most basic subclass of Widget.

    Simply displays one centered row of text. Has no unique attributes or methods

    Attributes
    ----------
    draw_border : bool
        Toggle for drawing label border
    """

    def __init__(self, id, title,  grid, row, column, row_span, column_span, padx, pady):
        """Constructor for Label
        """

        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady, selectable=False)
        self.draw_border = False


    def toggle_border(self):
        """Function that gives option to draw border around label
        """

        self.draw_border = not self.draw_border


    def draw(self):
        """Override base draw class.

        Center text and draw it
        """

        super().draw()
        self.renderer.set_color_mode(self.color)
        if self.draw_border:
            self.renderer.draw_border(self, with_title=False)
        target_y = self.start_y + int(self.height / 2)
        self.renderer.draw_text(self, self.title, target_y, centered=True, bordered=self.draw_border)
        self.renderer.unset_color_mode(self.color)


class BlockLabel(Widget):
    """A Variation of the label widget that renders a block of text.

    Attributes
    ----------
    lines : list of str
        list of lines that make up block text
    center : bool
        Decides whether or not label should be centered
    """

    def __init__(self, id, title,  grid, row, column, row_span, column_span, padx, pady, center):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady, selectable=False)
        self.lines = title.splitlines()
        self.center = center
        self.draw_border = False


    def toggle_border(self):
        """Function that gives option to draw border around label
        """

        self.draw_border = not self.draw_border


    def draw(self):
        """Override base draw class.

        Center text and draw it"""

        super().draw()
        self.renderer.set_color_mode(self.color)
        if self.draw_border:
            self.renderer.draw_border(self, with_title=False)
        counter = self.start_y
        for line in self.lines:
            if counter == self.start_y + self.height - self.pady:
                break
            self.renderer.draw_text(self, line, counter, centered = self.center, bordered=self.draw_border)
            counter = counter + 1
        self.renderer.unset_color_mode(self.color)


class ScrollMenu(Widget):
    """A scroll menu widget.

    Allows for creating a scrollable list of items of which one is selectable.
    Analogous to a RadioButton

    Attributes
    ----------
    top_view : int
        the uppermost menu element in view
    selected_item : int
        the currently highlighted menu item
    view_items : list of str
        list of menu items
    """

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady):
        """Constructor for scroll menu
        """

        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)
        self.top_view = 0
        self.selected_item = 0
        self.view_items = []
        self.set_focus_text('Focus mode on ScrollMenu. Use up/down to scroll, Enter to trigger command, Esc to exit.')
        self.key_map.bind_key(key=py_cui.keys.Key.UP_ARROW, definition=self.scroll_up)
        self.key_map.bind_key(key=py_cui.keys.Key.DOWN_ARROW, definition=self.scroll_down)

    def clear(self):
        """Clears all items from the Scroll Menu
        """

        self.view_items = []
        self.selected_item = 0
        self.top_view = 0


    def scroll_up(self, key: py_cui.keys.Key):
        """Function that scrolls the view up in the scroll menu

        Parameters
        ----------
        key : Key
            The key pressed to trigger this event
        """

        if self.selected:
            if self.top_view > 0 and self.selected_item == self.top_view:
                self.top_view = self.top_view - 1
            if self.selected_item > 0:
                self.selected_item = self.selected_item - 1


    def scroll_down(self, key: py_cui.keys.Key):
        """Function that scrolls the view down in the scroll menu

        Parameters
        ----------
        key : Key
            The key pressed to trigger this event
        """
        if self.selected:
            if self.selected_item < len(self.view_items) - 1:
                self.selected_item = self.selected_item + 1
            if self.selected_item > self.top_view + self.height - (2 * self.pady) - 3:
                self.top_view = self.top_view + 1


    def add_item(self, item_text):
        """Adds an item to the menu.

        Parameters
        ----------
        item_text : str
            The text for the item
        """

        self.view_items.append(item_text)


    def add_item_list(self, item_list):
        """Adds a list of items to the scroll menu.

        Parameters
        ----------
        item_list : list of str
            list of strings to add as items to the scrollmenu
        """

        for item in item_list:
            self.add_item(item)


    def remove_selected_item(self):
        """Function that removes the selected item from the scroll menu.
        """

        if len(self.view_items) == 0:
            return
        del self.view_items[self.selected_item]
        if self.selected_item >= len(self.view_items):
            self.selected_item = self.selected_item - 1


    def get_item_list(self):
        """Function that gets list of items in a scroll menu

        Returns
        -------
        item_list : list of str
            list of items in the scrollmenu
        """

        return self.view_items


    def get(self):
        """Function that gets the selected item from the scroll menu

        Returns
        -------
        item : str
            selected item, or None if there are no items in the menu
        """

        if len(self.view_items) > 0:
            return self.view_items[self.selected_item]
        return None

    def draw(self):
        """Overrides base class draw function
        """

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
    """Extension of ScrollMenu that allows for multiple items to be selected at once.

    Attributes
    ----------
    selected_item_list : list of str
        List of checked items
    checked_char : char
        Character to represent a checked item
    """

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, checked_char):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)

        self.selected_item_list = []
        self.checked_char = checked_char
        self.set_focus_text('Focus mode on CheckBoxMenu. Use up/down to scroll, Enter to toggle set, unset, Esc to exit.')
        self.key_map.bind(key=py_cui.keys.Key.ENTER, definition=self.select_item)
        
    def select_item(self, key: py_cui.keys.Key):
        """Select a given item and set its view

        Parameters
        ----------
        key : Key
            The key pressed to execute this event
        """
        if super().get() in self.selected_item_list:
            self.selected_item_list.remove(super().get())
            self.view_items[self.selected_item] = '[ ] - ' + self.view_items[self.selected_item][6:]
        else:
            self.view_items[self.selected_item] = '[{}] - '.format(self.checked_char) + self.view_items[self.selected_item][6:]
            self.selected_item_list.append(self.view_items[self.selected_item])

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

        if '[ ] - {}'.format(text) in self.view_items:
            item_index_of = self.view_items.index('[ ] - {}'.format(text))
            self.view_items[item_index_of] = '[{}] - '.format(self.checked_char) + self.view_items[item_index_of][6:]
            self.selected_item_list.append(text)
        elif '[{}] - {}'.format(self.checked_char, text) in self.view_items:
            item_index_of = self.view_items.index('[{}] - {}'.format(self.checked_char, text))
            self.view_items[item_index_of] = '[ ] - ' + self.view_items[item_index_of][6:]
            self.selected_item_list.remove(text)


class Button(Widget):
    """Basic button widget.

    Allows for running a command function on Enter

    Attributes
    ----------
    command : function
        A no-args function to run when the button is pressed.
    """

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, command):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)
        self.command = command
        self.set_standard_color(py_cui.MAGENTA_ON_BLACK)
        self.set_focus_text('Focus mode on Button. Press Enter to press button, Esc to exit focus mode.')
        self.key_map.bind_key(key=py_cui.keys.Key.ENTER, definition=self.button_action)

    def button_action(self, key: py_cui.keys.Key):
        """Called when the button is pressed

        Parameters
        ----------
        key : int
            The key used to trigger this event
        """
        self.selected_color = py_cui.WHITE_ON_RED
        if self.command is not None:
            ret = self.command()
        self.selected_color = py_cui.BLACK_ON_GREEN
        return ret

    def draw(self):
        """Override of base class draw function
        """

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
    """Widget for entering small single lines of text

    Attributes
    ----------
    text : str
        The text in the text box
    cursor_x, cursor_y : int
        The absolute positions of the cursor in the terminal window
    cursor_text_pos : int
        the cursor position relative to the text
    cursor_max_left, cursor_max_right : int
        The cursor bounds of the text box
    viewport_width : int
        The width of the textbox viewport
    password : bool
        Toggle to display password characters or text
    """

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, initial_text, password):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)
        self.text = initial_text
        self.cursor_x = self.start_x + padx + 2
        self.cursor_text_pos = 0
        self.cursor_max_left = self.cursor_x
        self.cursor_max_right = self.start_x + self.width - padx - 1
        self.cursor_y = self.start_y + int(self.height / 2) + 1
        self.set_focus_text('Focus mode on TextBox. Press Esc to exit focus mode.')
        self.viewport_width = self.cursor_max_right - self.cursor_max_left
        self.password = password
        self.key_map.bind_key(key=py_cui.keys.Key.LEFT_ARROW, definition=self.move_left)
        self.key_map.bind_key(key=py_cui.keys.Key.RIGHT_ARROW, definition=self.move_right)
        self.key_map.bind_key(key=py_cui.keys.Key.BACKSPACE, definition=self.erase_char)
        self.key_map.bind_key(key=py_cui.keys.Key.DELETE, definition=self.delete_char)
        self.key_map.bind_key(key=py_cui.keys.Key.HOME, definition=self.jump_to_start)
        self.key_map.bind_key(key=py_cui.keys.Key.END, definition=self.jump_to_end)
        
        self.raw_key_map.add_definition(self.insert_char)

    def update_height_width(self):
        """Need to update all cursor positions on resize
        """

        super().update_height_width()
        self.cursor_y = self.start_y + int(self.height / 2) + 1
        self.cursor_x = self.start_x + self.padx + 2
        self.cursor_text_pos = 0
        self.cursor_max_right = self.start_x + self.width - self.padx - 1
        self.cursor_max_left = self.cursor_x
        self.viewport_width = self.cursor_max_right - self.cursor_max_left


    def set_text(self, text):
        """Sets the value of the text. Overwrites existing text

        Parameters
        ----------
        text : str
            The text to write to the textbox
        """

        self.text = text
        if self.cursor_text_pos > len(self.text):
            diff = self.cursor_text_pos - len(self.text)
            self.cursor_text_pos = len(self.text)
            self.cursor_x = self.cursor_x - diff


    def get(self):
        """Gets value of the text in the textbox

        Returns
        -------
        text : str
            The current textbox test
        """

        return self.text


    def clear(self):
        """Clears the text in the textbox
        """

        self.cursor_x = self.cursor_max_left
        self.cursor_text_pos = 0
        self.text = ''


    def move_left(self):
        """Shifts the cursor the the left. Internal use only
        """

        if  self.cursor_text_pos > 0:
            if self.cursor_x > self.cursor_max_left:
                self.cursor_x = self.cursor_x - 1
            self.cursor_text_pos = self.cursor_text_pos - 1


    def move_right(self):
        """Shifts the cursor the the right. Internal use only
        """
        if self.cursor_text_pos < len(self.text):
            if self.cursor_x < self.cursor_max_right:
                self.cursor_x = self.cursor_x + 1
            self.cursor_text_pos = self.cursor_text_pos + 1


    def insert_char(self, key: int):
        """Inserts char at cursor position.

        Internal use only

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """
        self.text = self.text[:self.cursor_text_pos] + chr(key) + self.text[self.cursor_text_pos:]
        if len(self.text) < self.viewport_width:
            self.cursor_x = self.cursor_x + 1
        self.cursor_text_pos = self.cursor_text_pos + 1


    def jump_to_start(self, key: py_cui.keys.Key):
        """Jumps to the start of the textbox
        """

        self.cursor_x = self.start_x + self.padx + 2
        self.cursor_text_pos = 0


    def jump_to_end(self, key: py_cui.keys.Key):
        """Jumps to the end to the textbox
        """

        self.cursor_text_pos = len(self.text)
        self.cursor_x = self.start_x + self.padx + 2 + self.cursor_text_pos


    def erase_char(self, key: py_cui.keys.Key):
        """Erases character at textbox cursor
        """

        if self.cursor_text_pos > 0:
            self.text = self.text[:self.cursor_text_pos - 1] + self.text[self.cursor_text_pos:]
            if len(self.text) < self.width - 2 * self.padx - 4:
                self.cursor_x = self.cursor_x - 1
            self.cursor_text_pos = self.cursor_text_pos - 1

    def delete_char(self, key: py_cui.keys.Key):
        """Deletes character to right of texbox cursor
        """

        if self.cursor_text_pos < len(self.text):
            self.text = self.text[:self.cursor_text_pos] + self.text[self.cursor_text_pos + 1:]

    def draw(self):
        """Override of base draw function
        """

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
        if self.password:
            temp = '*' * len(render_text)
            render_text = temp
            
        self.renderer.draw_text(self, render_text, self.cursor_y, selected=self.selected)
        if self.selected:
            self.renderer.draw_cursor(self.cursor_y, self.cursor_x)
        else:
            self.renderer.reset_cursor(self, fill=False)
        self.renderer.unset_color_mode(self.color)


class ScrollTextBlock(Widget):
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
        self.set_focus_text('Focus mode on TextBlock. Press Esc to exit focus mode.')
        
        self.key_map.bind_key(key=py_cui.keys.Key.LEFT_ARROW, definition=self.move_left)
        self.key_map.bind_key(key=py_cui.keys.Key.RIGHT_ARROW, definition=self.move_right)
        self.key_map.bind_key(key=py_cui.keys.Key.UP_ARROW, definition=self.move_up)
        self.key_map.bind_key(key=py_cui.keys.Key.DOWN_ARROW, definition=self.move_down)
        self.key_map.bind_key(key=py_cui.keys.Key.BACKSPACE, definition=self.handle_backspace)
        self.key_map.bind_key(key=py_cui.keys.Key.DELETE, definition=self.handle_delete)
        self.key_map.bind_key(key=py_cui.keys.Key.ENTER, definition=self.handle_newline)
        self.key_map.bind_key(key=py_cui.keys.Key.TAB, definition=lambda x: [self.insert_char(py_cui.keys.Key.SPACE) for _ in range(4)])
        self.key_map.bind_key(key=py_cui.keys.Key.HOME, definition=self.handle_home)
        self.key_map.bind_key(key=py_cui.keys.Key.END, definition=self.handle_end)
        
        self.raw_key_map.add_definition(self.insert_char)

    def update_height_width(self):
        """Function that updates the position of the text and cursor on resize
        """

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
        """Gets all of the text in the textblock and returns it

        Returns
        -------
        text : str
            The current text in the text block
        """

        text = ''
        for line in self.text_lines:
            text = '{}{}\n'.format(text, line)
        return text


    def write(self, text):
        """Function used for writing text to the text block

        Parameters
        ----------
        text : str
            Text to write to the text block
        """

        lines = text.splitlines()
        if len(self.text_lines) == 1 and self.text_lines[0] == '':
            self.set_text(text)
        else:
            self.text_lines.append(lines)


    def clear(self):
        """Function that clears the text block
        """

        self.cursor_x = self.cursor_max_left
        self.cursor_y = self.cursor_max_up
        self.cursor_text_pos_x = 0
        self.cursor_text_pos_y = 0
        self.text_lines = []
        self.text_lines.append('')


    def get_current_line(self):
        """Returns the line on which the cursor currently resides

        Returns
        -------
        current_line : str
            The current line of text that the cursor is on
        """

        return self.text_lines[self.cursor_text_pos_y]


    def set_text(self, text):
        """Function that sets the text for the textblock.

        Note that this will overwrite any existing text

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
        """Function that sets the current line's text.

        Meant only for internal use

        Parameters
        ----------
        text : str
            text line to write into text block
        """

        self.text_lines[self.cursor_text_pos_y] = text


    def move_left(self, key: py_cui.keys.Key):
        """Function that moves the cursor/text position one location to the left
        """
        if self.cursor_text_pos_x > 0:
            if self.cursor_x > self.cursor_max_left:
                self.cursor_x = self.cursor_x - 1
            elif self.viewport_x_start > 0:
                self.viewport_x_start = self.viewport_x_start - 1
            self.cursor_text_pos_x = self.cursor_text_pos_x - 1


    def move_right(self, key: py_cui.keys.Key):
        """Function that moves the cursor/text position one location to the right
        """

        current_line = self.get_current_line()

        if self.cursor_text_pos_x < len(current_line):
            if self.cursor_x < self.cursor_max_right:
                self.cursor_x = self.cursor_x + 1
            elif self.viewport_x_start + self.width - 2 * self.padx - 4 < len(current_line):
                self.viewport_x_start = self.viewport_x_start + 1
            self.cursor_text_pos_x = self.cursor_text_pos_x + 1


    def move_up(self, key: py_cui.keys.Key):
        """Function that moves the cursor/text position one location up
        """

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


    def move_down(self, key: py_cui.keys.Key):
        """Function that moves the cursor/text position one location down
        """
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


    def handle_newline(self, key: py_cui.keys.Key):
        """Function that handles recieving newline characters in the text
        """

        current_line = self.get_current_line()

        new_line_1 = current_line[:self.cursor_text_pos_x]
        new_line_2 = current_line[self.cursor_text_pos_x:]
        self.text_lines[self.cursor_text_pos_y] = new_line_1
        self.text_lines.insert(self.cursor_text_pos_y + 1, new_line_2)
        self.cursor_text_pos_y = self.cursor_text_pos_y + 1
        self.cursor_text_pos_x = 0
        self.cursor_x = self.cursor_max_left
        self.viewport_x_start = 0
        if self.cursor_y < self.cursor_max_down:
            self.cursor_y = self.cursor_y + 1
        elif self.viewport_y_start + self.height - 2 < len(self.text_lines):
            self.viewport_y_start = self.viewport_y_start + 1


    def handle_backspace(self, key: py_cui.keys.Key):
        """Function that handles recieving backspace characters in the text
        """

        current_line = self.get_current_line()

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


    def handle_home(self, key: py_cui.keys.Key):
        """Function that handles recieving a home keypress
        """

        self.cursor_x = self.cursor_max_left
        self.cursor_text_pos_x = 0
        self.viewport_x_start = 0


    def handle_end(self, key: py_cui.keys.Key):
        """Function that handles recieving an end keypress
        """

        current_line = self.get_current_line()

        self.cursor_text_pos_x = len(current_line)
        if len(current_line) > self.viewport_width:
            self.cursor_x = self.cursor_max_right
            self.viewport_x_start = self.cursor_text_pos_x - self.viewport_width
        else:
            self.cursor_x = self.cursor_max_left + len(current_line)


    def handle_delete(self, key: py_cui.keys.Key):
        """Function that handles recieving a delete keypress
        """

        current_line = self.get_current_line()

        if self.cursor_text_pos_x == len(current_line) and self.cursor_text_pos_y < len(self.text_lines) - 1:
            self.text_lines[self.cursor_text_pos_y] = self.text_lines[self.cursor_text_pos_y] + self.text_lines[self.cursor_text_pos_y + 1]
            self.text_lines = self.text_lines[:self.cursor_text_pos_y+1] + self.text_lines[self.cursor_text_pos_y + 2:]
        elif self.cursor_text_pos_x < len(current_line):
            self.set_text_line(current_line[:self.cursor_text_pos_x] + current_line[self.cursor_text_pos_x+1:])


    def insert_char(self, key: int):
        """Function that handles recieving a character

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """

        current_line = self.get_current_line()

        self.set_text_line(current_line[:self.cursor_text_pos_x] + chr(key_pressed) + current_line[self.cursor_text_pos_x:])
        if len(current_line) <= self.width - 2 * self.padx - 4:
            self.cursor_x = self.cursor_x + 1
        elif self.viewport_x_start + self.width - 2 * self.padx - 4 < len(current_line):
            self.viewport_x_start = self.viewport_x_start + 1
        self.cursor_text_pos_x = self.cursor_text_pos_x + 1

    def draw(self):
        """Override of base class draw function
        """

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
