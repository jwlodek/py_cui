"""File containing class that abstracts a collection of widgets.

It can be used to swap between collections of widgets (screens) in a py_cui
"""

# Author:    Jakub Wlodek
# Created:   12-Aug-2019

# TODO: Should create an initial widget set in PyCUI class that widgets are added to by default.

import shutil
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING
import py_cui.widgets as widgets
import py_cui.grid as grid
import py_cui.controls as controls

if TYPE_CHECKING:
    import py_cui


class WidgetSet:
    """Class that represents a collection of widgets.

    Use PyCUI.apply_widget_set() to set a given widget set for display

    Attributes
    ----------
    grid : py_cui.grid.Grid
        The main layout manager for the CUI
    widgets : dict of str - py_cui.widgets.Widget
        dict of widget in the grid
    keybindings : list of py_cui.keybinding.KeyBinding
        list of keybindings to check against in the main CUI loop
    height, width : int
        height of the terminal in characters, width of terminal in characters
    root : py_cui.PyCUI
        Main PyCUI object reference
    """

    def __init__(self, num_rows: int, num_cols: int, logger: 'py_cui.debug.PyCUILogger', root:'py_cui.PyCUI', simulated_terminal: Optional[List[int]] =None):
        """Constructor for WidgetSet
        """

        self._widgets: Dict[int,Optional['py_cui.widgets.Widget']]      = {}
        self._keybindings: Dict[int,Callable[[],Any]]  = {}

        self._root = root
        self._simulated_terminal = simulated_terminal

        if self._simulated_terminal is None:
            term_size = shutil.get_terminal_size()
            height = term_size.lines
            width = term_size.columns
        else:
            height  = self._simulated_terminal[0]
            width   = self._simulated_terminal[1]

        self._height = height
        self._width = width
        status_bars_height = self._root.title_bar.get_height() + self._root.status_bar.get_height()
        self._height = self._height - status_bars_height - 2

        self._grid = grid.Grid(num_rows, num_cols, self._height, self._width, logger)

        self._selected_widget: Optional[int] = None
        self._logger = logger


    def set_selected_widget(self, widget_id: int) -> None:
        """Function that sets the selected cell for the CUI

        Parameters
        ----------
        cell_title : str
            the title of the cell
        """

        if widget_id in self._widgets.keys():
            self._selected_widget = widget_id


    def get_widgets(self) -> Dict[int, Optional['py_cui.widgets.Widget']]:
        """Function that gets current set of widgets

        Returns
        -------
        widgets : dict of str -> widget
            dictionary mapping widget IDs to object instances
        """

        return self._widgets


    def add_key_command(self, key: int, command: Callable[[],Any]):
        """Function that adds a keybinding to the CUI when in overview mode

        Parameters
        ----------
        key : py_cui.keys.KEY_*
            The key bound to the command
        command : Function
            A no-arg or lambda function to fire on keypress
        """

        self._keybindings[key] = command


    def add_scroll_menu(self, title: str, row: int, column: int, row_span: int = 1, column_span: int = 1, padx: int = 1, pady: int = 0) -> 'py_cui.widgets.ScrollMenu':
        """Function that adds a new scroll menu to the CUI grid

        Parameters
        ----------
        title : str
            The title of the scroll menu
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction

        Returns
        -------
        new_scroll_menu : ScrollMenu
            A reference to the created scroll menu object.
        """

        id = len(self.get_widgets().keys())
        new_scroll_menu     = widgets.ScrollMenu(id,
                                                 title,
                                                 self._grid,
                                                 row,
                                                 column,
                                                 row_span,
                                                 column_span,
                                                 padx,
                                                 pady,
                                                 self._logger)
        self._widgets[id]  = new_scroll_menu
        if self._selected_widget is None:
            self.set_selected_widget(id)
        self._logger.debug(f'Adding widget {title} w/ ID {id} of type {str(type(new_scroll_menu))}')
        return new_scroll_menu


    def add_checkbox_menu(self, title: str, row: int, column: int, row_span: int=1, column_span: int=1, padx: int=1, pady: int=0, checked_char: str='X') -> 'py_cui.widgets.CheckBoxMenu':
        """Function that adds a new checkbox menu to the CUI grid

        Parameters
        ----------
        title : str
            The title of the checkbox
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction
        checked_char='X' : char
            The character used to mark 'Checked' items

        Returns
        -------
        new_checkbox_menu : CheckBoxMenu
            A reference to the created checkbox object.
        """

        id = len(self.get_widgets().keys())
        new_checkbox_menu   = widgets.CheckBoxMenu(id,
                                                   title,
                                                   self._grid,
                                                   row,
                                                   column,
                                                   row_span,
                                                   column_span,
                                                   padx,
                                                   pady,
                                                   self._logger,
                                                   checked_char)
        self._widgets[id]  = new_checkbox_menu
        if self._selected_widget is None:
            self.set_selected_widget(id)
        self._logger.debug(f'Adding widget {title} w/ ID {id} of type {str(type(new_checkbox_menu))}')
        return new_checkbox_menu


    def add_text_box(self, title: str, row: int, column: int, row_span: int = 1, column_span: int = 1, padx: int = 1, pady: int = 0, initial_text: str = '', password: bool = False) -> 'py_cui.widgets.TextBox':
        """Function that adds a new text box to the CUI grid

        Parameters
        ----------
        title : str
            The title of the textbox
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction
        initial_text='' : str
            Initial text for the textbox
        password=False : bool
            Toggle to show '*' instead of characters.

        Returns
        -------
        new_text_box : TextBox
            A reference to the created textbox object.
        """

        id = len(self.get_widgets().keys())
        new_text_box        = widgets.TextBox(id,
                                              title,
                                              self._grid,
                                              row, column,
                                              row_span,
                                              column_span,
                                              padx, pady,
                                              self._logger,
                                              initial_text,
                                              password)
        self._widgets[id]    = new_text_box
        if self._selected_widget is None:
            self.set_selected_widget(id)
        self._logger.debug(f'Adding widget {title} w/ ID {id} of type {str(type(new_text_box))}')
        return new_text_box


    def add_text_block(self, title: str, row: int, column: int, row_span: int = 1, column_span: int = 1, padx: int = 1, pady: int = 0, initial_text: str = '') -> 'py_cui.widgets.ScrollTextBlock':
        """Function that adds a new text block to the CUI grid

        Parameters
        ----------
        title : str
            The title of the text block
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction
        initial_text='' : str
            Initial text for the text block

        Returns
        -------
        new_text_block : ScrollTextBlock
            A reference to the created textblock object.
        """

        id = len(self.get_widgets().keys())
        new_text_block      = widgets.ScrollTextBlock(id,
                                                      title,
                                                      self._grid,
                                                      row,
                                                      column,
                                                      row_span,
                                                      column_span,
                                                      padx,
                                                      pady,
                                                      self._logger,
                                                      initial_text)
        self._widgets[id]  = new_text_block
        if self._selected_widget is None:
            self.set_selected_widget(id)
        self._logger.debug(f'Adding widget {title} w/ ID {id} of type {str(type(new_text_block))}')
        return new_text_block


    def add_label(self, title: str, row: int, column: int, row_span: int = 1, column_span: int = 1, padx: int = 1, pady: int = 0) -> 'py_cui.widgets.Label':
        """Function that adds a new label to the CUI grid

        Parameters
        ----------
        title : str
            The title of the label
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction

        Returns
        -------
        new_label : Label
            A reference to the created label object.
        """

        id = len(self.get_widgets().keys())
        new_label           = widgets.Label(id,
                                            title,
                                            self._grid,
                                            row,
                                            column,
                                            row_span,
                                            column_span,
                                            padx,
                                            pady,
                                            self._logger)
        self._widgets[id]  = new_label
        self._logger.debug(f'Adding widget {title} w/ ID {id} of type {str(type(new_label))}')
        return new_label


    def add_block_label(self, title: str, row: int, column: int, row_span: int = 1, column_span: int = 1, padx: int = 1, pady: int = 0, center: bool=True) -> 'py_cui.widgets.BlockLabel':
        """Function that adds a new block label to the CUI grid

        Parameters
        ----------
        title : str
            The title of the block label
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction
        center : bool
            flag to tell label to be centered or left-aligned.

        Returns
        -------
        new_label : BlockLabel
            A reference to the created block label object.
        """

        id = len(self.get_widgets().keys())
        new_label           = widgets.BlockLabel(id,
                                                 title,
                                                 self._grid,
                                                 row,
                                                 column,
                                                 row_span,
                                                 column_span,
                                                 padx,
                                                 pady,
                                                 center,
                                                 self._logger)
        self._widgets[id]  = new_label
        self._logger.debug(f'Adding widget {title} w/ ID {id} of type {str(type(new_label))}')
        return new_label


    def add_button(self, title: str, row: int, column: int, row_span: int = 1, column_span: int = 1, padx: int = 1, pady: int = 0, command: Optional[Callable[[],Any]]=None) -> 'py_cui.widgets.Button':
        """Function that adds a new button to the CUI grid

        Parameters
        ----------
        title : str
            The title of the button
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction
        command=None : Function
            A no-argument or lambda function to fire on button press.

        Returns
        -------
        new_button : Button
            A reference to the created button object.
        """

        id = len(self.get_widgets().keys())
        new_button          = widgets.Button(id,
                                             title,
                                             self._grid,
                                             row,
                                             column,
                                             row_span,
                                             column_span,
                                             padx,
                                             pady,
                                             self._logger,
                                             command)
        self._widgets[id]  = new_button
        if self._selected_widget is None:
            self.set_selected_widget(id)
        self._logger.debug(f'Adding widget {title} w/ ID {id} of type {str(type(new_button))}')
        return new_button


    def add_slider(self, title: str, row: int, column: int, row_span: int=1,
                   column_span: int=1, padx: int=1, pady: int=0,
                   min_val: int=0, max_val: int=100, step: int=1, init_val: int=0) -> 'py_cui.controls.slider.SliderWidget':     
                   
                   
        """Function that adds a new label to the CUI grid

        Parameters
        ----------
        title : str
            The title of the label
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction
        min_val = 0 int
            min value of the slider
        max_val = 0 int
            max value of the slider
        step = 0 int
            step to incremento or decrement
        init_val = 0 int
            initial value of the slider


        Returns
        -------
        new_slider : Slider
            A reference to the created slider object.
        """

        id = len(self._widgets.keys())
        new_slider = controls.slider.SliderWidget(id,
                                                  title,
                                                  self._grid,
                                                  row,
                                                  column,
                                                  row_span,
                                                  column_span,
                                                  padx,
                                                  pady,
                                                  self._logger,
                                                  min_val,
                                                  max_val,
                                                  step,
                                                  init_val)
        self._widgets[id] = new_slider
        self._logger.debug(f'Adding widget {title} w/ ID {id} of type {str(type(new_slider))}')
        return new_slider
