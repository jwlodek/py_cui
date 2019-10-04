# Widgets

Below are details on each widget supported by `py_cui` including how to add them to a CUI, and their supported functions.

### Base Widget Class

This base class contains all shared functionality.


### Label


**Widget Specific Class Variables**

None

**Widget Specific Functions**

None

**Usage**

Labels only display text. You cannot enter focus mode on labels, and thus keybindings will have no effect.
Add labels for single lines to text to the center of a grid cell.

**Adding to CUI**
```
add_label(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0)
```

**Draw Behavior**

Draws `self.title` in the center of the grid location it is placed in.

**Default Keybindings**

None

### Block Label

**Widget Specific Class Variables**

* `self.lines` - represents the title passed in split on newline characters

**Widget Specific Functions**

None

**Usage**

Block Labels only display text. You cannot enter focus mode on block labels, and thus keybindings will have no effect.
Add block labels for multi line text that will be drawn in the center of the grid cell. One example for this is to display ASCII-Art.

**Adding to CUI**
```
add_block_label(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0)
```

**Draw Behavior**

Draws `self.title.splitlines()` in the center of the grid location it is placed in.

**Default Keybindings**

None

### Button

**Widget Specific Class Variables**

* `self.command` - represents the command executed when Enter key pressed on button

**Widget Specific Functions**

None

**Usage**

Buttons execute a no-args function when enter pressed. By default, pressing enter when hovering over a button executes the command instead of entering focus mode. To disable this behavior, add the `auto_focus_buttons=False` to the creation of the `PyCUI` object.

**Adding to CUI**
```
add_button(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, command=None)
```
**Draw Behavior**

Draws `self.title` centered in the grid cell, with a border. By default, buttons have a magenta color.

**Default Keybindings**

* KEY_ENTER - runs the command passed into the button

### Scroll Menu

**Widget Specific Class Variables**

* `self.top_view` - Uppermost menu item in viewport
* `self.selected_item` - currently selected item index
* `self.view_items` - list of menu items

**Widget Specific Functions**

* `clear()` - removes all selected items
* `scroll_up()` - Internal use only, scrolls up in menu
* `scroll_down()` - Internal use only, scrolls down in menu
* `add_item(item)` - Takes in a string, adds it as an item to the menu
* `add_item_list(item_list)` - Takes a list of strings, adds them all to the menu
* `remove_selected_item()` - Removes the currently selected item from the menu
* `get()` - Returns the currently selected item
* `get_item_list()` - gets current list of menu items

**Usage**

Scroll Menus are very useful for having multiple option menus or for showing a list of information. The most common usage is to add a keybinding for the `ENTER` which processes some function depending on the selected item.

**Adding to CUI**
```
menu_item_list = ["Item1", "Item2", ...]
menu = add_scroll_menu(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0)
menu.add_item_list(menu_item_list)
```
**Draw Behavior**

Draws all menu items starting with `self.top_view` down, along with a border. `self.title` is drawn inline with the top of the border

**Default Keybindings**

* KEY_UP_ARROW - Scrolls up if `self.selected_item` is greater than 0
* KEY_DOWN_ARROW - Scrolls down if `self.selected_item` is not at the end of the list

### Checkbox Menu

The checkbox menu extends from the scrollmenu, and so shares many functions with it.

**Widget Specific Class Variables**

* `self.selected_item_list` - list of selected items
* `self.checked_char` - character to mark item as checked

**Widget Specific Functions**

* `mark_item_as_checked(text)` - marks item matching text as checked
* `get()` - overrides the `ScrollMenu` function. Returns the selected item list

All functions included from `ScrollMenu` are also available.

**Usage**

Checkbox Menus are very useful for selecting several options. They should be used for having the user to select multiple items.

**Adding to CUI**
```
menu_item_list = ["Item1", "Item2", ...]
menu = add_checkbox_menu(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0)
menu.add_item_list(menu_item_list)
```
**Draw Behavior**

Draws all menu items starting with `self.top_view` down, along with a border. `self.title` is drawn inline with the top of the border

