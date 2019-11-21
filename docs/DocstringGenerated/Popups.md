# File containing classes for all popups used by py_cu


@author:Jakub Wlodek
@created: 12-Aug-2019


# Popup 

``` python 
 class Popup 
```

Base CUI popup class..


Contains constructor and initial definitions for key_press and draw
Unlike widgets, they do not have a set grid cell, they are simply centered in the view
frame

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     root | py_cui.PyCUI |         Root CUI window | 
|     title | str |         Popup title | 
|     text | str |         Popup message text | 
|     color | int |         PyCUI color value | 
|     renderer | py_cui.renderer.Renderer |         Renderer for drawing the popup | 
|     start_x, start_y | int |         top left corner of the popup | 
|     stop_x, stop_y | int |         bottom right corner of the popup | 
|     height, width | int |         The dimensions of the popup  | 
|     padx, pady | int |         The padding on either side of the popup | 
|     selected | bool |         Always true. Used by the renderer to highlight popup | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| handle_key_press | Handles key presses when popup is ope. | 
| draw | Function that uses renderer to draw the popu. | 
 
 

### handle_key_press

``` python 
    handle_key_press(key_pressed) 
```


Handles key presses when popup is ope.


Must be implemented by subclass


| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         key_pressed | int |             The ascii code for the key that was pressed | 


### draw

``` python 
    draw() 
```


Function that uses renderer to draw the popu.


Can be implemented by subclass. Base draw function will draw the title and text in a bordered box


# MessagePopup 

``` python 
 class MessagePopup(Popup) 
```

Class representing a simple message popu.

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     close_keys | list of int |         list of key codes that can be used to close the popup | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| handle_key_press | Implementation of handle_key_pressed. | 
| draw | Draw function for MessagePopup. Calls superclass draw(. | 
 
 

### handle_key_press

``` python 
    handle_key_press(key_pressed) 
```


Implementation of handle_key_pressed.

Closes popup if Enter, Space, or Escape is pressed.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         key_pressed | int |             key code of key pressed | 


### draw

``` python 
    draw() 
```


Draw function for MessagePopup. Calls superclass draw(.


# YesNoPopup 

``` python 
 class YesNoPopup(Popup) 
```

Class for Yes/No popup. Extends Popu.

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     command | function, 1 boolean parameter |         Function that takes one boolean parameter. Called with True if yes, called with False if no. | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| handle_key_press | Handle key press overwrite from superclas. | 
| draw | Uses base class draw functio. | 
 
 

### handle_key_press

``` python 
    handle_key_press(key_pressed) 
```


Handle key press overwrite from superclas.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         key_pressed | int |             key code of key pressed | 


### draw

``` python 
    draw() 
```


Uses base class draw functio.


# TextBoxPopup 

``` python 
 class TextBoxPopup(Popup) 
```

Class representing a textbox popu.

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     text | str |         The text in the text box | 
|     command | function |         The command to run when enter is pressed | 
|     cursor_x, cursor_y | int |         The absolute positions of the cursor in the terminal window | 
|     cursor_text_pos | int |         the cursor position relative to the text | 
|     cursor_max_left, cursor_max_right | int |         The cursor bounds of the text box | 
|     viewport_width | int |         The width of the textbox viewport | 
|     password | bool |         If set, replace all characters with * | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| get | Gets value of the text in the textbo. | 
| clear | Clears the text in the textbo. | 
| move_left | Shifts the cursor the the left. Internal use onl. | 
| move_right | Shifts the cursor the the right. Internal use onl. | 
| insert_char | Inserts char at cursor position. Internal use onl. | 
| jump_to_start | Jumps to the start of the textbo. | 
| jump_to_end | Jumps to the end to the textbo. | 
| erase_char | Erases character at textbox curso. | 
| handle_key_press | Override of base handle key press functio. | 
| draw | Override of base draw functio. | 
 
 

### get

``` python 
    get() 
```


Gets value of the text in the textbo.



| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         text | str |             The current textbox test | 


### clear

``` python 
    clear() 
```


Clears the text in the textbo.

### move_left

``` python 
    move_left() 
```


Shifts the cursor the the left. Internal use onl.

### move_right

``` python 
    move_right() 
```


Shifts the cursor the the right. Internal use onl.

### insert_char

``` python 
    insert_char(key_pressed) 
```


Inserts char at cursor position. Internal use onl.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         key_pressed | int |             key code of key pressed | 


### jump_to_start

``` python 
    jump_to_start() 
```


Jumps to the start of the textbo.

### jump_to_end

``` python 
    jump_to_end() 
```


Jumps to the end to the textbo.

### erase_char

``` python 
    erase_char() 
```


Erases character at textbox curso.

### handle_key_press

``` python 
    handle_key_press(key_pressed) 
```


Override of base handle key press functio.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         key_pressed | int |             key code of key pressed | 


### draw

``` python 
    draw() 
```


Override of base draw functio.


# MenuPopup 

``` python 
 class MenuPopup(Popup) 
```

A scroll menu popup.


Allows for popup with several menu items to select from

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     top_view | int |         the uppermost menu element in view | 
|     selected_item | int |         the currently highlighted menu item | 
|     view_items | list of str |         list of menu items | 
|     command | function |         a function that takes a single string parameter, run when ENTER pressed | 
|     run_command_if_none | bool |         Runs command even if there are no menu items (passes None)     | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| scroll_up | Function that scrolls the view up in the scroll men. | 
| scroll_down | Function that scrolls the view down in the scroll men. | 
| get | Function that gets the selected item from the scroll men. | 
| handle_key_press | Override of base handle key press functio. | 
| draw | Overrides base class draw functio. | 
 
 

### scroll_up

``` python 
    scroll_up() 
```


Function that scrolls the view up in the scroll men.

### scroll_down

``` python 
    scroll_down() 
```


Function that scrolls the view down in the scroll men.

### get

``` python 
    get() 
```


Function that gets the selected item from the scroll men.

| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         item | str |             selected item, or None if there are no items in the menu | 


### handle_key_press

``` python 
    handle_key_press(key_pressed) 
```


Override of base handle key press functio.

Enter key runs command, Escape key closes menu

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         key_pressed | int |             key code of key pressed | 


### draw

``` python 
    draw() 
```


Overrides base class draw functio.


# LoadingIconPopup 

``` python 
 class LoadingIconPopup(Popup) 
```

Loading icon popup clas.

MUST BE USED WITH A FORM OF ASYNC/THREADING

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     loading_icons | list of str |         Animation frames for loading icon | 
|     icon_counter | int |         Current frame of animation | 
|     message | str |         Loading message | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| draw | Overrides base draw functio. | 
 
 

### draw

``` python 
    draw() 
```


Overrides base draw functio.


# LoadingBarPopup 

``` python 
 class LoadingBarPopup(Popup) 
```

Class for Loading Bar Popu.

MUST BE USED WITH A FORM OF ASYNC/THREADING

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     num_items | int |         NUmber of items to count through | 
|     completed_items | int |         counter for completed items | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| draw | Override of base draw functio. | 
 
 

### draw

``` python 
    draw() 
```


Override of base draw functio.