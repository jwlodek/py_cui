"""
File containing the Grid Class. The grid is currently the only
supported layout manager for py_cui

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""


import py_cui.errors

class Grid:

    def __init__(self, num_rows, num_columns, height, width):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.height = height
        self.width = width
        self.offset_y = self.height % self.num_rows
        self.offset_x = self.width % self.num_columns
        self.row_height = int(self.height / self.num_rows)
        self.column_width = int(self.width / self.num_columns)

    def set_num_rows(self, num_rows):
        """ Sets the grid row size """

        if (3 * num_rows) >= self.height:
            raise py_cui.errors.PyCUIOutOfBoundsError
        self.num_rows = num_rows
        self.row_height = int(self.height / self.num_rows)


    def set_num_cols(self, num_columns):
        """ Sets the grid column size """

        if (3 * num_columns) >= self.width:
            raise py_cui.errors.PyCUIOutOfBoundsError
        self.num_columns = num_columns
        self.column_width = int(self.width / self.num_columns)


    def update_grid_height_width(self, height, width):
        """ Update grid height and width. Allows for on-the-fly size editing """

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