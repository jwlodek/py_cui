"""Module containing all error types for py_cui
"""

# Author:    Jakub Wlodek
# Created:   12-Aug-2019

# TODO - expand this


class PyCUIOutOfBoundsError(Exception):
    """Error for when widget or text goes off of the py_cui grid
    """

    pass


class PyCUIError(Exception):
    """General error
    """

    pass


class PyCUIMissingParentError(Exception):
    """Error for when parent widget is None or invalid
    """

    pass


class PyCUIMissingChildError(Exception):
    """Error for when child widget is None or invalid
    """

    pass


class PyCUIInvalidValue(Exception):
    """Error when a values passed is not valid or doeas not match requirements
    """

    pass
