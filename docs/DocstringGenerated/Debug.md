# debug

Module containing py_cui logging utilities



#### Classes

 Class  | Doc
-----|-----
 LiveDebugImplementation(py_cui.ui.MenuImplementation) | Implementation class for the live debug menu - builds off of the scroll menu implementation
 LiveDebugElement(py_cui.ui.UIElement, LiveDebugImplementation) | UIElement class for the live debug utility. extends from base UIElement class and LiveDebugImplementation
 PyCUILogger(logging.Logger) | Custom logger class for py_cui, extends the base logging.Logger Class

#### Functions

 Function  | Doc
-----|-----
 _enable_logging | Function that creates basic logging configuration for selected logger
 _initialize_logger | Function that retrieves an instance of either the default or custom py_cui logger.




### _enable_logging

```python
def _enable_logging(logger: 'PyCUILogger', replace_log_file: bool=True, filename: str='py_cui.log', logging_level=logging.DEBUG) 
```

Function that creates basic logging configuration for selected logger




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 logger  |  PyCUILogger | Main logger object
 filename  |  os.Pathlike | File path for output logfile
 logging_level  |  logging.LEVEL, optional | Level of messages to display, by default logging.DEBUG

#### Raises

 Error  | Type  | Doc
-----|----------|-----
 Unknown | PermissionError | py_cui logs require permission to cwd to operate.
 Unknown | TypeError | Only the custom PyCUILogger can be used here.





### _initialize_logger

```python
def _initialize_logger(py_cui_root: 'py_cui.PyCUI', name: Optional[str]=None, custom_logger: bool=True) 
```

Function that retrieves an instance of either the default or custom py_cui logger.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 py_cui_root  |  py_cui.PyCUI | reference to the root py_cui window
 name  |  str, optional | The name of the logger, by default None
 custom_logger  |  bool, optional | Use a custom py_cui logger, by default True

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 logger  |  py_cui.debug.PyCUILogger | A custom logger that allows for live debugging





## LiveDebugImplementation(py_cui.ui.MenuImplementation)

```python
class LiveDebugImplementation(py_cui.ui.MenuImplementation)
```

Implementation class for the live debug menu - builds off of the scroll menu implementation




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 level  |  int | Debug level at which to display messages. Can be separate from the default logging level
 _buffer_size  |  List[str] | Number of log messages to keep buffered in the live debug window

#### Methods

 Method  | Doc
-----|-----
 print_to_buffer | Override of default MenuImplementation add_item function




### __init__

```python
def __init__(self, parent_logger)
```

Initializer for LiveDebugImplementation







### print_to_buffer

```python
def print_to_buffer(self, msg: str, log_level) -> None
```

Override of default MenuImplementation add_item function



If items override the buffer pop the oldest log message


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 msg  |  str | Log message to add








## LiveDebugElement(py_cui.ui.UIElement, LiveDebugImplementation)

```python
class LiveDebugElement(py_cui.ui.UIElement, LiveDebugImplementation)
```

UIElement class for the live debug utility. extends from base UIElement class and LiveDebugImplementation



#### Methods

 Method  | Doc
-----|-----
 get_absolute_start_pos | Override of base UI element class function. Sets start position relative to entire UI size
 get_absolute_stop_pos | Override of base UI element class function. Sets stop position relative to entire UI size
 _handle_mouse_press | Override of base class function, handles mouse press in menu
 _handle_key_press | Override of base class function.
 _draw | Overrides base class draw function. Mostly a copy of ScrollMenu widget - but reverse item list




### __init__

```python
def __init__(self, parent_logger)
```

Initializer for LiveDebugElement class







### get_absolute_start_pos

```python
def get_absolute_start_pos(self) -> Tuple[int,int]
```

Override of base UI element class function. Sets start position relative to entire UI size




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 start_x, start_y  |  int, int | Start position x, y coords in terminal characters





### get_absolute_stop_pos

```python
def get_absolute_stop_pos(self) -> Tuple[int,int]
```

Override of base UI element class function. Sets stop position relative to entire UI size




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 stop_x, stop_y  |  int, int | Stop position x, y coords in terminal characters





### _handle_mouse_press

```python
def _handle_mouse_press(self, x: int, y: int, mouse_event: int) -> None
```

Override of base class function, handles mouse press in menu




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 x, y  |  int | Coordinates of mouse press
 mouse_event  |  int | Key code for py_cui mouse event





### _handle_key_press

```python
def _handle_key_press(self, key_pressed: int) -> None
```

Override of base class function.



Essentially the same as the ScrollMenu widget _handle_key_press, with the exception that Esc breaks
out of live debug mode.


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | The keycode of the pressed key





### _draw

```python
def _draw(self) -> None
```

Overrides base class draw function. Mostly a copy of ScrollMenu widget - but reverse item list










## PyCUILogger(logging.Logger)

```python
class PyCUILogger(logging.Logger)
```

Custom logger class for py_cui, extends the base logging.Logger Class




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 py_cui_root  |  py_cui.PyCUI | The root py_cui program for which the logger runs
 live_debug  |  bool | Flag to toggle live debugging messages

#### Methods

 Method  | Doc
-----|-----
 is_live_debug_enabled |
 toggle_live_debug |
 draw_live_debug | Function that draws the live debug UI element if applicable
 _assign_root_window | Function that assigns a PyCUI root object to the logger. Important for live-debug hooks
 _get_debug_text | Function that generates full debug text for the log
 info | Override of base logger info function to add hooks for live debug mode
 debug | Override of base logger debug function to add hooks for live debug mode
 warn | Override of base logger warn function to add hooks for live debug mode
 error | Override of base logger error function to add hooks for live debug mode
 critical | Override of base logger critical function to add hooks for live debug mode




### __init__

```python
def __init__(self, name)
```

Initializer for the PyCUILogger helper class




#### Raises

 Error  | Type  | Doc
-----|----------|-----
 Unknown | TypeError | If root variable instance is not a PyCUI object raise a typeerror





### is_live_debug_enabled

```python
def is_live_debug_enabled(self)
```









### toggle_live_debug

```python
def toggle_live_debug(self)
```









### draw_live_debug

```python
def draw_live_debug(self)
```

Function that draws the live debug UI element if applicable







### _assign_root_window

```python
def _assign_root_window(self, py_cui_root: 'py_cui.PyCUI') -> None
```

Function that assigns a PyCUI root object to the logger. Important for live-debug hooks




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 py_cui_root  |  PyCUI | Root PyCUI object for the application





### _get_debug_text

```python
def _get_debug_text(self, text: str) -> str
```

Function that generates full debug text for the log




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | Log message

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 msg  |  str | Log message with function, file, and line num info





### info

```python
def info(self, msg: Any, *args, **kwargs) -> None : # to overcome signature mismatch in erro
```

Override of base logger info function to add hooks for live debug mode




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | The log text ot display





### debug

```python
def debug(self, msg: str, *args, **kwargs) -> None
```

Override of base logger debug function to add hooks for live debug mode




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | The log text ot display





### warn

```python
def warn(self, msg: str, *args, **kwargs) -> None
```

Override of base logger warn function to add hooks for live debug mode




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | The log text ot display





### error

```python
def error(self, msg: str, *args, **kwargs) -> None
```

Override of base logger error function to add hooks for live debug mode




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | The log text ot display





### critical

```python
def critical(self, msg: str, *args, **kwargs) -> None
```

Override of base logger critical function to add hooks for live debug mode




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | The log text ot display








