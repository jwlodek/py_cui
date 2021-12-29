# ui

Module containing classes for generic UI elements.



Contains base UI element class, along with UI implementation agnostic UI element classes.

#### Classes

 Class  | Doc
-----|-----
 UIElement | Base class for all UI elements. Extended by base widget and popup classes.
 UIImplementation | Base class for ui implementations.
 TextBoxImplementation(UIImplementation) | UI implementation for a single-row textbox input
 MenuImplementation(UIImplementation) | A scrollable menu UI element
 CheckBoxMenuImplementation(MenuImplementation) | Class representing checkbox menu ui implementation
 TextBlockImplementation(UIImplementation) | Base class for TextBlockImplementation




## UIElement

```python
class UIElement
```

Base class for all UI elements. Extended by base widget and popup classes.



Interfaces between UIImplementation subclasses and CUI engine. For example,
a widget is a subclass of a UIElement. Then a TextBox widget would be a subclass
of the base widget class, and the TextBoxImplementation. The TextBoxImplementation
superclass contains logic for all textbox required operations, while the widget base
class contains all links to the CUI engine.


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _id  |  str | Internal UI element unique ID
 _title  |  str | UI element title
 _padx, pady  |  int, int | padding in terminal characters
 _start_x, _start_y |  int, int | Coords in terminal characters for top-left corner of element
 _stop_x, _stop_y  |  int, int | Coords in terminal characters for bottom-right corner of element
 _height, width  |  int, int | absolute dimensions of ui element in terminal characters
 _color  |  int | Default color for which to draw element
 _border_color |  int | Color used to draw the border of the element when not focused
 _focus_border_color |  int | Color used to draw the border of the element when focused
 _selected  |  bool | toggle for marking an element as selected
 _renderer  |  py_cui.renderer.Renderer | The default ui renderer
 _logger    |  py_cui.debug.PyCUILogger | The default logger inherited from the parent
 _help_text |  str | Text to diplay when selected in status bar

#### Methods

 Method  | Doc
-----|-----
 get_absolute_start_pos | Must be implemented by subclass, computes the absolute coords of upper-left corner
 get_absolute_stop_pos | Must be implemented by subclass, computes the absolute coords of bottom-right corner
 get_absolute_dimensions | Gets dimensions of element in terminal characters
 update_height_width | Function that refreshes position and dimensons on resize.
 get_viewport_height | Gets the height of the element viewport (height minus padding and borders)
 get_id | Gets the element ID
 get_title | Getter for ui element title
 get_padding | Gets ui element padding on in characters
 get_start_position | Gets coords of upper left corner
 get_stop_position | Gets coords of lower right corner
 get_color | Gets current element color
 get_border_color | Gets current element border color
 get_selected_color | Gets current selected item color
 is_selected | Get selected status
 get_renderer | Gets reference to renderer object
 get_help_text | Returns current help text
 set_title | Function that sets the widget title.
 set_color | Sets element default color
 set_border_color | Sets element border color
 set_focus_border_color | Sets element border color if the current element
 set_selected_color | Sets element sected color
 set_selected | Marks the UI element as selected or not selected
 set_help_text | Sets status bar help text
 set_focus_text | Sets status bar focus text. Legacy function, overridden by set_focus_text
 _handle_key_press | Must be implemented by subclass. Used to handle keypresses
 _handle_mouse_press | Can be implemented by subclass. Used to handle mouse presses
 _draw | Must be implemented by subclasses. Uses renderer to draw element to terminal
 _assign_renderer | Function that assigns a renderer object to the element
 _contains_position | Checks if character position is within element.




### __init__

```python
def __init__(self, id, title, renderer, logger)
```

Initializer for UIElement base class







### get_absolute_start_pos

```python
def get_absolute_start_pos(self) -> Tuple[int,int]
```

Must be implemented by subclass, computes the absolute coords of upper-left corner







### get_absolute_stop_pos

```python
def get_absolute_stop_pos(self) -> Tuple[int,int]
```

Must be implemented by subclass, computes the absolute coords of bottom-right corner







### get_absolute_dimensions

```python
def get_absolute_dimensions(self) -> Tuple[int,int]
```

