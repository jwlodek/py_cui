# renderer




Module containing the py_cui renderer. It is used to draw all of the onscreen widgets and items.

@author:    Jakub Wlodek  
@created:   12-Aug-2019




## Renderer

```python
class Renderer
```

Main renderer class used for drawing widgets to the terminal.



Has helper functions for drawing the borders, cursor,
and text required for the cui. All of the functions supplied by the renderer class should only be used internally.


#### Attributes

 Attribute  | Type  | Doc
-----|----------|----------|-----
 root  |  py_cui.PyCUI | The parent window
 stdscr  |  standard cursor | The cursor with which renderer draws text
 color_rules  |  list of py_cui.colors.ColorRule | List of currently loaded rules to apply during drawing

#### Methods

 Method  | Doc
-----|----------|-----
 set_bold | Sets bold draw mode
 unset_bold | Unsets bold draw mode
 set_color_rules | Sets current color rules
 set_color_mode | Sets the output color mode
 unset_color_mode | Unsets the output color mode
 reset_cursor | Positions the cursor at the bottom right of the selected widget
 draw_cursor | Draws the cursor at a particular location
 draw_border | Draws border around widget
 draw_border_top | Draws top of border
 draw_border_bottom | Draws bottom of border
 draw_blank_row | Draws a blank row, with an optional border
 get_render_text | Converts line into renderably sized text.
 generate_text_color_fragments | Function that applies color rules to text, dividing them if match is found
 draw_text | Function that draws widget text.




### __init__

```python
def __init__(self, root, stdscr)
```

Constructor for renderer object







### set_bold

```python
def set_bold(self)
```

Sets bold draw mode







### unset_bold

```python
def unset_bold(self)
```

Unsets bold draw mode







### set_color_rules

```python
def set_color_rules(self, color_rules)
```

Sets current color rules




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 color_rules  |  list of py_cui.colors.ColorRule | List of currently loaded rules to apply during drawing





### set_color_mode

```python
def set_color_mode(self, color_mode)
```

Sets the output color mode




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 color_mode  |  int | Color code to apply during drawing





### unset_color_mode

```python
def unset_color_mode(self, color_mode)
```

Unsets the output color mode




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 color_mode  |  int | Color code to unapply during drawing





### reset_cursor

```python
def reset_cursor(self, widget, fill=True)
```

Positions the cursor at the bottom right of the selected widget




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 widget  |  py_cui.widgets.Widget | widget for which to reset cursor
 fill  |  bool | a flag that tells the renderer if the widget is filling its grid space, or not (ex. Textbox vs textblock)





### draw_cursor

```python
def draw_cursor(self, cursor_y, cursor_x)
```

Draws the cursor at a particular location




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 cursor_x, cursor_y  |  int | x, y coordinates where to draw the cursor





### draw_border

```python
def draw_border(self, widget, fill=True, with_title=True)
```

Draws border around widget




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 widget  |  py_cui.widgets.Widget | The widget being drawn
 fill  |  bool | a flag that tells the renderer if the widget is filling its grid space, or not (ex. Textbox vs textblock)
 with_title  |  bool | flag that tells whether or not to draw widget title





### draw_border_top

```python
def draw_border_top(self, widget, y, with_title)
```

Internal function for drawing top of border




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 widget  |  py_cui.widgets.Widget | The widget being drawn
 y  |  int | the terminal row (top down) on which to draw the text
 with_title  |  bool | Flag that tells renderer if title should be superimposed into border.





### draw_border_bottom

```python
def draw_border_bottom(self, widget, y)
```

Internal function for drawing bottom of border




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 widget  |  py_cui.widgets.Widget | The widget being drawn
 y  |  int | the terminal row (top down) on which to draw the text





### draw_blank_row

```python
def draw_blank_row(self, widget, y)
```

Internal function for drawing a blank row




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 widget  |  py_cui.widgets.Widget | The widget being drawn
 y  |  int | the terminal row (top down) on which to draw the text





### get_render_text

```python
def get_render_text(self, widget, line, centered, bordered, start_pos)
```

Internal function that computes the scope of the text that should be drawn




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 widget  |  py_cui.widgets.Widget | The widget being drawn
 line  |  str | the line of text being drawn
 centered  |  bool | flag to set if the text should be centered
 bordered  |  bool | a flag to set if the text should be bordered
 start_pos  |  int | position to start rendering the text from.

#### Returns

 Return Variable  | Type  | Doc
-----|----------|----------|-----
 render_text  |  str | The text shortened to fit within given space





### generate_text_color_fragments

```python
def generate_text_color_fragments(self, widget, line, render_text)
```

Function that applies color rules to text, dividing them if match is found




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 widget  |  py_cui.widgets.Widget | The widget being drawn
 line  |  str | the line of text being drawn
 render_text  |  str | The text shortened to fit within given space

#### Returns

 Return Variable  | Type  | Doc
-----|----------|----------|-----
 fragments  |  list of [int, str] | list of text - color code combinations to write





### draw_text

```python
def draw_text(self, widget, line, y, centered = False, bordered = True, selected = False, start_pos = 0)
```

Function that draws widget text.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 widget  |  py_cui.widgets.Widget | The widget being drawn
 line  |  str | the line of text being drawn
 y  |  int | the terminal row (top down) on which to draw the text
 centered  |  bool | flag to set if the text should be centered
 bordered  |  bool | a flag to set if the text should be bordered
 selected  |  bool | Flag that tells renderer if widget is selected.
 start_pos  |  int | position to start rendering the text from.








