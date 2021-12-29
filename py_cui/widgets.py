"""Module containing all core widget classes for py_cui.

Widgets are the basic building blocks of a user interface made with py_cui.
This module contains classes for:

* Base Widget class
* Label
* Block Label
* Scroll Menu
* Checkbox Menu
* Button
* TextBox
* Text Block
* Slider

Additional widgets should be added in appropriate sub-modules, importing this
file and extending the base Widget class, or if appropriate one of the other core widgets.
"""

# Author:    Jakub Wlodek
# Created:   12-Aug-2019


import curses
import inspect
import py_cui
import py_cui.ui
import py_cui.colors
import py_cui.errors
import py_cui.debug

from typing import Union, Callable, List, Dict, Tuple, Any, Optional


class Widget(py_cui.ui.UIElement):
    """Top Level Widget Base Class

    Extended by all widgets. Contains base classes for handling key presses, drawing,
    and setting status bar text.

    Attributes
    ----------
    _grid : py_cui.grid.Grid
        The parent grid object of the widget
    _row, _column : int
        row and column position of the widget
    _row_span, _column_span : int
        number of rows or columns spanned by the widget
    _selectable : bool
        Flag that says if a widget can be selected
    _key_commands : dict
        Dictionary mapping key codes to functions
    _text_color_rules : List[py_cui.ColorRule]
        color rules to load into renderer when drawing widget
    """

    def __init__(self, id, title: str, grid: 'py_cui.grid.Grid', row: int, column: int, row_span: int, column_span: int, padx: int, pady: int, logger, selectable: bool = True):
        """Initializer for base widget class

        Class UIElement superclass initializer, and then assigns widget to grid, along with row/column info
        and color rules and key commands
        """

        super().__init__(id, title, None, logger)
        if grid is None:
            raise py_cui.errors.PyCUIMissingParentError("Cannot add widget to NoneType")

        self._grid = grid
        grid_rows, grid_cols = self._grid.get_dimensions()
        if (grid_cols < column + column_span) or (grid_rows < row + row_span):
            raise py_cui.errors.PyCUIOutOfBoundsError(f"Target grid too small for widget {title}")

        self._row          = row
        self._column       = column
        self._row_span     = row_span
        self._column_span  = column_span
        self._padx         = padx
        self._pady         = pady
        self._selectable       = selectable
        self._key_commands: Dict[int,Callable[[],Any]]     = {}
        self._mouse_commands: Dict[int,Callable[[],Any]]   = {}
        self._text_color_rules: List['py_cui.ColorRule'] = []
        self._default_color = py_cui.WHITE_ON_BLACK
        self._border_color = self._default_color
        self.update_height_width()


    def add_key_command(self, key: Union[int, List[int]], command: Callable[[],Any]) -> None:
        """Maps a keycode to a function that will be executed when in focus mode

        Parameters
        ----------
        key : py_cui.keys.KEY_*
            ascii keycode used to map the key
        command : function without args
            a non-argument function or lambda function to execute if in focus mode and key is pressed
        """

        if isinstance(key, list):
            for value in key:
                self._key_commands[value] = command
        else:
            self._key_commands[key] = command


    def add_mouse_command(self, mouse_event: int, command: Callable[[],Any]) -> None:
        """Maps a keycode to a function that will be executed when in focus mode

        Parameters
        ----------
        key : py_cui.keys.MOUSE_EVENT
            Mouse event code from py_cui.keys
        command : Callable
            a non-argument function or lambda function to execute if in focus mode and key is pressed

        Raises
        ------
        PyCUIError
            If input mouse event code is not valid
        """

        if mouse_event not in py_cui.keys.MOUSE_EVENTS:
            raise py_cui.errors.PyCUIError(f'Event code {mouse_event} is not a valid py_cui mouse event!')

        if mouse_event in self._mouse_commands.keys():
            self._logger.warn(f'Overriding mouse command for event {mouse_event}')

        self._mouse_commands[mouse_event] = command


    def update_key_command(self, key: Union[int, List[int]], command: Callable[[],Any]) -> Any:
        """Maps a keycode to a function that will be executed when in focus mode, if key is already mapped

        Parameters
        ----------
        key : py_cui.keys.KEY_*
            ascii keycode used to map the key
        command : function without args
            a non-argument function or lambda function to execute if in focus mode and key is pressed
        """

        if key in self._key_commands.keys():
            self.add_key_command(key, command)


    def add_text_color_rule(self, regex: str, color: int, rule_type: str, match_type: str='line', region: List[int]=[0,1], include_whitespace: bool=False, selected_color=None) -> None:
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
        region=[0,1] : [int, int]
            A specified region to color if using match_type='region'
        include_whitespace : bool
            if false, strip string before checking for match
        """

        selected = color
        if selected_color is not None:
            selected = selected_color

        new_color_rule = py_cui.colors.ColorRule(regex, color, selected, rule_type, match_type, region, include_whitespace, self._logger)
        self._text_color_rules.append(new_color_rule)


    def get_absolute_start_pos(self) -> Tuple[int,int]:
        """Gets the absolute position of the widget in characters. Override of base class function

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
        y_pos = self._row * row_height + y_adjust + self._grid._title_bar_offset + 1
        return x_pos, y_pos


    def get_absolute_stop_pos(self) -> Tuple[int,int]:
        """Gets the absolute dimensions of the widget in characters. Override of base class function

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


    def get_grid_cell(self) -> Tuple[int,int]:
        """Gets widget row, column in grid

        Returns
        -------
        row, column : int
            Initial row and column placement for widget in grid
        """

        return self._row, self._column


    def get_grid_cell_spans(self) -> Tuple[int,int]:
        """Gets widget row span, column span in grid

        Returns
        -------
        row_span, column_span : int
            Initial row span and column span placement for widget in grid
        """

        return self._row_span, self._column_span


    def set_selectable(self, selectable: bool) -> None:
        """Setter for widget selectablility

        Paramters
        ---------
        selectable : bool
            Widget selectable if true, otherwise not
        """

        self._selectable = selectable


    def is_selectable(self) -> bool:
        """Checks if the widget is selectable

        Returns
        -------
        selectable : bool
            True if selectable, false otherwise
        """

        return self._selectable


    def _is_row_col_inside(self, row: int, col: int) -> bool:
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


    def _handle_mouse_press(self, x: int, y: int, mouse_event: int):
        """Base class function that handles all assigned mouse presses.

        When overwriting this function, make sure to add a super()._handle_mouse_press(x, y, mouse_event) call,
        as this is required for user defined key command support

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """

        # Retrieve the command function if it exists
        if mouse_event in self._mouse_commands.keys():
            command = self._mouse_commands[mouse_event]

            # Identify num of args from callable. This allows for user to create commands that take in x, y
            # coords of the mouse press as input
            num_args = 0
            try:
                num_args = len(inspect.signature(command).parameters)
            except ValueError:
                self._logger.error('Failed to get mouse press command signature!')
            except TypeError:
                self._logger.error('Type of object not supported for signature identification!')

            # Depending on the number of parameters for the command, pass in the x and y
            # values, or do nothing
            if num_args == 2:
                command(x, y)
            else:
                command()


    def _handle_key_press(self, key_pressed: int) -> None:
        """Base class function that handles all assigned key presses.

        When overwriting this function, make sure to add a super()._handle_key_press(key_pressed) call,
        as this is required for user defined key command support

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """

        if key_pressed in self._key_commands.keys():
            command = self._key_commands[key_pressed]
            command()


    def _draw(self) -> None:
        """Base class draw class that checks if renderer is valid.

        Should be called with super()._draw() in overrides.
        Also intializes color rules, so if not called color rules will not be applied
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

    def __init__(self, id, title: str,  grid: 'py_cui.grid.Grid', row: int, column: int, row_span: int, column_span: int, padx: int, pady: int, logger):
        """Initalizer for Label widget
        """

        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady, logger, selectable=False)
        self._draw_border = False


    def toggle_border(self) -> None:
        """Function that gives option to draw border around label
        """

        self._draw_border = not self._draw_border


    def _draw(self) -> None:
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

    def __init__(self, id, title: str,  grid: 'py_cui.grid.Grid', row: int, column: int, row_span: int, column_span: int, padx: int, pady: int, logger: py_cui.debug.PyCUILogger, center: bool):
        """Initializer for blocklabel widget
        """

        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady, logger, selectable=False)
        self._lines        = title.splitlines()
        self._center       = center
        self._draw_border  = False


    def set_title(self, title: str) -> None:
        """Override of base class, splits title into lines for rendering line by line.

        Parameters
        ----------
        title : str
            The new title for the block label object.
        """

        self._title = title
        self._lines = title.splitlines()


    def toggle_border(self) -> None:
        """Function that gives option to draw border around label
        """

        self._draw_border = not self._draw_border


    def _draw(self) -> None:
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

    def __init__(self, id, title: str, grid: 'py_cui.grid.Grid', row: int, column: int, row_span: int, column_span: int, padx: int, pady: int, logger: 'py_cui.debug.PyCUILogger'):
        """Initializer for scroll menu. calls superclass initializers and sets help text
        """

        Widget.__init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger)
        py_cui.ui.MenuImplementation.__init__(self, logger)
        self.set_help_text('Focus mode on ScrollMenu. Use Up/Down/PgUp/PgDown/Home/End to scroll, Esc to exit.')


    def _handle_mouse_press(self, x: int, y: int, mouse_event: int):
        """Override of base class function, handles mouse press in menu

        Parameters
        ----------
        x, y : int
            Coordinates of mouse press
        """

        # For either click or double click we want to jump to the clicked-on item
        if mouse_event == py_cui.keys.LEFT_MOUSE_CLICK or mouse_event == py_cui.keys.LEFT_MOUSE_DBL_CLICK:
            current = self.get_selected_item_index()
            viewport_top = self._start_y + self._pady + 1

            if viewport_top <= y and viewport_top + len(self._view_items) - self._top_view >= y:
                elem_clicked = y - viewport_top + self._top_view
                self.set_selected_item_index(elem_clicked)

            if self.get_selected_item_index() != current and self._on_selection_change is not None:
                self._process_selection_change_event()

        # For scroll menu, handle custom mouse press after initial event, since we will likely want to
        # have access to the newly selected item
        Widget._handle_mouse_press(self, x, y, mouse_event)



    def _handle_key_press(self, key_pressed: int) -> None:
        """Override base class function.

        UP_ARROW scrolls up, DOWN_ARROW scrolls down.

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """

        Widget._handle_key_press(self, key_pressed)

        current = self.get_selected_item_index()
        viewport_height = self.get_viewport_height()

        if key_pressed == py_cui.keys.KEY_UP_ARROW:
            self._scroll_up()
        if key_pressed == py_cui.keys.KEY_DOWN_ARROW:
            self._scroll_down(viewport_height)
        if key_pressed == py_cui.keys.KEY_HOME:
            self._jump_to_top()
        if key_pressed == py_cui.keys.KEY_END:
            self._jump_to_bottom(viewport_height)
        if key_pressed == py_cui.keys.KEY_PAGE_UP:
            self._jump_up()
        if key_pressed == py_cui.keys.KEY_PAGE_DOWN:
            self._jump_down(viewport_height)
        if self.get_selected_item_index() != current and self._on_selection_change is not None:

            self._process_selection_change_event()


    def _draw(self) -> None:
        """Overrides base class draw function
        """

        Widget._draw(self)
        self._renderer.set_color_mode(self._color)
        self._renderer.draw_border(self)
        counter = self._pady + 1
        line_counter = 0
        for item in self._view_items:
            line = str(item)
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


