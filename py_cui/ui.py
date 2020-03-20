"""Module containing classes for generic UI elements.

Contains base UI element class, along with UI implementation agnostic UI element classes.
"""

import py_cui
import py_cui.errors
import py_cui.colors


class UIElement:

    def __init__(self, id, title, renderer, logger):

        self._id       = id
        self._title    = title
        self._padx     = 1
        self._pady     = 0
        self._start_x,  self._stop_y    = 0, 0
        self._stop_x,   self._start_y   = 0, 0
        self._height,   self._width     = 0, 0
        self._color    = py_cui.WHITE_ON_BLACK
        self._selected = False
        self._renderer = renderer
        self._logger   = logger
        self._help_text = ''


    def get_absolute_start_pos(self):

        return 0, 0


    def get_absolute_stop_pos(self):
        return 0, 0


    def get_absolute_dimensions(self):
        """Gets dimensions of element in terminal characters

        Returns
        -------
        height, width : int, int
            Dimensions of element in characters
        """
        start_x,    start_y = self.get_absolute_start_pos()
        stop_x,     stop_y  = self.get_absolute_stop_pos()
        return (stop_y - start_y), (stop_x - start_x)


    def get_viewport_height(self):
        return self._height - (2 * self._pady) - 3

    def get_id(self):
        """Gets the widget ID
        
        Returns
        -------
        id : int
            The ui element id
        """

        return self._id


    def get_title(self):
        """Getter for ui element title
        
        Returns
        -------
        title : str
            UI element title
        """
        return self._title


    def get_padding(self):
        """Gets ui element padding on in characters
        
        Returns
        -------
        padx, pady : int, int
            Padding on either axis in characters
        """
        return self._padx, self._pady


    def get_start_position(self):
        """Gets coords of upper left corner

        Returns
        -------
        start_x, start_y : int, int
            Coords of upper right corner
        """

        return self._start_x, self._start_y


    def get_stop_positions(self):
        """Gets coords of lower right corner
        
        Returns
        -------
        stop_x, stop_y : int, int
            Coords of lower right corner
        """

        return self._stop_x, self._stop_y



    def get_color(self):
        """Gets current element color

        Returns
        -------
        color : int
            color code for combination
        """

        return self._color


    def is_selected(self):
        """Get selected status

        Returns
        -------
        selected : bool
            True if selected, False otherwise
        """

        return self._selected


    def get_renderer(self):
        """Gets reference to renderer object

        Returns
        -------
        renderer : py_cui.renderer.Render
            renderer object used for drawing element
        """

        return self._renderer

    def get_help_text(self):
        return self._help_text


    def set_padding(self, padx, pady):


        self._padx = padx
        self._pady = pady


    def update_height_width(self):
        """Function that refreshes position and dimensons on resize.

        If necessary, make sure required widget attributes updated here as well.
        """

        self._start_x, self._start_y  = self.get_absolute_start_pos()
        self._stop_x,  self._stop_y   = self.get_absolute_stop_pos()
        self._height,  self._width    = self.get_absolute_dimensions()


    def set_color(self, color):

        self._color = color


    def set_selected(self, selected):

        self._selected = selected

    def set_help_text(self, help_text):
        self._help_text = help_text


    def _handle_key_press(self, key_pressed):

        pass

    
    def _draw(self):
        self._renderer.set_color_mode(self._color)


    def _assign_renderer(self, renderer):
        """Function that assigns a renderer object to the element

        (Meant for internal usage only)

        Parameters
        ----------
        renderer : py_cui.renderer.Renderer
            Renderer for drawing element

        Raises
        ------
        error : PyCUIError
            If parameter is not a initialized renderer.
        """

        if isinstance(renderer, py_cui.renderer.Renderer):
            self._renderer = renderer
        elif self._renderer is not None:
            raise py_cui.errors.PyCUIError('Renderer already assigned for the element')
        else:
            raise py_cui.errors.PyCUIError('Invalid renderer, must be of type py_cui.renderer.Renderer')


class UIImplementation:
    """Base class for ui implementations.

    Should be extended for creating logic common accross ui elements.
    For example, a textbox needs the same logic for a widget or popup.

    Attributes
    ----------
    _logger : py_cui.debug.PyCUILogger
        parent logger object reference.
    """

    def __init__(self, logger):
        self._logger = logger