Gets dimensions of element in terminal characters




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 height, width  |  int, int | Dimensions of element in terminal characters





### update_height_width

```python
def update_height_width(self) -> None
```

Function that refreshes position and dimensons on resize.



If necessary, make sure required widget attributes updated here as well.





### get_viewport_height

```python
def get_viewport_height(self) -> int
```

Gets the height of the element viewport (height minus padding and borders)




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 viewport_height  |  int | Height of element viewport in terminal characters





### get_id

```python
def get_id(self) -> int
```

Gets the element ID




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 id  |  int | The ui element id





### get_title

```python
def get_title(self) -> str
```

Getter for ui element title




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 title  |  str | UI element title





### get_padding

```python
def get_padding(self) -> Tuple[int,int]
```

Gets ui element padding on in characters




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 padx, pady  |  int, int | Padding on either axis in characters





### get_start_position

```python
def get_start_position(self) -> Tuple[int,int]
```

Gets coords of upper left corner




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 start_x, start_y  |  int, int | Coords of upper right corner





### get_stop_position

```python
def get_stop_position(self) -> Tuple[int,int]
```

Gets coords of lower right corner




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 stop_x, stop_y  |  int, int | Coords of lower right corner





### get_color

```python
def get_color(self) -> int
```

Gets current element color




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 color  |  int | color code for combination





### get_border_color

```python
def get_border_color(self) -> int
```

Gets current element border color




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 color  |  int | color code for combination





### get_selected_color

```python
def get_selected_color(self) -> int
```

Gets current selected item color




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 color  |  int | color code for combination





### is_selected

```python
def is_selected(self) -> bool
```

Get selected status




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 selected  |  bool | True if selected, False otherwise





### get_renderer

```python
def get_renderer(self) -> 'py_cui.renderer.Renderer'
```

Gets reference to renderer object




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 renderer  |  py_cui.renderer.Render | renderer object used for drawing element





### get_help_text

```python
def get_help_text(self) -> str
```

Returns current help text




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 help_text  |  str | Current element status bar help message





### set_title

```python
def set_title(self, title: str)
```

Function that sets the widget title.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 title  |  str | New widget title





### set_color

```python
def set_color(self, color: int) -> None
```

Sets element default color




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 color  |  int | New color pair key code





### set_border_color

```python
def set_border_color(self, color: int) -> None
```

Sets element border color




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 color  |  int | New color pair key code





### set_focus_border_color

```python
def set_focus_border_color(self, color: int) -> None
```

Sets element border color if the current element


is focused


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 color  |  int | New color pair key code





### set_selected_color

```python
def set_selected_color(self, color: int) -> None
```

Sets element sected color




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 color  |  int | New color pair key code





### set_selected

```python
def set_selected(self, selected: bool) -> None
```

Marks the UI element as selected or not selected




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 selected  |  bool | The new selected state of the element





### set_help_text

```python
def set_help_text(self, help_text: str) -> None
```

Sets status bar help text




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 help_text  |  str | New statusbar help text





### set_focus_text

```python
def set_focus_text(self, focus_text: str) -> None
```

Sets status bar focus text. Legacy function, overridden by set_focus_text




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 focus_text  |  str | New statusbar help text





### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Must be implemented by subclass. Used to handle keypresses







### _handle_mouse_press

```python
def _handle_mouse_press(self, x, y, mouse_event)
```

Can be implemented by subclass. Used to handle mouse presses




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 x, y  |  int, int | Coordinates of the mouse press event.





### _draw

```python
def _draw(self)
```

Must be implemented by subclasses. Uses renderer to draw element to terminal







### _assign_renderer

```python
def _assign_renderer(self, renderer: 'py_cui.renderer.Renderer', quiet: bool=False) 
```

Function that assigns a renderer object to the element



(Meant for internal usage only)


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 renderer  |  py_cui.renderer.Renderer | Renderer for drawing element

#### Raises

 Error  | Type  | Doc
-----|----------|-----
 error  |  PyCUIError | If parameter is not an initialized renderer.





### _contains_position

```python
def _contains_position(self, x: int, y: int) -> bool
```

Checks if character position is within element.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 x  |  int | X coordinate to check
 y  |  int | Y coordinate to check

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 contains  |  bool | True if (x,y) is within the element, false otherwise