class CheckBoxMenu(Widget, py_cui.ui.CheckBoxMenuImplementation):
    """Extension of ScrollMenu that allows for multiple items to be selected at once.

    Attributes
    ----------
    selected_item_list : list of str
        List of checked items
    checked_char : char
        Character to represent a checked item
    """

    def __init__(self, id, title: str, grid: 'py_cui.grid.Grid', row: int, column: int, row_span: int, column_span: int, padx: int, pady: int, logger, checked_char: str):
        """Initializer for CheckBoxMenu Widget
        """

        Widget.__init__(self,id, title, grid, row, column, row_span, column_span, padx, pady, logger)
        py_cui.ui.CheckBoxMenuImplementation.__init__(self, logger, checked_char)
        self.set_help_text('Focus mode on CheckBoxMenu. Use up/down to scroll, Enter to toggle set, unset, Esc to exit.')


    def _handle_mouse_press(self, x: int, y: int, mouse_event: int) -> None:
        """Override of base class function, handles mouse press in menu

        Parameters
        ----------
        x, y : int
            Coordinates of mouse press
        """

        Widget._handle_mouse_press(self, x, y, mouse_event)
        viewport_top = self._start_y + self._pady + 1
        if viewport_top <= y and viewport_top + len(self._view_items) - self._top_view >= y:
            elem_clicked = y - viewport_top + self._top_view
            self.set_selected_item_index(elem_clicked)
            self.mark_item_as_checked(self._view_items[elem_clicked])


    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of key presses.

        First, run the superclass function, scrolling should still work.
        Adds Enter command to toggle selection

        Parameters
        ----------
        key_pressed : int
            key code of pressed key
        """

        Widget._handle_key_press(self, key_pressed)
        viewport_height = self.get_viewport_height()
        if key_pressed == py_cui.keys.KEY_UP_ARROW:
            self._scroll_up()
        if key_pressed == py_cui.keys.KEY_DOWN_ARROW:
            self._scroll_down(viewport_height)
        if key_pressed == py_cui.keys.KEY_HOME:
            self._jump_to_top()
        if key_pressed == py_cui.keys.KEY_END:
            self._jump_to_bottom(viewport_height)
        if key_pressed == py_cui.keys.KEY_PAGE_UP:
            self._jump_up()
        if key_pressed == py_cui.keys.KEY_PAGE_DOWN:
            self._jump_down(viewport_height)
        if key_pressed == py_cui.keys.KEY_ENTER:
            self.toggle_item_checked(self.get())


    def _draw(self) -> None:
        """Overrides base class draw function
        """

        Widget._draw(self)
        self._renderer.set_color_mode(self._color)
        self._renderer.draw_border(self)
        counter = self._pady + 1
        line_counter = 0
        for item in self._view_items:
            if self._selected_item_dict[item]:
                line = f'[{self._checked_char}] - {str(item)}'
            else:
                line = f'[ ] - {str(item)}'
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



class Button(Widget):
    """Basic button widget.

    Allows for running a command function on Enter

    Attributes
    ----------
    command : function
        A no-args function to run when the button is pressed.
    """

    def __init__(self, id, title: str, grid: 'py_cui.grid.Grid', row: int, column: int, row_span: int, column_span: int, padx: int, pady: int, logger, command: Optional[Callable[[],Any]]):
        """Initializer for Button Widget
        """

        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady, logger)
        self.command = command
        self.set_color(py_cui.MAGENTA_ON_BLACK)
        self.set_help_text('Focus mode on Button. Press Enter to press button, Esc to exit focus mode.')

        # By default we will process command on click or double click
        if self.command is not None:
            self.add_mouse_command(py_cui.keys.LEFT_MOUSE_CLICK, self.command)
            self.add_mouse_command(py_cui.keys.LEFT_MOUSE_DBL_CLICK, self.command)


    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of base class, adds ENTER listener that runs the button's command

        Parameters
        ----------
        key_pressed : int
            Key code of pressed key
        """

        super()._handle_key_press(key_pressed)
        if key_pressed == py_cui.keys.KEY_ENTER:
            if self.command is not None:
                return self.command()


    def _draw(self) -> None:
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

    def __init__(self, id, title: str, grid: 'py_cui.grid.Grid', row: int, column: int, row_span: int, column_span: int, padx: int, pady: int, logger, initial_text: str, password: bool):
        """Initializer for TextBox widget. Uses TextBoxImplementation as base
        """

        Widget.__init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger)
        py_cui.ui.TextBoxImplementation.__init__(self, initial_text, password, logger)
        self.update_height_width()
        self.set_help_text('Focus mode on TextBox. Press Esc to exit focus mode.')


    def update_height_width(self) -> None:
        """Need to update all cursor positions on resize
        """

        Widget.update_height_width(self)
        padx, _             = self.get_padding()
        start_x, start_y    = self.get_start_position()
        height, width       = self.get_absolute_dimensions()
        self._initial_cursor     = start_x + padx + 2
        self._cursor_text_pos    = 0
        self._cursor_x           = start_x + padx + 2
        self._cursor_max_left    = start_x + padx + 2
        self._cursor_max_right   = start_x + width - padx - 1
        self._cursor_y           = start_y + int(height / 2) + 1
        self._viewport_width     = self._cursor_max_right - self._cursor_max_left


    def _handle_mouse_press(self, x: int, y: int, mouse_event: int) -> None:
        """Override of base class function, handles mouse press in menu

        Parameters
        ----------
        x, y : int
            Coordinates of mouse press
        """

        Widget._handle_mouse_press(self, x, y, mouse_event)
        if y == self._cursor_y and x >= self._cursor_max_left and x <= self._cursor_max_right:
            if x <= len(self._text) + self._cursor_max_left:
                old_text_pos = self._cursor_text_pos
                old_cursor_x = self._cursor_x
                self._cursor_x = x
                self._cursor_text_pos = old_text_pos + (x - old_cursor_x)
            else:
                self._cursor_x = self._cursor_max_left + len(self._text)
                self._cursor_text_pos = len(self._text)


    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of base handle key press function

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """

        Widget._handle_key_press(self, key_pressed)
        if key_pressed == py_cui.keys.KEY_LEFT_ARROW:
            self._move_left()
        elif key_pressed == py_cui.keys.KEY_RIGHT_ARROW:
            self._move_right()
        elif key_pressed in py_cui.keys.KEY_BACKSPACE:
            self._erase_char()
        elif key_pressed == py_cui.keys.KEY_DELETE:
            self._delete_char()
        elif key_pressed == py_cui.keys.KEY_HOME:
            self._jump_to_start()
        elif key_pressed == py_cui.keys.KEY_END:
            self._jump_to_end()
        elif key_pressed > 31 and key_pressed < 128 or \
                key_pressed > 1000 and key_pressed < 1128:
            self._insert_char(key_pressed)


    def _draw(self) -> None:
        """Override of base draw function
        """

        Widget._draw(self)

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
    """

    def __init__(self, id, title: str, grid: 'py_cui.grid.Grid', row: int, column: int, row_span: int, column_span: int, padx: int, pady: int, logger, initial_text: str):
        """Initializer for TextBlock Widget. Uses TextBlockImplementation as base
        """

        Widget.__init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger)
        py_cui.ui.TextBlockImplementation.__init__(self, initial_text, logger)
        self.update_height_width()
        self.set_help_text('Focus mode on TextBlock. Press Esc to exit focus mode.')


    def update_height_width(self) -> None:
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


    def _handle_mouse_press(self, x: int, y: int, mouse_event: int) -> None:
        """Override of base class function, handles mouse press in menu

        Parameters
        ----------
        x, y : int
            Coordinates of mouse press
        """

        Widget._handle_mouse_press(self, x, y, mouse_event)

        if mouse_event == py_cui.keys.LEFT_MOUSE_CLICK:
            if y >= self._cursor_max_up and y <= self._cursor_max_down:
                if x >= self._cursor_max_left and x <= self._cursor_max_right:
                    line_clicked_index = y - self._cursor_max_up + self._viewport_y_start
                    if len(self._text_lines) <= line_clicked_index:
                        self._cursor_text_pos_y = len(self._text_lines) - 1
                        self._cursor_y = self._cursor_max_up + self._cursor_text_pos_y - self._viewport_y_start
                        line = self._text_lines[len(self._text_lines) - 1]
                    else:
                        self._cursor_text_pos_y = line_clicked_index
                        self._cursor_y = y
                        line = self._text_lines[line_clicked_index]

                    if x <= len(line) + self._cursor_max_left:
                        old_text_pos = self._cursor_text_pos_x
                        old_cursor_x = self._cursor_x
                        self._cursor_x = x
                        self._cursor_text_pos_x = old_text_pos + (x - old_cursor_x)
                    else:
                        self._cursor_x = self._cursor_max_left + len(line)
                        self._cursor_text_pos_x = len(line)


    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of base class handle key press function

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """

        Widget._handle_key_press(self, key_pressed)

        if key_pressed == py_cui.keys.KEY_LEFT_ARROW:
            self._move_left()
        elif key_pressed == py_cui.keys.KEY_RIGHT_ARROW:
            self._move_right()
        elif key_pressed == py_cui.keys.KEY_UP_ARROW:
            self._move_up()
        # TODO: Fix this janky operation here
        elif key_pressed == py_cui.keys.KEY_DOWN_ARROW and self._cursor_text_pos_y < len(self._text_lines) - 1:
            self._move_down()
        elif key_pressed in py_cui.keys.KEY_BACKSPACE:
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


    def _draw(self) -> None:
        """Override of base class draw function
        """

        Widget._draw(self)

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