class TextBoxImplementation(UIImplementation):
    """UI implementation for a single-row textbox input

    Attributes
    ----------
    _text : str
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

    def __init__(self, initial_text, password, logger):

        super().__init__(logger)
        self._text             = initial_text
        self._password         = password
        self._initial_cursor   = 0
        self._cursor_text_pos  = 0
        self._cursor_max_left  = 0
        self._cursor_x         = 0
        self._cursor_max_right = 0
        self._cursor_y         = 0
        self._viewport_width   = 0

    # Variable getter + setter functions

    def get_initial_cursor_pos(self):
        return self._initial_cursor

    def get_cursor_text_pos(self):
        return self._cursor_text_pos

    def get_cursor_limits(self):
        return self._cursor_max_left, self._cursor_max_right

    def get_cursor_position(self):
        return self._cursor_x, self._cursor_y

    def get_viewport_width(self):
        return self._viewport_width


    def set_text(self, text):
        """Sets the value of the text. Overwrites existing text

        Parameters
        ----------
        text : str
            The text to write to the textbox
        """

        self._text = text
        if self._cursor_text_pos > len(self._text):
            diff = self._cursor_text_pos - len(self._text)
            self._cursor_text_pos = len(self._text)
            self._cursor_x = self._cursor_x - diff


    def get(self):
        """Gets value of the text in the textbox

        Returns
        -------
        text : str
            The current textbox test
        """

        return self._text


    def clear(self):
        """Clears the text in the textbox
        """

        self._cursor_x         = self._cursor_max_left
        self._cursor_text_pos  = 0
        self._text             = ''


    def _move_left(self):
        """Shifts the cursor the the left. Internal use only
        """

        if  self._cursor_text_pos > 0:
            if self._cursor_x > self._cursor_max_left:
                self._cursor_x = self._cursor_x - 1
            self._cursor_text_pos = self._cursor_text_pos - 1


    def _move_right(self):
        """Shifts the cursor the the right. Internal use only
        """
        if self._cursor_text_pos < len(self._text):
            if self._cursor_x < self._cursor_max_right:
                self._cursor_x = self._cursor_x + 1
            self._cursor_text_pos = self._cursor_text_pos + 1


    def _insert_char(self, key_pressed):
        """Inserts char at cursor position.

        Internal use only

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """
        self._text = self._text[:self._cursor_text_pos] + chr(key_pressed) + self._text[self._cursor_text_pos:]
        if len(self._text) < self._viewport_width:
            self._cursor_x = self._cursor_x + 1
        self._cursor_text_pos = self._cursor_text_pos + 1


    def _jump_to_start(self):
        """Jumps to the start of the textbox
        """

        self._cursor_x = self._initial_cursor
        self._cursor_text_pos = 0


    def _jump_to_end(self):
        """Jumps to the end to the textbox
        """

        self._cursor_text_pos = len(self._text)
        self._cursor_x = self._initial_cursor + self._cursor_text_pos


    def _erase_char(self):
        """Erases character at textbox cursor
        """

        if self._cursor_text_pos > 0:
            self._text = self._text[:self._cursor_text_pos - 1] + self._text[self._cursor_text_pos:]
            if len(self._text) < self._viewport_width:
                self._cursor_x = self._cursor_x - 1
            self._cursor_text_pos = self._cursor_text_pos - 1


    def _delete_char(self):
        """Deletes character to right of texbox cursor
        """

        if self._cursor_text_pos < len(self._text):
            self._text = self._text[:self._cursor_text_pos] + self._text[self._cursor_text_pos + 1:]


class MenuImplementation(UIImplementation):
    """A scrollable menu UI element

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

    def __init__(self, logger):
        super().__init__(logger)
        self._top_view         = 0
        self._selected_item    = 0
        self._view_items       = []


    def clear(self):
        """Clears all items from the Scroll Menu
        """

        self._view_items = []
        self._selected_item = 0
        self._top_view = 0

    def get_selected_item(self):
        return self._selected_item

    def set_selected_item(self, selected_item):
        self._selected_item = selected_item


    def _scroll_up(self):
        """Function that scrolls the view up in the scroll menu
        """

        if self._top_view > 0 and self._selected_item == self._top_view:
            self._top_view = self._top_view - 1
        if self._selected_item > 0:
            self._selected_item = self._selected_item - 1


    def _scroll_down(self, viewport_height):
        """Function that scrolls the view down in the scroll menu

        Parameters
        ----------
        viewport_height : int
            The number of visible viewport items
        """

        if self._selected_item < len(self._view_items) - 1:
            self._selected_item = self._selected_item + 1
        if self._selected_item > self._top_view + viewport_height:
            self._top_view = self._top_view + 1


    def add_item(self, item_text):
        """Adds an item to the menu.

        Parameters
        ----------
        item_text : str
            The text for the item
        """

        self._view_items.append(item_text)


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

        if len(self._view_items) == 0:
            return
        del self._view_items[self._selected_item]
        if self._selected_item >= len(self._view_items):
            self._selected_item = self._selected_item - 1


    def get_item_list(self):
        """Function that gets list of items in a scroll menu

        Returns
        -------
        item_list : list of str
            list of items in the scrollmenu
        """

        return self._view_items


    def get(self):
        """Function that gets the selected item from the scroll menu

        Returns
        -------
        item : str
            selected item, or None if there are no items in the menu
        """

        if len(self._view_items) > 0:
            return self._view_items[self._selected_item]
        return None