**Default Keybindings**

* KEY_UP_ARROW - Scrolls up if `self.selected_item` is greater than 0
* KEY_DOWN_ARROW - Scrolls down if `self.selected_item` is not at the end of the list

### Text Box

**Widget Specific Class Variables**

* `self.text` - text currently in the text box
* `self.cursor_x` - cursor x  location in terms of terminal characters
* `self.cursor_text_pos` - cursor position relative to the text
* `self.cursor_max_left` - maximum terminal position for the cursor on the left
* `self.cursor_max_right` - maximum terminal position for the cursor on the right
* `self.cursor_y` - cursor y location in terms of terminal characters
* `self.viewport_width` - Width of the text viewport
        
**Widget Specific Functions**

* `update_height_width()` - Updates the height/width of the textbox. Internal use only
* `set_text(, text)` - Sets the textbox text
* `get()` - Gets text from textbox
* `clear()` - Clears text in textbox
* `move_left()` - Shifts the cursor the the left. Internal use only
* `move_right()` - Shifts the cursor the the right. Internal use only
* `insert_char(key_pressed)` - Inserts char at cursor position. Internal use only
* `jump_to_start()` - Jumps to the start to the textbox. Internal use only
* `jump_to_end()` - Jumps to the end to the textbox. Internal use only
* `erase_char()` - Erases character at textbox cursor. Internal use only

**Usage**

Used for user entering text into CUI. For prompts, it is suggested to use the Textbox popup instead.

**Adding to CUI**
```
add_text_box(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, initial_text = '')
```
**Draw Behavior**

Draws `self.title` above a bordered entry field centered in the grid cell assigned

**Default Keybindings**

* KEY_END - Jumps to the end of the text
* KEY_HOME - Jumps to start of the text
* KEY_LEFT_ARROW - Shifts cursor to left
* KEY_RIGHT_ARROW - Shifts cursor to right
* Letter Keys - writes the appropriate letter to the text
* KEY_BACKSPACE - Erases character in text

### Text Block

**Widget Specific Class Variables**

* `self.text` - text currently in the text box
* `self.cursor_x` - cursor x  location in terms of terminal characters
* `self.cursor_text_pos` - cursor position relative to the text
* `self.cursor_max_left` - maximum terminal position for the cursor on the left
* `self.cursor_max_right` - maximum terminal position for the cursor on the right
* `self.cursor_y` - cursor y location in terms of terminal characters
* `self.viewport_width` - Width of the text viewport
        
**Widget Specific Functions**

* `update_height_width()` - Updates the height/width of the textbox. Internal use only
* `set_text(, text)` - Sets the textbox text
* `get()` - Gets text from textbox
* `clear()` - Clears text in textbox
* `move_left(current_line)` - Shifts the cursor to the  left. Internal use only
* `move_right(current_line)` - Shifts the cursor to the right. Internal use only
* `move_down(current_line)` - Shifts the cursor down. Internal use only
* `move_up(current_line)` - Shifts the cursor up. Internal use only
* `write(text)` - writes text to the textblock
* `insert_char(key_pressed)` - Inserts char at cursor position. Internal use only
* `jump_to_start()` - Jumps to the start to the textbox. Internal use only
* `jump_to_end()` - Jumps to the end to the textbox. Internal use only
* `erase_char()` - Erases character at textbox cursor. Internal use only
* `handle_delete(current_line)` - Handles deleting characters. Internal use only
* `handle_end(current_line)` - handles end key. Internal use only
* `handle_home(current_line)` - handles home key. Internal use only
* `handle_backspace(current_line)` - handles backspace key. Internal use only
* `handle_newline(current_line)` - handles newline key. Internal use only

**Usage**

TextBoxes have two key uses:
* For editing larger blocks of text, such as if you wish to create a CUI text editor (see `snano` example)
* For displaying large amounts of text, such as statuses, logs etc. (see `pyautogit` example)

**Adding to CUI**
```
add_text_block(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, initial_text = '')
```
**Draw Behavior**

Draws `self.title` above a bordered entry box that fills the grid cells.

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