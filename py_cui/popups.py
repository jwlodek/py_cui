"""File containing classes for all popups used by py_cui

@author:    Jakub Wlodek  
@created:   12-Aug-2019
"""

# required library imports
import curses
import py_cui
import py_cui.ui
import py_cui.errors


class Popup(py_cui.ui.UIElement):
    """Base CUI popup class.

    Contains constructor and initial definitions for key_press and draw
    Unlike widgets, they do not have a set grid cell, they are simply centered in the view
    frame

    Attributes
    ----------
    _root : py_cui.PyCUI
        Root CUI window
    _text : str
        Popup message text
    _selected : bool
        Always true. Used by the renderer to highlight popup
    _close_keys : List[int]
        List of keycodes used to close popup
    """


    def __init__(self, root, title, text, color, renderer, logger):
        """Initializer for main popup class. Calls UIElement intialier, and sets some initial values
        """

        super().__init__(0, title, renderer, logger)
        self._root         = root
        self._text         = text
        self._selected     = True
        self._close_keys   = [py_cui.keys.KEY_ESCAPE]
        self._color        = color
        self.update_height_width()

    
    def _increment_counter(self):
        """Function that increments an internal counter
        """

        pass


    def set_text(self, text):
        """Sets popup text (message)

        Parameters
        ----------
        text : str
            The new popup text
        """

        self._text = text


    def get_absolute_start_pos(self):
        """Override of base class, computes position based on root dimensions
        
        Returns
        -------
        start_x, start_y : int
            The coords of the upper-left corner of the popup
        """

        root_height, root_width = self._root.get_absolute_size()
        return int(root_width / 4), int(root_height / 3)


    def get_absolute_stop_pos(self):
        """Override of base class, computes position based on root dimensions
        
        Returns
        -------
        stop_x, stop_y : int
            The coords of the lower-right corner of the popup
        """

        root_height, root_width = self._root.get_absolute_size()
        return (int(3 * root_width / 4)), (int(2 * root_height / 3))


    def _handle_key_press(self, key_pressed):
        """Handles key presses when popup is open

        By default, only closes popup when Escape is pressed

        Parameters
        ----------
        key_pressed : int
            The ascii code for the key that was pressed
        """

        if key_pressed in self._close_keys:
            self._root.close_popup()


    def _draw(self):
        """Function that uses renderer to draw the popup

        Can be implemented by subclass. Base draw function will draw the title and text in a bordered box
        """

        super()._draw()
        target_y = int(self._stop_y - self._start_y / 2)
        self._renderer.set_color_rules([])
        self._renderer._set_bold()
        self._renderer.set_color_mode(self._color)
        self._renderer.draw_border(self, with_title=False)
        self._renderer.draw_text(  self, self._title, target_y - 2, centered=True, selected=True)
        self._renderer.draw_text(  self, self._text,  target_y,     centered=True, selected=True)
        self._renderer.unset_color_mode(self._color)
        self._renderer._unset_bold()
        self._renderer.reset_cursor(self)



class MessagePopup(Popup):
    """Class representing a simple message popup
    """

    def __init__(self, root, title, text, color, renderer, logger):
        """Initializer for MessagePopup
        """

        super().__init__(root, title, text, color, renderer, logger)
        self._close_keys = [ py_cui.keys.KEY_ENTER, 
                            py_cui.keys.KEY_ESCAPE, 
                            py_cui.keys.KEY_SPACE, 
                            py_cui.keys.KEY_BACKSPACE, 
                            py_cui.keys.KEY_DELETE]


    def _draw(self):
        """Draw function for MessagePopup. Calls superclass draw()
        """

        super()._draw()


class YesNoPopup(Popup):
    """Class for Yes/No popup. Extends Popup

    Attributes
    ----------
    _command : function, 1 boolean parameter
        Function that takes one boolean parameter. Called with True if yes, called with False if no.
    """

    def __init__(self, root, title, text, color, command, renderer, logger):
        """Initializer for YesNoPopup
        """

        super().__init__(root, title, text, color, renderer, logger)
        self._command = command


    def _handle_key_press(self, key_pressed):
        """Handle key press overwrite from superclass

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """

        super()._handle_key_press(key_pressed)
        valid_pressed = False
        if key_pressed == py_cui.keys.KEY_Y_LOWER or key_pressed == py_cui.keys.KEY_Y_UPPER:
            ret_val = True
            valid_pressed = True
        elif key_pressed == py_cui.keys.KEY_N_UPPER or key_pressed == py_cui.keys.KEY_N_LOWER:
            ret_val = False
            valid_pressed = True

        if valid_pressed:
            self._root.close_popup()
            if self._command is not None:
                self._command(ret_val)
            else:
                self._root.show_warning_popup('No Command Specified', 'The Yes/No popup had no specified command')


    def _draw(self):
        """Uses base class draw function
        """

        super()._draw()


