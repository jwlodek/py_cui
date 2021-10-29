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
 set_bar_char |
 update_slider_value |
 get_slider_value |
 set_slider_step |




### __init__

```python
def __init__(self, min_val: int, max_val: int, init_val: int, step: int, logger)
```









### set_bar_char

```python
def set_bar_char(self, char: str) -> None
```




Updates the character used to represent the slider bar.


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 char  |  str | Character to represent progressive bar.





### update_slider_value

```python
def update_slider_value(self, offset: int) -> float
```




Steps up or down the value in offset fashion.


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 offset  |  int | Number of steps to increase or decrease the slider value.

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 self._cur_val |  float | Current slider value.





### get_slider_value

```python
def get_slider_value(self) -> float
```




Returns current slider value.


#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 self._cur_val |  float | Current slider value.





### set_slider_step

```python
def set_slider_step(self, step: int) -> None
```




Changes the step value.


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 step  |  int | Step size of the slider.








## SliderWidget(py_cui.widgets.Widget, SliderImplementation)

```python
class SliderWidget(py_cui.widgets.Widget, SliderImplementation)
```




Widget for a Slider


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 min_val  |  int | Lowest value of the slider
 max_val |  int | Highest value of the slider
 step  |  int | Increment from low to high value
 init_val |  | Initial value of the slider

#### Methods

 Method  | Doc
-----|-----
 toggle_title | Toggles visibility of the widget's name.
 toggle_border | Toggles visibility of the widget's border.
 toggle_value | Toggles visibility of the widget's current value in integer.
 align_to_top | Aligns widget height to top.
 align_to_middle | Aligns widget height to middle. default configuration.
 align_to_bottom | Aligns widget height to bottom.
 _custom_draw_with_border |
 _generate_bar |
 _draw | Override of base class draw function.
 _handle_key_press |




### __init__

```python
def __init__(self, id, title, grid, row, column, row_span, column_span
```









### toggle_title

```python
def toggle_title(self) -> None
```

Toggles visibility of the widget's name.







### toggle_border

```python
def toggle_border(self) -> None
```

Toggles visibility of the widget's border.







### toggle_value

```python
def toggle_value(self) -> None
```

Toggles visibility of the widget's current value in integer.







### align_to_top

```python
def align_to_top(self) -> None
```

Aligns widget height to top.







### align_to_middle

```python
def align_to_middle(self) -> None
```

Aligns widget height to middle. default configuration.







### align_to_bottom

```python
def align_to_bottom(self) -> None
```

Aligns widget height to bottom.







### _custom_draw_with_border

```python
def _custom_draw_with_border(self, start_y: int, content: str) -> None
```




Custom method made from renderer.draw_border to support alignment for bordered variants.


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 start_y  |  int | border's Y-axis starting coordination
 content |  str | string to be drawn inside the border





### _generate_bar

```python
def _generate_bar(self, width: int) -> str
```




Internal implementation to generate progression bar.


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 width  |  int | Width of bar in character length.

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 progress |  str | progressive bar string  with length of width.





### _draw

```python
def _draw(self) -> None
```

Override of base class draw function.







### _handle_key_press

```python
def _handle_key_press(self, key_pressed: int) -> None
```




LEFT_ARROW decreases value, RIGHT_ARROW increases.


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | key code of pressed key








## SliderPopup(py_cui.popups.Popup, SliderImplementation)

```python
class SliderPopup(py_cui.popups.Popup, SliderImplementation)
```











