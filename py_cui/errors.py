"""
File containing all error types for py_cui

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""

class PyCUIOutOfBoundsError(Exception):
    pass


class PyCUIError(Exception):
    pass

class PyCUIMissingParentError(Exception):
    pass

class PyCUIMissingChildError(Exception):
    pass