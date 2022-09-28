# py_cui

A python library for intuitively creating CUI/TUI interfaces with pre-built widgets.



#### Classes

 Class  | Doc
-----|-----
 PyCUI | Base CUI class

#### Functions

 Function  | Doc
-----|-----
 fit_text | Fits text to screen size




### fit_text

```python
def fit_text(width: int, text: str, center: bool = False) -> str
```

Fits text to screen size



Helper function to fit text within a given width. Used to fix issue with status/title bar text
being too long


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 width  |  int | width of window in characters
 text  |  str | input text
 center  |  Boolean | flag to center text

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 fitted_text  |  str | text fixed depending on width





## PyCUI

```python
class PyCUI
```

Base CUI class



Main user interface class for py_cui. To create a user interface, you must
first create an instance of this class, and then add cells + widgets to it.


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 cursor_x, cursor_y  |  int | absolute position of the cursor in the CUI
 grid  |  py_cui.grid.Grid | The main layout manager for the CUI
 widgets  |  dict of str - py_cui.widgets.Widget | dict of widget in the grid
 title_bar  |  py_cui.statusbar.StatusBar | a status bar object that gets drawn at the top of the CUI
 status_bar  |  py_cui.statusbar.StatusBar | a status bar object that gets drawn at the bottom of the CUI
 keybindings  |  list of py_cui.keybinding.KeyBinding | list of keybindings to check against in the main CUI loop
 height, width  |  int | height of the terminal in characters, width of terminal in characters
 exit_key  |  key_code | a key code for a key that exits the CUI
 simulated_terminal  |  List[int] | Dimensions for an alternative simulated terminal (used for testing)

#### Methods

 Method  | Doc
-----|-----
 set_refresh_timeout | Sets the CUI auto-refresh timeout to a number of seconds.
 set_on_draw_update_func | Adds a function that is fired during each draw call of the CUI
 set_widget_cycle_key | Assigns a key for automatically cycling through widgets in both focus and overview modes
 set_toggle_live_debug_key |
 enable_logging | Function enables logging for py_cui library
 apply_widget_set | Function that replaces all widgets in a py_cui with those of a different widget set
 create_new_widget_set | Function that is used to create additional widget sets
 start | Function that starts the CUI
 stop | Function that stops the CUI, and fires the callback function.
 run_on_exit | Sets callback function on CUI exit. Must be a no-argument function or lambda function
 set_title | Sets the title bar text
 set_status_bar_text | Sets the status bar text when in overview mode
 _initialize_colors | Function for initialzing curses colors. Called when CUI is first created.
 _initialize_widget_renderer | Function that creates the renderer object that will draw each widget
 toggle_unicode_borders | Function for toggling unicode based border rendering
 set_widget_border_characters | Function that can be used to set arbitrary border characters for drawing widget borders by renderer.
 get_widgets | Function that gets current set of widgets
 add_scroll_menu | Function that adds a new scroll menu to the CUI grid
 add_checkbox_menu | Function that adds a new checkbox menu to the CUI grid
 add_text_box | Function that adds a new text box to the CUI grid
 add_text_block | Function that adds a new text block to the CUI grid
 add_label | Function that adds a new label to the CUI grid
 add_block_label | Function that adds a new block label to the CUI grid
 add_button | Function that adds a new button to the CUI grid
 add_slider | Function that adds a new label to the CUI grid
 forget_widget | Function that is used to destroy or "forget" widgets. Forgotten widgets will no longer be drawn
 get_element_at_position | Returns containing widget for character position
 _get_horizontal_neighbors | Gets all horizontal (left, right) neighbor widgets
 _get_vertical_neighbors | Gets all vertical (up, down) neighbor widgets
 _check_if_neighbor_exists | Function that checks if widget has neighbor in specified cell.
 get_selected_widget | Function that gets currently selected widget
 set_selected_widget | Function that sets the selected widget for the CUI
 lose_focus | Function that forces py_cui out of focus mode.
 move_focus | Moves focus mode to different widget
 _cycle_widgets | Function that is fired if cycle key is pressed to move to next widget
 add_key_command | Function that adds a keybinding to the CUI when in overview mode
 show_message_popup | Shows a message popup
 show_warning_popup | Shows a warning popup
 show_error_popup | Shows an error popup
 show_yes_no_popup | Shows a yes/no popup.
 show_text_box_popup | Shows a textbox popup.
 show_menu_popup | Shows a menu popup.
 show_loading_icon_popup | Shows a loading icon popup
 show_loading_bar_popup | Shows loading bar popup.
 show_form_popup | Shows form popup.
 show_filedialog_popup | Shows form popup.
 increment_loading_bar | Increments progress bar if loading bar popup is open
 stop_loading_popup | Leaves loading state, and closes popup.
 close_popup | Closes the popup, and resets focus
 _refresh_height_width | Function that updates the height and width of the CUI based on terminal window size.
 get_absolute_size | Returns dimensions of CUI
 _draw_widgets | Function that draws all of the widgets to the screen
 _draw_status_bars | Draws status bar and title bar
 _display_window_warning | Function that prints some basic error info if there is an error with the CUI
 _handle_key_presses | Function that handles all main loop key presses.
 _draw | Main CUI draw loop called by start()
 format | Override of base format function. Prints list of current widgets.




