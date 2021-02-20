"""Module containing classes for generic UI elements.

Contains base UI element class, along with UI implementation agnostic UI element classes.
"""

# Author:    Jakub Wlodek
# Created:   19-Mar-2020


import py_cui
import py_cui.errors
import py_cui.colors


class UIElement:
    """Base class for all UI elements. Extended by base widget and popup classes.

    Interfaces between UIImplementation subclasses and CUI engine. For example,
    a widget is a subclass of a UIElement. Then a TextBox widget would be a subclass
    of the base widget class, and the TextBoxImplementation. The TextBoxImplementation
    superclass contains logic for all textbox required operations, while the widget base
    class contains all links to the CUI engine.

    Attributes
    ----------
    _id : str
        Internal UI element unique ID
    _title : str
        UI element title
    _padx, pady : int, int
        padding in terminal characters
    _start_x, _start_y: int, int
        Coords in terminal characters for top-left corner of element
    _stop_x, _stop_y : int, int
        Coords in terminal characters for bottom-right corner of element
    _height, width : int, int
        absolute dimensions of ui element in terminal characters
    _color : int
        Default color for which to draw element
    _border_color: int
        Color used to draw the border of the element when not focused
    _focus_border_color: int
        Color used to draw the border of the element when focused
    _selected : bool
        toggle for marking an element as selected
    _renderer : py_cui.renderer.Renderer
        The default ui renderer
    _logger   : py_cui.debug.PyCUILogger
        The default logger inherited from the parent
    _help_text: str
        Text to diplay when selected in status bar
    """

    def __init__(self, id, title, renderer, logger):
        """Initializer for UIElement base class
        """

        self._id                        = id
        self._title                     = title
        self._padx                      = 1
        self._pady                      = 0
        self._start_x,  self._stop_y    = 0, 0
        self._stop_x,   self._start_y   = 0, 0
        self._height,   self._width     = 0, 0
        # Default UI Element color is white on black.
        self._color                     = py_cui.WHITE_ON_BLACK
        self._border_color              = self._color
        self._focus_border_color        = self._color
        self._selected_color            = self._color
        self._mouse_press_handler       = None
        self._selected                  = False
        self._renderer                  = renderer
        self._logger                    = logger
        self._help_text                 = ''


    def get_absolute_start_pos(self):
        """Must be implemented by subclass, computes the absolute coords of upper-left corner
        """

        raise NotImplementedError


    def get_absolute_stop_pos(self):
        """Must be implemented by subclass, computes the absolute coords of bottom-right corner
        """

        raise NotImplementedError


    def get_absolute_dimensions(self):
        """Gets dimensions of element in terminal characters

        Returns
        -------
        height, width : int, int
            Dimensions of element in terminal characters
        """
        start_x,    start_y = self.get_absolute_start_pos()
        stop_x,     stop_y  = self.get_absolute_stop_pos()
        return (stop_y - start_y), (stop_x - start_x)


    def update_height_width(self):
        """Function that refreshes position and dimensons on resize.

        If necessary, make sure required widget attributes updated here as well.
        """

        self._start_x, self._start_y  = self.get_absolute_start_pos()
        self._stop_x,  self._stop_y   = self.get_absolute_stop_pos()
        self._height,  self._width    = self.get_absolute_dimensions()


    def get_viewport_height(self):
        """Gets the height of the element viewport (height minus padding and borders)

        Returns
        -------
        viewport_height : int
            Height of element viewport in terminal characters
        """

        return self._height - (2 * self._pady) - 3


    def get_id(self):
        """Gets the element ID

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


    def get_stop_position(self):
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


    def get_border_color(self):
        """Gets current element border color

        Returns
        -------
        color : int
            color code for combination
        """

        if self._selected:
            return self._focus_border_color
        else:
            return self._border_color


    def get_selected_color(self):
        """Gets current selected item color

        Returns
        -------
        color : int
            color code for combination
        """

        return self._selected_color


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
        """Returns current help text

        Returns
        -------
        help_text : str
            Current element status bar help message
        """

        return self._help_text


    def set_title(self, title):
        """Function that sets the widget title.

        Parameters
        ----------
        title : str
            New widget title
        """

        self._title = title


    def set_color(self, color):
        """Sets element default color

        Parameters
        ----------
        color : int
            New color pair key code
        """

        if self._border_color == self._color:
            self._border_color = color
        if self._focus_border_color == self._color:
            self._focus_border_color = color
        if self._selected_color == self._color:
            self._selected_color = color
        self._color = color


    def set_border_color(self, color):
        """Sets element border color

        Parameters
        ----------
        color : int
            New color pair key code
        """

        self._border_color = color


    def set_focus_border_color(self, color):
        """Sets element border color if the current element
        is focused

        Parameters
        ----------
        color : int
            New color pair key code
        """

        self._focus_border_color = color


    def set_selected_color(self, color):
        """Sets element sected color

        Parameters
        ----------
        color : int
            New color pair key code
        """

        self._selected_color = color


    def set_selected(self, selected):
        """Marks the UI element as selected or not selected

        Parameters
        ----------
        selected : bool
            The new selected state of the element
        """

        self._selected = selected


    def set_help_text(self, help_text):
        """Sets status bar help text

        Parameters
        ----------
        help_text : str
            New statusbar help text
        """

        self._help_text = help_text


    def set_focus_text(self, focus_text):
        """Sets status bar focus text. Legacy function, overridden by set_focus_text

        Parameters
        ----------
        focus_text : str
            New statusbar help text
        """

        self._help_text = focus_text


    def _handle_key_press(self, key_pressed):
        """Must be implemented by subclass. Used to handle keypresses
        """

        raise NotImplementedError


    def add_mouse_press_handler(self, mouse_press_handler_func):
        """Sets a mouse press handler function

        Parameters
        ----------
        mouse_press_handler_func : function / lambda function
            Function that takes 2 parameters: x and y of a mouse press. Executes when mouse pressed and element is selected
        """

        self._mouse_press_handler = mouse_press_handler_func


    def _handle_mouse_press(self, x, y):
        """Can be implemented by subclass. Used to handle mouse presses

        Parameters
        ----------
        x, y : int, int
            Coordinates of the mouse press event.
        """

        if self._mouse_press_handler is not None:
            self._mouse_press_handler(x, y)


    def _draw(self):
        """Must be implemented by subclasses. Uses renderer to draw element to terminal
        """

        raise NotImplementedError


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
            If parameter is not an initialized renderer.
        """

        if isinstance(renderer, py_cui.renderer.Renderer):
            self._renderer = renderer
        elif self._renderer is not None:
            raise py_cui.errors.PyCUIError('Renderer already assigned for the element')
        else:
            raise py_cui.errors.PyCUIError('Invalid renderer, must be of type py_cui.renderer.Renderer')


    def _contains_position(self, x, y):
        """Checks if character position is within element.

        Parameters
        ----------
        x : int
            X coordinate to check
        y : int
            Y coordinate to check

        Returns
        -------
        contains : bool
            True if (x,y) is within the element, false otherwise
        """

        within_x = self._start_x <= x and self._start_x + self._width >= x
        within_y = self._start_y <= y and self._start_y + self._height >= y
        return within_x and within_y


