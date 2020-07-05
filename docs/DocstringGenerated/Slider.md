# slider





#### Classes

 Class  | Doc
-----|-----
 SliderImplementation(py_cui.ui.UIImplementation) |
 SliderWidget(py_cui.widgets.Widget, SliderImplementation) |
 SliderPopup(py_cui.popups.Popup, SliderImplementation) |




## SliderImplementation(py_cui.ui.UIImplementation)

```python
class SliderImplementation(py_cui.ui.UIImplementation)
```





#### Methods

 Method  | Doc
-----|-----
 set_bar_char | Updates the character used to represent the slider bar
 update_slider_value | Sets the value of the slider - increment decrement
 get_slider_value | return current slider value
 set_slider_step | change step value




### __init__

```python
def __init__(self, min_val, max_val, init_val, step)
```









### set_bar_char

```python
def set_bar_char(self, char)
```

Updates the character used to represent the slider bar







### update_slider_value

```python
def update_slider_value(self, direction)
```

Sets the value of the slider - increment decrement







### get_slider_value

```python
def get_slider_value(self)
```

return current slider value







### set_slider_step

```python
def set_slider_step(self,step)
```

change step value










## SliderWidget(py_cui.widgets.Widget, SliderImplementation)

```python
class SliderWidget(py_cui.widgets.Widget, SliderImplementation)
```





#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _min_val  |  int | Lowest value of the slider
 _max_val |  int | Highest value of the slider
 _step  |  int | Increment from low to high value
 _cur_val |  | Current value of the slider

#### Methods

 Method  | Doc
-----|-----
 _draw |
 _handle_key_press | LEFT_ARROW decrease value, RIGHT_ARROW increase.




### __init__

```python
def __init__(self, id, title, grid, row, column, row_span, column_span
```









### _draw

```python
def _draw(self)
```









### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

LEFT_ARROW decrease value, RIGHT_ARROW increase.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of key pressed








## SliderPopup(py_cui.popups.Popup, SliderImplementation)

```python
class SliderPopup(py_cui.popups.Popup, SliderImplementation)
```