## UIImplementation

```python
class UIImplementation
```

Base class for ui implementations.



Should be extended for creating logic common accross ui elements.
For example, a textbox needs the same logic for a widget or popup.
This base class is only used to initialize the logger


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _logger  |  py_cui.debug.PyCUILogger | parent logger object reference.




### __init__

```python
def __init__(self, logger)
```












## TextBoxImplementation(UIImplementation)

```python
class TextBoxImplementation(UIImplementation)
```

UI implementation for a single-row textbox input




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _text  |  str | The text in the text box
 _initial_cursor  |  int | Initial position of the cursor
 _cursor_x, _cursor_y  |  int | The absolute positions of the cursor in the terminal window
 _cursor_text_pos  |  int | the cursor position relative to the text
 _cursor_max_left, cursor_max_right  |  int | The cursor bounds of the text box
 _viewport_width  |  int | The width of the textbox viewport
 _password  |  bool | Toggle to display password characters or text

#### Methods

 Method  | Doc
-----|-----
 get_initial_cursor_pos | Gets initial cursor position
 get_cursor_text_pos | Gets current position of cursor relative to text
 get_cursor_limits | Gets cursor extreme points in terminal position
 get_cursor_position | Returns current cursor poition
 get_viewport_width | Gets the width of the textbox viewport
 set_text | Sets the value of the text. Overwrites existing text
 get | Gets value of the text in the textbox
 clear | Clears the text in the textbox
 _move_left | Shifts the cursor the the left. Internal use only
 _move_right | Shifts the cursor the the right. Internal use only
 _insert_char | Inserts char at cursor position. Internal use only
 _jump_to_start | Jumps to the start of the textbox. Internal use only
 _jump_to_end | Jumps to the end to the textbox. Internal use only
 _erase_char | Erases character at textbox cursor. Internal Use only
 _delete_char | Deletes character to right of texbox cursor. Internal use only




### __init__

```python
def __init__(self, initial_text: str, password: bool , logger)
```

Initializer for the TextBoxImplementation base class







### get_initial_cursor_pos

```python
def get_initial_cursor_pos(self) -> int
```

Gets initial cursor position




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 initial_cursor  |  int | Initial position of the cursor





### get_cursor_text_pos

```python
def get_cursor_text_pos(self) -> int
```

Gets current position of cursor relative to text




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 cursor_text_pos  |  int | the cursor position relative to the text





### get_cursor_limits

```python
def get_cursor_limits(self) -> Tuple[int,int]
```

Gets cursor extreme points in terminal position




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 cursor_max_left, cursor_max_right  |  int | The cursor bounds of the text box





### get_cursor_position

```python
def get_cursor_position(self) -> Tuple[int,int]
```

Returns current cursor poition




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 cursor_x, cursor_y  |  int | The absolute positions of the cursor in the terminal window





### get_viewport_width

```python
def get_viewport_width(self) -> int
```

Gets the width of the textbox viewport




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 viewport_width  |  int | The width of the textbox viewport





### set_text

```python
def set_text(self, text: str)
```

Sets the value of the text. Overwrites existing text




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | The text to write to the textbox





### get

```python
def get(self) -> str
```

Gets value of the text in the textbox




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 text  |  str | The current textbox test





### clear

```python
def clear(self) -> None
```

Clears the text in the textbox







### _move_left

```python
def _move_left(self) -> None
```

Shifts the cursor the the left. Internal use only







### _move_right

```python
def _move_right(self) -> None
```

Shifts the cursor the the right. Internal use only







### _insert_char

```python
def _insert_char(self, key_pressed: int) -> None
```

Inserts char at cursor position. Internal use only




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of key pressed





### _jump_to_start

```python
def _jump_to_start(self) -> None
```

Jumps to the start of the textbox. Internal use only







### _jump_to_end

```python
def _jump_to_end(self) -> None
```

Jumps to the end to the textbox. Internal use only







### _erase_char

```python
def _erase_char(self) -> None
```

Erases character at textbox cursor. Internal Use only







### _delete_char

```python
def _delete_char(self) -> None
```

Deletes character to right of texbox cursor. Internal use only