### __init__

```python
def __init__(self, num_rows: int, num_cols: int, auto_focus_buttons: bool=True
```

Initializer for PyCUI class







### set_refresh_timeout

```python
def set_refresh_timeout(self, timeout: int)
```

Sets the CUI auto-refresh timeout to a number of seconds.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 timeout  |  int | Number of seconds to wait before refreshing the CUI





### set_on_draw_update_func

```python
def set_on_draw_update_func(self, update_function: Callable[[],Any])
```

Adds a function that is fired during each draw call of the CUI




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 update_function  |  function | A no-argument or lambda function that is fired at the start of each draw call





### set_widget_cycle_key

```python
def set_widget_cycle_key(self, forward_cycle_key: int=None, reverse_cycle_key: int=None) -> None
```

Assigns a key for automatically cycling through widgets in both focus and overview modes




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 widget_cycle_key  |  py_cui.keys.KEY | Key code for key to cycle through widgets





### set_toggle_live_debug_key

```python
def set_toggle_live_debug_key(self, toggle_debug_key: int) -> None
```









### enable_logging

```python
def enable_logging(self, log_file_path: str='py_cui.log', logging_level = logging.DEBUG, live_debug_key: int = py_cui.keys.KEY_CTRL_D) -> None
```

Function enables logging for py_cui library




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 log_file_path  |  str | The target log filepath. Default 'py_cui_log.txt
 logging_level  |  int | Default logging level = logging.DEBUG





### apply_widget_set

```python
def apply_widget_set(self, new_widget_set: py_cui.widget_set.WidgetSet) -> None
```

Function that replaces all widgets in a py_cui with those of a different widget set




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 new_widget_set  |  WidgetSet | The new widget set to switch to

#### Raises

 Error  | Type  | Doc
-----|----------|-----
 Unknown | TypeError | If input is not of type WidgetSet





### create_new_widget_set

```python
def create_new_widget_set(self, num_rows: int, num_cols: int) -> 'py_cui.widget_set.WidgetSet'
```

Function that is used to create additional widget sets



Use this function instead of directly creating widget set object instances, to allow
for logging support.


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 num_rows  |  int | row count for new widget set
 num_cols  |  int | column count for new widget set

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 new_widget_set  |  py_cui.widget_set.WidgetSet | The new widget set object instance





### start

```python
def start(self) -> None
```

Function that starts the CUI







### stop

```python
def stop(self) -> None
```

Function that stops the CUI, and fires the callback function.



Callback must be a no arg method





### run_on_exit

```python
def run_on_exit(self, command: Callable[[],Any])
```

Sets callback function on CUI exit. Must be a no-argument function or lambda function




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 command  |  function | A no-argument or lambda function to be fired on exit





### set_title

