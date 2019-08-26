"""
File containing class for the status bar

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""


class StatusBar:
    """
    Very simple class representing a status bar

    Attributes
    ----------
    text : str
        status bar text
    color : py_cui.COLOR
        color to display the statusbar
    """

    def __init__(self, text, color):
        """ Constructor for statusbar """

        self.text = text
        self.color = color


    def set_text(self, text):
        """ Sets the statusbar text """

        self.text = text