## MenuImplementation(UIImplementation)

```python
class MenuImplementation(UIImplementation)
```

A scrollable menu UI element



Allows for creating a scrollable list of items of which one is selectable.
Analogous to a RadioButton


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _top_view  |  int | the uppermost menu element in view
 _selected_item  |  int | the currently highlighted menu item
 _view_items  |  list of str | list of menu items

#### Methods

 Method  | Doc
-----|-----
 clear | Clears all items from the Scroll Menu
 set_on_selection_change_event | Function that sets the function fired when menu selection changes.
 _process_selection_change_event | Function that executes on-selection change event either with the current menu item, or with no-args"""
 set_selected_item_index | Sets the currently selected item
 _scroll_up | Function that scrolls the view up in the scroll menu
 _scroll_down | Function that scrolls the view down in the scroll menu
 _jump_up | Function for jumping up menu several spots at a time
 _jump_down | Function for jumping down the menu several spots at a time
 _jump_to_top | Function that jumps to the top of the menu
 _jump_to_bottom | Function that jumps to the bottom of the menu
 add_item | Adds an item to the menu.
 add_item_list | Adds a list of items to the scroll menu.
 remove_selected_item | Function that removes the selected item from the scroll menu.
 remove_item | Function that removes a specific item from the menu
 get_item_list | Function that gets list of items in a scroll menu
 get | Function that gets the selected item from the scroll menu
 set_selected_item | Function that replaces the currently selected item with a new item




### __init__

```python
def __init__(self, logger)
```

Initializer for MenuImplementation base class







### clear

```python
def clear(self) -> None
```

Clears all items from the Scroll Menu







### set_on_selection_change_event

```python
def set_on_selection_change_event(self, on_selection_change_event: Callable[[Any],Any])
```

Function that sets the function fired when menu selection changes.



Event function must take 0 or 1 parameters. If 1 parameter, the new selcted item will be passed in.


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 on_selection_change_event  |  Callable | Callable function that takes in as an argument the newly selected element

#### Raises

 Error  | Type  | Doc
-----|----------|-----
 Unknown | TypeError | Raises a type error if event function is not callable





### _process_selection_change_event

```python
def _process_selection_change_event(self)
```

Function that executes on-selection change event either with the current menu item, or with no-args"""



# Identify num of args from callable. This allows for user to create commands that take in x, y
# coords of the mouse press as input
num_args = 0
try:
num_args = len(inspect.signature(self._on_selection_change).parameters)
except ValueError:
self._logger.error('Failed to get on_selection_change signature!')
except TypeError:
self._logger.error('Type of object not supported for signature identification!')

# Depending on the number of parameters for the self._on_selection_change, pass in the x and y
# values, or do nothing
if num_args == 1:
self._on_selection_change(self.get())
elif num_args == 0:
self._on_selection_change()
else:
raise ValueError('On selection change event must accept either 0 or 1 parameters!')


