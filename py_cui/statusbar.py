"""File containing class for the status bar

TODO: File can probably be abstracted away - probably doesn't need a class
"""

# Author:    Jakub Wlodek
# Created:   12-Aug-2019


class StatusBar:
    """Very simple class representing a status bar

    Attributes
    ----------
    text : str
        status bar text
    color : py_cui.COLOR
        color to display the statusbar
    """

    def __init__(self, text, color):
        """Initializer for statusbar
        """

        self.__text = text
        self.__color = color


    def get_color(self):
        """Getter for status bar color
        
        Returns
        -------
        color : int
            statusbar color
        """

        return self.__color


    def get_text(self):
        """Getter for stattus bar text

        Returns
        -------
        text : str
            The statusbar text
        """

        return self.__text


    def set_color(self, color):
        """Setter for statusbar color

        Parameters
        ----------
        color : int
            new statusbar color code
        """

        self.__color = color


    def set_text(self, text):
        """Sets the statusbar text

        Parameters
        ----------
        text : str
            New statusbar text
        """

        self.__text = text