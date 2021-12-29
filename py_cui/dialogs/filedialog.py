"""Implementation, widget, and popup classes for file selection dialogs
"""

import py_cui.ui
import py_cui.widgets
import py_cui.popups
import py_cui.colors
import os
from typing import List, Optional, Tuple

# Imports used to detect hidden files
import sys
import stat


def is_filepath_hidden(path:  str) -> bool:
    """Function checks if file or folder is considered "hidden"

    Parameters
    ----------
    path : str
        Path to file or folder

    Returns
    -------
    marked_hidden : bool
        True if name starts with '.', or has hidden attribute in OS
    """


    name = os.path.basename(path)
    marked_hidden = name.startswith('.')
    if sys.platform != 'win32':
        return marked_hidden
    else:
        return bool(os.stat(path).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN) or marked_hidden


class FileDirElem:
    """Simple helper class defining a single file or directory

    Attributes
    ----------
    _type : str
        Either dir or file
    _name : str
        The name of the file or directory
    _path : str
        The absolute path to the directory or file
    _folder_icon : str
        icon or text for folder
    _file_icon : str
        icon for file
    """

    def __init__(self, elem_type: str, name: str, fullpath: str, ascii_icons: bool=False):
        """Intializer for FilDirElem
        """

        self._type = elem_type
        self._name = name
        self._path = fullpath

        # Use unicode icons of folder and file, or use text instead
        # for compatibility reasons.
        if not ascii_icons:
            self._folder_icon = '\U0001f4c1'
            # Folder icon is two characters, so 
            self._file_icon = '\U0001f5ce' + ' '
        else:
            self._folder_icon = '<DIR>'
            self._file_icon = '     '


    def get_path(self) -> str:
        """Getter for path

        Returns
        -------
        path : str
            Path of file/dir represented by elem
        """

        return self._path


    def __str__(self) -> str:
        """Override of to-string function

        Returns
        -------
        description : str
            Icon and name of dir or file
        """

        if self._type == 'file':
            return f'{self._file_icon} {self._name}'
        else:
            return f'{self._folder_icon} {self._name}'



class FileSelectImplementation(py_cui.ui.MenuImplementation):
    """Extension of menu implementation that allows for listing files and dirs in a location

    Attributes
    ----------
    _current_dir : str
        The current focused-on directory
    _ascii_icons : bool
        Toggle using ascii or unicode icons
    _dialog_type : str
        Type of open dialog
    _limit_extensions : List[str]
        List of file extensions to show as visible
    """


    def __init__(self, initial_loc: str, dialog_type: str, ascii_icons, logger, limit_extensions: List[str] = [], show_hidden: bool=False):
        """Initalizer for the file select menu implementation. Includes some logic for getting list of file and folders.
        """

        super().__init__(logger)
        
        self._current_dir = os.path.abspath(initial_loc)
        self._ascii_icons = ascii_icons
        self._dialog_type = dialog_type
        self._show_hidden = show_hidden

        self._limit_extensions = limit_extensions
        self.refresh_view()


    def refresh_view(self) -> None:
        """Function that refreshes the current list of files and folders in view
        """

        if not os.path.exists(self._current_dir):
            raise FileNotFoundError
        else:
            self.clear()
            dirs = []
            files = []
            for item in os.listdir(self._current_dir):
                if not self._show_hidden and is_filepath_hidden(os.path.join(self._current_dir, item)):
                    pass
                else:
                    item_path = os.path.join(self._current_dir, item)
                    if os.path.isdir(item_path):
                        dirs.append(FileDirElem('dir', item, item_path, ascii_icons=self._ascii_icons))
                    else:
                        if len(self._limit_extensions) > 0:
                            for ext in self._limit_extensions:
                                if item.endswith(ext):
                                    files.append(FileDirElem('file', item, item_path, ascii_icons=self._ascii_icons))
                                    break
                        else:
                            files.append(FileDirElem('file', item, item_path, ascii_icons=self._ascii_icons))

            # If not at root of file system, add a .. directory.
            up_dir = os.path.dirname(self._current_dir)
            if self._current_dir != up_dir:
                self.add_item(FileDirElem('dir', '..', up_dir, ascii_icons=self._ascii_icons))

            if self._dialog_type == 'openfile' or self._dialog_type == 'saveas':
                self.add_item_list(dirs)
                self.add_item_list(files)
            elif self._dialog_type == 'opendir':
                self.add_item_list(dirs)


