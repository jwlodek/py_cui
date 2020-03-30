# debug

Module containing py_cui logging utilities



#### Classes

 Class  | Doc
-----|-----
 PyCUILogger(logging.Logger) | Custom logger class for py_cui, extends the base logging.Logger Class

#### Functions

 Function  | Doc
-----|-----
 _enable_logging | Function that creates basic logging configuration for selected logger
 _initialize_logger | Function that retrieves an instance of either the default or custom py_cui logger.




### _enable_logging

```python
def _enable_logging(logger, filename='py_cui_log.txt', logging_level=logging.DEBUG)
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
def _initialize_logger(py_cui_root, name=None, custom_logger=True)
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
 _assign_root_window | Attaches logger to the root window for live debugging
 _get_debug_text | Function that generates full debug text for the log
 info | Adds stacktrace info to log
 debug | Function that allows for live debugging of py_cui programs by displaying log messages in the satus bar
 warn | Function that allows for live debugging of py_cui programs by displaying log messages in the satus bar
 error | Function that displays error messages live in status bar for py_cui logging
 toggle_live_debug | Toggles live debugging mode




### __init__

```python
def __init__(self, name)
```

Initializer for the PyCUILogger helper class




#### Raises

 Error  | Type  | Doc
-----|----------|-----
 Unknown | TypeError | If root variable instance is not a PyCUI object raise a typeerror





### _assign_root_window

```python
def _assign_root_window(self, py_cui_root)
```

Attaches logger to the root window for live debugging







### _get_debug_text

```python
def _get_debug_text(self, text)
```

Function that generates full debug text for the log







### info

```python
def info(self, text)
```

Adds stacktrace info to log




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | The log text ot display





### debug

```python
def debug(self, text)
```

Function that allows for live debugging of py_cui programs by displaying log messages in the satus bar




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | The log text ot display





### warn

```python
def warn(self, text)
```

Function that allows for live debugging of py_cui programs by displaying log messages in the satus bar




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | The log text ot display





### error

```python
def error(self, text)
```

Function that displays error messages live in status bar for py_cui logging




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | The log text ot display





### toggle_live_debug

```python
def toggle_live_debug(self, level=logging.ERROR)
```

Toggles live debugging mode










