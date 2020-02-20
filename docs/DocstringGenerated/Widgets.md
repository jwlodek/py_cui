# widgets

File contatining all core widget classes for py_cui.



Widgets are the basic building blocks of a user interface made with py_cui. 
This file contains classes for:

* Base Widget class
* Label
* Block Label
* Scroll Menu
* Checkbox Menu
* Button
* TextBox
* Text Block

Additional widgets should be added in as additional_widgets/$WIDGET_NAME.py, importing this
file and extending the base Widget class, or if appropriate one of the other core widgets.

@author:    Jakub Wlodek  
@created:   12-Aug-2019




## Widget

```python
class Widget
```

Top Level Widget Base Class



Extended by all widgets. Contains base classes for handling key presses, drawing,
and setting status bar text.


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 id  |  int | Id of the widget
 title  |  str | Widget title
 grid  |  py_cui.grid.Grid | The parent grid object of the widget
 renderer  |  py_cui.renderer.Renderer | The renderer object that draws the widget
 row, column  |  int | row and column position of the widget
 row_span, column_span  |  int | number of rows or columns spanned by the widget
 padx, pady  |  int | Padding size in terminal characters
 start_x, start_y  |  int | The position on the terminal of the top left corner of the widget
 width, height  |  int | The width/height of the widget
 color  |  int | Color code combination
 selected_color  |  int | color code combination for when widget is selected
 selected  |  bool | Flag that says if widget is selected
 is_selectable  |  bool | Flag that says if a widget can be selected
 help_text  |  str | text displayed in status bar when selected
 key_commands  |  dict | Dictionary mapping key codes to functions
 text_color_rules  |  list of py_cui.ColorRule | color rules to load into renderer when drawing widget

#### Methods

 Method  | Doc
-----|-----
 set_focus_text | Sets status bar text when focused
 add_key_command | Maps a keycode that will be executed in focus mode
 add_text_color_rule | Adds a color rule for text rendering in the widget
 set_standard_color | Sets the default color of the widget
 set_selected_color | Sets the default color of widget when selected
 assign_renderer | Assigns a renderer object to the widget
 get_absolute_position | Gets absolute position of widget in characters
 get_absolute_dims | Gets absolute dimensions of the widget
 is_row_col_inside | Checks if given row/column spot in grid is occupied by the widget
 update_height_width | Refreshes widget position and dims on resize
 get_help_text | Gets status bar text
 handle_key_press | Executes appropriate function based on key press
 draw | Uses the renderer to display the widget




### __init__

```python
def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, selectable = True)
```

Constructor for base widget class







### set_focus_text

```python
def set_focus_text(self, text)
```

Function that sets the text of the status bar on focus for a particular widget




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | text to write to status bar when in focus mode.





### add_key_command

```python
def add_key_command(self, key, command)
```

Maps a keycode to a function that will be executed when in focus mode




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key  |  py_cui.keys.KEY | ascii keycode used to map the key
 command  |  function without args | a non-argument function or lambda function to execute if in focus mode and key is pressed





### add_text_color_rule

```python
def add_text_color_rule(self, regex, color, rule_type, match_type='line', region=[0,1], include_whitespace=False)
```

Forces renderer to draw text using given color if text_condition_function returns True




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 regex  |  str | A string to check against the line for a given rule type
 color  |  int | a supported py_cui color value
 rule_type  |  string | A supported color rule type
 match_type='line'  |  str | sets match type. Can be 'line', 'regex', or 'region'
 region  |  [int, int] | A specified region to color if using match_type='region'
 include_whitespace  |  bool | if false, strip string before checking for match





### set_standard_color

```python
def set_standard_color(self, color)
```

Sets the standard color for the widget




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 color  |  int | Color code for widegt





### set_selected_color

```python
def set_selected_color(self, color)
```

Sets the selected color for the widget




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 color  |  int | Color code for widegt when selected





### assign_renderer

```python
def assign_renderer(self, renderer)
```

Function that assigns a renderer object to the widget



(Meant for internal usage only)


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 renderer  |  py_cui.renderer.Renderer | Renderer for drawing widget
 Raises | ------
 error  |  PyCUIError | If parameter is not a initialized renderer.





