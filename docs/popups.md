# Popups

This page contains information regarding all popups supported by `py_cui`. Please see the `popups_example.py` in the `examples/` directory in the repository. In general, `py_cui` popups are handled by using callback functions. A popup is opened with a special `show` method, and then upon some user action a callback function is fired, with some specified input parameters.

### Message/Warning/Error Popup

**Spawn Command**
```
show_message_popup(title, text, color = WHITE_ON_BLACK)
show_warning_popup(title, text)
show_error_popup(title, text)
```
**Usage**

`show_message_popup` takes an optional `color` argument which defaults to standard WHITE_ON_BLACK.
`show_warning_popup` and `show_error_popup` are shorthand for respectively yellow and red colors.

**Keys**

Exit from the popup with `KEY_ENTER`, `KEY_ESCAPE`, or `KEY_SPACE`.

### Yes/No Popup

**Spawn Command**
```
show_yes_no_popup(self, title, command)
```
**Usage**

Ask user yes/no question. The `command` parameter passed to the spawn function must be a function that takes a single boolean parameter.

**Keys**

If `KEY_Y_LOWER` is pressed, the command will be run with `True` passed in, otherwise `False` is passed in.

### Loading Icon/Bar Popup

**Spawn Command**
```
show_loading_icon_popup(title, message)
show_loading_bar_popup(title, num_items)
```
**Usage**
The loading popups must be used in conjunction with some sort of async/threading. First, spawn the popup and then start a thread performing the long operation. At the end of the long operation, call:
```
stop_loading_popup()
```
Which will escape the loading popup.
When using the loading bar popup, increment yout item counter with:
```
increment_loading_bar()
```
**Keys**

None

### TextBox Popup

**Spawn Command**
```
show_text_box_popup(title, command)
```
**Usage**

Spawn a text box, and on `KEY_ENTER` pressed, the command function is triggered with the text from the popup as the parameter.

**Keys**

The letter keys will write the text, and `KEY_ENTER` submits.

### Menu Popup

**Spawn Command**
```
show_menu_popup(title, menu_items, command, run_command_if_none=False)
```
**Usage**

Use as an overall menu system for your application. Gives user option to select from list. Fires the command with the selected menu item as a parameter on `KEY_ENTER`

**Keys**

Arrow keys scroll up and down, enter key submits.
