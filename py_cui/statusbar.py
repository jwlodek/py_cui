"""
File containing class for the status bar

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""


class StatusBar:

    def __init__(self, text, color):
        self.text = text
        self.color = color


    def set_text(self, text):
        self.text = text