### get_absolute_position

```python
def get_absolute_position(self)
```

Gets the absolute position of the widget in characters




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 x_pos, y_pos  |  int | position of widget in terminal





### get_absolute_dims

```python
def get_absolute_dims(self)
```

Gets the absolute dimensions of the widget in characters




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 width, height  |  int | dimensions of widget in terminal





### is_row_col_inside

```python
def is_row_col_inside(self, row, col)
```

Checks if a particular row + column is inside the widget area




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 row, col  |  int | row and column position to check

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 is_inside  |  bool | True if row, col is within widget bounds, false otherwise





### update_height_width

```python
def update_height_width(self)
```

Function that refreshes position and dimensons on resize.



If necessary, make sure required widget attributes updated here as well.





### get_help_text

```python
def get_help_text(self)
```

Returns help text




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 help_text  |  str | Status bar text





### handle_key_press

```python
def handle_key_press(self, key_pressed)
```

Base class function that handles all assigned key presses.



When overwriting this function, make sure to add a super().handle_key_press(key_pressed) call,
as this is required for user defined key command support


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of key pressed





### draw

```python
def draw(self)
```

Base class draw class that checks if renderer is valid.



Should be called with super().draw() in overrides








## Label(Widget)

```python
class Label(Widget)
```

The most basic subclass of Widget.



Simply displays one centered row of text. Has no unique attributes or methods


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 draw_border  |  bool | Toggle for drawing label border

#### Methods

 Method  | Doc
-----|-----
 toggle_border | Toggle drawing label border
 draw | Override base draw class.




### __init__

```python
def __init__(self, id, title,  grid, row, column, row_span, column_span, padx, pady)
```

Constructor for Label







### toggle_border

```python
def toggle_border(self)
```

Function that gives option to draw border around label







### draw

```python
def draw(self)
```

Override base draw class.



Center text and draw it








## BlockLabel(Widget)

```python
class BlockLabel(Widget)
```

A Variation of the label widget that renders a block of text.




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 lines  |  list of str | list of lines that make up block text
 center  |  bool | Decides whether or not label should be centered

#### Methods

 Method  | Doc
-----|-----
 toggle_border | Toggle drawing label border
 draw | Override base draw class.




### __init__

```python
def __init__(self, id, title,  grid, row, column, row_span, column_span, padx, pady, center)
```









### toggle_border

```python
def toggle_border(self)
```

Function that gives option to draw border around label







### draw

```python
def draw(self)
```

Override base draw class.











## ScrollMenu(Widget)

```python
class ScrollMenu(Widget)
```

A scroll menu widget.



Allows for creating a scrollable list of items of which one is selectable.
Analogous to a RadioButton


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 top_view  |  int | the uppermost menu element in view
 selected_item  |  int | the currently highlighted menu item
 view_items  |  list of str | list of menu items

#### Methods

 Method  | Doc
-----|-----
 clear | clears items from menu
 scroll_up | Function that scrolls the view up in the scroll menu
 scroll_down | Function that scrolls the view down in the scroll menu
 add_item | Adds an item to the menu.
 add_item_list | Adds a list of items to the scroll menu.
 remove_selected_item | Function that removes the selected item from the scroll menu.
 get_item_list | Function that gets list of items in a scroll menu
 get | Function that gets the selected item from the scroll menu
 handle_key_press | Override of base class function
 draw | Override of base class function




### __init__

```python
def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady)
```

Constructor for scroll menu







### clear

```python
def clear(self)
```

Clears all items from the Scroll Menu







### scroll_up

```python
def scroll_up(self)
```

Function that scrolls the view up in the scroll menu







### scroll_down

```python
def scroll_down(self)
```

Function that scrolls the view down in the scroll menu







### add_item

```python
def add_item(self, item_text)
```

Adds an item to the menu.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 item_text  |  str | The text for the item





### add_item_list

```python
def add_item_list(self, item_list)
```

Adds a list of items to the scroll menu.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 item_list  |  list of str | list of strings to add as items to the scrollmenu





