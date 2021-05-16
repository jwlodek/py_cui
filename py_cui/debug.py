"""Module containing py_cui logging utilities
"""

# Author:    Jakub Wlodek
# Created:   18-Mar-2020

import os
import logging
import inspect
import py_cui
import datetime


def _enable_logging(logger, replace_log_file=True, filename='py_cui_log.txt', logging_level=logging.DEBUG):
    """Function that creates basic logging configuration for selected logger

    Parameters
    ----------
    logger : PyCUILogger
        Main logger object
    filename : os.Pathlike
        File path for output logfile
    logging_level : logging.LEVEL, optional
        Level of messages to display, by default logging.DEBUG

    Raises
    ------
    PermissionError
        py_cui logs require permission to cwd to operate.
    TypeError
        Only the custom PyCUILogger can be used here.
    """

    abs_path = os.path.abspath(filename)
    if replace_log_file and os.path.exists(abs_path):
        os.remove(abs_path)

    if not os.access(os.path.dirname(abs_path), os.W_OK):
        raise PermissionError('You do not have permission to create py_cui.log file.')

    if not isinstance(logger, PyCUILogger):
        raise TypeError('Only the PyCUILogger can be used for logging in the py_cui module.')

    log_file    = logging.FileHandler(filename)
    formatter   = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s | %(message)s')
    log_file.setFormatter(formatter)
    logger.addHandler(log_file)
    logger.setLevel(logging_level)