def get_selected_item_index(self) -> int:
"""Gets the currently selected item


#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 selected_item  |  int | the currently highlighted menu item





### set_selected_item_index

```python
def set_selected_item_index(self, selected_item_index: int) -> None
```

Sets the currently selected item




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 selected_item  |  int | The new selected item index





### _scroll_up

```python
def _scroll_up(self) -> None
```

Function that scrolls the view up in the scroll menu







### _scroll_down

```python
def _scroll_down(self, viewport_height: int) -> None
```

Function that scrolls the view down in the scroll menu



TODO: Viewport height should be calculated internally, and not rely on a parameter.


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 viewport_height  |  int | The number of visible viewport items





### _jump_up

```python
def _jump_up(self) -> None
```

Function for jumping up menu several spots at a time







### _jump_down

```python
def _jump_down(self, viewport_height: int) -> None
```

Function for jumping down the menu several spots at a time




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 viewport_height  |  int | The number of visible viewport items





### _jump_to_top

```python
def _jump_to_top(self) -> None
```

Function that jumps to the top of the menu







### _jump_to_bottom

```python
def _jump_to_bottom(self, viewport_height: int) -> None
```

Function that jumps to the bottom of the menu




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 viewport_height  |  int | The number of visible viewport items





### add_item

```python
def add_item(self, item: Any) -> None
```

Adds an item to the menu.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 item  |  Object | Object to add to the menu. Must have implemented __str__ function





### add_item_list

```python
def add_item_list(self, item_list: List[Any]) -> None
```

Adds a list of items to the scroll menu.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 item_list  |  List[Object] | list of objects to add as items to the scrollmenu





### remove_selected_item

```python
def remove_selected_item(self) -> None
```

Function that removes the selected item from the scroll menu.







### remove_item

```python
def remove_item(self, item: Any) -> None
```

Function that removes a specific item from the menu




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 item  |  Object | Reference of item to remove





### get_item_list

```python
def get_item_list(self) -> List[Any]
```

Function that gets list of items in a scroll menu




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 item_list  |  List[Object] | list of items in the scrollmenu





### get

```python
def get(self) -> Optional[Any]
```

Function that gets the selected item from the scroll menu




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 item  |  Object | selected item, or None if there are no items in the menu





### set_selected_item

```python
def set_selected_item(self, selected_item: Any)
```

Function that replaces the currently selected item with a new item




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 item  |  Object | A new selected item to replace the current one








## CheckBoxMenuImplementation(MenuImplementation)

```python
class CheckBoxMenuImplementation(MenuImplementation)
```

Class representing checkbox menu ui implementation




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _selected_item_dict  |  dict of object -> bool | stores each object and maps to its current selected status
 _checked_char  |  char | Character to mark checked items

#### Methods

 Method  | Doc
-----|-----
 add_item | Extends base class function, item is added and marked as unchecked to start
 remove_selected_item | Removes selected item from item list and selected item dictionary
 remove_item | Removes item from item list and selected item dict
 toggle_item_checked | Function that marks an item as selected
 mark_item_as_checked | Function that marks an item as selected
 mark_item_as_not_checked | Function that marks an item as selected




### __init__

```python
def __init__(self, logger, checked_char)
```

Initializer for the checkbox menu implementation







### add_item

```python
def add_item(self, item: Any) -> None
```

Extends base class function, item is added and marked as unchecked to start




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 item  |  object | The item being added





### remove_selected_item

```python
def remove_selected_item(self) -> None
```

Removes selected item from item list and selected item dictionary







### remove_item

```python
def remove_item(self, item) -> None
```

Removes item from item list and selected item dict




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 item  |  object | Item to remove from menu





### toggle_item_checked

```python
def toggle_item_checked(self, item: Any)
```

Function that marks an item as selected




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 item  |  object | Toggle item checked state





### mark_item_as_checked

```python
def mark_item_as_checked(self, item: Any) -> None
```

Function that marks an item as selected




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 item  |  object | Toggle item checked state





### mark_item_as_not_checked

```python
def mark_item_as_not_checked(self, item) -> None
```

Function that marks an item as selected




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 item  |  object | Item to uncheck








## TextBlockImplementation(UIImplementation)

```python
class TextBlockImplementation(UIImplementation)
```

Base class for TextBlockImplementation



Contains all logic required for a textblock ui element to function.
Currently only implemented in widget form, though popup form is possible.


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _text_lines  |  List[str] | the lines of text in the texbox
 _viewport_x_start, _viewport_y_start  |  int | Initial location of viewport relative to text
 _cursor_text_pos_x, _cursor_text_pos_y  |  int | Cursor position relative to text
 _cursor_x, _cursor_y  |  int | Absolute cursor position in characters
 _cursor_max_up, _cursor_max_down  |  int | cursor limits in vertical space
 _cursor_max_left, _cursor_max_right  |  int | Cursor limits in horizontal space
 _viewport_height, _viewport_width  |  int | The dimensions of the viewport in characters

#### Methods

 Method  | Doc
-----|-----
 get_viewport_start_pos | Gets upper left corner position of viewport
 get_viewport_dims | Gets viewport dimensions in characters
 get_cursor_text_pos | Gets cursor postion relative to text
 get_abs_cursor_position | Gets absolute cursor position in terminal characters
 get_cursor_limits_vertical | Gets limits for cursor in vertical direction
 get_cursor_limits_horizontal | Gets limits for cursor in horizontal direction
 get | Gets all of the text in the textblock and returns it
 write | Function used for writing text to the text block
 clear | Function that clears the text block
 get_current_line | Returns the line on which the cursor currently resides
 set_text | Function that sets the text for the textblock.
 set_text_line | Function that sets the current line's text.
 _move_left | Function that moves the cursor/text position one location to the left
 _move_right | Function that moves the cursor/text position one location to the right
 _move_up | Function that moves the cursor/text position one location up
 _move_down | Function that moves the cursor/text position one location down
 _handle_newline | Function that handles recieving newline characters in the text
 _handle_backspace | Function that handles recieving backspace characters in the text
 _handle_home | Function that handles recieving a home keypress
 _handle_end | Function that handles recieving an end keypress
 _handle_delete | Function that handles recieving a delete keypress
 _insert_char | Function that handles recieving a character




### __init__

```python
def __init__(self, initial_text: str, logger)
```

Initializer for TextBlockImplementation base class



Zeros attributes, and parses initial text





### get_viewport_start_pos

```python
def get_viewport_start_pos(self) -> Tuple[int,int]
```

Gets upper left corner position of viewport




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 viewport_x_start, viewport_y_start  |  int | Initial location of viewport relative to text





### get_viewport_dims

```python
def get_viewport_dims(self) -> Tuple[int,int]
```

Gets viewport dimensions in characters




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 viewport_height, viewport_width  |  int | The dimensions of the viewport in characters





### get_cursor_text_pos

```python
def get_cursor_text_pos(self) -> Tuple[int,int]
```

Gets cursor postion relative to text




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 cursor_text_pos_x, cursor_text_pos_y  |  int | Cursor position relative to text





### get_abs_cursor_position

```python
def get_abs_cursor_position(self) -> Tuple[int,int]
```

Gets absolute cursor position in terminal characters




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 cursor_x, cursor_y  |  int | Absolute cursor position in characters





### get_cursor_limits_vertical

```python
def get_cursor_limits_vertical(self) -> Tuple[int,int]
```

Gets limits for cursor in vertical direction




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 cursor_max_up, cursor_max_down  |  int | cursor limits in vertical space





### get_cursor_limits_horizontal

```python
def get_cursor_limits_horizontal(self) -> Tuple[int,int]
```

Gets limits for cursor in horizontal direction




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 cursor_max_left, cursor_max_right  |  int | Cursor limits in horizontal space





### get

```python
def get(self) -> str
```

Gets all of the text in the textblock and returns it




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 text  |  str | The current text in the text block





### write

```python
def write(self, text: str) -> None
```

Function used for writing text to the text block




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | Text to write to the text block





### clear

```python
def clear(self) -> None
```

Function that clears the text block







### get_current_line

```python
def get_current_line(self) -> str
```

Returns the line on which the cursor currently resides




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 current_line  |  str | The current line of text that the cursor is on





### set_text

```python
def set_text(self, text: str) -> None
```

Function that sets the text for the textblock.



Note that this will overwrite any existing text


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | text to write into text block





### set_text_line

```python
def set_text_line(self, text: str) -> None
```

Function that sets the current line's text.



Meant only for internal use


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | text line to write into text block





### _move_left

```python
def _move_left(self) -> None
```

Function that moves the cursor/text position one location to the left







### _move_right

```python
def _move_right(self) -> None
```

Function that moves the cursor/text position one location to the right







### _move_up

```python
def _move_up(self) -> None
```

Function that moves the cursor/text position one location up







### _move_down

```python
def _move_down(self) -> None
```

Function that moves the cursor/text position one location down







### _handle_newline

```python
def _handle_newline(self) -> None
```

Function that handles recieving newline characters in the text







### _handle_backspace

```python
def _handle_backspace(self) -> None
```

Function that handles recieving backspace characters in the text







### _handle_home

```python
def _handle_home(self) -> None
```

Function that handles recieving a home keypress







### _handle_end

```python
def _handle_end(self) -> None
```

Function that handles recieving an end keypress







### _handle_delete

```python
def _handle_delete(self) -> None
```

Function that handles recieving a delete keypress







### _insert_char

```python
def _insert_char(self, key_pressed: int) -> None
```

Function that handles recieving a character




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of key pressed