### remove_selected_item

```python
def remove_selected_item(self)
```

Function that removes the selected item from the scroll menu.







### get_item_list

```python
def get_item_list(self)
```

Function that gets list of items in a scroll menu




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 item_list  |  list of str | list of items in the scrollmenu





### get

```python
def get(self)
```

Function that gets the selected item from the scroll menu




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 item  |  str | selected item, or None if there are no items in the menu





### handle_key_press

```python
def handle_key_press(self, key_pressed)
```

Override base class function.



UP_ARROW scrolls up, DOWN_ARROW scrolls down.


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of key pressed





### draw

```python
def draw(self)
```

Overrides base class draw function










## CheckBoxMenu(ScrollMenu)

```python
class CheckBoxMenu(ScrollMenu)
```

Extension of ScrollMenu that allows for multiple items to be selected at once.




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 selected_item_list  |  list of str | List of checked items
 checked_char  |  char | Character to represent a checked item

#### Methods

 Method  | Doc
-----|-----
 add_item | Adds item to Checkbox
 add_item_list | Adds list of items to the checkbox
 get | Gets list of selected items from the checkbox
 mark_item_as_checked | Function that marks an item as selected
 handle_key_press | Override of base class function




### __init__

```python
def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, checked_char)
```









### add_item

```python
def add_item(self, item_text)
```

Adds item to Checkbox




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 item_text  |  str | Menu item to add





### add_item_list

```python
def add_item_list(self, item_list)
```

Adds list of items to the checkbox




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 item_list  |  list of str | Menu item list to add





### get

```python
def get(self)
```

Gets list of selected items from the checkbox




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 selected_items  |  list of str | list of checked items





### mark_item_as_checked

```python
def mark_item_as_checked(self, text)
```

Function that marks an item as selected




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | Mark item with text = text as checked





### handle_key_press

```python
def handle_key_press(self, key_pressed)
```

Override of key presses.



First, run the superclass function, scrolling should still work.
Adds Enter command to toggle selection


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of pressed key








## Button(Widget)

```python
class Button(Widget)
```

Basic button widget.



Allows for running a command function on Enter


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 command  |  function | A no-args function to run when the button is pressed.

#### Methods

 Method  | Doc
-----|-----
 handle_key_press | Override of base class function
 draw | Override of base class function




### __init__

```python
def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, command)
```









### handle_key_press

```python
def handle_key_press(self, key_pressed)
```

Override of base class, adds ENTER listener that runs the button's command




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | Key code of pressed key





### draw

```python
def draw(self)
```

Override of base class draw function










## TextBox(Widget)

```python
class TextBox(Widget)
```

Widget for entering small single lines of text




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 text  |  str | The text in the text box
 cursor_x, cursor_y  |  int | The absolute positions of the cursor in the terminal window
 cursor_text_pos  |  int | the cursor position relative to the text
 cursor_max_left, cursor_max_right  |  int | The cursor bounds of the text box
 viewport_width  |  int | The width of the textbox viewport

#### Methods

 Method  | Doc
-----|-----
 set_text | sets textbox text
 get | Gets value of the text in the textbox
 clear | Clears the text in the textbox
 move_left | Shifts the cursor the the left. Internal use only
 move_right | Shifts the cursor the the right. Internal use only
 insert_char | Inserts char at cursor position.
 jump_to_start | Jumps to the start of the textbox
 jump_to_end | Jumps to the end to the textbox
 erase_char | Erases character at textbox cursor
 handle_key_press | Override of base class function
 draw | Override of base class function




### __init__

```python
def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, initial_text)
```









### update_height_width

```python
def update_height_width(self)
```

Need to update all cursor positions on resize







### set_text

```python
def set_text(self, text)
```

Sets the value of the text. Overwrites existing text




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | The text to write to the textbox





### get

```python
def get(self)
```

Gets value of the text in the textbox




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 text  |  str | The current textbox test





### clear

```python
def clear(self)
```

Clears the text in the textbox







### move_left

```python
def move_left(self)
```

Shifts the cursor the the left. Internal use only







### move_right

```python
def move_right(self)
```

