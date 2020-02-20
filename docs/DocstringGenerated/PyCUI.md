# py_cui

A python library for creating command line based user interfaces.



@author:    Jakub Wlodek  
@created:   12-Aug-2019




### fit_text

```python
def fit_text(width, text, center=False)
```

Fits text to screen size



Helper function to fit text within a given width. Used to fix issue with status/title bar text
being too long


#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 width  |  int | width of window in characters
 text  |  str | input text
 center  |  Boolean | flag to center text

#### Returns

 Return Variable  | Type  | Doc
-----|----------|----------|-----
 fitted_text  |  str | text fixed depending on width





## PyCUI

```python
class PyCUI
```

Base CUI class



Main user interface class for py_cui. To create a user interface, you must first
create an instance of this class, and then add cells + widgets to it.


#### Attributes

 Attribute  | Type  | Doc
-----|----------|----------|-----
 cursor_x, cursor_y  |  int | absolute position of the cursor in the CUI
 grid  |  py_cui.grid.Grid | The main layout manager for the CUI
 widgets  |  dict of str - py_cui.widgets.Widget | dict of widget in the grid
 title_bar  |  py_cui.statusbar.StatusBar | a status bar object that gets drawn at the top of the CUI
 status_bar  |  py_cui.statusbar.StatusBar | a status bar object that gets drawn at the bottom of the CUI
 keybindings  |  list of py_cui.keybinding.KeyBinding | list of keybindings to check against in the main CUI loop
 height, width  |  int | height of the terminal in characters, width of terminal in characters
 exit_key  |  key_code | a key code for a key that exits the CUI

#### Methods

 Method  | Doc
-----|----------|-----
 get_widget_set | Gets widget set object from current widgets.
 apply_widget_set | Function that replaces all widgets in a py_cui with those of a different widget set
 start | starts the CUI once all of the widgets have been added
 stop | Function that stops CUI and runs the run_on_exit function if set.
 run_on_exit | Sets callback function on CUI exit. Must be a no-argument function or lambda function
 add_scroll_menu | Function that adds a new scroll menu to the CUI grid
 add_checkbox_menu | Function that adds a new checkbox menu to the CUI grid
 add_text_box | Function that adds a new text box to the CUI grid
 add_text_block | Function that adds a new text block to the CUI grid
 add_label | Function that adds a new label to the CUI grid
 add_block_label | Function that adds a new block label to the CUI grid
 add_button | Function that adds a new button to the CUI grid
 add_key_command | Function that adds a keybinding to the CUI when in overview mode
 show_message_popup | Shows a message popup
 show_warning_popup | Shows a warning popup
 show_error_popup | Shows an error popup
 show_yes_no_popup | Shows a yes/no popup.
 show_text_box_popup | Shows a textbox popup.
 show_menu_popup | Shows a menu popup.
 show_loading_icon_popup | Shows a loading icon popup
 show_loading_bar_popup | Shows loading bar popup.
 increment_loading_bar | Increments progress bar if loading bar popup is open
 stop_loading_popup | Leaves loading state, and closes popup.
 close_popup | Closes the popup, and resets focus
 refresh_height_width | Function that updates the height and width of the CUI based on terminal window size
 draw_widgets | Function that draws all of the widgets to the screen
 draw_status_bars | Draws status bar and title bar
 display_window_warning | Function that prints some basic error info if there is an error with the CUI
 handle_key_presses | Function that handles all main loop key presses.
 draw | Main CUI draw loop called by start()
 set_title | Sets the title bar text
 set_status_bar_text | Sets the status bar text when in overview mode
 initialize_colors | Function for initialzing curses colors. Called when CUI is first created.
 initialize_widget_renderer | Function that creates the renderer object that will draw each widget
 check_if_neighbor_exists | Function that checks if widget has neighbor in specified cell.
 set_selected_widget | Function that sets the selected cell for the CUI
 get_widget_id | Function for grabbing widget ID
 lose_focus | Function that forces py_cui out of focus mode.
 move_focus | Moves focus mode to different widget
 add_status_bar | function that adds a status bar widget to the CUI




