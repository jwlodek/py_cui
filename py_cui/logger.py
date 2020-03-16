"""Module containing py_cui logging utilities
"""

import os
import logging
import py_cui


def initialize_logging(logging_level=logging.DEBUG, name=None, custom_logger=True):
    """Function that retrieves an instance of either the default or custom py_cui logger.
    
    Parameters
    ----------
    logging_level : logging.LEVEL, optional
        Level of messages to display, by default logging.DEBUG
    name : str, optional
        The name of the logger, by default None
    custom_logger : bool, optional
        Use a custom py_cui logger, by default True
    
    Returns
    -------
    logger : logging.Logger
        A logging.Logger
    
    Raises
    ------
    PermissionError
        py_cui logs require permission to cwd to operate.
    """

    if not os.access('.', os.W_OK):
        raise PermissionError('You do not have permission to create py_cui.log file.')

    logging.basicConfig(filename='py_cui.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging_level,
                        )

    if not custom_logger:
        return logging.getLogger(name)
    else:
        default_logging_class = logging.getLoggerClass()
        logging._acquireLock()
        try:
            logging.setLoggerClass(PyCUILogger)
            logger = logging.getLogger()
            logging.setLoggerClass(default_logging_class)
            return logger
        finally:
            logging._releaseLock()


def get_logger_name(name):
    """Helper function that gives a generic py_cui logger name for module
    
    Parameters
    ----------
    name : str
        Usually __name__ for the module
    
    Returns
    -------
    logger_name : str
        A name for the logger
    """

    return 'py_cui.{}'.format(name)


class PyCUILogger(logging.Logger):
    """Custom logger class for py_cui, extends the base logging.Logger Class
    
    Attributes
    ----------
    py_cui_root : py_cui.PyCUI
        The root py_cui program for which the logger runs
    live_debug : bool
        Flag to toggle live debugging messages
    """


    def __init__(self, name, py_cui_root):
        """Initializer for the PyCUILogger helper class

        Raises
        ------
        TypeError
            If root variable instance is not a PyCUI object raise a typeerror
        """

        super(PyCUILogger, self).__init__(name)
        
        if not isinstance(py_cui_root, py_cui.PyCUI):
            raise TypeError('py_cui_root type must be py_cui.PyCUI')

        self.py_cui_root = py_cui_root
        self.live_debug = False


    def debug(self, text):
        """Function that allows for live debugging of py_cui programs by displaying log messages in the satus bar
        
        Parameters
        ----------
        text : str
            The log text ot display
        """

        if logging._Level >= logging.DEBUG and self.live_debug:
            self.py_cui_root.status_bar.set_text(text)
            super().debug(text)
        else:
            super().debug(text)


    def toggle_live_debug(self):
        """Toggles live debugging mode
        """

        self.live_debug = not self.live_debug