class TextBlockImplementation(UIImplementation):

    def __init__(self, initial_text, logger):

        super().__init__(logger)
        self._text_lines = initial_text.splitlines()
        if len(self._text_lines) == 0:
            self._text_lines.append('')

        self._viewport_y_start   = 0
        self._viewport_x_start   = 0
        self._cursor_text_pos_x  = 0
        self._cursor_text_pos_y  = 0
        self._cursor_y           = 0
        self._cursor_x           = 0
        self._cursor_max_up      = 0
        self._cursor_max_down    = 0
        self._cursor_max_left    = 0
        self._cursor_max_right   = 0
        self._viewport_width     = 0
        self._viewport_height    = 0


    # Getters and setters

    def viewport_y_start(self):
        return self._viewport_y_start

    def get_viewport_start_pos(self):
        return self._viewport_x_start, self._viewport_y_start

    def get_viewport_dims(self):
        return self._viewport_height, self._viewport_width

    def get_cursor_text_pos(self):
        return self._cursor_text_pos_x, self._cursor_text_pos_y

    def get_abs_cursor_position(self):
        return self._cursor_x, self._cursor_y

    def get_cursor_limits_vertical(self):
        return self._cursor_max_up, self._cursor_max_down

    def get_cursor_limits_horizontal(self):
        return self._cursor_max_left, self._cursor_max_right


    def get(self):
        """Gets all of the text in the textblock and returns it

        Returns
        -------
        text : str
            The current text in the text block
        """

        text = ''
        for line in self._text_lines:
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
        if len(self._text_lines) == 1 and self._text_lines[0] == '':
            self.set_text(text)
        else:
            self._text_lines.append(lines)


    def clear(self):
        """Function that clears the text block
        """

        self._cursor_x = self._cursor_max_left
        self._cursor_y = self._cursor_max_up
        self._cursor_text_pos_x = 0
        self._cursor_text_pos_y = 0
        self._text_lines = []
        self._text_lines.append('')


    def get_current_line(self):
        """Returns the line on which the cursor currently resides

        Returns
        -------
        current_line : str
            The current line of text that the cursor is on
        """

        return self._text_lines[self._cursor_text_pos_y]


    def set_text(self, text):
        """Function that sets the text for the textblock.

        Note that this will overwrite any existing text

        Parameters
        ----------
        text : str
            text to write into text block
        """

        self._text_lines = text.splitlines()
        if len(self._text_lines) == 0:
            self._text_lines.append('')

        self._cursor_text_pos_y    = 0
        self._cursor_y             = self._cursor_max_up
        self._viewport_y_start     = 0
        self._cursor_x             = self._cursor_max_left
        self._cursor_text_pos_x    = 0


    def set_text_line(self, text):
        """Function that sets the current line's text.

        Meant only for internal use

        Parameters
        ----------
        text : str
            text line to write into text block
        """

        self._text_lines[self._cursor_text_pos_y] = text


    def _move_left(self):
        """Function that moves the cursor/text position one location to the left
        """

        if self._cursor_text_pos_x > 0:
            if self._cursor_x > self._cursor_max_left:
                self._cursor_x = self._cursor_x - 1
            elif self._viewport_x_start > 0:
                self._viewport_x_start = self._viewport_x_start - 1
            self._cursor_text_pos_x = self._cursor_text_pos_x - 1


    def _move_right(self):
        """Function that moves the cursor/text position one location to the right
        """

        current_line = self.get_current_line()

        if self._cursor_text_pos_x < len(current_line):
            if self._cursor_x < self._cursor_max_right:
                self._cursor_x = self._cursor_x + 1
            elif self._viewport_x_start + self._viewport_width < len(current_line):
                self._viewport_x_start = self._viewport_x_start + 1
            self._cursor_text_pos_x = self._cursor_text_pos_x + 1


    def _move_up(self):
        """Function that moves the cursor/text position one location up
        """

        if self._cursor_text_pos_y > 0:
            if self._cursor_y > self._cursor_max_up:
                self._cursor_y = self._cursor_y - 1
            elif self._viewport_y_start > 0:
                self._viewport_y_start = self._viewport_y_start - 1
            self._cursor_text_pos_y = self._cursor_text_pos_y - 1
            if self._cursor_text_pos_x > len(self._text_lines[self._cursor_text_pos_y]):
                temp = len(self._text_lines[self._cursor_text_pos_y])
                self._cursor_x = self._cursor_x - (self._cursor_text_pos_x - temp)
                self._cursor_text_pos_x = temp


    def _move_down(self):
        """Function that moves the cursor/text position one location down
        """

        if self._cursor_text_pos_y < len(self._text_lines) - 1:
            if self._cursor_y < self._cursor_max_down:
                self._cursor_y = self._cursor_y + 1
            elif self._viewport_y_start + self._viewport_height < len(self._text_lines):
                self._viewport_y_start = self._viewport_y_start + 1
            self._cursor_text_pos_y = self._cursor_text_pos_y + 1
            if self._cursor_text_pos_x > len(self._text_lines[self._cursor_text_pos_y]):
                temp = len(self._text_lines[self._cursor_text_pos_y])
                self._cursor_x = self._cursor_x - (self._cursor_text_pos_x - temp)
                self._cursor_text_pos_x = temp


    def _handle_newline(self):
        """Function that handles recieving newline characters in the text
        """

        current_line = self.get_current_line()

        new_line_1 = current_line[:self._cursor_text_pos_x]
        new_line_2 = current_line[self._cursor_text_pos_x:]
        self._text_lines[self._cursor_text_pos_y] = new_line_1
        self._text_lines.insert(self._cursor_text_pos_y + 1, new_line_2)
        self._cursor_text_pos_y = self._cursor_text_pos_y + 1
        self._cursor_text_pos_x = 0
        self._cursor_x = self._cursor_max_left
        self._viewport_x_start = 0
        if self._cursor_y < self._cursor_max_down:
            self._cursor_y = self._cursor_y + 1
        elif self._viewport_y_start + self._viewport_height < len(self._text_lines):
            self._viewport_y_start = self._viewport_y_start + 1


    def _handle_backspace(self):
        """Function that handles recieving backspace characters in the text
        """

        current_line = self.get_current_line()

        if self._cursor_text_pos_x == 0 and self._cursor_text_pos_y != 0:
            self._cursor_text_pos_x = len(self._text_lines[self._cursor_text_pos_y - 1])
            self._text_lines[self._cursor_text_pos_y - 1] = self._text_lines[self._cursor_text_pos_y - 1] + self._text_lines[self._cursor_text_pos_y]
            self._text_lines = self._text_lines[:self._cursor_text_pos_y] + self._text_lines[self._cursor_text_pos_y + 1:]
            self._cursor_text_pos_y = self._cursor_text_pos_y - 1
            self._cursor_x = self._cursor_max_left + self._cursor_text_pos_x
            if self._cursor_y > self._cursor_max_up:
                self._cursor_y = self._cursor_y - 1
            elif self._viewport_y_start > 0:
                self._viewport_y_start = self._viewport_y_start - 1
        elif self._cursor_text_pos_x > 0:
            self.set_text_line(current_line[:self._cursor_text_pos_x - 1] + current_line[self._cursor_text_pos_x:])
            if len(current_line) <= self._viewport_width:
                self._cursor_x = self._cursor_x - 1
            self._cursor_text_pos_x = self._cursor_text_pos_x - 1


    def _handle_home(self):
        """Function that handles recieving a home keypress
        """

        self._cursor_x = self._cursor_max_left
        self._cursor_text_pos_x = 0
        self._viewport_x_start = 0


    def _handle_end(self):
        """Function that handles recieving an end keypress
        """

        current_line = self.get_current_line()

        self._cursor_text_pos_x = len(current_line)
        if len(current_line) > self._viewport_width:
            self._cursor_x = self._cursor_max_right
            self._viewport_x_start = self._cursor_text_pos_x - self._viewport_width
        else:
            self._cursor_x = self._cursor_max_left + len(current_line)


    def _handle_delete(self):
        """Function that handles recieving a delete keypress
        """

        current_line = self.get_current_line()

        if self._cursor_text_pos_x == len(current_line) and self._cursor_text_pos_y < len(self._text_lines) - 1:
            self._text_lines[self._cursor_text_pos_y] = self._text_lines[self._cursor_text_pos_y] + self._text_lines[self._cursor_text_pos_y + 1]
            self._text_lines = self._text_lines[:self._cursor_text_pos_y+1] + self._text_lines[self._cursor_text_pos_y + 2:]
        elif self._cursor_text_pos_x < len(current_line):
            self.set_text_line(current_line[:self._cursor_text_pos_x] + current_line[self._cursor_text_pos_x+1:])


    def _insert_char(self, key_pressed):
        """Function that handles recieving a character

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """

        current_line = self.get_current_line()

        self.set_text_line(current_line[:self._cursor_text_pos_x] + chr(key_pressed) + current_line[self._cursor_text_pos_x:])
        if len(current_line) <= self._viewport_width:
            self._cursor_x = self._cursor_x + 1
        elif self._viewport_x_start + self._viewport_width < len(current_line):
            self._viewport_x_start = self._viewport_x_start + 1
        self._cursor_text_pos_x = self._cursor_text_pos_x + 1