def _initialize_logger(py_cui_root, name=None, custom_logger=True):
    """Function that retrieves an instance of either the default or custom py_cui logger.
    
    Parameters
    ----------
    py_cui_root : py_cui.PyCUI
        reference to the root py_cui window
    name : str, optional
        The name of the logger, by default None
    custom_logger : bool, optional
        Use a custom py_cui logger, by default True
    
    Returns
    -------
    logger : py_cui.debug.PyCUILogger
        A custom logger that allows for live debugging
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


class LiveDebugImplementation(py_cui.ui.MenuImplementation):

    def __init__(self, parent_logger):

        super().__init__(parent_logger)
        self._live_debug_level      = logging.ERROR
        self._live_debug_enabled    = False
        self._buffer_size           = 100
        self._num_view_msg          = 10
        #self._live_debug_alignment  = 'TOP'
        self._current_bottom_debug_msg = 0

    def add_item(self, item):
        if len(self._view_items) == self._buffer_size:
            self._view_items.pop(0)
        self._view_items.append(str(item))


class LiveDebugElement(py_cui.ui.UIElement, LiveDebugImplementation):


    def __init__(self, parent_logger):
        LiveDebugImplementation.__init__(self, parent_logger)
        py_cui.ui.UIElement.__init__(self, 'LiveDebug', 'PyCUI Live Debug', None, parent_logger)
        self._start_x = 5
        self._start_y = 5
        self._stop_x = 150
        self._stop_y = 25


    def print_to_live_debug_buffer(self, msg, msg_type):

        self.add_item(f'{datetime.datetime.now()} - {msg_type} | {msg}')


    def get_absolute_start_pos(self):
        start_x = int(self._logger.py_cui_root._width / 7) + 2
        start_y = int(self._logger.py_cui_root._height / 7) + 2
        return start_x, start_y 


    def get_absolute_stop_pos(self):
        stop_x = 6 * int(self._logger.py_cui_root._width / 7) - 2
        stop_y = 6 * int(self._logger.py_cui_root._height / 7) - 2
        return stop_x, stop_y 


    def _handle_mouse_press(self, x, y):
        """Override of base class function, handles mouse press in menu

        Parameters
        ----------
        x, y : int
            Coordinates of mouse press
        """

        super()._handle_mouse_press(x, y)
        viewport_top = self._start_y + self._pady + 1
        if viewport_top <= y and viewport_top + len(self._view_items) - self._top_view >= y:
            elem_clicked = y - viewport_top + self._top_view
            self.set_selected_item_index(elem_clicked)


    def _handle_key_press(self, key_pressed):

        if key_pressed == py_cui.keys.KEY_ESCAPE:
            self._logger.toggle_live_debug()

        viewport_height = self.get_viewport_height()
        if key_pressed == py_cui.keys.KEY_UP_ARROW:
            self._scroll_up()
        if key_pressed == py_cui.keys.KEY_DOWN_ARROW:
            self._scroll_down(viewport_height)
        if key_pressed == py_cui.keys.KEY_HOME:
            self._jump_to_top()
        if key_pressed == py_cui.keys.KEY_END:
            self._jump_to_bottom(viewport_height)
        if key_pressed == py_cui.keys.KEY_PAGE_UP:
            self._jump_up()
        if key_pressed == py_cui.keys.KEY_PAGE_DOWN:
            self._jump_down(viewport_height)
        

    def _draw(self):
        """Overrides base class draw function
        """

        self._renderer.set_color_mode(py_cui.WHITE_ON_BLACK)
        self._renderer.draw_border(self)
        counter = self._pady + 1
        line_counter = 0
        for item in reversed(self._view_items):
            line = str(item)
            if line_counter < self._top_view:
                line_counter = line_counter + 1
            else:
                if counter >= self._height - self._pady - 1:
                    break
                if line_counter == self._selected_item:
                    self._renderer.draw_text(self, line, self._start_y + counter, selected=True)
                else:
                    self._renderer.draw_text(self, line, self._start_y + counter)
                counter = counter + 1
                line_counter = line_counter + 1
        self._renderer.unset_color_mode(py_cui.WHITE_ON_BLACK)
        self._renderer.reset_cursor(self)


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
        self.py_cui_root            = None
        self._live_debug_element    = LiveDebugElement(self)


    def set_live_debug_alignment(self, alignment = 'TOP'):
        self._live_debug_alignment = alignment


    def is_live_debug_enabled(self):
        return self._live_debug_enabled

    def toggle_live_debug(self):
        self._live_debug_enabled = not self._live_debug_enabled

    def draw_live_debug(self):
        if self.is_live_debug_enabled() and self.py_cui_root is not None:
            self._live_debug_element._draw()

    def _assign_root_window(self, py_cui_root):
        """Attaches logger to the root window for live debugging
        """

        if not isinstance(py_cui_root, py_cui.PyCUI):
            raise TypeError('py_cui_root type must be py_cui.PyCUI')

        self.py_cui_root = py_cui_root
        self._live_debug_element.update_height_width()


    def _get_debug_text(self, text):
        """Function that generates full debug text for the log
        """

        func = inspect.currentframe().f_back.f_back.f_code
        return "{} -> {}:{} - {}".format(text, 
                                         func.co_name, 
                                         os.path.basename(func.co_filename), 
                                         func.co_firstlineno)
    
    
    def info(self, text):
        """Adds stacktrace info to log
        
        Parameters
        ----------
        text : str
            The log text ot display
        """

        debug_text = self._get_debug_text(text)
        if self._live_debug_level <= logging.INFO and self._live_debug_enabled:
            self._live_debug_element.print_to_live_debug_buffer(debug_text, 'INFO')
        super().info(debug_text)


    def debug(self, text):
        """Function that allows for live debugging of py_cui programs by displaying log messages in the satus bar
        
        Parameters
        ----------
        text : str
            The log text ot display
        """

        debug_text = self._get_debug_text(text)
        if self._live_debug_level <= logging.DEBUG and self._live_debug_enabled:
            self._live_debug_element.print_to_live_debug_buffer(debug_text, 'DEBUG')
        super().debug(debug_text)


    def warn(self, text):
        """Function that allows for live debugging of py_cui programs by displaying log messages in the satus bar
        
        Parameters
        ----------
        text : str
            The log text ot display
        """

        debug_text = self._get_debug_text(text)
        if self._live_debug_level <= logging.WARN and self._live_debug_enabled:
            self._live_debug_element.print_to_live_debug_buffer(debug_text, 'WARN')
        super().warn(debug_text)


    def error(self, text):
        """Function that displays error messages live in status bar for py_cui logging
        
        Parameters
        ----------
        text : str
            The log text ot display
        """

        debug_text = self._get_debug_text(text)
        if self._live_debug_level <= logging.ERROR and self._live_debug_enabled:
            self._live_debug_element.print_to_live_debug_buffer(debug_text, 'ERROR')
        super().error(debug_text)
