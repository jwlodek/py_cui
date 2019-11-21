# File contatining all core widget classes for py_cui.


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

@author:Jakub Wlodek
@created: 12-Aug-2019


# Widget 

``` python 
 class Widget 
```

Top Level Widget Base Clas.

Extended by all widgets. Contains base classes for handling key presses, drawing,
and setting status bar text.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     id | int |         Id of the widget | 
|     title | str |         Widget title | 
|     grid | py_cui.grid.Grid |         The parent grid object of the widget | 
|     renderer | py_cui.renderer.Renderer |         The renderer object that draws the widget | 
|     row, column | int |         row and column position of the widget | 
|     row_span, column_span | int |         number of rows or columns spanned by the widget | 
|     padx, pady | int |         Padding size in terminal characters | 
|     start_x, start_y | int |         The position on the terminal of the top left corner of the widget | 
|     width, height | int |         The width/height of the widget | 
|     color | int |         Color code combination | 
|     selected_color | int |         color code combination for when widget is selected | 
|     selected | bool |         Flag that says if widget is selected | 
|     is_selectable | bool |         Flag that says if a widget can be selected | 
|     help_text | str |         text displayed in status bar when selected | 
|     key_commands | dict |         Dictionary mapping key codes to functions | 
|     text_color_rules | list of py_cui.ColorRule |         color rules to load into renderer when drawing widget | 


| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| set_focus_text | Function that sets the text of the status bar on focus for a particular widge. | 
| add_key_command | Maps a keycode to a function that will be executed when in focus mod. | 
| add_text_color_rule | Forces renderer to draw text using given color if text_condition_function returns Tru. | 
| set_standard_color | Sets the standard color for the widge. | 
| set_selected_color | Sets the selected color for the widge. | 
| assign_renderer | Function that assigns a renderer object to the widge. | 
| get_absolute_position | Gets the absolute position of the widget in character. | 
| get_absolute_dims | Gets the absolute dimensions of the widget in character. | 
| is_row_col_inside | Checks if a particular row + column is inside the widget are. | 
| update_height_width | Function that refreshes position and dimensons on resize.. | 
| get_help_text | Returns help tex. | 
| handle_key_press | Base class function that handles all assigned key presses. | 
| draw | Base class draw class that checks if renderer is valid. | 
 
 

### set_focus_text

``` python 
    set_focus_text(text) 
```


Function that sets the text of the status bar on focus for a particular widge.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         text | str |             text to write to status bar when in focus mode. | 


### add_key_command

``` python 
    add_key_command(key, command) 
```


Maps a keycode to a function that will be executed when in focus mod.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         key | py_cui.keys.KEY |             ascii keycode used to map the key | 
|         command | function without args |             a non-argument function or lambda function to execute if in focus mode and key is pressed | 


### add_text_color_rule

``` python 
    add_text_color_rule(regex, color, rule_type, match_type='line', region=[0,1], include_whitespace=False) 
```


Forces renderer to draw text using given color if text_condition_function returns Tru.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         regex | str |             A string to check against the line for a given rule type | 
|         color | int |             a supported py_cui color value | 
|         rule_type | string |             A supported color rule type | 
|         match_type='line' | str |             sets match type. Can be 'line', 'regex', or 'region' | 
|         region | [int, int] |             A specified region to color if using match_type='region' | 
|         include_whitespace | bool |             if false, strip string before checking for match | 


### set_standard_color

``` python 
    set_standard_color(color) 
```


Sets the standard color for the widge.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         color | int |             Color code for widegt | 


### set_selected_color

``` python 
    set_selected_color(color) 
```


Sets the selected color for the widge.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         color | int |             Color code for widegt when selected | 


### assign_renderer

``` python 
    assign_renderer(renderer) 
```


Function that assigns a renderer object to the widge.


(Meant for internal usage only)

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         renderer | py_cui.renderer.Renderer |             Renderer for drawing widget | 


### get_absolute_position

``` python 
    get_absolute_position() 
```


Gets the absolute position of the widget in character.

| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         x_pos, y_pos | int |             position of widget in terminal | 


### get_absolute_dims

``` python 
    get_absolute_dims() 
```


Gets the absolute dimensions of the widget in character.

| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         width, height | int |             dimensions of widget in terminal | 


### is_row_col_inside

``` python 
    is_row_col_inside(row, col) 
```


Checks if a particular row + column is inside the widget are.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         row, col | int |             row and column position to check         | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         is_inside | bool |             True if row, col is within widget bounds, false otherwise | 


### update_height_width

``` python 
    update_height_width() 
```


Function that refreshes position and dimensons on resize..


If necessary, make sure required widget attributes updated here as well.

### get_help_text

``` python 
    get_help_text() 
```


