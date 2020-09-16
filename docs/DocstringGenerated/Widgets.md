# widgets

Module contatining all core widget classes for py_cui.



Widgets are the basic building blocks of a user interface made with py_cui.
This module contains classes for:

* Base Widget class
* Label
* Block Label
* Scroll Menu
* Checkbox Menu
* Button
* TextBox
* Text Block
* Slider

Additional widgets should be added in appropriate sub-modules, importing this
file and extending the base Widget class, or if appropriate one of the other core widgets.

#### Classes

 Class  | Doc
-----|-----
 Widget(py_cui.ui.UIElement) | Top Level Widget Base Class
 Label(Widget) | The most basic subclass of Widget.
 BlockLabel(Widget) | A Variation of the label widget that renders a block of text.
 ScrollMenu(Widget, py_cui.ui.MenuImplementation) | A scroll menu widget.
 CheckBoxMenu(Widget, py_cui.ui.CheckBoxMenuImplementation) | Extension of ScrollMenu that allows for multiple items to be selected at once.
 Button(Widget) | Basic button widget.
 TextBox(Widget, py_cui.ui.TextBoxImplementation) | Widget for entering small single lines of text
 ScrollTextBlock(Widget, py_cui.ui.TextBlockImplementation) | Widget for editing large multi-line blocks of text




## Widget(py_cui.ui.UIElement)

```python
class Widget(py_cui.ui.UIElement)
```

Top Level Widget Base Class



Extended by all widgets. Contains base classes for handling key presses, drawing,
and setting status bar text.


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _grid  |  py_cui.grid.Grid | The parent grid object of the widget
 _row, _column  |  int | row and column position of the widget
 _row_span, _column_span  |  int | number of rows or columns spanned by the widget
 _selectable  |  bool | Flag that says if a widget can be selected
 _key_commands  |  dict | Dictionary mapping key codes to functions
 _text_color_rules  |  List[py_cui.ColorRule] | color rules to load into renderer when drawing widget

#### Methods

 Method  | Doc
-----|-----
 add_key_command | Maps a keycode to a function that will be executed when in focus mode
 update_key_command | Maps a keycode to a function that will be executed when in focus mode, if key is already mapped
 add_text_color_rule | Forces renderer to draw text using given color if text_condition_function returns True
 get_absolute_start_pos | Gets the absolute position of the widget in characters. Override of base class function
 get_absolute_stop_pos | Gets the absolute dimensions of the widget in characters. Override of base class function
 get_grid_cell | Gets widget row, column in grid
 get_grid_cell_spans | Gets widget row span, column span in grid
 set_selectable | Setter for widget selectablility
 is_selectable | Checks if the widget is selectable
 _is_row_col_inside | Checks if a particular row + column is inside the widget area
 _handle_key_press | Base class function that handles all assigned key presses.
 _draw | Base class draw class that checks if renderer is valid.




### __init__

```python
def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger, selectable = True)
```

Initializer for base widget class



Calss UIElement superclass initialzier, and then assigns widget to grid, along with row/column info
and color rules and key commands





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





### update_key_command

```python
def update_key_command(self, key, command)
```

Maps a keycode to a function that will be executed when in focus mode, if key is already mapped




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key  |  py_cui.keys.KEY | ascii keycode used to map the key
 command  |  function without args | a non-argument function or lambda function to execute if in focus mode and key is pressed





### add_text_color_rule

```python
def add_text_color_rule(self, regex, color, rule_type, match_type='line', region=[0,1], include_whitespace=False, selected_color=None)
```

Forces renderer to draw text using given color if text_condition_function returns True




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 regex  |  str | A string to check against the line for a given rule type
 color  |  int | a supported py_cui color value
 rule_type  |  string | A supported color rule type
 match_type='line'  |  str | sets match type. Can be 'line', 'regex', or 'region'
 region=[0,1]  |  [int, int] | A specified region to color if using match_type='region'
 include_whitespace  |  bool | if false, strip string before checking for match





### get_absolute_start_pos

```python
def get_absolute_start_pos(self)
```

Gets the absolute position of the widget in characters. Override of base class function




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 x_pos, y_pos  |  int | position of widget in terminal





### get_absolute_stop_pos

```python
def get_absolute_stop_pos(self)
```

Gets the absolute dimensions of the widget in characters. Override of base class function




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 width, height  |  int | dimensions of widget in terminal





### get_grid_cell

```python
def get_grid_cell(self)
```

Gets widget row, column in grid




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 row, column  |  int | Initial row and column placement for widget in grid





### get_grid_cell_spans

```python
def get_grid_cell_spans(self)
```

Gets widget row span, column span in grid




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 row_span, column_span  |  int | Initial row span and column span placement for widget in grid





### set_selectable

```python
def set_selectable(self, selectable)
```

Setter for widget selectablility



Paramters
---------
selectable : bool
Widget selectable if true, otherwise not





### is_selectable

```python
def is_selectable(self)
```

Checks if the widget is selectable




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 selectable  |  bool | True if selectable, false otherwise





### _is_row_col_inside