class UIImplementation:
    """Base class for ui implementations.

    Should be extended for creating logic common accross ui elements.
    For example, a textbox needs the same logic for a widget or popup.
    This base class is only used to initialize the logger

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
    _initial_cursor : int
        Initial position of the cursor
    _cursor_x, _cursor_y : int
        The absolute positions of the cursor in the terminal window
    _cursor_text_pos : int
        the cursor position relative to the text
    _cursor_max_left, cursor_max_right : int
        The cursor bounds of the text box
    _viewport_width : int
        The width of the textbox viewport
    _password : bool
        Toggle to display password characters or text
    """

    def __init__(self, initial_text, password, logger):
        """Initializer for the TextBoxImplementation base class
        """

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
        """Gets initial cursor position

        Returns
        -------
        initial_cursor : int
            Initial position of the cursor
        """

        return self._initial_cursor


    def get_cursor_text_pos(self):
        """Gets current position of cursor relative to text

        Returns
        -------
        cursor_text_pos : int
            the cursor position relative to the text
        """

        return self._cursor_text_pos


    def get_cursor_limits(self):
        """Gets cursor extreme points in terminal position

        Returns
        -------
        cursor_max_left, cursor_max_right : int
            The cursor bounds of the text box
        """

        return self._cursor_max_left, self._cursor_max_right


    def get_cursor_position(self):
        """Returns current cursor poition

        Returns
        -------
        cursor_x, cursor_y : int
            The absolute positions of the cursor in the terminal window
        """

        return self._cursor_x, self._cursor_y


    def get_viewport_width(self):
        """Gets the width of the textbox viewport

        Returns
        -------
        viewport_width : int
            The width of the textbox viewport
        """

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
        """Inserts char at cursor position. Internal use only

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
        """Jumps to the start of the textbox. Internal use only
        """

        self._cursor_x = self._initial_cursor
        self._cursor_text_pos = 0


    def _jump_to_end(self):
        """Jumps to the end to the textbox. Internal use only
        """

        self._cursor_text_pos = len(self._text)
        self._cursor_x = self._initial_cursor + self._cursor_text_pos


    def _erase_char(self):
        """Erases character at textbox cursor. Internal Use only
        """

        if self._cursor_text_pos > 0:
            self._text = self._text[:self._cursor_text_pos - 1] + self._text[self._cursor_text_pos:]
            if len(self._text) < self._viewport_width:
                self._cursor_x = self._cursor_x - 1
            self._cursor_text_pos = self._cursor_text_pos - 1


    def _delete_char(self):
        """Deletes character to right of texbox cursor. Internal use only
        """

        if self._cursor_text_pos < len(self._text):
            self._text = self._text[:self._cursor_text_pos] + self._text[self._cursor_text_pos + 1:]


class MenuImplementation(UIImplementation):
    """A scrollable menu UI element

    Allows for creating a scrollable list of items of which one is selectable.
    Analogous to a RadioButton

    Attributes
    ----------
    _top_view : int
        the uppermost menu element in view
    _selected_item : int
        the currently highlighted menu item
    _view_items : list of str
        list of menu items
    """

    def __init__(self, logger):
        """Initializer for MenuImplementation base class
        """

        super().__init__(logger)
        self._top_view         = 0
        self._selected_item    = 0
        self._page_scroll_len  = 5
        self._view_items       = []


    def clear(self):
        """Clears all items from the Scroll Menu
        """

        self._view_items = []
        self._selected_item = 0
        self._top_view = 0

        self._logger.info('Clearing menu')



    def get_selected_item_index(self):
        """Gets the currently selected item

        Returns
        -------
        selected_item : int
            the currently highlighted menu item
        """

        return self._selected_item


    def set_selected_item_index(self, selected_item_index):
        """Sets the currently selected item

        Parameters
        ----------
        selected_item : int
            The new selected item index
        """

        self._selected_item = selected_item_index


    def _scroll_up(self):
        """Function that scrolls the view up in the scroll menu
        """

        if self._top_view > 0 and self._selected_item == self._top_view:
            self._top_view = self._top_view - 1
        if self._selected_item > 0:
            self._selected_item = self._selected_item - 1

        self._logger.info('Scrolling up to item {}'.format(self._selected_item))


    def _scroll_down(self, viewport_height):
        """Function that scrolls the view down in the scroll menu

        TODO: Viewport height should be calculated internally, and not rely on a parameter.

        Parameters
        ----------
        viewport_height : int
            The number of visible viewport items
        """

        if self._selected_item < len(self._view_items) - 1:
            self._selected_item = self._selected_item + 1
        if self._selected_item > self._top_view + viewport_height:
            self._top_view = self._top_view + 1

        self._logger.info('Scrolling down to item {}'.format(self._selected_item))


    def _jump_up(self):
        """Function for jumping up menu several spots at a time
        """

        for _ in range(self._page_scroll_len):
            self._scroll_up()


    def _jump_down(self, viewport_height):
        """Function for jumping down the menu several spots at a time

        Parameters
        ----------
        viewport_height : int
            The number of visible viewport items
        """

        for _ in range(self._page_scroll_len):
            self._scroll_down(viewport_height)


    def _jump_to_top(self):
        """Function that jumps to the top of the menu
        """

        self._top_view      = 0
        self._selected_item = 0


    def _jump_to_bottom(self, viewport_height):
        """Function that jumps to the bottom of the menu

        Parameters
        ----------
        viewport_height : int
            The number of visible viewport items
        """

        self._selected_item = len(self._view_items) - 1
        self._top_view = self._selected_item - viewport_height
        if self._top_view < 0:
            self._top_view = 0


    def add_item(self, item):
        """Adds an item to the menu.

        Parameters
        ----------
        item : Object
            Object to add to the menu. Must have implemented __str__ function
        """

        self._logger.info('Adding item {} to menu'.format(str(item)))
        self._view_items.append(item)


    def add_item_list(self, item_list):
        """Adds a list of items to the scroll menu.

        Parameters
        ----------
        item_list : List[Object]
            list of objects to add as items to the scrollmenu
        """

        self._logger.info('Adding item list {} to menu'.format(str(item_list)))
        for item in item_list:
            self.add_item(item)


    def remove_selected_item(self):
        """Function that removes the selected item from the scroll menu.
        """

        if len(self._view_items) == 0:
            return
        self._logger.info('Removing {}'.format(str(self._view_items[self._selected_item])))
        del self._view_items[self._selected_item]
        if self._selected_item >= len(self._view_items) and self._selected_item > 0:
            self._selected_item = self._selected_item - 1


    def remove_item(self, item):
        """Function that removes a specific item from the menu

        Parameters
        ----------
        item : Object
            Reference of item to remove
        """

        if len(self._view_items) == 0 or item not in self._view_items:
            return
        self._logger.info('Removing {}'.format(str(item)))
        i_index = self._view_items.index(item)
        del self._view_items[i_index]
        if self._selected_item >= i_index:
            self._selected_item = self._selected_item - 1


    def get_item_list(self):
        """Function that gets list of items in a scroll menu

        Returns
        -------
        item_list : List[Object]
            list of items in the scrollmenu
        """

        return self._view_items


    def get(self):
        """Function that gets the selected item from the scroll menu

        Returns
        -------
        item : Object
            selected item, or None if there are no items in the menu
        """

        if len(self._view_items) > 0:
            return self._view_items[self._selected_item]
        return None


    def set_selected_item(self, selected_item):
        """Function that replaces the currently selected item with a new item

        Parameters
        ----------
        item : Object
            A new selected item to replace the current one
        """

        if selected_item is not None and self.get() is not None:
            self._view_items[self._selected_item] = selected_item


class CheckBoxMenuImplementation(MenuImplementation):
    """Class representing checkbox menu ui implementation

    Attributes
    ----------
    _selected_item_dict : dict of object -> bool
        stores each object and maps to its current selected status
    _checked_char : char
        Character to mark checked items
    """

    def __init__(self, logger, checked_char):
        """Initializer for the checkbox menu implementation
        """

        super().__init__(logger)
        self._selected_item_dict = {}
        self._checked_char       = checked_char


    def add_item(self, item):
        """Extends base class function, item is added and marked as unchecked to start

        Parameters
        ----------
        item : object
            The item being added
        """

        super().add_item(item)
        self._selected_item_dict[item] = False


    def remove_selected_item(self):
        """Removes selected item from item list and selected item dictionary
        """

        del self._selected_item_dict[self.get()]
        super().remove_selected_item()


    def remove_item(self, item):
        """Removes item from item list and selected item dict

        Parameters
        ----------
        item : object
            Item to remove from menu
        """

        del self._selected_item_dict[item]
        super().remove_item(item)


    def mark_item_as_checked(self, item):
        """Function that marks an item as selected

        Parameters
        ----------
        item : object
            Mark item as checked
        """

        self._selected_item_dict[item] = not self._selected_item_dict[item]


class TextBlockImplementation(UIImplementation):
    """Base class for TextBlockImplementation

    Contains all logic required for a textblock ui element to function.
    Currently only implemented in widget form, though popup form is possible.

    Attributes
    ----------
    _text_lines : List[str]
        the lines of text in the texbox
    _viewport_x_start, _viewport_y_start : int
        Initial location of viewport relative to text
    _cursor_text_pos_x, _cursor_text_pos_y : int
        Cursor position relative to text
    _cursor_x, _cursor_y : int
        Absolute cursor position in characters
    _cursor_max_up, _cursor_max_down : int
        cursor limits in vertical space
    _cursor_max_left, _cursor_max_right : int
        Cursor limits in horizontal space
    _viewport_height, _viewport_width : int
        The dimensions of the viewport in characters
    """

    def __init__(self, initial_text, logger):
        """Initializer for TextBlockImplementation base class

        Zeros attributes, and parses initial text
        """

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

    def get_viewport_start_pos(self):
        """Gets upper left corner position of viewport

        Returns
        -------
        viewport_x_start, viewport_y_start : int
            Initial location of viewport relative to text
        """

        return self._viewport_x_start, self._viewport_y_start


    def get_viewport_dims(self):
        """Gets viewport dimensions in characters

        Returns
        -------
        viewport_height, viewport_width : int
            The dimensions of the viewport in characters
        """

        return self._viewport_height, self._viewport_width


    def get_cursor_text_pos(self):
        """Gets cursor postion relative to text

        Returns
        -------
        cursor_text_pos_x, cursor_text_pos_y : int
            Cursor position relative to text
        """


        return self._cursor_text_pos_x, self._cursor_text_pos_y


    def get_abs_cursor_position(self):
        """Gets absolute cursor position in terminal characters

        Returns
        -------
        cursor_x, cursor_y : int
            Absolute cursor position in characters
        """

        return self._cursor_x, self._cursor_y


    def get_cursor_limits_vertical(self):
        """Gets limits for cursor in vertical direction

        Returns
        -------
        cursor_max_up, cursor_max_down : int
            cursor limits in vertical space
        """

        return self._cursor_max_up, self._cursor_max_down


    def get_cursor_limits_horizontal(self):
        """Gets limits for cursor in horizontal direction

        Returns
        -------
        cursor_max_left, cursor_max_right : int
            Cursor limits in horizontal space
        """

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
        self._logger.info('Cleared textblock')


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

        self._logger.info('Moved cursor left to pos {}'.format(self._cursor_text_pos_x))


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

        self._logger.info('Moved cursor right to pos {}'.format(self._cursor_text_pos_x))


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

        self._logger.info('Moved cursor up to line {}'.format(self._cursor_text_pos_y))


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

        self._logger.info('Moved cursor down to line {}'.format(self._cursor_text_pos_y))



    def _handle_newline(self):
        """Function that handles recieving newline characters in the text
        """

        current_line = self.get_current_line()
        self._logger.info('Inserting newline in location {}'.format(self._cursor_text_pos_x))

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
        self._logger.info('Inserting backspace in location {}'.format(self._cursor_text_pos_x))

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

        self._logger.info('Inserting Home')

        self._cursor_x = self._cursor_max_left
        self._cursor_text_pos_x = 0
        self._viewport_x_start = 0


    def _handle_end(self):
        """Function that handles recieving an end keypress
        """

        current_line = self.get_current_line()
        self._logger.info('Inserting End')

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
        self._logger.info('Inserting delete to pos {}'.format(self._cursor_text_pos_x))

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
        self._logger.info('Inserting character {} to pos {}'.format(chr(key_pressed), self._cursor_text_pos_x))

        self.set_text_line(current_line[:self._cursor_text_pos_x] + chr(key_pressed) + current_line[self._cursor_text_pos_x:])
        if len(current_line) <= self._viewport_width:
            self._cursor_x = self._cursor_x + 1
        elif self._viewport_x_start + self._viewport_width < len(current_line):
            self._viewport_x_start = self._viewport_x_start + 1
        self._cursor_text_pos_x = self._cursor_text_pos_x + 1