class TextBoxPopup(Popup, py_cui.ui.TextBoxImplementation):
    """Class representing a textbox popup

    Attributes
    ----------
    _command : function
        The command to run when enter is pressed
    """

    def __init__(self, root, title, color, command, renderer, password, logger):
        """Initializer for textbox popup. Uses TextBoxImplementation as base
        """

        Popup.__init__(self, root, title, '', color, renderer, logger)
        py_cui.ui.TextBoxImplementation.__init__(self, '', password, logger)
        self._command           = command
        self.update_height_width()


    def update_height_width(self):
        """Need to update all cursor positions on resize
        """

        super().update_height_width()
        padx, pady              = self.get_padding()
        start_x, start_y        = self.get_start_position()
        height, width           = self.get_absolute_dimensions()
        self._cursor_text_pos   = 0
        self._cursor_x          = start_x + 2 + padx
        self._cursor_max_left   = self._cursor_x
        self._cursor_max_right  = start_x + width - 1 - pady
        self._cursor_y          = start_y + int(height / 2) + 1
        self._viewport_width    = self._cursor_max_right - self._cursor_max_left


    def _handle_key_press(self, key_pressed):
        """Override of base handle key press function

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """

        super()._handle_key_press(key_pressed)
        valid_pressed = False
        if key_pressed == py_cui.keys.KEY_ENTER:
            self._ret_val = self._text
            valid_pressed = True

        if valid_pressed:
            self._root.close_popup()
            if self._command is not None:
                self._command(self._ret_val)
            else:
                self._root.show_warning_popup('No Command Specified', 'The Yes/No popup had no specified command')

        if key_pressed == py_cui.keys.KEY_LEFT_ARROW:
            self._move_left()
        elif key_pressed == py_cui.keys.KEY_RIGHT_ARROW:
            self._move_right()
        elif key_pressed == py_cui.keys.KEY_BACKSPACE:
            self._erase_char()
        elif key_pressed == py_cui.keys.KEY_DELETE:
            self._delete_char()
        elif key_pressed == py_cui.keys.KEY_HOME:
            self._jump_to_start()
        elif key_pressed == py_cui.keys.KEY_END:
            self._jump_to_end()
        elif key_pressed > 31 and key_pressed < 128:
            self._insert_char(key_pressed)


    def _draw(self):
        """Override of base draw function
        """

        self._renderer.set_color_mode(self._color)
        self._renderer.set_color_rules([])
        self._renderer.draw_text(self, self._title, self._cursor_y - 2, bordered=False, selected=True)
        self._renderer.draw_border(self, fill=False, with_title=False)
        render_text = self._text
        if len(self._text) >self._viewport_width:
            end = len(self._text) - (self._viewport_width)
            if self._cursor_text_pos < end:
                render_text = self._text[self._cursor_text_pos:self._cursor_text_pos + (self._viewport_width)]
            else:
                render_text = self._text[end:]
        if self._password:
            temp = '*' * len(render_text)
            render_text = temp
        self._renderer.draw_text(self, render_text, self._cursor_y, selected=self._selected)

        if self._selected:
            self._renderer.draw_cursor(self._cursor_y, self._cursor_x)
        else:
            self._renderer.reset_cursor(self, fill=False)
        self._renderer.unset_color_mode(self._color)