### __init__

```python
def __init__(self, num_rows, num_cols, auto_focus_buttons=True, exit_key=py_cui.keys.KEY_Q_LOWER)
```

Constructor for PyCUI class







### get_widget_set

```python
def get_widget_set(self)
```

Gets widget set object from current widgets.




#### Returns

 Return Variable  | Type  | Doc
-----|----------|----------|-----
 new_widget_set  |  py_cui.widget_set.WidgetSet | Widget set collected from widgets currently added to the py_cui





### apply_widget_set

```python
def apply_widget_set(self, new_widget_set)
```

Function that replaces all widgets in a py_cui with those of a different widget set




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 new_widget_set  |  WidgetSet | The new widget set to switch to
 Raises | ------
 TypeError | If input is not of type widget set





### start

```python
def start(self)
```

Function that starts the CUI







### stop

```python
def stop(self)
```

Function that stops the CUI, and fires the callback function.



Callback must be a no arg method





### run_on_exit

```python
def run_on_exit(self, command)
```

Sets callback function on CUI exit. Must be a no-argument function or lambda function




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 command  |  function | A no-argument or lambda function to be fired on exit





### set_title

```python
def set_title(self, title)
```

Sets the title bar text




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 title  |  str | New title for CUI





### set_status_bar_text

```python
def set_status_bar_text(self, text)
```

Sets the status bar text when in overview mode




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 text  |  str | Status bar text





### initialize_colors

```python
def initialize_colors(self)
```

Function for initialzing curses colors. Called when CUI is first created.







### initialize_widget_renderer

```python
def initialize_widget_renderer(self)
```

Function that creates the renderer object that will draw each widget







### add_scroll_menu

```python
def add_scroll_menu(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0)
```

Function that adds a new scroll menu to the CUI grid




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 title  |  str | The title of the scroll menu
 row  |  int | The row value, from the top down
 column  |  int | The column value from the top down
 row_span=1  |  int | The number of rows to span accross
 column_span=1  |  int | the number of columns to span accross
 padx=1  |  int | number of padding characters in the x direction
 pady=0  |  int | number of padding characters in the y direction

#### Returns

 Return Variable  | Type  | Doc
-----|----------|----------|-----
 new_scroll_menu  |  ScrollMenu | A reference to the created scroll menu object.





### add_checkbox_menu

```python
def add_checkbox_menu(self, title, row, column, row_span=1, column_span=1, padx=1, pady=0, checked_char='X')
```

Function that adds a new checkbox menu to the CUI grid




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 title  |  str | The title of the checkbox
 row  |  int | The row value, from the top down
 column  |  int | The column value from the top down
 row_span=1  |  int | The number of rows to span accross
 column_span=1  |  int | the number of columns to span accross
 padx=1  |  int | number of padding characters in the x direction
 pady=0  |  int | number of padding characters in the y direction
 checked_char='X'  |  char | The character used to mark 'Checked' items

#### Returns

 Return Variable  | Type  | Doc
-----|----------|----------|-----
 new_checkbox_menu  |  CheckBoxMenu | A reference to the created checkbox object.





### add_text_box

```python
def add_text_box(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, initial_text = '')
```

Function that adds a new text box to the CUI grid




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 title  |  str | The title of the textbox
 row  |  int | The row value, from the top down
 column  |  int | The column value from the top down
 row_span=1  |  int | The number of rows to span accross
 column_span=1  |  int | the number of columns to span accross
 padx=1  |  int | number of padding characters in the x direction
 pady=0  |  int | number of padding characters in the y direction
 initial_text=''  |  str | Initial text for the textbox

#### Returns

 Return Variable  | Type  | Doc
-----|----------|----------|-----
 new_text_box  |  TextBox | A reference to the created textbox object.





### add_text_block

```python
def add_text_block(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, initial_text = '')
```

