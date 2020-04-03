# Widgets

Below are details on each widget supported by `py_cui` including how to add them to a CUI, draw behavior, and default keybindings. Please take a look at `Classes and Functions` section of these docs to see function/attribute information.

### Label

**Usage**

Labels only display text. You cannot enter focus mode on labels, and thus keybindings will have no effect.
Add labels for single lines to text to the center of a grid cell.

**Adding to CUI**
```
add_label(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0)
```

**Draw Behavior**

Draws `self._title` in the center of the grid location it is placed in.

**Default Keybindings**

None

### Block Label

**Usage**

Block Labels only display text. You cannot enter focus mode on block labels, and thus keybindings will have no effect.
Add block labels for multi line text that will be drawn in the center of the grid cell. One example for this is to display ASCII-Art.

**Adding to CUI**
```
add_block_label(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0)
```

**Draw Behavior**

Draws `self._title.splitlines()` in the center of the grid location it is placed in.

**Default Keybindings**

None

### Button

**Usage**

Buttons execute a no-args function when enter pressed. By default, pressing enter when hovering over a button executes the command instead of entering focus mode. To disable this behavior, add the `auto_focus_buttons=False` to the creation of the `PyCUI` object.

**Adding to CUI**
```
add_button(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, command=None)
```
**Draw Behavior**

Draws `self._title` centered in the grid cell, with a border. By default, buttons have a magenta color.

**Default Keybindings**

* KEY_ENTER - runs the command passed into the button

### Scroll Menu

**Usage**

Scroll Menus are very useful for having multiple option menus or for showing a list of information. The most common usage is to add a keybinding for the `ENTER` which processes some function depending on the selected item.

**Adding to CUI**
```
menu_item_list = ["Item1", "Item2", ...]
menu = add_scroll_menu(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0)
menu.add_item_list(menu_item_list)
```
**Draw Behavior**

Draws all menu items starting with upper viewport item down, along with a border. The title is drawn inline with the top of the border

**Default Keybindings**

* KEY_UP_ARROW - Scrolls up if selected item index is greater than 0
* KEY_DOWN_ARROW - Scrolls down if selected item index is not at the end of the list

### Checkbox Menu

The checkbox menu extends from the scrollmenu, and so shares many functions with it.

**Usage**

Checkbox Menus are very useful for selecting several options. They should be used for having the user to select multiple items.

**Adding to CUI**
```
menu_item_list = ["Item1", "Item2", ...]
menu = add_checkbox_menu(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0)
menu.add_item_list(menu_item_list)
```
**Draw Behavior**

Draws all menu items starting with upper viewport item down, along with a border. The title is drawn inline with the top of the border

**Default Keybindings**

* KEY_UP_ARROW - Scrolls up if selected item index is greater than 0
* KEY_DOWN_ARROW - Scrolls down if selected item index is not at the end of the list

### Text Box

**Usage**

Used for user entering text into CUI. For prompts, it is suggested to use the Textbox popup instead.

**Adding to CUI**
```
add_text_box(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, initial_text = '')
```
**Draw Behavior**

Draws title above a bordered entry field centered in the grid cell assigned

**Default Keybindings**

* KEY_END - Jumps to the end of the text
* KEY_HOME - Jumps to start of the text
* KEY_LEFT_ARROW - Shifts cursor to left
* KEY_RIGHT_ARROW - Shifts cursor to right
* Letter Keys - writes the appropriate letter to the text
* KEY_BACKSPACE - Erases character in text

### Text Block

**Usage**

TextBoxes have two key uses:
* For editing larger blocks of text, such as if you wish to create a CUI text editor (see `snano` example)
* For displaying large amounts of text, such as statuses, logs etc. (see `pyautogit` example)

**Adding to CUI**
```
add_text_block(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, initial_text = '')
```
**Draw Behavior**

Draws title above a bordered entry box that fills the grid cells.

**Default Keybindings**

* KEY_END - Jumps to the end of the text
* KEY_HOME - Jumps to start of the text
* KEY_LEFT_ARROW - Shifts cursor to left
* KEY_RIGHT_ARROW - Shifts cursor to right
* KEY_DOWN_ARROW - Shifts cursor down
* KEY_UP_ARROW - Shifts cursor up
* Letter Keys - writes the appropriate letter to the text
* KEY_BACKSPACE - Erases character in text
* KEY_TAB - Enters 4 space characters (Sorry tab people)
* KEY_DELETE - Deletes next character
* KEY_ENTER - Inserts newline character