class FileSelectElement(py_cui.ui.UIElement, FileSelectImplementation):
    """Custom UI Element for selecting files or directories.

    Displays list of files and dirs in a given location

    Attributes
    ----------
    _command : function
        a function that takes a single string parameter, run when ENTER pressed
    _run_command_if_none : bool
        Runs command even if there are no menu items (passes None)
    """

    def __init__(self, root, initial_dir, dialog_type: str, ascii_icons, title, color, command, renderer, logger, limit_extensions: List[str]=[]):
        """Initializer for MenuPopup. Uses MenuImplementation as base
        """

        py_cui.ui.UIElement.__init__(self, 0, os.path.abspath(initial_dir), renderer, logger)
        FileSelectImplementation.__init__(self, initial_dir, dialog_type, ascii_icons, logger, limit_extensions=limit_extensions)
        self._command              = command
        self._parent_dialog        = root
        self._text_color_rules = [
            py_cui.colors.ColorRule('\U0001f4c1', py_cui.BLUE_ON_BLACK, py_cui.WHITE_ON_BLUE,
                                    'startswith', 'region', [3, 1000], False, logger),
            py_cui.colors.ColorRule('<DIR>', py_cui.BLUE_ON_BLACK, py_cui.WHITE_ON_BLUE,
                                    'startswith', 'region', [6, 1000], False, logger),
            py_cui.colors.ColorRule('     ', py_cui.WHITE_ON_BLACK, py_cui.BLACK_ON_WHITE,
                                    'startswith', 'region', [6, 1000], True, logger),
            py_cui.colors.ColorRule('\U0001f5ce', py_cui.WHITE_ON_BLACK, py_cui.BLACK_ON_WHITE,
                                    'startswith', 'region', [3, 1000], False, logger)
        ]
        #self._run_command_if_none  = run_command_if_none


    def get_absolute_start_pos(self) -> Tuple[int,int]:
        """Override of base function. Uses the parent element do compute start position

        Returns
        -------
        start_x, start_y : int, int
            The position in characters in the terminal window to start the Field element
        """

        parent_start_x, parent_start_y = self._parent_dialog.get_start_position()
        start_x = (parent_start_x + 3 + self._parent_dialog._padx)
        start_y = (parent_start_y + self._parent_dialog._pady + 3)
        return start_x, start_y


    def get_absolute_stop_pos(self) -> Tuple[int,int]:
        """Override of base function. Uses the parent element do compute stop position

        Returns
        -------
        stop_x, stop_y : int, int
            The position in characters in the terminal window to stop the Field element
        """

        parent_stop_x, parent_stop_y = self._parent_dialog.get_stop_position()
        stop_x = (parent_stop_x - 3 - self._parent_dialog._padx)
        stop_y = (parent_stop_y - self._parent_dialog._pady - 7)
        return stop_x, stop_y


    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of base handle key press function

        Enter key runs command, Escape key closes menu

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """

        #super()._handle_key_press(key_pressed)
        if key_pressed == py_cui.keys.KEY_ENTER:
            old_dir = self._current_dir
            item = self.get()
            if item is not None:
                if os.path.isdir(item._path):
                    self._current_dir = item._path
                    try:
                        self.refresh_view()
                    except FileNotFoundError:
                        self._parent_dialog.display_warning('Selected directory does not exist!')
                        self._current_dir = old_dir
                        self.refresh_view()
                    except PermissionError:
                        self._parent_dialog.display_warning(f'Permission Error Accessing: {self._current_dir} !')
                        self._current_dir = old_dir
                        self.refresh_view()
                    finally:
                        self.set_title(self._current_dir)
                elif self._parent_dialog._dialog_type == 'openfile':
                    self._parent_dialog._submit(item._path)
                else:
                    pass

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


    def _draw(self) -> None:
        """Overrides base class draw function
        """

        self._renderer.set_color_mode(self._color)
        self._renderer.draw_border(self)
        self._renderer.set_color_rules(self._text_color_rules)
        counter = self._pady + 1
        line_counter = 0
        for item in self._view_items:
            line = str(item)
            if line_counter < self._top_view:
                line_counter = line_counter + 1
            else:
                if counter >= self._height - self._pady - 1:
                    break
                if line_counter == self.get_selected_item_index():
                    self._renderer.draw_text(self, line, self._start_y + counter, selected=True)
                else:
                    self._renderer.draw_text(self, line, self._start_y + counter)
                counter = counter + 1
                line_counter = line_counter + 1
        self._renderer.unset_color_mode(self._color)
        self._renderer.reset_cursor(self)


class FileNameInput(py_cui.ui.UIElement, py_cui.ui.TextBoxImplementation):
    """UI Element class representing name input field for filedialog

    Attributes
    ----------
    _parent_dialog : FileDialog
        parent dialog widget or popup
    """


    def __init__(self, parent_dialog, title, initial_dir, renderer, logger):
        """Initializer for the FormFieldElement class
        """

        self._parent_dialog = parent_dialog
        py_cui.ui.UIElement.__init__(self, 0, title, renderer, logger)
        py_cui.ui.TextBoxImplementation.__init__(self, title, False, logger)
        self._help_text = 'Press Tab to move to the next field, or Enter to submit.'
        self.set_text(initial_dir)
        self._padx = 0
        self._pady = 0
        self._selected = False
        self.update_height_width()


    def get_absolute_start_pos(self) -> Tuple[int,int]:
        """Override of base function. Uses the parent element do compute start position

        Returns
        -------
        start_x, start_y : int, int
            The position in characters in the terminal window to start the Field element
        """

        parent_start_x, _ = self._parent_dialog.get_start_position()
        _, parent_stop_y = self._parent_dialog.get_stop_position()
        start_x = (parent_start_x + 4 + self._parent_dialog._padx)
        start_y = (parent_stop_y - self._parent_dialog._pady - 7)
        return start_x, start_y


    def get_absolute_stop_pos(self) -> Tuple[int,int]:
        """Override of base function. Uses the parent element do compute stop position

        Returns
        -------
        stop_x, stop_y : int, int
            The position in characters in the terminal window to stop the Field element
        """

        _, parent_width = self._parent_dialog.get_absolute_dimensions()
        parent_stop_x, parent_stop_y = self._parent_dialog.get_stop_position()
        stop_x = (parent_stop_x - 4 - int(3 * parent_width / 7))
        stop_y = (parent_stop_y - self._parent_dialog._pady - 2)
        return stop_x, stop_y


    def update_height_width(self) -> None:
        """Override of base class. Updates text field variables for form field
        """

        py_cui.popups.Popup.update_height_width(self)
        padx, pady              = self.get_padding()
        start_x, start_y        = self.get_start_position()
        height, width           = self.get_absolute_dimensions()
        self._cursor_text_pos   = 0
        self._cursor_x          = start_x + 2 + padx
        self._initial_cursor    = self._cursor_x
        self._cursor_max_left   = self._cursor_x
        self._cursor_max_right  = start_x + width - 1 - pady
        self._cursor_y          = start_y + int(height / 2) + 1
        self._viewport_width    = self._cursor_max_right - self._cursor_max_left


    def _handle_key_press(self, key_pressed: int) -> None:
        """Handles text input for the field. Called by parent
        """

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
        elif key_pressed == py_cui.keys.KEY_ENTER:
            old_dir = self._parent_dialog._file_dir_select._current_dir
            new_elem = os.path.join(old_dir, self.get())
            try:
                if self._parent_dialog._dialog_type == 'saveas':
                    self._parent_dialog._submit(new_elem)

                elif self._parent_dialog._dialog_type == 'opendir':
                    os.mkdir(new_elem)
                    self._parent_dialog._file_dir_select.refresh_view()

                else:
                    fp = open(new_elem, 'w')
                    fp.close()
                    self._parent_dialog._file_dir_select.refresh_view()
                    
            except FileExistsError:
                self._parent_dialog.display_warning('File/Directory already exists!')
            except PermissionError:
                self._parent_dialog.display_warning('Insufficient permissions!')
            finally:
                self.clear()


    def _draw(self) -> None:
        """Draw function for the field. Called from parent. Essentially the same as a TextboxPopup
        """

        self._renderer.set_color_mode(self._parent_dialog._color)
        self._renderer.set_color_rules([])
        self._renderer.draw_text(self, self._title, self._cursor_y - 2, bordered=False, selected=self._selected)
        self._renderer.draw_border(self, fill=False, with_title=False)
        render_text = self._text
        if len(self._text) >self._viewport_width:
            end = len(self._text) - (self._viewport_width)
            if self._cursor_text_pos < end:
                render_text = self._text[self._cursor_text_pos:self._cursor_text_pos + (self._viewport_width)]
            else:
                render_text = self._text[end:]

        self._renderer.draw_text(self, render_text, self._cursor_y, selected=self._selected)

        if self._selected:
            self._renderer.draw_cursor(self._cursor_y, self._cursor_x)
        else:
            self._renderer.reset_cursor(self, fill=False)
        self._renderer.unset_color_mode(self._color)


class FileDialogButton(py_cui.ui.UIElement):
    """Utility button element for parent filedialog

    Attributes
    ----------
    _parent_dialog : FileDialog
        Main filedialog popup or widget
    _button_num : int
        0 for submit button, 1 for cancel button
    """


    def __init__(self, parent_dialog, statusbar_msg, command, button_num, *args):
        """Initializer for Button Widget
        """

        super().__init__(*args)
        self._parent_dialog = parent_dialog
        if self.get_title() == 'OK':
            self.set_color(py_cui.GREEN_ON_BLACK)
        else:
            self.set_color(py_cui.RED_ON_BLACK)
        self.set_help_text(statusbar_msg)
        self.command = command
        self._button_num = button_num


    def get_absolute_start_pos(self) -> Tuple[int,int]:
        """Override of base function. Uses the parent element do compute start position

        Returns
        -------
        start_x, start_y : int, int
            The position in characters in the terminal window to start the Field element
        """

        _, parent_width = self._parent_dialog.get_absolute_dimensions()
        parent_stop_x, parent_stop_y = self._parent_dialog.get_stop_position()
        start_x = (parent_stop_x - 4 - int((3 - self._button_num) * parent_width / 7))
        start_y = (parent_stop_y - self._parent_dialog._pady - 7)
        return start_x, start_y


    def get_absolute_stop_pos(self) -> Tuple[int,int]:
        """Override of base function. Uses the parent element do compute stop position

        Returns
        -------
        stop_x, stop_y : int, int
            The position in characters in the terminal window to stop the Field element
        """

        _, parent_width = self._parent_dialog.get_absolute_dimensions()
        parent_stop_x, parent_stop_y = self._parent_dialog.get_stop_position()
        stop_x = (parent_stop_x - 4 - int((2 - self._button_num) * parent_width / 7))
        stop_y = (parent_stop_y - self._parent_dialog._pady - 2)
        return stop_x, stop_y


    def _handle_mouse_press(self, x: int, y: int, mouse_event: int) -> None:
        """Handles mouse presses 

        Parameters
        ----------
        x : int
            x coordinate of click in characters
        y : int
            y coordinate of click in characters
        mouse_event : int
            Mouse event keycode of mouse press
        """

        super()._handle_mouse_press(x, y, mouse_event)
        if mouse_event == py_cui.keys.LEFT_MOUSE_CLICK:
            self.perform_command()


    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of base class, adds ENTER listener that runs the button's command

        Parameters
        ----------
        key_pressed : int
            Key code of pressed key
        """

        super()._handle_key_press(key_pressed)
        if key_pressed == py_cui.keys.KEY_ENTER:
            self.perform_command()

    
    def perform_command(self) -> None:
        if self.command is not None:
            if self._button_num == 1:
                if self._parent_dialog._dialog_type == 'saveas':
                    # If submitting 'saveas', we return the currently opened dir joined with the filename
                    res = os.path.join(self._parent_dialog._file_dir_select._current_dir, self._parent_dialog._filename_input.get())
                elif self._parent_dialog._dialog_type == 'opendir':
                    # Otherwise, return the currently opened directory
                    res = self._parent_dialog._file_dir_select._current_dir
                else:
                    res = self._parent_dialog._file_dir_select.get().get_path()
                if res is not None:
                    self.command(res)
                else:
                    self._parent_dialog.display_warning('No path is selected!')
            else:
                self._parent_dialog._root.close_popup()


    def _draw(self) -> None:
        """Override of base class draw function
        """

        #super()._draw()
        self._renderer.set_color_mode(self.get_color())
        self._renderer.draw_border(self, with_title=False)
        button_text_y_pos = self._start_y + int(self._height / 2)
        self._renderer.draw_text(self, self._title, button_text_y_pos, centered=True, selected=self._selected)
        self._renderer.reset_cursor(self)
        self._renderer.unset_color_mode(self.get_color())