```python
def set_title(self, title: str) -> None
```

Sets the title bar text




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 title  |  str | New title for CUI





### set_status_bar_text

```python
def set_status_bar_text(self, text: str) -> None
```

Sets the status bar text when in overview mode




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | Status bar text





### _initialize_colors

```python
def _initialize_colors(self) -> None
```

Function for initialzing curses colors. Called when CUI is first created.







### _initialize_widget_renderer

```python
def _initialize_widget_renderer(self) -> None
```

Function that creates the renderer object that will draw each widget







### toggle_unicode_borders

```python
def toggle_unicode_borders(self) -> None
```

Function for toggling unicode based border rendering







### set_widget_border_characters

```python
def set_widget_border_characters(self, upper_left_corner: str, upper_right_corner: str, lower_left_corner: str, lower_right_corner: str, horizontal: str, vertical: str) -> None
```

Function that can be used to set arbitrary border characters for drawing widget borders by renderer.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 upper_left_corner  |  char | Upper left corner character
 upper_right_corner  |  char | Upper right corner character
 lower_left_corner  |  char | Upper left corner character
 lower_right_corner  |  char | Lower right corner character
 horizontal  |  char | Horizontal border character
 vertical  |  char | Vertical border character





### get_widgets

```python
def get_widgets(self) -> Dict[int,Optional['py_cui.widgets.Widget']]
```

Function that gets current set of widgets




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 widgets  |  dict of int -> widget | dictionary mapping widget IDs to object instances





### add_scroll_menu

```python
def add_scroll_menu(self, title: str, row: int, column: int, row_span: int=1, column_span: int=1, padx: int=1, pady: int=0) -> 'py_cui.widgets.ScrollMenu'
```

Function that adds a new scroll menu to the CUI grid




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 title  |  str | The title of the scroll menu
 row  |  int | The row value, from the top down
 column  |  int | The column value from the top down
 row_span=1  |  int | The number of rows to span accross
 column_span=1  |  int | the number of columns to span accross
 padx=1  |  int | number of padding characters in the x direction
 pady=0  |  int | number of padding characters in the y direction

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 new_scroll_menu  |  ScrollMenu | A reference to the created scroll menu object.





### add_checkbox_menu

```python
def add_checkbox_menu(self, title: str, row: int, column: int, row_span: int=1, column_span: int=1, padx: int=1, pady: int=0, checked_char: str='X') -> 'py_cui.widgets.CheckBoxMenu'
```

Function that adds a new checkbox menu to the CUI grid




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
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
-----|----------|-----
 new_checkbox_menu  |  CheckBoxMenu | A reference to the created checkbox object.





### add_text_box

```python
def add_text_box(self, title: str, row: int, column: int, row_span: int = 1, column_span: int = 1, padx: int = 1, pady: int = 0, initial_text: str = '', password: bool = False) -> 'py_cui.widgets.TextBox'
```

Function that adds a new text box to the CUI grid




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 title  |  str | The title of the textbox
 row  |  int | The row value, from the top down
 column  |  int | The column value from the top down
 row_span=1  |  int | The number of rows to span accross
 column_span=1  |  int | the number of columns to span accross
 padx=1  |  int | number of padding characters in the x direction
 pady=0  |  int | number of padding characters in the y direction
 initial_text=''  |  str | Initial text for the textbox
 password=False  |  bool | Toggle to show '*' instead of characters.

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 new_text_box  |  TextBox | A reference to the created textbox object.





### add_text_block

```python
def add_text_block(self, title: str, row: int, column: int, row_span: int = 1, column_span: int = 1, padx: int = 1, pady: int = 0, initial_text: str = '') -> 'py_cui.widgets.ScrollTextBlock'
```

Function that adds a new text block to the CUI grid




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
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
-----|----------|-----
 new_text_block  |  ScrollTextBlock | A reference to the created textblock object.





### add_label

```python
def add_label(self, title: str, row: int, column: int, row_span: int = 1, column_span: int = 1, padx: int = 1, pady: int = 0) -> 'py_cui.widgets.Label'
```

