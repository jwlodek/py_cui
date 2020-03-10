# popups

File containing classes for all popups used by py_cui



@author:    Jakub Wlodek  
@created:   12-Aug-2019

#### Classes

 Class  | Doc
-----|-----
 Popup | Base CUI popup class.
 MessagePopup(Popup) | Class representing a simple message popup
 YesNoPopup(Popup) | Class for Yes/No popup. Extends Popup
 TextBoxPopup(Popup) | Class representing a textbox popup
 MenuPopup(Popup) | A scroll menu popup.
 LoadingIconPopup(Popup) | Loading icon popup class
 LoadingBarPopup(Popup) | Class for Loading Bar Popup




## Popup

```python
class Popup
```

Base CUI popup class.



Contains constructor and initial definitions for key_press and draw
Unlike widgets, they do not have a set grid cell, they are simply centered in the view
frame


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 root  |  py_cui.PyCUI | Root CUI window
 title  |  str | Popup title
 text  |  str | Popup message text
 color  |  int | PyCUI color value
 renderer  |  py_cui.renderer.Renderer | Renderer for drawing the popup
 start_x, start_y  |  int | top left corner of the popup
 stop_x, stop_y  |  int | bottom right corner of the popup
 height, width  |  int | The dimensions of the popup
 padx, pady  |  int | The padding on either side of the popup
 selected  |  bool | Always true. Used by the renderer to highlight popup

#### Methods

 Method  | Doc
-----|-----
 handle_key_press | Handles key presses when popup is open
 draw | Function that uses renderer to draw the popup




### __init__

```python
def __init__(self, root, title, text, color, renderer)
```

Constructor for popup class







### handle_key_press

```python
def handle_key_press(self, key_pressed)
```

Handles key presses when popup is open



By default, only closes popup when Escape is pressed


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | The ascii code for the key that was pressed





### draw

```python
def draw(self)
```

Function that uses renderer to draw the popup



Can be implemented by subclass. Base draw function will draw the title and text in a bordered box








## MessagePopup(Popup)

```python
class MessagePopup(Popup)
```

Class representing a simple message popup




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 close_keys  |  list of int | list of key codes that can be used to close the popup

#### Methods

 Method  | Doc
-----|-----
 draw | Draw function for MessagePopup. Calls superclass draw()




### __init__

```python
def __init__(self, root, title, text, color, renderer)
```

Constructor for MessagePopup







### draw

```python
def draw(self)
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
 command  |  function, 1 boolean parameter | Function that takes one boolean parameter. Called with True if yes, called with False if no.

#### Methods

 Method  | Doc
-----|-----
 handle_key_press | Handle key press overwrite from superclass
 draw | Uses base class draw function




### __init__

```python
def __init__(self, root, title, text, color, command, renderer)
```

Constructor for YesNoPopup







### handle_key_press

```python
def handle_key_press(self, key_pressed)
```

Handle key press overwrite from superclass




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of key pressed





### draw

```python
def draw(self)
```

Uses base class draw function










## TextBoxPopup(Popup)

```python
class TextBoxPopup(Popup)
```

Class representing a textbox popup




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 text  |  str | The text in the text box
 command  |  function | The command to run when enter is pressed
 cursor_x, cursor_y  |  int | The absolute positions of the cursor in the terminal window
 cursor_text_pos  |  int | the cursor position relative to the text
 cursor_max_left, cursor_max_right  |  int | The cursor bounds of the text box
 viewport_width  |  int | The width of the textbox viewport
 password  |  bool | If set, replace all characters with *

#### Methods

 Method  | Doc
-----|-----
 set_text | Sets the value of the text. Overwrites existing text
 get | Gets value of the text in the textbox
 clear | Clears the text in the textbox
 move_left | Shifts the cursor the the left. Internal use only
 move_right | Shifts the cursor the the right. Internal use only
 insert_char | Inserts char at cursor position. Internal use only
 jump_to_start | Jumps to the start of the textbox
 jump_to_end | Jumps to the end to the textbox
 erase_char | Erases character at textbox cursor
 delete_char | Deletes character to right of texbox cursor
 handle_key_press | Override of base handle key press function
 draw | Override of base draw function




### __init__

```python
def __init__(self, root, title, color, command, renderer, password)
```









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

Inserts char at cursor position. Internal use only




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







### delete_char

```python
def delete_char(self)
```

Deletes character to right of texbox cursor







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










## MenuPopup(Popup)

```python
class MenuPopup(Popup)
```

A scroll menu popup.



Allows for popup with several menu items to select from


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 top_view  |  int | the uppermost menu element in view
 selected_item  |  int | the currently highlighted menu item
 view_items  |  list of str | list of menu items
 command  |  function | a function that takes a single string parameter, run when ENTER pressed
 run_command_if_none  |  bool | Runs command even if there are no menu items (passes None)

#### Methods

 Method  | Doc
-----|-----
 scroll_up | Function that scrolls the view up in the scroll menu
 scroll_down | Function that scrolls the view down in the scroll menu
 get | Function that gets the selected item from the scroll menu
 handle_key_press | Override of base handle key press function
 draw | Overrides base class draw function




### __init__

```python
def __init__(self, root, items, title, color, command, renderer, run_command_if_none)
```

Constructor for MenuPopup







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

Override of base handle key press function



Enter key runs command, Escape key closes menu


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of key pressed





### draw

```python
def draw(self)
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
 loading_icons  |  list of str | Animation frames for loading icon
 icon_counter  |  int | Current frame of animation
 message  |  str | Loading message

#### Methods

 Method  | Doc
-----|-----
 handle_key_press | Override of base class function.
 draw | Overrides base draw function




### __init__

```python
def __init__(self, root, title, message, color, renderer)
```

Constructor for LoadingIconPopup







### handle_key_press

```python
def handle_key_press(self, key_pressed)
```

Override of base class function.



Loading icon popups cannot be cancelled, so we wish to avoid default behavior


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of pressed key





### draw

```python
def draw(self)
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
 handle_key_press | Override of base class function.
 draw | Override of base draw function




### __init__

```python
def __init__(self, root, title, num_items, color, renderer)
```

Constructor for LoadingBarPopup







### handle_key_press

```python
def handle_key_press(self, key_pressed)
```

Override of base class function.



Loading icon popups cannot be cancelled, so we wish to avoid default behavior


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of pressed key





### draw

```python
def draw(self)
```

Override of base draw function