Function that adds a new text block to the CUI grid




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 title  |  str | The title of the text block
 row  |  int | The row value, from the top down
 column  |  int | The column value from the top down
 row_span=1  |  int | The number of rows to span accross
 column_span=1  |  int | the number of columns to span accross
 padx=1  |  int | number of padding characters in the x direction
 pady=0  |  int | number of padding characters in the y direction
 initial_text=''  |  str | Initial text for the text block

#### Returns

 Return Variable  | Type  | Doc
-----|----------|----------|-----
 new_text_block  |  ScrollTextBlock | A reference to the created textblock object.





### add_label

```python
def add_label(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0)
```

Function that adds a new label to the CUI grid




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 title  |  str | The title of the label
 row  |  int | The row value, from the top down
 column  |  int | The column value from the top down
 row_span=1  |  int | The number of rows to span accross
 column_span=1  |  int | the number of columns to span accross
 padx=1  |  int | number of padding characters in the x direction
 pady=0  |  int | number of padding characters in the y direction

#### Returns

 Return Variable  | Type  | Doc
-----|----------|----------|-----
 new_label  |  Label | A reference to the created label object.





### add_block_label

```python
def add_block_label(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, center=True)
```

Function that adds a new block label to the CUI grid




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 title  |  str | The title of the block label
 row  |  int | The row value, from the top down
 column  |  int | The column value from the top down
 row_span=1  |  int | The number of rows to span accross
 column_span=1  |  int | the number of columns to span accross
 padx=1  |  int | number of padding characters in the x direction
 pady=0  |  int | number of padding characters in the y direction
 center  |  bool | flag to tell label to be centered or left-aligned.

#### Returns

 Return Variable  | Type  | Doc
-----|----------|----------|-----
 new_label  |  BlockLabel | A reference to the created block label object.





### add_button

```python
def add_button(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, command=None)
```

Function that adds a new button to the CUI grid




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 title  |  str | The title of the button
 row  |  int | The row value, from the top down
 column  |  int | The column value from the top down
 row_span=1  |  int | The number of rows to span accross
 column_span=1  |  int | the number of columns to span accross
 padx=1  |  int | number of padding characters in the x direction
 pady=0  |  int | number of padding characters in the y direction
 command=None  |  Function | A no-argument or lambda function to fire on button press.

#### Returns

 Return Variable  | Type  | Doc
-----|----------|----------|-----
 new_button  |  Button | A reference to the created button object.





### check_if_neighbor_exists

```python
def check_if_neighbor_exists(self, row, column, row_span, col_span, direction)
```

Function that checks if widget has neighbor in specified cell.



Used for navigating CUI, as arrow keys find the immediate neighbor


#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 row  |  int | row of current widget
 column  |  int | column of current widget
 row_span  |  int | row span of current widget
 col_span  |  int | column span of current widget
 direction  |  py_cui.keys.KEY_* | The direction in which to search

#### Returns

 Return Variable  | Type  | Doc
-----|----------|----------|-----
 widget_id  |  str | The widget neighbor ID if found, None otherwise





### set_selected_widget

```python
def set_selected_widget(self, widget_id)
```

Function that sets the selected cell for the CUI




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 widget_id  |  str | the id of the widget





### get_widget_id

```python
def get_widget_id(self, widget)
```

Function for grabbing widget ID




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 widget  |  Widget | The widget object we wish to get an ID from

#### Returns

 Return Variable  | Type  | Doc
-----|----------|----------|-----
 widget_id  |  str | The id if found, None otherwise





### lose_focus

```python
def lose_focus(self)
```

Function that forces py_cui out of focus mode.



After popup is called, focus is lost





### move_focus

```python
def move_focus(self, widget)
```

Moves focus mode to different widget




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 widget  |  Widget | The widget object we want to move focus to.





### add_key_command

```python
def add_key_command(self, key, command)
```

Function that adds a keybinding to the CUI when in overview mode




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 key  |  py_cui.keys.KEY_* | The key bound to the command
 command  |  Function | A no-arg or lambda function to fire on keypress