Function that adds a new label to the CUI grid




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 title  |  str | The title of the label
 row  |  int | The row value, from the top down
 column  |  int | The column value from the top down
 row_span=1  |  int | The number of rows to span accross
 column_span=1  |  int | the number of columns to span accross
 padx=1  |  int | number of padding characters in the x direction
 pady=0  |  int | number of padding characters in the y direction

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 new_label  |  Label | A reference to the created label object.





### add_block_label

```python
def add_block_label(self, title: str, row: int, column: int, row_span: int = 1, column_span: int = 1, padx: int = 1, pady: int = 0, center: bool=True) -> 'py_cui.widgets.BlockLabel'
```

Function that adds a new block label to the CUI grid




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
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
-----|----------|-----
 new_label  |  BlockLabel | A reference to the created block label object.





### add_button

```python
def add_button(self, title: str, row: int, column: int, row_span: int = 1, column_span: int = 1, padx: int = 1, pady: int = 0, command: Callable[[],Any]=None) -> 'py_cui.widgets.Button'
```

Function that adds a new button to the CUI grid




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
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
-----|----------|-----
 new_button  |  Button | A reference to the created button object.





### add_slider

```python
def add_slider(self, title: str, row: int, column: int, row_span: int=1
```

Function that adds a new label to the CUI grid




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 title  |  str | The title of the label
 row  |  int | The row value, from the top down
 column  |  int | The column value from the top down
 row_span=1  |  int | The number of rows to span accross
 column_span=1  |  int | the number of columns to span accross
 padx=1  |  int | number of padding characters in the x direction
 pady=0  |  int | number of padding characters in the y direction
 Unknown | min_val = 0 int | min value of the slider
 Unknown | max_val = 0 int | max value of the slider
 Unknown | step = 0 int | step to incremento or decrement
 Unknown | init_val = 0 int | initial value of the slider

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 new_slider  |  Slider | A reference to the created slider object.





### forget_widget

```python
def forget_widget(self, widget : 'py_cui.widgets.Widget') -> None
```

Function that is used to destroy or "forget" widgets. Forgotten widgets will no longer be drawn




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 widget  |  py_cui.widgets.Widget | Widget to remove from the UI

#### Raises

 Error  | Type  | Doc
-----|----------|-----
 Unknown | TypeError | If input parameter is not of the py_cui widget type
 Unknown | KeyError | If input widget does not exist in the current UI or has already been removed.





### get_element_at_position

```python
def get_element_at_position(self, x: int, y: int) -> Optional['py_cui.ui.UIElement']
```

Returns containing widget for character position




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 x  |  int | Horizontal character position
 y  |  int | Vertical character position, top down

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 in_widget  |  UIElement | Widget or popup that is within the position None if nothing





### _get_horizontal_neighbors

```python
def _get_horizontal_neighbors(self, widget: 'py_cui.widgets.Widget', direction: int) -> Optional[List[int]]
```

Gets all horizontal (left, right) neighbor widgets




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 widget  |  py_cui.widgets.Widget | The currently selected widget
 direction  |  py_cui.keys.KEY* | must be an arrow key value

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 id_list  |  list[] | A list of the neighbor widget ids





### _get_vertical_neighbors

```python
def _get_vertical_neighbors(self, widget: 'py_cui.widgets.Widget', direction: int) -> Optional[List[int]]
```

Gets all vertical (up, down) neighbor widgets




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 widget  |  py_cui.widgets.Widget | The currently selected widget
 direction  |  py_cui.keys.KEY* | must be an arrow key value

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 id_list  |  list[] | A list of the neighbor widget ids





### _check_if_neighbor_exists

```python
def _check_if_neighbor_exists(self, direction: int) -> Optional[int]
```

Function that checks if widget has neighbor in specified cell.



Used for navigating CUI, as arrow keys find the immediate neighbor


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 direction  |  py_cui.keys.KEY_* | The direction in which to search

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 widget_id  |  int | The widget neighbor ID if found, None otherwise





### get_selected_widget