class InternalFileDialogPopup(py_cui.popups.MessagePopup):
    """A helper class for abstracting a message popup tied to a parent popup

    Attributes
    ----------
    parent : FormPopup
        The parent form popup that spawned the message popup
    """

    def __init__(self, parent, *args):
        """Initializer for Internal form Popup
        """

        super().__init__(*args)
        self._parent = parent


    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of base class, close in parent instead of root
        """

        if key_pressed in self._close_keys:
            self._parent._internal_popup = None


class FileDialogPopup(py_cui.popups.Popup):
    """Main implementation class of a FileDialog poup.

    Attributes
    ----------
    _submit_action : func
        A function that takes a single string argument. Called with selected path when submit button is pressed
    _filename_input : FileNameInput
        Extension of textbox, acts as input field to create new dirs/files or select save name
    _file_dir_select : FileSelectElement
        Extension  of scroll menu used to display current files and dirs
    _submit_button : FileDialogButton
        Extension of button - Runs the callback with the selected file
    _cancel_button : FileDialogButton
        Extension of button - closes popup
    _internal_popup : InternalFileDialogPopup
        Extension of message popup, used to display warnings as secondary popup.
    _currently_selected : UIElement
        Currently selected sub-element of file dialog popup
    """


    def __init__(self, root, callback, initial_dir, dialog_type, ascii_icons, limit_extensions, color, renderer, logger):
        """Initalizer for the FileDialogPopup
        """

        # Convert dialog type into popup title message
        title = ''
        input_title = 'Path'
        if dialog_type == 'openfile':
            title = 'Open File'
            input_title = 'New File'
        elif dialog_type == 'opendir':
            title = 'Open Directory'
            input_title = 'New Dir'
        elif dialog_type == 'saveas':
            title = 'Save As'
            input_title = 'New Name'

        # Call superclass initailizer
        py_cui.popups.Popup.__init__(self, root, title, '', color, renderer, logger)

        # Our submit action must be a function that takes a string as its only parameter.
        self._submit_action = callback
        self._dialog_type = dialog_type

        # Create our internal UI elements. Menu for selection, field for new elements, buttons for submit/cancel.
        self._filename_input = FileNameInput(self, input_title, '', renderer, logger)
        self._file_dir_select = FileSelectElement(self, initial_dir, dialog_type, ascii_icons, title, color, None, renderer, logger, limit_extensions=limit_extensions)
        self._submit_button = FileDialogButton(self, title, self._submit, 1, '', 'OK', renderer, logger)
        self._cancel_button = FileDialogButton(self, f'Cancel {title}', self._root.close_popup, 2, '', 'ESC', renderer, logger)

        # Internal popup used for secondary errors and warnings
        self._internal_popup = None

        # Initialize current state.
        self.update_height_width()
        self._file_dir_select.set_selected(True)
        self._currently_selected = self._file_dir_select


    def _submit(self, output: str) -> None:
        valid, msg = self.output_valid(output)
        if not valid and msg is not None:
            self.display_warning(msg)
        else:
            self._submit_action(output)


    def display_warning(self, message: str) -> None:
        """Helper function for showing internal popup warning message

        Parameters
        ----------
        message : str
            Warning message to display
        """


        self._internal_popup = InternalFileDialogPopup(self,
                                                        self._root,
                                                        'Warning!',
                                                        message,
                                                        py_cui.YELLOW_ON_BLACK,
                                                        self._renderer,
                                                        self._logger)


    def output_valid(self, output) -> Tuple[bool,Optional[str]]:
        if self._dialog_type == 'openfile' and not os.path.isfile(output):
            return False, 'Please select a valid file path!'
        elif self._dialog_type == 'opendir' and not os.path.isdir(output):
            return False, 'Please select a valid directory path!'
        elif self._dialog_type == 'saveas' and not os.access(self._file_dir_select._current_dir, os.W_OK):
            return False, 'Permission Error!'
        return True, None


    def get_absolute_start_pos(self) -> Tuple[int,int]:
        """Override of base class, computes position based on root dimensions
        
        Returns
        -------
        start_x, start_y : int
            The coords of the upper-left corner of the popup
        """

        root_height, root_width = self._root.get_absolute_size()
        form_start_x = int(root_width / 8)
        form_start_y = int(root_height / 9)

        return form_start_x, form_start_y


    def get_absolute_stop_pos(self) -> Tuple[int,int]:
        """Override of base class, computes position based on root dimensions
        
        Returns
        -------
        stop_x, stop_y : int
            The coords of the lower-right corner of the popup
        """

        root_height, root_width = self._root.get_absolute_size()
        form_stop_x = int(7 * root_width / 8)
        form_stop_y = int(8.75 * root_height / 9)

        return form_stop_x, form_stop_y


    def update_height_width(self) -> None:
        """Override of base class function

        Also updates all form field elements in the form
        """

        super().update_height_width()
        try:
            self._file_dir_select.update_height_width()
            self._filename_input.update_height_width()
            self._submit_button.update_height_width()
            self._cancel_button.update_height_width()
        except AttributeError:
            pass


    def _handle_key_press(self, key_pressed:int) -> None:
        """Override of base class. Here, we handle tabs, enters, and escapes

        All other key presses are passed to the currently selected field element

        Parameters
        ----------
        key_pressed : int
            Key code of pressed key
        """

        # If internal popup is active, pass keypresses down to it.
        if self._internal_popup is None:
            # Use the TAB key to cycle between sub-elements
            if key_pressed == py_cui.keys.KEY_TAB:
                if self._currently_selected == self._file_dir_select:
                    self._file_dir_select.set_selected(False)
                    self._currently_selected = self._filename_input
                    self._filename_input.set_selected(True)
                elif self._currently_selected == self._filename_input:
                    self._filename_input.set_selected(False)
                    self._currently_selected = self._submit_button
                    self._submit_button.set_selected(True)
                elif self._currently_selected == self._submit_button:
                    self._submit_button.set_selected(False)
                    self._currently_selected = self._cancel_button
                    self._cancel_button.set_selected(True)
                elif self._currently_selected == self._cancel_button:
                    self._cancel_button.set_selected(False)
                    self._currently_selected = self._file_dir_select
                    self._file_dir_select.set_selected(True)

            # Use the escape key to cancel
            elif key_pressed == py_cui.keys.KEY_ESCAPE:
                self._root.close_popup()

            # Otherwise pass key to currently selected sub-element
            else:
                self._currently_selected._handle_key_press(key_pressed)
        else:
            self._internal_popup._handle_key_press(key_pressed)


    def _handle_mouse_press(self, x: int, y: int, mouse_event: int) -> None:
        """Override of base class function

        Simply enters the appropriate field when mouse is pressed on it

        Parameters
        ----------
        x, y : int, int
            Coordinates of the mouse press
        """

        super()._handle_mouse_press(x, y, mouse_event)
        if self._file_dir_select._contains_position(x, y):
            self._filename_input.set_selected(False)
            self._file_dir_select.set_selected(True)
            self._file_dir_select._handle_mouse_press(x, y, mouse_event)
            
        elif self._filename_input._contains_position(x, y):
            self._filename_input.set_selected(True)
            self._file_dir_select.set_selected(False)
            self._filename_input._handle_mouse_press(x, y, mouse_event)
        
        elif self._submit_button._contains_position(x, y):
            self._submit_button._handle_mouse_press(x, y, mouse_event)

        elif self._cancel_button._contains_position(x, y):
            self._cancel_button._handle_mouse_press(x, y, mouse_event)


    def _draw(self) -> None:
        """Override of base class.
        
        Here, we only draw a border, and then the individual form elements
        """

        # Renderer prep
        self._renderer.set_color_mode(self._color)
        self._renderer.set_color_rules([])
        self._renderer.draw_border(self)

        # Draw all sub-elements
        self._file_dir_select._draw()
        self._filename_input._draw()
        self._submit_button._draw()
        self._cancel_button._draw()

        # Re-draw the selected element last so we have cursor in correct spot
        self._currently_selected._draw()

        # If required, draw internal popup.
        if self._internal_popup is not None:
            self._internal_popup._draw()
        self._renderer.unset_color_mode(self._color)

#class FileDialogWidget