Returns help tex.

| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         help_text | str |             Status bar text | 


### handle_key_press

``` python 
    handle_key_press(key_pressed) 
```


Base class function that handles all assigned key presses.

When overwriting this function, make sure to add a super().handle_key_press(key_pressed) call,
as this is required for user defined key command support

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         key_pressed | int |             key code of key pressed | 


### draw

``` python 
    draw() 
```


Base class draw class that checks if renderer is valid.


Should be called with super().draw() in overrides


# Label 

``` python 
 class Label(Widget) 
```

The most basic subclass of Widget.


Simply displays one centered row of text. Has no unique attributes or methods

--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| draw | Override base draw class. | 
 
 

### draw

``` python 
    draw() 
```


Override base draw class.


Center text and draw it


# BlockLabel 

``` python 
 class BlockLabel(Widget) 
```

A Variation of the label widget that renders a block of text.

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     lines | list of str |         list of lines that make up block text | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
 
 


# ScrollMenu 

``` python 
 class ScrollMenu(Widget) 
```

A scroll menu widget.


Allows for creating a scrollable list of items of which one is selectable.
Analogous to a RadioButton

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     top_view | int |         the uppermost menu element in view | 
|     selected_item | int |         the currently highlighted menu item | 
|     view_items | list of str |         list of menu items     | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| clear | Clears all items from the Scroll Men. | 
| scroll_up | Function that scrolls the view up in the scroll men. | 
| scroll_down | Function that scrolls the view down in the scroll men. | 
| add_item | Adds an item to the menu. | 
| add_item_list | Adds a list of items to the scroll menu. | 
| remove_selected_item | Function that removes the selected item from the scroll menu. | 
| get_item_list | Function that gets list of items in a scroll men. | 
| get | Function that gets the selected item from the scroll men. | 
| handle_key_press | Override base class function. | 
| draw | Overrides base class draw functio. | 
 
 

### clear

``` python 
    clear() 
```


Clears all items from the Scroll Men.

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

### add_item

``` python 
    add_item(item_text) 
```


Adds an item to the menu.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         item_text | str |             The text for the item | 


### add_item_list

``` python 
    add_item_list(item_list) 
```


Adds a list of items to the scroll menu.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         item_list | list of str |             list of strings to add as items to the scrollmenu | 


### remove_selected_item

``` python 
    remove_selected_item() 
```


Function that removes the selected item from the scroll menu.

### get_item_list

``` python 
    get_item_list() 
```


Function that gets list of items in a scroll men.

| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         item_list | list of str |             list of items in the scrollmenu | 


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


Override base class function.


UP_ARROW scrolls up, DOWN_ARROW scrolls down.


| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         key_pressed | int |             key code of key pressed | 


### draw

``` python 
    draw() 
```


Overrides base class draw functio.


# CheckBoxMenu 

``` python 
 class CheckBoxMenu(ScrollMenu) 
```

Extension of ScrollMenu that allows for multiple items to be selected at once.

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     selected_item_list | list of str |         List of checked items | 
|     checked_char | char |         Character to represent a checked item | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| add_item_list | Adds list of items to the checkbo. | 
| get | Gets list of selected items from the checkbo. | 
| mark_item_as_checked | Function that marks an item as selecte. | 
| handle_key_press | Override of key presses. | 
 
 

### add_item_list

``` python 
    add_item_list(item_list) 
```


Adds list of items to the checkbo.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         item_list | list of str |             Menu item list to add | 


### get

``` python 
    get() 
```


Gets list of selected items from the checkbo.

| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         selected_items | list of str |             list of checked items | 


### mark_item_as_checked

``` python 
    mark_item_as_checked(text) 
```


Function that marks an item as selecte.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         text | str |             Mark item with text = text as checked | 


### handle_key_press

``` python 
    handle_key_press(key_pressed) 
```


Override of key presses.


First, run the superclass function, scrolling should still work.
Adds Enter command to toggle selection

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         key_pressed | int |             key code of pressed key | 



# Button 

``` python 
 class Button(Widget) 
```

Basic button widget.


Allows for running a command function on Enter

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     command | function |         A no-args function to run when the button is pressed. | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| draw | Override of base class draw functio. | 
 
 

### draw

``` python 
    draw() 
```


Override of base class draw functio.


# TextBox 

``` python 
 class TextBox(Widget) 
```