```python
def get_selected_widget(self) -> Optional['py_cui.widgets.Widget']
```

Function that gets currently selected widget




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 selected_widget  |  py_cui.widgets.Widget | Reference to currently selected widget object





### set_selected_widget

```python
def set_selected_widget(self, widget_id: int) -> None
```

Function that sets the selected widget for the CUI




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 widget_id  |  int | the id of the widget to select





### lose_focus

```python
def lose_focus(self) -> None
```

Function that forces py_cui out of focus mode.



After popup is called, focus is lost





### move_focus

```python
def move_focus(self, widget: 'py_cui.widgets.Widget', auto_press_buttons: bool=True) -> None
```

Moves focus mode to different widget




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 widget  |  Widget | The widget object we want to move focus to.





### _cycle_widgets

```python
def _cycle_widgets(self, reverse: bool=False) -> None
```

Function that is fired if cycle key is pressed to move to next widget




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 reverse  |  bool | Default false. If true, cycle widgets in reverse order.





### add_key_command

```python
def add_key_command(self, key: int, command: Callable[[],Any]) -> None
```

Function that adds a keybinding to the CUI when in overview mode




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key  |  py_cui.keys.KEY_* | The key bound to the command
 command  |  Function | A no-arg or lambda function to fire on keypress





### show_message_popup

```python
def show_message_popup(self, title: str, text: str, color: int = WHITE_ON_BLACK) -> None
```

Shows a message popup




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 title  |  str | Message title
 text  |  str | Message text
 color |  int | Popup color with format FOREGOUND_ON_BACKGROUND. See colors module. Default: WHITE_ON_BLACK.





### show_warning_popup

```python
def show_warning_popup(self, title: str, text: str) -> None
```

Shows a warning popup




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 title  |  str | Warning title
 text  |  str | Warning text





### show_error_popup

```python
def show_error_popup(self, title: str, text: str) -> None
```

Shows an error popup




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 title  |  str | Error title
 text  |  str | Error text





### show_yes_no_popup

```python
def show_yes_no_popup(self, title: str, command: Callable[[bool], Any])
```

Shows a yes/no popup.



The 'command' parameter must be a function with a single boolean parameter


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 title  |  str | Message title
 command  |  function | A function taking in a single boolean parameter. Will be fired with True if yes selected, false otherwise





### show_text_box_popup

```python
def show_text_box_popup(self, title: str, command: Callable[[str], Any], password: bool=False)
```

Shows a textbox popup.



The 'command' parameter must be a function with a single string parameter


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 title  |  str | Message title
 command  |  Function | A function with a single string parameter, fired with contents of textbox when enter key pressed
 password=False  |  bool | If true, write characters as '*'





### show_menu_popup

```python
def show_menu_popup(self, title: str, menu_items: List[str], command: Callable[[str], Any], run_command_if_none: bool=False)
```

Shows a menu popup.



The 'command' parameter must be a function with a single string parameter


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 title  |  str | menu title
 menu_items  |  list of str | A list of menu items
 command  |  Function | A function taking in a single string argument. Fired with selected menu item when ENTER pressed.
 run_command_if_none=False  |  bool | If True, will run command passing in None if no menu item selected.





### show_loading_icon_popup

```python
def show_loading_icon_popup(self, title: str, message: str, callback: Callable[[],Any]=None)
```

Shows a loading icon popup




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 title  |  str | Message title
 message  |  str | Message text. Will show as '$message...'
 callback=None  |  Function | If not none, fired after loading is completed. Must be a no-arg function





### show_loading_bar_popup

```python
def show_loading_bar_popup(self, title: str, num_items: List[int], callback: Callable[[],Any]=None) -> None
```

Shows loading bar popup.



Use 'increment_loading_bar' to show progress


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 title  |  str | Message title
 num_items  |  int | Number of items to iterate through for loading
 callback=None  |  Function | If not none, fired after loading is completed. Must be a no-arg function





### show_form_popup

