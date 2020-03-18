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
    __num_rows, __num_columns : int
        Number of grid rows and columns
    __height, __width : int
        The height, width in characters of the terminal window
    __offset_y, __offset_x : int
        The number of additional characters found by height mod rows and width mod columns
    __row_height, __column_width : int
        The number of characters in a single grid row, column
    __logger : py_cui.debug.PyCUILogger
        logger object for maintaining debug messages
    """


    def __init__(self, num_rows, num_columns, height, width, logger):
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

        self.__num_rows      = num_rows
        self.__num_columns   = num_columns
        self.__height        = height
        self.__width         = width
        self.__offset_y      = self.__height  % self.__num_rows    - 1
        self.__offset_x      = self.__width   % self.__num_columns - 1
        self.__row_height    = int(self.__height   / self.__num_rows)
        self.__column_width  = int(self.__width    / self.__num_columns)
        self.__logger        = logger


    def get_dimensions(self):
        """Gets dimensions in rows/columns

        Returns
        -------
        num_rows : int
            size of grid in rows
        num_cols : int
            size of grid in columns
        """

        return self.__num_rows, self.__num_columns


    def get_dimensions_absolute(self):
        """Gets dimensions of grid in terminal characters

        Returns
        -------
        height : int
            height in characters
        width : int
            width in characters
        """

        return self.__height, self.__width


    def get_offsets(self):
        """Gets leftover characters for x and y

        Returns
        -------
        offset_x : int
            leftover chars in x direction
        offset_y : int
            leftover chars in y direction
        """

        return self.__offset_x, self.__offset_y


    def get_cell_dimensions(self):
        """Gets size in characters of single (row, column) cell location

        Returns
        -------
        row_height : int
            height of row in characters
        column_width : int
            width of column in characters
        """

        return self.__row_height, self.__column_width


    def set_num_rows(self, num_rows):
        """Sets the grid row size
        
        Parameters
        ----------
        num_rows : int
            New number of grid rows

        Raises
        ------
        error : PyCUIOutOfBoundsError
            If the size of the terminal window is too small
        """

        self.__logger.debug('Updating row count and height')
        if (3 * num_rows) >= self.__height:
            raise py_cui.errors.PyCUIOutOfBoundsError
        self.__num_rows = num_rows
        self.__row_height = int(self.__height / self.__num_rows)


    def set_num_cols(self, num_columns):
        """Sets the grid column size
        
        Parameters
        ----------
        num_columns : int
            New number of grid columns
        
        Raises
        ------
        error : PyCUIOutOfBoundsError
            If the size of the terminal window is too small
        """

        self.__logger.debug('Updating column count and width')
        if (3 * num_columns) >= self.__width:
            raise py_cui.errors.PyCUIOutOfBoundsError
        
        self.__num_columns   = num_columns
        self.__column_width  = int(self.__width / self.__num_columns)


    def update_grid_height_width(self, height, width):
        """Update grid height and width. Allows for on-the-fly size editing
        
        Parameters
        ----------
        height : int
            The height in characters of the terminal window
        width : int
            The width in characters of the terminal window

        Raises
        ------
        error : PyCUIOutOfBoundsError
            If the size of the terminal window is too small
        """

        self.__logger.debug('Updating grid height and width')
        self.__height = height
        self.__width  = width

        self.__logger.debug('Checking height width based on terminal dimensions')
        if (3 * self.__num_columns) >= self.__width:
            raise py_cui.errors.PyCUIOutOfBoundsError

        if (3 * self.__num_rows) >= self.__height:
            raise py_cui.errors.PyCUIOutOfBoundsError

        self.__row_height     = int(self.__height   / self.__num_rows)
        self.__column_width   = int(self.__width    / self.__num_columns)
        self.__offset_y       = self.__height   % self.__num_rows
        self.__offset_x       = self.__width    % self.__num_columns
        self.__logger.debug('Finished updating grid height/width')