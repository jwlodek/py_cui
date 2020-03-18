"""Module containing py_cui logging utilities
"""

import os
import logging
import inspect
import py_cui


def _enable_logging(logger, logging_level=logging.DEBUG):
    """Function that creates basic logging configuration

    Parameters
    ----------
    logger : PyCUILogger
        Main logger object
    logging_level : logging.LEVEL, optional
        Level of messages to display, by default logging.DEBUG

    Raises
    ------
    PermissionError
        py_cui logs require permission to cwd to operate.
    """

    if not os.access('.', os.W_OK):
        raise PermissionError('You do not have permission to create py_cui.log file.')

    if not isinstance(logger, PyCUILogger):
        raise TypeError('Only the PyCUILogger can be used for logging in the py_cui module.')

    log_file    = logging.FileHandler('py_cui.log')
    formatter   = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')
    log_file.setFormatter(formatter)
    logger.addHandler(log_file)
    logger.setLevel(logging_level)


def _initialize_logger(py_cui_root, name=None, custom_logger=True):
    """Function that retrieves an instance of either the default or custom py_cui logger.
    
    Parameters
    ----------
    name : str, optional
        The name of the logger, by default None
    custom_logger : bool, optional
        Use a custom py_cui logger, by default True
    
    Returns
    -------
    logger : logging.Logger
        A logging.Logger
    """

    if not custom_logger:
        return logging.getLogger(name)
    else:
        logging._acquireLock()
        try:
            logger = PyCUILogger(name)
            logger._assign_root_window(py_cui_root)
            return logger
        finally:
            logging._releaseLock()


class PyCUILogger(logging.Logger):
    """Custom logger class for py_cui, extends the base logging.Logger Class
    
    Attributes
    ----------
    py_cui_root : py_cui.PyCUI
        The root py_cui program for which the logger runs
    live_debug : bool
        Flag to toggle live debugging messages
    """

    def __init__(self, name):
        """Initializer for the PyCUILogger helper class

        Raises
        ------
        TypeError
            If root variable instance is not a PyCUI object raise a typeerror
        """

        super(PyCUILogger, self).__init__(name)
        self._live_debug_level      = logging.ERROR
        self._live_debug_enabled    = False


    def _assign_root_window(self, py_cui_root):
        """Attaches logger to the root window for live debugging
        """

        if not isinstance(py_cui_root, py_cui.PyCUI):
            raise TypeError('py_cui_root type must be py_cui.PyCUI')

        self.py_cui_root = py_cui_root


    def __get_debug_text(self, text):
        """Function that generates full debug text for the log
        """

        func = inspect.currentframe().f_back.f_back.f_code
        return "{}: {} in {}:{}".format(text, func.co_name, func.co_filename, func.co_firstlineno)


    def debug(self, text):
        """Function that allows for live debugging of py_cui programs by displaying log messages in the satus bar
        
        Parameters
        ----------
        text : str
            The log text ot display
        """

        debug_text = self.__get_debug_text(text)
        if self._live_debug_level > logging.DEBUG and self._live_debug_enabled:
            self.py_cui_root.status_bar.set_text(debug_text)
            super().debug(debug_text)
        else:
            super().debug(debug_text)


    def warn(self, text):
        """Function that allows for live debugging of py_cui programs by displaying log messages in the satus bar
        
        Parameters
        ----------
        text : str
            The log text ot display
        """

        debug_text = self.__get_debug_text(text)
        if self._live_debug_level > logging.WARN and self._live_debug_enabled:
            self.py_cui_root.status_bar.set_text(debug_text)
            super().warn(debug_text)
        else:
            super().warn(debug_text)


    def error(self, text):
        """Function that displays error messages live in status bar for py_cui logging
        
        Parameters
        ----------
        text : str
            The log text ot display
        """

        debug_text = self.__get_debug_text(text)
        if self._live_debug_level > logging.ERROR and self._live_debug_enabled:
            self.py_cui_root.status_bar.set_text(debug_text)
            super().error(debug_text)
        else:
            super().error(debug_text)


    def toggle_live_debug(self, level=logging.ERROR):
        """Toggles live debugging mode
        """

        self._live_debug_enabled    = not self._live_debug_enabled
        self._live_debug_level      = level