```python
def show_form_popup(self, title: str, fields: List[str], passwd_fields: List[str]=[], required: List[str]=[], callback: Callable[[],Any]=None) -> None
```

Shows form popup.



Used for inputting several fields worth of values


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 title  |  str | Message title
 fields  |  List[str] | Names of each individual field
 passwd_fields  |  List[str] | Field names that should have characters hidden
 required  |  List[str] | Fields that are required before submission
 callback=None  |  Function | If not none, fired after loading is completed. Must be a no-arg function





### show_filedialog_popup

```python
def show_filedialog_popup(self, popup_type: str='openfile', initial_dir: str ='.', callback: Callable[[],Any]=None, ascii_icons: bool=True, limit_extensions: List[str]=[]) -> None
```

Shows form popup.



Used for inputting several fields worth of values


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 popup_type  |  str | Type of filedialog popup - either openfile, opendir, or saveas
 initial_dir  |  os.PathLike | Path to directory in which to open the file dialog, default "."
 callback=None  |  Callable | If not none, fired after loading is completed. Must be a no-arg function, default=None
 ascii_icons  |  bool | Compatibility option - use ascii icons instead of unicode file/folder icons, default True
 limit_extensions  |  List[str] | Only show files with extensions in this list if not empty. Default, []





### increment_loading_bar

```python
def increment_loading_bar(self) -> None
```

Increments progress bar if loading bar popup is open







### stop_loading_popup

```python
def stop_loading_popup(self) -> None
```

Leaves loading state, and closes popup.



Must be called by user to escape loading.





### close_popup

```python
def close_popup(self) -> None
```

Closes the popup, and resets focus







### _refresh_height_width

```python
def _refresh_height_width(self) -> None
```

Function that updates the height and width of the CUI based on terminal window size.


```
if self._simulated_terminal is None:
if self._stdscr is None:
term_size = shutil.get_terminal_size()
height  = term_size.lines
width   = term_size.columns
else:
# Use curses termsize when possible to fix resize bug on windows.
height, width = self._stdscr.getmaxyx()
else:
height  = self._simulated_terminal[0]
width   = self._simulated_terminal[1]

height  = height - self.title_bar.get_height() - self.status_bar.get_height() - 2

self._logger.debug(f'Resizing CUI to new dimensions {height} by {width}')

self._height = height
self._width  = width
self._grid.update_grid_height_width(self._height, self._width)
for widget_id in self.get_widgets().keys():
widget = self.get_widgets()[widget_id] #using temp variable, for mypy
if widget is not None:
widget.update_height_width()
if self._popup is not None:
self._popup.update_height_width()
if self._logger._live_debug_element is not None:
self._logger._live_debug_element.update_height_width()
```







### get_absolute_size

```python
def get_absolute_size(self) -> Tuple[int,int]:
```

Returns dimensions of CUI




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 height, width  |  int | The dimensions of drawable CUI space in characters





### _draw_widgets

```python
def _draw_widgets(self) -> None
```

Function that draws all of the widgets to the screen







### _draw_status_bars

```python
def _draw_status_bars(self, stdscr, height: int, width: int) -> None
```

Draws status bar and title bar




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 stdscr  |  curses Standard cursor | The cursor used to draw the status bar
 height  |  int | Window height in terminal characters
 width  |  int | Window width in terminal characters





### _display_window_warning

```python
def _display_window_warning(self, stdscr, error_info: str) -> None
```

Function that prints some basic error info if there is an error with the CUI




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 stdscr  |  curses Standard cursor | The cursor used to draw the warning
 error_info  |  str | The information regarding the error.





### _handle_key_presses

```python
def _handle_key_presses(self, key_pressed: int) -> None
```

Function that handles all main loop key presses.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  py_cui.keys.KEY_* | The key being pressed





### _draw

```python
def _draw(self, stdscr) -> None
```

Main CUI draw loop called by start()




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 stdscr  |  curses Standard screen | The screen buffer used for drawing CUI elements





### __format__

```python
def __format__(self, fmt)
```

Override of base format function. Prints list of current widgets.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 fmt  |  Format | The format to override








