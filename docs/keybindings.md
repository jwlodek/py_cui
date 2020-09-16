# Keybindings

Almost all CUI elements in `py_cui` support some degree of keybindings. The order in which these keybindings are executed depend on the order they are added, however, user keybindings are always executed prior to default keybindings, so make sure you don't unintentionally override an already bound key. Lists of default keybindings for each widget are available in the `Widgets` section of this documentation, and a list of default keybindings for overview mode is found in the `Usage` section.

### Adding a Keybinding

For all keybindings, you must pass a `py_cui` key and a function with no arguments. This function will be fired when the key bound to it is detected. The function may also be a class funciton, with `self.FUNCTION` being passed into the add keybinding function. Make sure to take a look at the examples for more uses of keybindings.

**Overview Mode**

To add a keybinding to overview mode, you need to add it to the `PyCUI` object itself. For example, if I wanted to add a binding for the `c` key to clear all text fields in my `cui`:

```Python
# import the library
import py_cui

# Create the PyCUI and add a text field
root = py_cui.PyCUI(3, 3)
text_field = root.add_text_box('Text Field', 1, 1)

# This function simply clears the text in the text field
def clear_text_field():
    text_field.clear()

# Add the key binding to the PyCUI object itself for overview mode.
root.add_key_command(py_cui.keys.KEY_C_LOWER, clear_text_field)

# Start the CUI
root.start()
```

**Focus Mode**

Adding keybindings to focus mode is done at a widget by widget basis. When a widget is added to the `PyCUI`, the returned object is used to add a key command. Once again, make sure to check default key bindings that should only be overridden if the user specifically desires to replace their functionality.

For example, in a menu widget, if we wish to set the window title to the selected menu item with the `t` key, we could write the following:
```Python
# import the library
import py_cui

# Create the CUI object
root  = py_cui.PyCUI(3,3)

# Add the scroll menu with the three menu items
menu_items = ['Item1', 'Item2', 'Item3']
menu = root.add_scroll_menu('Test Menu', 1, 1)
menu.add_item_list(menu_items)

# Function that sets the root window title
def set_title_from_menu():
    root.set_title(menu.get())

# Bind the 't' key to the above function
menu.add_key_command(py_cui.keys.KEY_T_LOWER, set_title_from_menu)

# start the CUI
root.start()
```

### Supported Keys

There are many supported keys in `py_cui`. These include alpha-numeric keys (in both uppercase and lowercase), as well as those keys with `Ctrl` and `Alt` modifiers. These can be accessed with (using the letter x as an example):

* `py_cui.keys.KEY_X_LOWER` - Lowercase `X` key
* `py_cui.keys.KEY_X_UPPER` - Uppercase `X` key (`Shift + x`)
* `py_cui.keys.KEY_CTRL_X` - Control key modified `X` (`Ctrl + x`)
* `py_cui.keys.KEY_ALT_X` - Alt key modified `X` (`Alt + x`)

In the case of numeric keys, there is no upper/lower distinction.

In addition, `py_cui` supports several non alpha-numeric keys, as described in the below table.

Key Code | Key Presses
---------|------------
KEY_ENTER      | Enter (newline) Key
KEY_ESCAPE     | Escape Key
KEY_SPACE      | Space Key
KEY_DELETE     | Delete Key
KEY_TAB        | Tab Key
KEY_UP_ARROW   | Up Arrow Key
KEY_DOWN_ARROW | Down Arrow Key
KEY_LEFT_ARROW | Left Arrow Key
KEY_RIGHT_ARROW | Right Arrow Key
KEY_SHIFT_LEFT  | Shift Modified Left
KEY_SHIFT_RIGHT | Shift Modified Right
KEY_SHIFT_UP    | Shift Modified Up
KEY_SHIFT_DOWN  | Shift Modified Down
KEY_CTRL_LEFT   | Ctrl Modified Left
KEY_CTRL_RIGHT  | Ctrl Modified Right
KEY_CTRL_UP     | Ctrl Modified Up
KEY_CTRL_DOWN   | Ctrl Modified Down
KEY_PAGE_UP    | Page Up Key
KEY_PAGE_DOWN  | Page Down Key
KEY_F1         | F1 Function Key
KEY_F2         | F2 Function Key
KEY_F3         | F3 Function Key
KEY_F4         | F4 Function Key
KEY_F5         | F5 Function Key
KEY_F6         | F6 Function Key
KEY_F7         | F7 Function Key
KEY_F8         | F8 Function Key
KEY_HOME       | Home Key
KEY_END        | End Key
KEY_BACKSPACE | Backspace Key

There are also abstractions provided by `py_cui` for considering sets of keys. For example `py_cui.keys.ARROW_KEYS` is a list of key codes for each arrow key. These abstractions are useful for applying a key command for each key in a set of keys.