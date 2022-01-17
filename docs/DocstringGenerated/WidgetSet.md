# widget_set

File containing class that abstracts a collection of widgets.



It can be used to swap between collections of widgets (screens) in a py_cui

#### Classes

 Class  | Doc
-----|-----
 WidgetSet | Class that represents a collection of widgets.




## WidgetSet

```python
class WidgetSet
```

Class that represents a collection of widgets.



Use PyCUI.apply_widget_set() to set a given widget set for display


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 grid  |  py_cui.grid.Grid | The main layout manager for the CUI
 widgets  |  dict of str - py_cui.widgets.Widget | dict of widget in the grid
 keybindings  |  list of py_cui.keybinding.KeyBinding | list of keybindings to check against in the main CUI loop
 height, width  |  int | height of the terminal in characters, width of terminal in characters
 root  |  py_cui.PyCUI | Main PyCUI object reference

#### Methods

 Method  | Doc
-----|-----
 set_selected_widget | Function that sets the selected cell for the CUI
 get_widgets | Function that gets current set of widgets
 add_key_command | Function that adds a keybinding to the CUI when in overview mode
 add_scroll_menu | Function that adds a new scroll menu to the CUI grid
 add_checkbox_menu | Function that adds a new checkbox menu to the CUI grid
 add_text_box | Function that adds a new text box to the CUI grid
 add_text_block | Function that adds a new text block to the CUI grid
 add_label | Function that adds a new label to the CUI grid
 add_block_label | Function that adds a new block label to the CUI grid
 add_button | Function that adds a new button to the CUI grid
 add_slider | Function that adds a new label to the CUI grid




### __init__

```python
def __init__(self, num_rows: int, num_cols: int, logger: 'py_cui.debug.PyCUILogger', root:'py_cui.PyCUI', simulated_terminal: Optional[List[int]] =None)
```

Constructor for WidgetSet







### set_selected_widget

```python
def set_selected_widget(self, widget_id: int) -> None
```

Function that sets the selected cell for the CUI




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 cell_title  |  str | the title of the cell





### get_widgets

```python
def get_widgets(self) -> Dict[int, Optional['py_cui.widgets.Widget']]
```

Function that gets current set of widgets




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 widgets  |  dict of str -> widget | dictionary mapping widget IDs to object instances





### add_key_command

```python
def add_key_command(self, key: int, command: Callable[[],Any])
```

Function that adds a keybinding to the CUI when in overview mode




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key  |  py_cui.keys.KEY_* | The key bound to the command
 command  |  Function | A no-arg or lambda function to fire on keypress





### add_scroll_menu

```python
def add_scroll_menu(self, title: str, row: int, column: int, row_span: int = 1, column_span: int = 1, padx: int = 1, pady: int = 0) -> 'py_cui.widgets.ScrollMenu'
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
def add_button(self, title: str, row: int, column: int, row_span: int = 1, column_span: int = 1, padx: int = 1, pady: int = 0, command: Optional[Callable[[],Any]]=None) -> 'py_cui.widgets.Button'
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








