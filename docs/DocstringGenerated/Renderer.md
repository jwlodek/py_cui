# 

Module containing the py_cui renderer. It is used to draw all of the onscreen widgets and items.

@author:Jakub Wlodek
@created: 12-Aug-2019


# Renderer 

``` python 
 class Renderer 
```

Main renderer class used for drawing widgets to the terminal.


Has helper functions for drawing the borders, cursor,
and text required for the cui. All of the functions supplied by the renderer class should only be used internally.

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     root | py_cui.PyCUI |         The parent window | 
|     stdscr | standard cursor |         The cursor with which renderer draws text | 
|     color_rules | list of py_cui.colors.ColorRule |         List of currently loaded rules to apply during drawing | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| set_bold | Sets bold draw mod. | 
| unset_bold | Unsets bold draw mod. | 
| set_color_rules | Sets current color rule. | 
| set_color_mode | Sets the output color mod. | 
| unset_color_mode | Unsets the output color mod. | 
| reset_cursor | Positions the cursor at the bottom right of the selected widge. | 
| draw_cursor | Draws the cursor at a particular locatio. | 
| draw_border | Draws border around widge. | 
| draw_border_top | Internal function for drawing top of borde. | 
| draw_border_bottom | Internal function for drawing bottom of borde. | 
| draw_blank_row | Internal function for drawing a blank ro. | 
| get_render_text | Internal function that computes the scope of the text that should be draw. | 
| generate_text_color_fragments | Function that applies color rules to text, dividing them if match is foun. | 
| draw_text | Function that draws widget text. | 
 
 

### set_bold

``` python 
    set_bold() 
```


Sets bold draw mod.

### unset_bold

``` python 
    unset_bold() 
```


Unsets bold draw mod.

### set_color_rules

``` python 
    set_color_rules(color_rules) 
```


Sets current color rule.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         color_rules | list of py_cui.colors.ColorRule |             List of currently loaded rules to apply during drawing | 


### set_color_mode

``` python 
    set_color_mode(color_mode) 
```


Sets the output color mod.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         color_mode | int |             Color code to apply during drawing | 


### unset_color_mode

``` python 
    unset_color_mode(color_mode) 
```


Unsets the output color mod.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         color_mode | int |             Color code to unapply during drawing | 


### reset_cursor

``` python 
    reset_cursor(widget, fill=True) 
```


Positions the cursor at the bottom right of the selected widge.



| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         widget | py_cui.widgets.Widget |             widget for which to reset cursor | 
|         fill | bool |             a flag that tells the renderer if the widget is filling its grid space, or not (ex. Textbox vs textblock) | 


### draw_cursor

``` python 
    draw_cursor(cursor_y, cursor_x) 
```


Draws the cursor at a particular locatio.



| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         cursor_x, cursor_y | int |             x, y coordinates where to draw the cursor | 


### draw_border

``` python 
    draw_border(widget, fill=True, with_title=True) 
```


Draws border around widge.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         widget | py_cui.widgets.Widget |             The widget being drawn | 
|         fill | bool |             a flag that tells the renderer if the widget is filling its grid space, or not (ex. Textbox vs textblock) | 
|         with_title | bool |             flag that tells whether or not to draw widget title | 


### draw_border_top

``` python 
    draw_border_top(widget, y, with_title) 
```


Internal function for drawing top of borde.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         widget | py_cui.widgets.Widget |             The widget being drawn | 
|         y | int |             the terminal row (top down) on which to draw the text | 
|         with_title | bool |             Flag that tells renderer if title should be superimposed into border. | 


### draw_border_bottom

``` python 
    draw_border_bottom(widget, y) 
```


Internal function for drawing bottom of borde.



| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         widget | py_cui.widgets.Widget |             The widget being drawn | 
|         y | int |             the terminal row (top down) on which to draw the text | 


### draw_blank_row

``` python 
    draw_blank_row(widget, y) 
```


Internal function for drawing a blank ro.



| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         widget | py_cui.widgets.Widget |             The widget being drawn | 
|         y | int |             the terminal row (top down) on which to draw the text | 


### get_render_text

``` python 
    get_render_text(widget, line, centered, bordered, start_pos) 
```


Internal function that computes the scope of the text that should be draw.



| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         widget | py_cui.widgets.Widget |             The widget being drawn | 
|         line | str |             the line of text being drawn | 
|         centered | bool |             flag to set if the text should be centered | 
|         bordered | bool |             a flag to set if the text should be bordered | 
|         start_pos | int |             position to start rendering the text from. | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         render_text | str |             The text shortened to fit within given space | 


### generate_text_color_fragments

``` python 
    generate_text_color_fragments(widget, line, render_text) 
```


Function that applies color rules to text, dividing them if match is foun.



| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         widget | py_cui.widgets.Widget |             The widget being drawn | 
|         line | str |             the line of text being drawn | 
|         render_text | str |             The text shortened to fit within given space         | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         fragments | list of [int, str] |             list of text - color code combinations to write | 


### draw_text

``` python 
    draw_text(widget, line, y, centered = False, bordered = True, selected = False, start_pos = 0) 
```


Function that draws widget text.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         widget | py_cui.widgets.Widget |             The widget being drawn | 
|         line | str |             the line of text being drawn | 
|         y | int |             the terminal row (top down) on which to draw the text | 
|         centered | bool |             flag to set if the text should be centered | 
|         bordered | bool |             a flag to set if the text should be bordered | 
|         selected | bool |             Flag that tells renderer if widget is selected. | 
|         start_pos | int |             position to start rendering the text from. | 
