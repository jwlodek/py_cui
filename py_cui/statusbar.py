"""File containing class for the status bar

TODO: File can probably be abstracted away - probably doesn't need a class
"""

# Author:    Jakub Wlodek
# Created:   12-Aug-2019
import py_cui

class StatusBar:
    """Very simple class representing a status bar

    Attributes
    ----------
    text : str
        status bar text
    color : py_cui.COLOR
        color to display the statusbar
    root : py_cui.PyCUI
        Main PyCUI object reference
    is_title_bar : bool
        Is the StatusBar displayed on the top of the grid
    """

    def __init__(self, text: str, color: int, root: 'py_cui.PyCUI', is_title_bar: bool=False):
        """Initializer for statusbar
        """

        self.__text = text
        self.__color = color
        self.__height = 1
        self.__root = root
        self.__is_title_bar = is_title_bar


    def get_color(self) -> int:
        """Getter for status bar color

        Returns
        -------
        color : int
            statusbar color
        """

        return self.__color


    def get_text(self) -> str:
        """Getter for status bar text

        Returns
        -------
        text : str
            The statusbar text
        """

        return self.__text


    def set_color(self, color) -> None:
        """Setter for statusbar color

        Parameters
        ----------
        color : int
            new statusbar color code
        """

        self.__color = color


    def set_text(self, text: str) -> None :
        """Sets the statusbar text

        Parameters
        ----------
        text : str
            New statusbar text
        """

        self.__text = text

    def get_height(self) -> int :
        """Getter for status bar height in row

        Returns
        -------
        height : int
            The statusbar height in row
        """

        return self.__height

    def show(self) -> None:
        """Sets the status bar height to 1"""

        self.__height = 1
        self._refresh_root_size()

    def hide(self) -> None:
        """Sets the status bar height to 0"""

        self.__height = 0
        self._refresh_root_size()

    def _refresh_root_size(self) -> None:
        """Resets the grid's title bar offset if needed and calls a UI size update."""

        if self.__is_title_bar:
            self.__root._grid._title_bar_offset = self.__height
        self.__root._refresh_height_width()