```python
def _is_row_col_inside(self, row, col)
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





### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Base class function that handles all assigned key presses.



When overwriting this function, make sure to add a super()._handle_key_press(key_pressed) call,
as this is required for user defined key command support


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of key pressed





### _draw

```python
def _draw(self)
```

Base class draw class that checks if renderer is valid.



Should be called with super()._draw() in overrides.
Also intializes color rules, so if not called color rules will not be applied








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
 toggle_border | Function that gives option to draw border around label
 _draw | Override base draw class.




### __init__

```python
def __init__(self, id, title,  grid, row, column, row_span, column_span, padx, pady, logger)
```

Initalizer for Label widget







### toggle_border

```python
def toggle_border(self)
```

Function that gives option to draw border around label







### _draw

```python
def _draw(self)
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
 set_title | Override of base class, splits title into lines for rendering line by line.
 toggle_border | Function that gives option to draw border around label
 _draw | Override base draw class.




### __init__

```python
def __init__(self, id, title,  grid, row, column, row_span, column_span, padx, pady, center, logger)
```

Initializer for blocklabel widget







### set_title

```python
def set_title(self, title)
```

Override of base class, splits title into lines for rendering line by line.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 title  |  str | The new title for the block label object.





### toggle_border

```python
def toggle_border(self)
```

Function that gives option to draw border around label







### _draw

```python
def _draw(self)
```

Override base draw class.



Center text and draw it








## ScrollMenu(Widget, py_cui.ui.MenuImplementation)

```python
class ScrollMenu(Widget, py_cui.ui.MenuImplementation)
```

A scroll menu widget.



#### Methods

 Method  | Doc
-----|-----
 _handle_mouse_press | Override of base class function, handles mouse press in menu
 _handle_key_press | Override base class function.
 _draw | Overrides base class draw function




### __init__

```python
def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger)
```

Initializer for scroll menu. calls superclass initializers and sets help text







### _handle_mouse_press

```python
def _handle_mouse_press(self, x, y)
```

Override of base class function, handles mouse press in menu




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 x, y  |  int | Coordinates of mouse press





### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Override base class function.



UP_ARROW scrolls up, DOWN_ARROW scrolls down.


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of key pressed





### _draw

```python
def _draw(self)
```

Overrides base class draw function










## CheckBoxMenu(Widget, py_cui.ui.CheckBoxMenuImplementation)

```python
class CheckBoxMenu(Widget, py_cui.ui.CheckBoxMenuImplementation)
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
 _handle_mouse_press | Override of base class function, handles mouse press in menu
 _handle_key_press | Override of key presses.
 _draw | Overrides base class draw function




### __init__

```python
def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger, checked_char)
```

Initializer for CheckBoxMenu Widget







### _handle_mouse_press

```python
def _handle_mouse_press(self, x, y)
```

Override of base class function, handles mouse press in menu




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 x, y  |  int | Coordinates of mouse press





### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Override of key presses.



First, run the superclass function, scrolling should still work.
Adds Enter command to toggle selection


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of pressed key





### _draw

```python
def _draw(self)
```

Overrides base class draw function










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
 _handle_key_press | Override of base class, adds ENTER listener that runs the button's command
 _draw | Override of base class draw function




### __init__

```python
def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger, command)
```

Initializer for Button Widget







### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Override of base class, adds ENTER listener that runs the button's command




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | Key code of pressed key





### _draw

```python
def _draw(self)
```

Override of base class draw function










## TextBox(Widget, py_cui.ui.TextBoxImplementation)

```python
class TextBox(Widget, py_cui.ui.TextBoxImplementation)
```

Widget for entering small single lines of text



#### Methods

 Method  | Doc
-----|-----
 update_height_width | Need to update all cursor positions on resize
 _handle_mouse_press | Override of base class function, handles mouse press in menu
 _handle_key_press | Override of base handle key press function
 _draw | Override of base draw function




### __init__

```python
def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger, initial_text, password)
```

Initializer for TextBox widget. Uses TextBoxImplementation as base







### update_height_width

```python
def update_height_width(self)
```

Need to update all cursor positions on resize







### _handle_mouse_press

```python
def _handle_mouse_press(self, x, y)
```

Override of base class function, handles mouse press in menu




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 x, y  |  int | Coordinates of mouse press





### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Override of base handle key press function




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of key pressed





### _draw

```python
def _draw(self)
```

Override of base draw function










## ScrollTextBlock(Widget, py_cui.ui.TextBlockImplementation)

```python
class ScrollTextBlock(Widget, py_cui.ui.TextBlockImplementation)
```

Widget for editing large multi-line blocks of text



#### Methods

 Method  | Doc
-----|-----
 update_height_width | Function that updates the position of the text and cursor on resize
 _handle_mouse_press | Override of base class function, handles mouse press in menu
 _handle_key_press | Override of base class handle key press function
 _draw | Override of base class draw function




### __init__

```python
def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger, initial_text)
```

Initializer for TextBlock Widget. Uses TextBlockImplementation as base







### update_height_width

```python
def update_height_width(self)
```

Function that updates the position of the text and cursor on resize







### _handle_mouse_press

```python
def _handle_mouse_press(self, x, y)
```

Override of base class function, handles mouse press in menu




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 x, y  |  int | Coordinates of mouse press





### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Override of base class handle key press function




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of key pressed





### _draw

```python
def _draw(self)
```

Override of base class draw function










