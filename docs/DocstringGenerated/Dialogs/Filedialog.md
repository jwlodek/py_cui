# filedialog

Implementation, widget, and popup classes for file selection dialogs



#### Classes

 Class  | Doc
-----|-----
 FileDirElem | Simple helper class defining a single file or directory
 FileSelectImplementation(py_cui.ui.MenuImplementation) | Extension of menu implementation that allows for listing files and dirs in a location
 FileSelectElement(py_cui.ui.UIElement, FileSelectImplementation) | Custom UI Element for selecting files or directories.
 FileNameInput(py_cui.ui.UIElement, py_cui.ui.TextBoxImplementation) | UI Element class representing name input field for filedialog
 FileDialogButton(py_cui.ui.UIElement) | Utility button element for parent filedialog
 InternalFileDialogPopup(py_cui.popups.MessagePopup) | A helper class for abstracting a message popup tied to a parent popup
 FileDialogPopup(py_cui.popups.Popup) | Main implementation class of a FileDialog poup.

#### Functions

 Function  | Doc
-----|-----
 is_filepath_hidden | Function checks if file or folder is considered "hidden"




### is_filepath_hidden

```python
def is_filepath_hidden(path)
```

Function checks if file or folder is considered "hidden"




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 path  |  str | Path to file or folder

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 marked_hidden  |  bool | True if name starts with '.', or has hidden attribute in OS





## FileDirElem

```python
class FileDirElem
```

Simple helper class defining a single file or directory




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _type  |  str | Either dir or file
 _name  |  str | The name of the file or directory
 _path  |  str | The absolute path to the directory or file
 _folder_icon  |  str | icon or text for folder
 _file_icon  |  str | icon for file

#### Methods

 Method  | Doc
-----|-----
 get_path | Getter for path
 __str__ | Override of to-string function




### __init__

```python
def __init__(self, elem_type, name, fullpath, ascii_icons=False)
```

Intializer for FilDirElem







### get_path

```python
def get_path(self)
```

Getter for path




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 path  |  str | Path of file/dir represented by elem





### __str__

```python
def __str__(self)
```

Override of to-string function




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 description  |  str | Icon and name of dir or file








## FileSelectImplementation(py_cui.ui.MenuImplementation)

```python
class FileSelectImplementation(py_cui.ui.MenuImplementation)
```

Extension of menu implementation that allows for listing files and dirs in a location




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _current_dir  |  str | The current focused-on directory
 _ascii_icons  |  bool | Toggle using ascii or unicode icons
 _dialog_type  |  str | Type of open dialog
 _limit_extensions  |  List[str] | List of file extensions to show as visible

#### Methods

 Method  | Doc
-----|-----
 refresh_view | Function that refreshes the current list of files and folders in view




### __init__

```python
def __init__(self, initial_loc, dialog_type, ascii_icons, logger, limit_extensions = [], show_hidden=False)
```

Initalizer for the file select menu implementation. Includes some logic for getting list of file and folders.







### refresh_view

```python
def refresh_view(self)
```

Function that refreshes the current list of files and folders in view










## FileSelectElement(py_cui.ui.UIElement, FileSelectImplementation)

```python
class FileSelectElement(py_cui.ui.UIElement, FileSelectImplementation)
```

Custom UI Element for selecting files or directories.



Displays list of files and dirs in a given location


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _command  |  function | a function that takes a single string parameter, run when ENTER pressed
 _run_command_if_none  |  bool | Runs command even if there are no menu items (passes None)

#### Methods

 Method  | Doc
-----|-----
 get_absolute_start_pos | Override of base function. Uses the parent element do compute start position
 get_absolute_stop_pos | Override of base function. Uses the parent element do compute stop position
 _handle_key_press | Override of base handle key press function
 _draw | Overrides base class draw function




### __init__

```python
def __init__(self, root, initial_dir, dialog_type, ascii_icons, title, color, command, renderer, logger, limit_extensions=[])
```

Initializer for MenuPopup. Uses MenuImplementation as base







### get_absolute_start_pos

```python
def get_absolute_start_pos(self)
```

Override of base function. Uses the parent element do compute start position




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 start_x, start_y  |  int, int | The position in characters in the terminal window to start the Field element





### get_absolute_stop_pos

```python
def get_absolute_stop_pos(self)
```

Override of base function. Uses the parent element do compute stop position




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 stop_x, stop_y  |  int, int | The position in characters in the terminal window to stop the Field element





### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Override of base handle key press function



Enter key runs command, Escape key closes menu


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of key pressed





### _draw

```python
def _draw(self)
```

Overrides base class draw function










## FileNameInput(py_cui.ui.UIElement, py_cui.ui.TextBoxImplementation)

```python
class FileNameInput(py_cui.ui.UIElement, py_cui.ui.TextBoxImplementation)
```

UI Element class representing name input field for filedialog




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _parent_dialog  |  FileDialog | parent dialog widget or popup

#### Methods

 Method  | Doc
-----|-----
 get_absolute_start_pos | Override of base function. Uses the parent element do compute start position
 get_absolute_stop_pos | Override of base function. Uses the parent element do compute stop position
 update_height_width | Override of base class. Updates text field variables for form field
 _handle_key_press | Handles text input for the field. Called by parent
 _draw | Draw function for the field. Called from parent. Essentially the same as a TextboxPopup




### __init__

```python
def __init__(self, parent_dialog, title, initial_dir, renderer, logger)
```

Initializer for the FormFieldElement class







### get_absolute_start_pos

```python
def get_absolute_start_pos(self)
```

