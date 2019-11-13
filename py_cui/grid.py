"""File containing the Grid Class. 

The grid is currently the only supported layout manager for py_cui

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""


import py_cui.errors

class Grid:
    """Class representing the CUI grid

    Attributes
    ----------
    num_rows : int
        Number of grid rows
    num_columns : int
        Number of grid columns
    height : int
        The height in characters of the terminal window
    width : int
        The width in characters of the terminal window
    offset_y : int
        The number of additional characters found by height mod rows
    offset_x : int
        The number of additional characters found by width mod columns
    row_height : int
        The number of characters in a single grid row
    column_width : int
        The number of characters in a single grid column
    
    Methods
    -------
    set_num_rows(num_rows : int)
        Sets the grid row size
    set_num_cols(num_columns : int)
        Sets the grid column size
    update_grid_height_width(height : int, width : int)
        Update grid height and width. Allows for on-the-fly size editing
    """


    def __init__(self, num_rows, num_columns, height, width):
        """Constructor for the Grid class

        Parameters
        ----------
        num_rows : int
            Number of grid rows
        num_columns : int
            Number of grid columns
        height : int
            The height in characters of the terminal window
        width : int
            The width in characters of the terminal window
        """

        self.num_rows = num_rows
        self.num_columns = num_columns
        self.height = height
        self.width = width
        self.offset_y = self.height % self.num_rows - 1
        self.offset_x = self.width % self.num_columns - 1
        self.row_height = int(self.height / self.num_rows)
        self.column_width = int(self.width / self.num_columns)


    def set_num_rows(self, num_rows):
        """Sets the grid row size
        
        Parameters
        ----------
        num_rows : int
            New number of grid rows
        """

        if (3 * num_rows) >= self.height:
            raise py_cui.errors.PyCUIOutOfBoundsError
        self.num_rows = num_rows
        self.row_height = int(self.height / self.num_rows)


    def set_num_cols(self, num_columns):
        """Sets the grid column size
        
        Parameters
        ----------
        num_columns : int
            New number of grid columns
        """

        if (3 * num_columns) >= self.width:
            raise py_cui.errors.PyCUIOutOfBoundsError
        self.num_columns = num_columns
        self.column_width = int(self.width / self.num_columns)


    def update_grid_height_width(self, height, width):
        """Update grid height and width. Allows for on-the-fly size editing
        
        Parameters
        ----------
        height : int
            The height in characters of the terminal window
        width : int
            The width in characters of the terminal window
        """

        self.height = height
        self.width = width
        if (3 * self.num_columns) >= self.width:
            raise py_cui.errors.PyCUIOutOfBoundsError

        if (3 * self.num_rows) >= self.height:
            raise py_cui.errors.PyCUIOutOfBoundsError
        self.row_height = int(self.height / self.num_rows)
        self.column_width = int(self.width / self.num_columns)
        self.offset_y = self.height % self.num_rows
        self.offset_x = self.width % self.num_columns