Widget for entering small single lines of tex.

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     text | str |         The text in the text box | 
|     cursor_x, cursor_y | int |         The absolute positions of the cursor in the terminal window | 
|     cursor_text_pos | int |         the cursor position relative to the text | 
|     cursor_max_left, cursor_max_right | int |         The cursor bounds of the text box | 
|     viewport_width | int |         The width of the textbox viewport | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| set_text | Sets the value of the text. Overwrites existing tex. | 
| get | Gets value of the text in the textbo. | 
| clear | Clears the text in the textbo. | 
| move_left | Shifts the cursor the the left. Internal use onl. | 
| move_right | Shifts the cursor the the right. Internal use onl. | 
| insert_char | Inserts char at cursor position. | 
| jump_to_start | Jumps to the start of the textbo. | 
| jump_to_end | Jumps to the end to the textbo. | 
| erase_char | Erases character at textbox curso. | 
| handle_key_press | Override of base handle key press functio. | 
| draw | Override of base draw functio. | 
 
 

### set_text

``` python 
    set_text(text) 
```


Sets the value of the text. Overwrites existing tex.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         text | str |             The text to write to the textbox | 


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


Inserts char at cursor position.


Internal use only

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


# ScrollTextBlock 

``` python 
 class ScrollTextBlock(Widget) 
```

Widget for editing large multi-line blocks of tex.



| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     text_lines | list of str |         The lines of text in the text box | 
|     cursor_x, cursor_y | int |         The absolute positions of the cursor in the terminal window | 
|     cursor_text_pos_x, cursor_text_pos_y | int |         the cursor position relative to the text | 
|     cursor_max_left, cursor_max_right | int |         The cursor bounds of the text box | 
|     cursor_max_up, cursor_max_down | int |         The cursor bounds of the text box | 
|     viewport_x_start, viewport_y_start | int |         upper left corner of the viewport | 
|     viewport_width | int |         The width of the textbox viewport | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| get | Gets all of the text in the textblock and returns i. | 
| write | Function used for writing text to the text bloc. | 
| clear | Function that clears the text bloc. | 
| get_current_line | Returns the line on which the cursor currently reside. | 
| set_text | Function that sets the text for the textblock.. | 
| set_text_line | Function that sets the current line's text. | 
| move_left | Function that moves the cursor/text position one location to the lef. | 
| move_right | Function that moves the cursor/text position one location to the righ. | 
| move_up | Function that moves the cursor/text position one location u. | 
| move_down | Function that moves the cursor/text position one location dow. | 
| handle_newline | Function that handles recieving newline characters in the tex. | 
| handle_backspace | Function that handles recieving backspace characters in the tex. | 
| handle_home | Function that handles recieving a home keypres. | 
| handle_end | Function that handles recieving an end keypres. | 
| handle_delete | Function that handles recieving a delete keypres. | 
| insert_char | Function that handles recieving a characte. | 
| handle_key_press | Override of base class handle key press functio. | 
| draw | Override of base class draw functio. | 
 
 

### get

``` python 
    get() 
```


Gets all of the text in the textblock and returns i.

| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         text | str |             The current text in the text block | 


### write

``` python 
    write(text) 
```


Function used for writing text to the text bloc.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         text | str |             Text to write to the text block | 


### clear

``` python 
    clear() 
```


Function that clears the text bloc.

### get_current_line

``` python 
    get_current_line() 
```


Returns the line on which the cursor currently reside.

| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         current_line | str |             The current line of text that the cursor is on | 


### set_text

``` python 
    set_text(text) 
```


Function that sets the text for the textblock..


Note that this will overwrite any existing text 

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         text | str |             text to write into text block | 


### set_text_line

``` python 
    set_text_line(text) 
```


Function that sets the current line's text.


Meant only for internal use


| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         text | str |             text line to write into text block | 


### move_left

``` python 
    move_left() 
```


Function that moves the cursor/text position one location to the lef.

### move_right

``` python 
    move_right() 
```


Function that moves the cursor/text position one location to the righ.

### move_up

``` python 
    move_up() 
```


Function that moves the cursor/text position one location u.

### move_down

``` python 
    move_down() 
```


Function that moves the cursor/text position one location dow.

### handle_newline

``` python 
    handle_newline() 
```


Function that handles recieving newline characters in the tex.

### handle_backspace

``` python 
    handle_backspace() 
```


Function that handles recieving backspace characters in the tex.

### handle_home

``` python 
    handle_home() 
```


Function that handles recieving a home keypres.

### handle_end

``` python 
    handle_end() 
```


Function that handles recieving an end keypres.

### handle_delete

``` python 
    handle_delete() 
```


Function that handles recieving a delete keypres.

### insert_char

``` python 
    insert_char(key_pressed) 
```


Function that handles recieving a characte.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         key_pressed | int |             key code of key pressed | 


### handle_key_press

``` python 
    handle_key_press(key_pressed) 
```


Override of base class handle key press functio.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         key_pressed | int |             key code of key pressed | 


### draw

``` python 
    draw() 
```


Override of base class draw functio.