class MenuPopup(Popup, py_cui.ui.MenuImplementation):
    """A scroll menu popup.

    Allows for popup with several menu items to select from

    Attributes
    ----------
    _command : function
        a function that takes a single string parameter, run when ENTER pressed
    _run_command_if_none : bool
        Runs command even if there are no menu items (passes None)
    """

    def __init__(self, root, items, title, color, command, renderer, logger, run_command_if_none):
        """Initializer for MenuPopup. Uses MenuImplementation as base
        """

        Popup.__init__(self, root, title, '', color, renderer, logger)
        py_cui.ui.MenuImplementation.__init__(self, logger)
        self.add_item_list(items)
        self._command              = command
        self._run_command_if_none  = run_command_if_none


    def _handle_key_press(self, key_pressed):
        """Override of base handle key press function

        Enter key runs command, Escape key closes menu

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """

        super()._handle_key_press(key_pressed)
        valid_pressed = False
        if key_pressed == py_cui.keys.KEY_ENTER:
            ret_val = self.get()
            valid_pressed = True
        elif key_pressed == py_cui.keys.KEY_ESCAPE:
            ret_val = None
            valid_pressed = True

        if valid_pressed:
            self._root.close_popup()
            if self._command is not None:
                if ret_val is not None or self._run_command_if_none:
                    self._command(ret_val)
            else:
                self._root.show_warning_popup('No Command Specified', 'The menu popup had no specified command')

        if key_pressed == py_cui.keys.KEY_UP_ARROW:
            self._scroll_up()
        if key_pressed == py_cui.keys.KEY_DOWN_ARROW:
            viewport_height = self._height - (2 * self._pady) - 3
            self._scroll_down(viewport_height)


    def _draw(self):
        """Overrides base class draw function
        """

        self._renderer.set_color_mode(self._color)
        self._renderer.draw_border(self)
        self._renderer.set_color_rules([])
        counter = self._pady + 1
        line_counter = 0
        for line in self._view_items:
            if line_counter < self._top_view:
                line_counter = line_counter + 1
            else:
                if counter >= self._height - self._pady - 1:
                    break
                if line_counter == self.get_selected_item():
                    self._renderer.draw_text(self, line, self._start_y + counter, selected=True)
                else:
                    self._renderer.draw_text(self, line, self._start_y + counter)
                counter = counter + 1
                line_counter = line_counter + 1
        self._renderer.unset_color_mode(self._color)
        self._renderer.reset_cursor(self)


class LoadingIconPopup(Popup):
    """Loading icon popup class

    MUST BE USED WITH A FORM OF ASYNC/THREADING

    Attributes
    ----------
    _loading_icons : list of str
        Animation frames for loading icon
    _icon_counter : int
        Current frame of animation
    _message : str
        Loading message
    """

    def __init__(self, root, title, message, color, renderer, logger):
        """Initializer for LoadingIconPopup
        """

        super().__init__(root, title, '{} ... \\'.format(message), color, renderer, logger)
        self._loading_icons = ['\\', '|', '/', '-']
        self._icon_counter = 0
        self._message = message


    def _handle_key_press(self, key_pressed):
        """Override of base class function.

        Loading icon popups cannot be cancelled, so we wish to avoid default behavior

        Parameters
        ----------
        key_pressed : int
            key code of pressed key
        """

        pass


    def _draw(self):
        """Overrides base draw function
        """

        self._text = '{} ... {}'.format(self._message, self._loading_icons[self._icon_counter])
        self._icon_counter = self._icon_counter + 1
        if self._icon_counter == len(self._loading_icons):
            self._icon_counter = 0
        
        # Use Superclass draw after new text is computed
        super()._draw()


class LoadingBarPopup(Popup):
    """Class for Loading Bar Popup

    MUST BE USED WITH A FORM OF ASYNC/THREADING

    Attributes
    ----------
    num_items : int
        NUmber of items to count through
    completed_items : int
        counter for completed items
    """

    def __init__(self, root, title, num_items, color, renderer, logger):
        """Initializer for LoadingBarPopup
        """

        super().__init__(root, title, '{} (0/{})'.format('-' * num_items, num_items), color, renderer, logger)
        self._num_items          = num_items
        self._loading_icons      = ['\\', '|', '/', '-']
        self._icon_counter       = 0
        self._completed_items    = 0


    def _handle_key_press(self, key_pressed):
        """Override of base class function.

        Loading icon popups cannot be cancelled, so we wish to avoid default behavior

        Parameters
        ----------
        key_pressed : int
            key code of pressed key
        """

        pass

    def _increment_counter(self):
        """Function that increments an internal counter
        """

        self._completed_items += 1


    def _draw(self):
        """Override of base draw function
        """

        width = self._stop_x - self._start_x
        bar_width = 2 * int(width / 3)
        items_per_bar_block = self._num_items / bar_width
        bar_blocks_per_item = bar_width / self._num_items

        if self._completed_items == self._num_items:
            self._root.stop_loading_popup()

        if items_per_bar_block >= 1:
            completed_blocks = int(self._completed_items / items_per_bar_block)
        else:
            completed_blocks = int(bar_blocks_per_item * self._completed_items)

        non_completed_blocks = bar_width - completed_blocks
        self._icon_counter = self._icon_counter + 1
        if self._icon_counter == len(self._loading_icons):
            self._icon_counter = 0

        self.set_text('{}{} ({}/{}) {}'.format( '#' * completed_blocks, 
                                                '-' * non_completed_blocks, 
                                                self._completed_items, 
                                                self._num_items, 
                                                self._loading_icons[self._icon_counter]))
        
        # Use Superclass draw after new text is computed
        super()._draw()