### show_message_popup

```python
def show_message_popup(self, title, text)
```

Shows a message popup




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 title  |  str | Message title
 text  |  str | Message text





### show_warning_popup

```python
def show_warning_popup(self, title, text)
```

Shows a warning popup




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 title  |  str | Warning title
 text  |  str | Warning text





### show_error_popup

```python
def show_error_popup(self, title, text)
```

Shows an error popup




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 title  |  str | Error title
 text  |  str | Error text





### show_yes_no_popup

```python
def show_yes_no_popup(self, title, command)
```

Shows a yes/no popup.



The 'command' parameter must be a function with a single boolean parameter


#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 title  |  str | Message title
 command  |  function | A function taking in a single boolean parameter. Will be fired with True if yes selected, false otherwise





### show_text_box_popup

```python
def show_text_box_popup(self, title, command, password=False)
```

Shows a textbox popup.



The 'command' parameter must be a function with a single string parameter


#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 title  |  str | Message title
 command  |  Function | A function with a single string parameter, fired with contents of textbox when enter key pressed
 password=False  |  bool | If true, write characters as '*'





### show_menu_popup

```python
def show_menu_popup(self, title, menu_items, command, run_command_if_none=False)
```

Shows a menu popup.



The 'command' parameter must be a function with a single string parameter


#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 title  |  str | menu title
 menu_items  |  list of str | A list of menu items
 command  |  Function | A function taking in a single string argument. Fired with selected menu item when ENTER pressed.
 run_command_if_none=False  |  bool | If True, will run command passing in None if no menu item selected.





### show_loading_icon_popup

```python
def show_loading_icon_popup(self, title, message, callback=None)
```

Shows a loading icon popup




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 title  |  str | Message title
 message  |  str | Message text. Will show as '$message...'
 callback=None  |  Function | If not none, fired after loading is completed. Must be a no-arg function





### show_loading_bar_popup

```python
def show_loading_bar_popup(self, title, num_items, callback=None)
```

Shows loading bar popup.



Use 'increment_loading_bar' to show progress


#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 title  |  str | Message title
 num_items  |  int | Number of items to iterate through for loading
 callback=None  |  Function | If not none, fired after loading is completed. Must be a no-arg function





### increment_loading_bar

```python
def increment_loading_bar(self)
```

Increments progress bar if loading bar popup is open







### stop_loading_popup

```python
def stop_loading_popup(self)
```

Leaves loading state, and closes popup.



Must be called by user to escape loading.





### close_popup

```python
def close_popup(self)
```

Closes the popup, and resets focus







### refresh_height_width

```python
def refresh_height_width(self, height, width)
```

Function that updates the height and width of the CUI based on terminal window size




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 height  |  int | Window height in terminal characters
 width  |  int | Window width in terminal characters





### draw_widgets

```python
def draw_widgets(self)
```

Function that draws all of the widgets to the screen







### draw_status_bars

```python
def draw_status_bars(self, stdscr, height, width)
```

Draws status bar and title bar




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 stdscr  |  curses Standard cursor | The cursor used to draw the status bar
 height  |  int | Window height in terminal characters
 width  |  int | Window width in terminal characters





### display_window_warning

```python
def display_window_warning(self, stdscr, error_info)
```

Function that prints some basic error info if there is an error with the CUI




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 stdscr  |  curses Standard cursor | The cursor used to draw the warning
 error_info  |  str | The information regarding the error.





### handle_key_presses

```python
def handle_key_presses(self, key_pressed)
```

Function that handles all main loop key presses.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 key_pressed  |  py_cui.keys.KEY_* | The key being pressed





### draw

```python
def draw(self, stdscr)
```

Main CUI draw loop called by start()




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 stdscr  |  curses Standard cursor | The cursor used to draw the CUI





### __format__

```python
def __format__(self, fmt)
```

Override of base format function. Prints list of current widgets.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 fmt  |  Format | The format to override