Override of base function. Uses the parent element do compute start position




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 start_x, start_y  |  int, int | The position in characters in the terminal window to start the Field element





### get_absolute_stop_pos

```python
def get_absolute_stop_pos(self)
```

Override of base function. Uses the parent element do compute stop position




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 stop_x, stop_y  |  int, int | The position in characters in the terminal window to stop the Field element





### update_height_width

```python
def update_height_width(self)
```

Override of base class. Updates text field variables for form field







### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Handles text input for the field. Called by parent







### _draw

```python
def _draw(self)
```

Draw function for the field. Called from parent. Essentially the same as a TextboxPopup










## FileDialogButton(py_cui.ui.UIElement)

```python
class FileDialogButton(py_cui.ui.UIElement)
```

Utility button element for parent filedialog




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _parent_dialog  |  FileDialog | Main filedialog popup or widget
 _button_num  |  int | 0 for submit button, 1 for cancel button

#### Methods

 Method  | Doc
-----|-----
 get_absolute_start_pos | Override of base function. Uses the parent element do compute start position
 get_absolute_stop_pos | Override of base function. Uses the parent element do compute stop position
 _handle_mouse_press | Handles mouse presses
 _handle_key_press | Override of base class, adds ENTER listener that runs the button's command
 perform_command |
 _draw | Override of base class draw function




### __init__

```python
def __init__(self, parent_dialog, statusbar_msg, command, button_num, *args)
```

Initializer for Button Widget







### get_absolute_start_pos

```python
def get_absolute_start_pos(self)
```

Override of base function. Uses the parent element do compute start position




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 start_x, start_y  |  int, int | The position in characters in the terminal window to start the Field element





### get_absolute_stop_pos

```python
def get_absolute_stop_pos(self)
```

Override of base function. Uses the parent element do compute stop position




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 stop_x, stop_y  |  int, int | The position in characters in the terminal window to stop the Field element





### _handle_mouse_press

```python
def _handle_mouse_press(self, x, y)
```

Handles mouse presses




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 x  |  int | x coordinate of click in characters
 y  |  int | y coordinate of click in characters





### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Override of base class, adds ENTER listener that runs the button's command




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | Key code of pressed key





### perform_command

```python
def perform_command(self)
```









### _draw

```python
def _draw(self)
```

Override of base class draw function










## InternalFileDialogPopup(py_cui.popups.MessagePopup)

```python
class InternalFileDialogPopup(py_cui.popups.MessagePopup)
```

A helper class for abstracting a message popup tied to a parent popup




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 parent  |  FormPopup | The parent form popup that spawned the message popup

#### Methods

 Method  | Doc
-----|-----
 _handle_key_press | Override of base class, close in parent instead of root




### __init__

```python
def __init__(self, parent, *args)
```

Initializer for Internal form Popup







### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Override of base class, close in parent instead of root










## FileDialogPopup(py_cui.popups.Popup)

```python
class FileDialogPopup(py_cui.popups.Popup)
```

Main implementation class of a FileDialog poup.




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _submit_action  |  func | A function that takes a single string argument. Called with selected path when submit button is pressed
 _filename_input  |  FileNameInput | Extension of textbox, acts as input field to create new dirs/files or select save name
 _file_dir_select  |  FileSelectElement | Extension  of scroll menu used to display current files and dirs
 _submit_button  |  FileDialogButton | Extension of button - Runs the callback with the selected file
 _cancel_button  |  FileDialogButton | Extension of button - closes popup
 _internal_popup  |  InternalFileDialogPopup | Extension of message popup, used to display warnings as secondary popup.
 _currently_selected  |  UIElement | Currently selected sub-element of file dialog popup

#### Methods

 Method  | Doc
-----|-----
 _submit |
 display_warning | Helper function for showing internal popup warning message
 output_valid |
 get_absolute_start_pos | Override of base class, computes position based on root dimensions
 get_absolute_stop_pos | Override of base class, computes position based on root dimensions
 update_height_width | Override of base class function
 _handle_key_press | Override of base class. Here, we handle tabs, enters, and escapes
 _handle_mouse_press | Override of base class function
 _draw | Override of base class.




### __init__

```python
def __init__(self, root, callback, initial_dir, dialog_type, ascii_icons, limit_extensions, color, renderer, logger)
```

Initalizer for the FileDialogPopup







### _submit

```python
def _submit(self, output)
```









### display_warning

```python
def display_warning(self, message)
```

Helper function for showing internal popup warning message




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 message  |  str | Warning message to display





### output_valid

```python
def output_valid(self, output)
```









### get_absolute_start_pos

```python
def get_absolute_start_pos(self)
```

Override of base class, computes position based on root dimensions




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 start_x, start_y  |  int | The coords of the upper-left corner of the popup





### get_absolute_stop_pos

```python
def get_absolute_stop_pos(self)
```

Override of base class, computes position based on root dimensions




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 stop_x, stop_y  |  int | The coords of the lower-right corner of the popup





### update_height_width

```python
def update_height_width(self)
```

Override of base class function



Also updates all form field elements in the form





### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Override of base class. Here, we handle tabs, enters, and escapes



All other key presses are passed to the currently selected field element


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | Key code of pressed key





### _handle_mouse_press

```python
def _handle_mouse_press(self, x, y)
```

Override of base class function



Simply enters the appropriate field when mouse is pressed on it


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 x, y  |  int, int | Coordinates of the mouse press





### _draw

```python
def _draw(self)
```

Override of base class.



Here, we only draw a border, and then the individual form elements