Shifts the cursor the the right. Internal use only







### insert_char

```python
def insert_char(self, key_pressed)
```

Inserts char at cursor position.



Internal use only


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of key pressed





### jump_to_start

```python
def jump_to_start(self)
```

Jumps to the start of the textbox







### jump_to_end

```python
def jump_to_end(self)
```

Jumps to the end to the textbox







### erase_char

```python
def erase_char(self)
```

Erases character at textbox cursor







### handle_key_press

```python
def handle_key_press(self, key_pressed)
```

Override of base handle key press function




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of key pressed





### draw

```python
def draw(self)
```

Override of base draw function










## ScrollTextBlock(Widget)

```python
class ScrollTextBlock(Widget)
```

Widget for editing large multi-line blocks of text




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 text_lines  |  list of str | The lines of text in the text box
 cursor_x, cursor_y  |  int | The absolute positions of the cursor in the terminal window
 cursor_text_pos_x, cursor_text_pos_y  |  int | the cursor position relative to the text
 cursor_max_left, cursor_max_right  |  int | The cursor bounds of the text box
 cursor_max_up, cursor_max_down  |  int | The cursor bounds of the text box
 viewport_x_start, viewport_y_start  |  int | upper left corner of the viewport
 viewport_width  |  int | The width of the textbox viewport

#### Methods

 Method  | Doc
-----|-----
 get | Gets value of the text in the textbox
 write | Writes text to the textblock
 clear | Clears the text in the textbox
 get_current_line | Gets current line of text (cursor pos)
 set_text | Function that sets the text for the textblock.
 set_text_line | Function that sets the current line's text.
 move_left | Shifts the cursor the the left. Internal use only
 move_right | Shifts the cursor the the right. Internal use only
 move_up | Shifts the cursor upwards. Internal use only
 move_right | Shifts the cursor downwards. Internal use only
 handle_newline | Handles newline characters
 handle_backspace | Handles backspace presses
 handle_home | Handles home key presses
 handle_end | Handles end key presses
 handle_delete | handles delete key presses
 insert_char | Inserts char at cursor position.
 handle_key_press | Override of base class function
 draw | Override of base class function




### __init__

```python
def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, initial_text)
```









### update_height_width

```python
def update_height_width(self)
```

Function that updates the position of the text and cursor on resize







### get

```python
def get(self)
```

Gets all of the text in the textblock and returns it




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 text  |  str | The current text in the text block





### write

```python
def write(self, text)
```

Function used for writing text to the text block




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | Text to write to the text block





### clear

```python
def clear(self)
```

Function that clears the text block







### get_current_line

```python
def get_current_line(self)
```

Returns the line on which the cursor currently resides




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 current_line  |  str | The current line of text that the cursor is on





### set_text

```python
def set_text(self, text)
```

Function that sets the text for the textblock.



Note that this will overwrite any existing text 


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | text to write into text block





### set_text_line

```python
def set_text_line(self, text)
```

Function that sets the current line's text.



Meant only for internal use


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | text line to write into text block





### move_left

```python
def move_left(self)
```

Function that moves the cursor/text position one location to the left







### move_right

```python
def move_right(self)
```

Function that moves the cursor/text position one location to the right







### move_up

```python
def move_up(self)
```

Function that moves the cursor/text position one location up







### move_down

```python
def move_down(self)
```

Function that moves the cursor/text position one location down







### handle_newline

```python
def handle_newline(self)
```

Function that handles recieving newline characters in the text







### handle_backspace

```python
def handle_backspace(self)
```

Function that handles recieving backspace characters in the text







### handle_home

```python
def handle_home(self)
```

Function that handles recieving a home keypress







### handle_end

```python
def handle_end(self)
```

Function that handles recieving an end keypress







### handle_delete

```python
def handle_delete(self)
```

Function that handles recieving a delete keypress







### insert_char

```python
def insert_char(self, key_pressed)
```

Function that handles recieving a character




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of key pressed





### handle_key_press

```python
def handle_key_press(self, key_pressed)
```

Override of base class handle key press function




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of key pressed





### draw

```python
def draw(self)
```

Override of base class draw function










