# renderer

Module containing the py_cui renderer. It is used to draw all of the onscreen ui_elements and items.



#### Classes

 Class  | Doc
-----|-----
 Renderer | Main renderer class used for drawing ui_elements to the terminal.




## Renderer

```python
class Renderer
```

Main renderer class used for drawing ui_elements to the terminal.



Has helper functions for drawing the borders, cursor,
and text required for the cui. All of the functions supplied by the renderer class should only be used internally.


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 root  |  py_cui.PyCUI | The parent window
 stdscr  |  standard cursor | The cursor with which renderer draws text
 color_rules  |  list of py_cui.colors.ColorRule | List of currently loaded rules to apply during drawing

#### Methods

 Method  | Doc
-----|-----
 _set_border_renderer_chars | Function that sets the border characters for ui_elements
 _set_bold | Sets bold draw mode
 _unset_bold | Unsets bold draw mode
 set_color_rules | Sets current color rules
 set_color_mode | Sets the output color mode
 unset_color_mode | Unsets the output color mode
 reset_cursor | Positions the cursor at the bottom right of the selected element
 draw_cursor | Draws the cursor at a particular location
 draw_border | Draws ascii border around ui element
 _draw_border_top | Internal function for drawing top of border
 _draw_border_bottom | Internal function for drawing bottom of border
 _draw_blank_row | Internal function for drawing a blank row
 _get_render_text | Internal function that computes the scope of the text that should be drawn
 _generate_text_color_fragments | Function that applies color rules to text, dividing them if match is found
 draw_text | Function that draws ui_element text.




### __init__

```python
def __init__(self, root, stdscr, logger)
```

Constructor for renderer object







### _set_border_renderer_chars

```python
def _set_border_renderer_chars(self, border_char_set)
```

Function that sets the border characters for ui_elements




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 border_characters  |  Dict of str to str | The border characters as specified by user





### _set_bold

```python
def _set_bold(self)
```

Sets bold draw mode







### _unset_bold

```python
def _unset_bold(self)
```

Unsets bold draw mode







### set_color_rules

```python
def set_color_rules(self, color_rules)
```

Sets current color rules




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 color_rules  |  List[py_cui.colors.ColorRule] | List of currently loaded rules to apply during drawing





### set_color_mode

```python
def set_color_mode(self, color_mode)
```

Sets the output color mode




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 color_mode  |  int | Color code to apply during drawing





### unset_color_mode

```python
def unset_color_mode(self, color_mode)
```

Unsets the output color mode




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 color_mode  |  int | Color code to unapply during drawing





### reset_cursor

```python
def reset_cursor(self, ui_element, fill=True)
```

Positions the cursor at the bottom right of the selected element




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 ui_element  |  py_cui.ui.UIElement | ui element for which to reset cursor
 fill  |  bool | a flag that tells the renderer if the element is filling its grid space, or not (ex. Textbox vs textblock)





### draw_cursor

```python
def draw_cursor(self, cursor_y, cursor_x)
```

Draws the cursor at a particular location




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 cursor_x, cursor_y  |  int | x, y coordinates where to draw the cursor





### draw_border

```python
def draw_border(self, ui_element, fill=True, with_title=True)
```

Draws ascii border around ui element




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 ui_element  |  py_cui.ui.UIElement | The ui_element being drawn
 fill  |  bool | a flag that tells the renderer if the ui_element is filling its grid space, or not (ex. Textbox vs textblock)
 with_title  |  bool | flag that tells whether or not to draw ui_element title





### _draw_border_top

```python
def _draw_border_top(self, ui_element, y, with_title)
```

Internal function for drawing top of border




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 ui_element  |  py_cui.ui.UIElement | The ui_element being drawn
 y  |  int | the terminal row (top down) on which to draw the text
 with_title  |  bool | Flag that tells renderer if title should be superimposed into border.





### _draw_border_bottom

```python
def _draw_border_bottom(self, ui_element, y)
```

Internal function for drawing bottom of border




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 ui_element  |  py_cui.ui.UIElement | The ui_element being drawn
 y  |  int | the terminal row (top down) on which to draw the text





### _draw_blank_row

```python
def _draw_blank_row(self, ui_element, y)
```

Internal function for drawing a blank row




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 ui_element  |  py_cui.ui.UIElement | The ui_element being drawn
 y  |  int | the terminal row (top down) on which to draw the text





### _get_render_text

```python
def _get_render_text(self, ui_element, line, centered, bordered, start_pos)
```

Internal function that computes the scope of the text that should be drawn




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 ui_element  |  py_cui.ui.UIElement | The ui_element being drawn
 line  |  str | the line of text being drawn
 centered  |  bool | flag to set if the text should be centered
 bordered  |  bool | a flag to set if the text should be bordered
 start_pos  |  int | position to start rendering the text from.

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 render_text  |  str | The text shortened to fit within given space





### _generate_text_color_fragments

```python
def _generate_text_color_fragments(self, ui_element, line, render_text)
```

Function that applies color rules to text, dividing them if match is found




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 ui_element  |  py_cui.ui.UIElement | The ui_element being drawn
 line  |  str | the line of text being drawn
 render_text  |  str | The text shortened to fit within given space

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 fragments  |  list of [int, str] | list of text - color code combinations to write





### draw_text

```python
def draw_text(self, ui_element, line, y, centered = False, bordered = True, selected = False, start_pos = 0)
```

Function that draws ui_element text.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 ui_element  |  py_cui.ui.UIElement | The ui_element being drawn
 line  |  str | the line of text being drawn
 y  |  int | the terminal row (top down) on which to draw the text
 centered  |  bool | flag to set if the text should be centered
 bordered  |  bool | a flag to set if the text should be bordered
 selected  |  bool | Flag that tells renderer if ui_element is selected.
 start_pos  |  int | position to start rendering the text from.








