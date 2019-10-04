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
root.add_key_binding(py_cui.keys.KEY_C_LOWER, clear_text_field)

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

Below is a table of all keys supported by `py_cui`. Each key is accessed within your program with `py_cui.keys.YOUR_KEY_CODE`. There are some differences in the way keycodes are handled on win32 vs. UNIX, though this is abstracted away by py_cui.

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
KEY_A_LOWER    | a Key
KEY_B_LOWER    | b Key
KEY_C_LOWER    | c Key
KEY_D_LOWER    | d Key
KEY_E_LOWER    | e Key
KEY_F_LOWER    | f Key
KEY_G_LOWER    | g Key
KEY_H_LOWER    | h Key
KEY_I_LOWER    | i Key
KEY_J_LOWER    | j Key
KEY_K_LOWER    | k Key
KEY_L_LOWER    | l Key
KEY_M_LOWER    | m Key
KEY_N_LOWER    | n Key
KEY_O_LOWER    | o Key
KEY_P_LOWER    | p Key
KEY_Q_LOWER    | q Key
KEY_R_LOWER    | r Key
KEY_S_LOWER    | s Key
KEY_T_LOWER    | t Key
KEY_U_LOWER    | u Key
KEY_V_LOWER    | v Key
KEY_W_LOWER    | w Key
KEY_X_LOWER    | x Key
KEY_Y_LOWER    | y Key
KEY_Z_LOWER    | z Key
KEY_A_UPPER    | a Key + Shift Key
KEY_B_UPPER    | b Key + Shift Key
KEY_C_UPPER    | c Key + Shift Key
KEY_D_UPPER    | d Key + Shift Key
KEY_E_UPPER    | e Key + Shift Key
KEY_F_UPPER    | f Key + Shift Key
KEY_G_UPPER    | g Key + Shift Key
KEY_H_UPPER    | h Key + Shift Key
KEY_I_UPPER    | i Key + Shift Key
KEY_J_UPPER    | j Key + Shift Key
KEY_K_UPPER    | k Key + Shift Key
KEY_L_UPPER    | l Key + Shift Key
KEY_M_UPPER    | m Key + Shift Key
KEY_N_UPPER    | n Key + Shift Key
KEY_O_UPPER    | o Key + Shift Key
KEY_P_UPPER    | p Key + Shift Key
KEY_Q_UPPER    | q Key + Shift Key
KEY_R_UPPER    | r Key + Shift Key
KEY_S_UPPER    | s Key + Shift Key
KEY_T_UPPER    | t Key + Shift Key
KEY_U_UPPER    | u Key + Shift Key
KEY_V_UPPER    | v Key + Shift Key
KEY_W_UPPER    | w Key + Shift Key
KEY_X_UPPER    | x Key + Shift Key
KEY_Y_UPPER    | y Key + Shift Key
KEY_Z_UPPER    | z Key + Shift Key
KEY_BACKSPACE | Backspace Key