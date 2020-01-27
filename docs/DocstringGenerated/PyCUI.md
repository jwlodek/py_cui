# A python library for creating command line based user interfaces


@author:Jakub Wlodek
@created: 12-Aug-2019


# PyCUI 

``` python 
 class PyCUI 
```

Base CUI clas.

Main user interface class for py_cui. To create a user interface, you must first
create an instance of this class, and then add cells + widgets to it.

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     cursor_x, cursor_y | int |         absolute position of the cursor in the CUI | 
|     grid | py_cui.grid.Grid |         The main layout manager for the CUI | 
|     widgets | dict of str - py_cui.widgets.Widget |         dict of widget in the grid | 
|     title_bar | py_cui.statusbar.StatusBar |         a status bar object that gets drawn at the top of the CUI | 
|     status_bar | py_cui.statusbar.StatusBar |         a status bar object that gets drawn at the bottom of the CUI | 
|     keybindings | list of py_cui.keybinding.KeyBinding |         list of keybindings to check against in the main CUI loop | 
|     height, width | int |         height of the terminal in characters, width of terminal in characters | 
|     exit_key | key_code |         a key code for a key that exits the CUI | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| get_widget_set | Gets widget set object from current widgets. | 
| apply_widget_set | Function that replaces all widgets in a py_cui with those of a different widget se. | 
| start | Function that starts the CU. | 
| stop | Function that stops the CUI, and fires the callback function.. | 
| run_on_exit | Sets callback function on CUI exit. Must be a no-argument function or lambda functio. | 
| set_title | Sets the title bar tex. | 
| set_status_bar_text | Sets the status bar text when in overview mod. | 
| initialize_colors | Function for initialzing curses colors. Called when CUI is first created. | 
| initialize_widget_renderer | Function that creates the renderer object that will draw each widge. | 
| add_scroll_menu | Function that adds a new scroll menu to the CUI gri. | 
| add_checkbox_menu | Function that adds a new checkbox menu to the CUI gri. | 
| add_text_box | Function that adds a new text box to the CUI gri. | 
| add_text_block | Function that adds a new text block to the CUI gri. | 
| add_label | Function that adds a new label to the CUI gri. | 
| add_block_label | Function that adds a new block label to the CUI gri. | 
| add_button | Function that adds a new button to the CUI gri. | 
| check_if_neighbor_exists | Function that checks if widget has neighbor in specified cell.. | 
| set_selected_widget | Function that sets the selected cell for the CU. | 
| get_widget_id | Function for grabbing widget I. | 
| lose_focus | Function that forces py_cui out of focus mode. | 
| move_focus | Moves focus mode to different widge. | 
| add_key_command | Function that adds a keybinding to the CUI when in overview mod. | 
| show_message_popup | Shows a message popu. | 
| show_warning_popup | Shows a warning popu. | 
| show_error_popup | Shows an error popu. | 
| show_yes_no_popup | Shows a yes/no popup. | 
| show_text_box_popup | Shows a textbox popup. | 
| show_menu_popup | Shows a menu popup. | 
| show_loading_icon_popup | Shows a loading icon popu. | 
| show_loading_bar_popup | Shows loading bar popup. | 
| increment_loading_bar | Increments progress bar if loading bar popup is ope. | 
| stop_loading_popup | Leaves loading state, and closes popup. | 
| close_popup | Closes the popup, and resets focu. | 
| refresh_height_width | Function that updates the height and width of the CUI based on terminal window siz. | 
| draw_widgets | Function that draws all of the widgets to the scree. | 
| draw_status_bars | Draws status bar and title ba. | 
| display_window_warning | Function that prints some basic error info if there is an error with the CU. | 
| handle_key_presses | Function that handles all main loop key presses. | 
| draw | Main CUI draw loop called by start(. | 
| __format__ | Override of base format function. Prints list of current widgets. | 
 
 

### get_widget_set

``` python 
    get_widget_set() 
```


Gets widget set object from current widgets.

| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         new_widget_set | py_cui.widget_set.WidgetSet |             Widget set collected from widgets currently added to the py_cui | 


### apply_widget_set

``` python 
    apply_widget_set(new_widget_set) 
```


Function that replaces all widgets in a py_cui with those of a different widget se.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         new_widget_set | WidgetSet |             The new widget set to switch to | 


### start

``` python 
    start() 
```


Function that starts the CU.

### stop

``` python 
    stop() 
```


Function that stops the CUI, and fires the callback function..


Callback must be a no arg method

### run_on_exit

``` python 
    run_on_exit(command) 
```


Sets callback function on CUI exit. Must be a no-argument function or lambda functio.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         command | function |             A no-argument or lambda function to be fired on exit | 


### set_title

``` python 
    set_title(title) 
```


Sets the title bar tex.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         title | str |             New title for CUI | 


### set_status_bar_text

``` python 
    set_status_bar_text(text) 
```


Sets the status bar text when in overview mod.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         text | str |             Status bar text | 


### initialize_colors

``` python 
    initialize_colors() 
```


Function for initialzing curses colors. Called when CUI is first created.

### initialize_widget_renderer

``` python 
    initialize_widget_renderer() 
```


Function that creates the renderer object that will draw each widge.

### add_scroll_menu

``` python 
    add_scroll_menu(title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0) 
```


Function that adds a new scroll menu to the CUI gri.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         title | str |             The title of the scroll menu | 
|         row | int |             The row value, from the top down | 
|         column | int |             The column value from the top down | 
|         row_span=1 | int |             The number of rows to span accross | 
|         column_span=1 | int |             the number of columns to span accross | 
|         padx=1 | int |             number of padding characters in the x direction | 
|         pady=0 | int |             number of padding characters in the y direction | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         new_scroll_menu | ScrollMenu |             A reference to the created scroll menu object. | 


### add_checkbox_menu

``` python 
    add_checkbox_menu(title, row, column, row_span=1, column_span=1, padx=1, pady=0, checked_char='X') 
```


Function that adds a new checkbox menu to the CUI gri.



| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         title | str |             The title of the checkbox | 
|         row | int |             The row value, from the top down | 
|         column | int |             The column value from the top down | 
|         row_span=1 | int |             The number of rows to span accross | 
|         column_span=1 | int |             the number of columns to span accross | 
|         padx=1 | int |             number of padding characters in the x direction | 
|         pady=0 | int |             number of padding characters in the y direction | 
|         checked_char='X' | char |             The character used to mark 'Checked' items | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         new_checkbox_menu | CheckBoxMenu |             A reference to the created checkbox object. | 


### add_text_box

``` python 
    add_text_box(title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, initial_text = '') 
```


Function that adds a new text box to the CUI gri.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         title | str |             The title of the textbox | 
|         row | int |             The row value, from the top down | 
|         column | int |             The column value from the top down | 
|         row_span=1 | int |             The number of rows to span accross | 
|         column_span=1 | int |             the number of columns to span accross | 
|         padx=1 | int |             number of padding characters in the x direction | 
|         pady=0 | int |             number of padding characters in the y direction | 
|         initial_text='' | str |             Initial text for the textbox | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         new_text_box | TextBox |             A reference to the created textbox object. | 


### add_text_block

``` python 
    add_text_block(title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, initial_text = '') 
```


Function that adds a new text block to the CUI gri.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         title | str |             The title of the text block | 
|         row | int |             The row value, from the top down | 
|         column | int |             The column value from the top down | 
|         row_span=1 | int |             The number of rows to span accross | 
|         column_span=1 | int |             the number of columns to span accross | 
|         padx=1 | int |             number of padding characters in the x direction | 
|         pady=0 | int |             number of padding characters in the y direction | 
|         initial_text='' | str |             Initial text for the text block | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         new_text_block | ScrollTextBlock |             A reference to the created textblock object. | 


### add_label

``` python 
    add_label(title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0) 
```


Function that adds a new label to the CUI gri.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         title | str |             The title of the label | 
|         row | int |             The row value, from the top down | 
|         column | int |             The column value from the top down | 
|         row_span=1 | int |             The number of rows to span accross | 
|         column_span=1 | int |             the number of columns to span accross | 
|         padx=1 | int |             number of padding characters in the x direction | 
|         pady=0 | int |             number of padding characters in the y direction | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         new_label | Label |             A reference to the created label object. | 


### add_block_label

``` python 
    add_block_label(title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, center=True) 
```


Function that adds a new block label to the CUI gri.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         title | str |             The title of the block label | 
|         row | int |             The row value, from the top down | 
|         column | int |             The column value from the top down | 
|         row_span=1 | int |             The number of rows to span accross | 
|         column_span=1 | int |             the number of columns to span accross | 
|         padx=1 | int |             number of padding characters in the x direction | 
|         pady=0 | int |             number of padding characters in the y direction | 
|         center | bool |             flag to tell label to be centered or left-aligned. | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         new_label | BlockLabel |             A reference to the created block label object. | 


### add_button

``` python 
    add_button(title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0, command=None) 
```


Function that adds a new button to the CUI gri.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         title | str |             The title of the button | 
|         row | int |             The row value, from the top down | 
|         column | int |             The column value from the top down | 
|         row_span=1 | int |             The number of rows to span accross | 
|         column_span=1 | int |             the number of columns to span accross | 
|         padx=1 | int |             number of padding characters in the x direction | 
|         pady=0 | int |             number of padding characters in the y direction | 
|         command=None | Function |             A no-argument or lambda function to fire on button press. | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         new_button | Button |             A reference to the created button object. | 


### check_if_neighbor_exists

``` python 
    check_if_neighbor_exists(row, column, row_span, col_span, direction) 
```


Function that checks if widget has neighbor in specified cell..


Used for navigating CUI, as arrow keys find the immediate neighbor

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         row | int |             row of current widget | 
|         column | int |             column of current widget | 
|         row_span | int |             row span of current widget | 
|         col_span | int |             column span of current widget | 
|         direction | py_cui.keys.KEY_* |             The direction in which to search | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         widget_id | str |             The widget neighbor ID if found, None otherwise | 


### set_selected_widget

``` python 
    set_selected_widget(widget_id) 
```


Function that sets the selected cell for the CU.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         widget_id | str |             the id of the widget | 


### get_widget_id

``` python 
    get_widget_id(widget) 
```


Function for grabbing widget I.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         widget | Widget |             The widget object we wish to get an ID from         | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         widget_id | str |             The id if found, None otherwise | 


### lose_focus

``` python 
    lose_focus() 
```


Function that forces py_cui out of focus mode.


After popup is called, focus is lost

### move_focus

``` python 
    move_focus(widget) 
```


Moves focus mode to different widge.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         widget | Widget |             The widget object we want to move focus to. | 


### add_key_command

``` python 
    add_key_command(key, command) 
```


Function that adds a keybinding to the CUI when in overview mod.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         key | py_cui.keys.KEY_* |             The key bound to the command | 
|         command | Function |             A no-arg or lambda function to fire on keypress | 


### show_message_popup

``` python 
    show_message_popup(title, text) 
```


Shows a message popu.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         title | str |             Message title | 
|         text | str |             Message text | 


### show_warning_popup

``` python 
    show_warning_popup(title, text) 
```


Shows a warning popu.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         title | str |             Warning title | 
|         text | str |             Warning text | 


### show_error_popup

``` python 
    show_error_popup(title, text) 
```


Shows an error popu.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         title | str |             Error title | 
|         text | str |             Error text | 


### show_yes_no_popup

``` python 
    show_yes_no_popup(title, command) 
```


Shows a yes/no popup.


The 'command' parameter must be a function with a single boolean parameter

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         title | str |             Message title | 
|         command | function |             A function taking in a single boolean parameter. Will be fired with True if yes selected, false otherwise | 


### show_text_box_popup

``` python 
    show_text_box_popup(title, command, password=False) 
```


Shows a textbox popup.


The 'command' parameter must be a function with a single string parameter

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         title | str |             Message title | 
|         command | Function |             A function with a single string parameter, fired with contents of textbox when enter key pressed | 
|         password=False | bool |             If true, write characters as '*' | 


### show_menu_popup

``` python 
    show_menu_popup(title, menu_items, command, run_command_if_none=False) 
```


Shows a menu popup.


The 'command' parameter must be a function with a single string parameter

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         title | str |             menu title | 
|         menu_items | list of str |             A list of menu items | 
|         command | Function |             A function taking in a single string argument. Fired with selected menu item when ENTER pressed. | 
|         run_command_if_none=False | bool |             If True, will run command passing in None if no menu item selected. | 


### show_loading_icon_popup

``` python 
    show_loading_icon_popup(title, message, callback=None) 
```


Shows a loading icon popu.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         title | str |             Message title | 
|         message | str |             Message text. Will show as '$message...' | 
|         callback=None | Function |             If not none, fired after loading is completed. Must be a no-arg function | 


### show_loading_bar_popup

``` python 
    show_loading_bar_popup(title, num_items, callback=None) 
```


Shows loading bar popup.


Use 'increment_loading_bar' to show progress

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         title | str |             Message title | 
|         num_items | int |             Number of items to iterate through for loading | 
|         callback=None | Function |             If not none, fired after loading is completed. Must be a no-arg function | 


### increment_loading_bar

``` python 
    increment_loading_bar() 
```


Increments progress bar if loading bar popup is ope.

### stop_loading_popup

``` python 
    stop_loading_popup() 
```


Leaves loading state, and closes popup.


Must be called by user to escape loading.

### close_popup

``` python 
    close_popup() 
```


Closes the popup, and resets focu.

### refresh_height_width

``` python 
    refresh_height_width(height, width) 
```


Function that updates the height and width of the CUI based on terminal window siz.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         height | int |             Window height in terminal characters | 
|         width | int |             Window width in terminal characters | 


### draw_widgets

``` python 
    draw_widgets() 
```


Function that draws all of the widgets to the scree.

### draw_status_bars

``` python 
    draw_status_bars(stdscr, height, width) 
```


Draws status bar and title ba.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         stdscr | curses Standard cursor |             The cursor used to draw the status bar | 
|         height | int |             Window height in terminal characters | 
|         width | int |             Window width in terminal characters | 


### display_window_warning

``` python 
    display_window_warning(stdscr, error_info) 
```


Function that prints some basic error info if there is an error with the CU.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         stdscr | curses Standard cursor |             The cursor used to draw the warning | 
|         error_info | str |             The information regarding the error. | 


### handle_key_presses

``` python 
    handle_key_presses(key_pressed) 
```


Function that handles all main loop key presses.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         key_pressed | py_cui.keys.KEY_* |             The key being pressed | 


### draw

``` python 
    draw(stdscr) 
```


Main CUI draw loop called by start(.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         stdscr | curses Standard cursor |             The cursor used to draw the CUI | 


### __format__

``` python 
    __format__(fmt) 
```


Override of base format function. Prints list of current widgets.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         fmt | Format |             The format to override | 
