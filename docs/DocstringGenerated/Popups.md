# popups

File containing classes for all popups used by py_cui



#### Classes

 Class  | Doc
-----|-----
 Popup(py_cui.ui.UIElement) | Base CUI popup class.
 MessagePopup(Popup) | Class representing a simple message popup
 YesNoPopup(Popup) | Class for Yes/No popup. Extends Popup
 TextBoxPopup(Popup, py_cui.ui.TextBoxImplementation) | Class representing a textbox popup
 MenuPopup(Popup, py_cui.ui.MenuImplementation) | A scroll menu popup.
 LoadingIconPopup(Popup) | Loading icon popup class
 LoadingBarPopup(Popup) | Class for Loading Bar Popup




## Popup(py_cui.ui.UIElement)

```python
class Popup(py_cui.ui.UIElement)
```

Base CUI popup class.



Contains constructor and initial definitions for key_press and draw
Unlike widgets, they do not have a set grid cell, they are simply centered in the view
frame


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _root  |  py_cui.PyCUI | Root CUI window
 _text  |  str | Popup message text
 _selected  |  bool | Always true. Used by the renderer to highlight popup
 _close_keys  |  List[int] | List of keycodes used to close popup

#### Methods

 Method  | Doc
-----|-----
 _increment_counter | Function that increments an internal counter
 set_text | Sets popup text (message)
 get_absolute_start_pos | Override of base class, computes position based on root dimensions
 get_absolute_stop_pos | Override of base class, computes position based on root dimensions
 _handle_key_press | Handles key presses when popup is open
 _draw | Function that uses renderer to draw the popup




### __init__

```python
def __init__(self, root, title, text, color, renderer, logger)
```

Initializer for main popup class. Calls UIElement intialier, and sets some initial values







### _increment_counter

```python
def _increment_counter(self)
```

Function that increments an internal counter







### set_text

```python
def set_text(self, text)
```

Sets popup text (message)




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | The new popup text





### get_absolute_start_pos

```python
def get_absolute_start_pos(self)
```

Override of base class, computes position based on root dimensions




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 start_x, start_y  |  int | The coords of the upper-left corner of the popup





### get_absolute_stop_pos

```python
def get_absolute_stop_pos(self)
```

Override of base class, computes position based on root dimensions




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 stop_x, stop_y  |  int | The coords of the lower-right corner of the popup





### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Handles key presses when popup is open



By default, only closes popup when Escape is pressed


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | The ascii code for the key that was pressed





### _draw

```python
def _draw(self)
```

Function that uses renderer to draw the popup



Can be implemented by subclass. Base draw function will draw the title and text in a bordered box








## MessagePopup(Popup)

```python
class MessagePopup(Popup)
```

Class representing a simple message popup



#### Methods

 Method  | Doc
-----|-----
 _draw | Draw function for MessagePopup. Calls superclass draw()




### __init__

```python
def __init__(self, root, title, text, color, renderer, logger)
```

Initializer for MessagePopup







### _draw

```python
def _draw(self)
```

Draw function for MessagePopup. Calls superclass draw()










## YesNoPopup(Popup)

```python
class YesNoPopup(Popup)
```

Class for Yes/No popup. Extends Popup




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _command  |  function, 1 boolean parameter | Function that takes one boolean parameter. Called with True if yes, called with False if no.

#### Methods

 Method  | Doc
-----|-----
 _handle_key_press | Handle key press overwrite from superclass
 _draw | Uses base class draw function




### __init__

```python
def __init__(self, root, title, text, color, command, renderer, logger)
```

Initializer for YesNoPopup







### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Handle key press overwrite from superclass




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of key pressed





### _draw

```python
def _draw(self)
```

Uses base class draw function










## TextBoxPopup(Popup, py_cui.ui.TextBoxImplementation)

```python
class TextBoxPopup(Popup, py_cui.ui.TextBoxImplementation)
```

Class representing a textbox popup




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _command  |  function | The command to run when enter is pressed

#### Methods

 Method  | Doc
-----|-----
 update_height_width | Need to update all cursor positions on resize
 _handle_key_press | Override of base handle key press function
 _draw | Override of base draw function




### __init__

```python
def __init__(self, root, title, color, command, renderer, password, logger)
```

Initializer for textbox popup. Uses TextBoxImplementation as base







### update_height_width

```python
def update_height_width(self)
```

Need to update all cursor positions on resize







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










## MenuPopup(Popup, py_cui.ui.MenuImplementation)

```python
class MenuPopup(Popup, py_cui.ui.MenuImplementation)
```

A scroll menu popup.



Allows for popup with several menu items to select from


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _command  |  function | a function that takes a single string parameter, run when ENTER pressed
 _run_command_if_none  |  bool | Runs command even if there are no menu items (passes None)

#### Methods

 Method  | Doc
-----|-----
 _handle_key_press | Override of base handle key press function
 _draw | Overrides base class draw function




### __init__

```python
def __init__(self, root, items, title, color, command, renderer, logger, run_command_if_none)
```

Initializer for MenuPopup. Uses MenuImplementation as base







### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Override of base handle key press function



Enter key runs command, Escape key closes menu


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of key pressed





### _draw

```python
def _draw(self)
```

Overrides base class draw function










## LoadingIconPopup(Popup)

```python
class LoadingIconPopup(Popup)
```

Loading icon popup class



MUST BE USED WITH A FORM OF ASYNC/THREADING


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _loading_icons  |  list of str | Animation frames for loading icon
 _icon_counter  |  int | Current frame of animation
 _message  |  str | Loading message

#### Methods

 Method  | Doc
-----|-----
 _handle_key_press | Override of base class function.
 _draw | Overrides base draw function




### __init__

```python
def __init__(self, root, title, message, color, renderer, logger)
```

Initializer for LoadingIconPopup







### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Override of base class function.



Loading icon popups cannot be cancelled, so we wish to avoid default behavior


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of pressed key





### _draw

```python
def _draw(self)
```

Overrides base draw function










## LoadingBarPopup(Popup)

```python
class LoadingBarPopup(Popup)
```

Class for Loading Bar Popup



MUST BE USED WITH A FORM OF ASYNC/THREADING


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 num_items  |  int | NUmber of items to count through
 completed_items  |  int | counter for completed items

#### Methods

 Method  | Doc
-----|-----
 _handle_key_press | Override of base class function.
 _increment_counter | Function that increments an internal counter
 _draw | Override of base draw function




### __init__

```python
def __init__(self, root, title, num_items, color, renderer, logger)
```

Initializer for LoadingBarPopup







### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Override of base class function.



Loading icon popups cannot be cancelled, so we wish to avoid default behavior


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of pressed key





### _increment_counter

```python
def _increment_counter(self)
```

Function that increments an internal counter







### _draw

```python
def _draw(self)
```

Override of base draw function










