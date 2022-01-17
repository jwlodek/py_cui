# grid

File containing the Grid Class.



The grid is currently the only supported layout manager for py_cui

#### Classes

 Class  | Doc
-----|-----
 Grid | Class representing the CUI grid




## Grid

```python
class Grid
```

Class representing the CUI grid




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _num_rows, _num_columns  |  int | Number of grid rows and columns
 _height, _width  |  int | The height, width in characters of the terminal window
 _offset_y, _offset_x  |  int | The number of additional characters found by height mod rows and width mod columns
 _row_height, _column_width  |  int | The number of characters in a single grid row, column
 _title_bar_offset  |  int | Title bar row offset. Defaults to 1. Set to 0 if title bar is hidden.
 _logger  |  py_cui.debug.PyCUILogger | logger object for maintaining debug messages

#### Methods

 Method  | Doc
-----|-----
 get_dimensions | Gets dimensions in rows/columns
 get_dimensions_absolute | Gets dimensions of grid in terminal characters
 get_offsets | Gets leftover characters for x and y
 get_cell_dimensions | Gets size in characters of single (row, column) cell location
 set_num_rows | Sets the grid row size
 set_num_cols | Sets the grid column size
 update_grid_height_width | Update grid height and width. Allows for on-the-fly size editing




### __init__

```python
def __init__(self, num_rows: int, num_columns: int, height: int, width: int, logger: 'py_cui.debug.PyCUILogger')
```

Constructor for the Grid class




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 num_rows  |  int | Number of grid rows
 num_columns  |  int | Number of grid columns
 height  |  int | The height in characters of the terminal window
 width  |  int | The width in characters of the terminal window





### get_dimensions

```python
def get_dimensions(self) -> Tuple[int,int]
```

Gets dimensions in rows/columns




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 num_rows  |  int | size of grid in rows
 num_cols  |  int | size of grid in columns





### get_dimensions_absolute

```python
def get_dimensions_absolute(self) -> Tuple[int,int]
```

Gets dimensions of grid in terminal characters




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 height  |  int | height in characters
 width  |  int | width in characters





### get_offsets

```python
def get_offsets(self) -> Tuple[int,int]
```

Gets leftover characters for x and y




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 offset_x  |  int | leftover chars in x direction
 offset_y  |  int | leftover chars in y direction





### get_cell_dimensions

```python
def get_cell_dimensions(self) -> Tuple[int,int]
```

Gets size in characters of single (row, column) cell location




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 row_height  |  int | height of row in characters
 column_width  |  int | width of column in characters





### set_num_rows

```python
def set_num_rows(self, num_rows: int) -> None
```

Sets the grid row size




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 num_rows  |  int | New number of grid rows

#### Raises

 Error  | Type  | Doc
-----|----------|-----
 error  |  PyCUIOutOfBoundsError | If the size of the terminal window is too small





### set_num_cols

```python
def set_num_cols(self, num_columns: int) -> None
```

Sets the grid column size




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 num_columns  |  int | New number of grid columns

#### Raises

 Error  | Type  | Doc
-----|----------|-----
 error  |  PyCUIOutOfBoundsError | If the size of the terminal window is too small





### update_grid_height_width

```python
def update_grid_height_width(self, height: int, width: int)
```

Update grid height and width. Allows for on-the-fly size editing




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 height  |  int | The height in characters of the terminal window
 width  |  int | The width in characters of the terminal window

#### Raises

 Error  | Type  | Doc
-----|----------|-----
 error  |  PyCUIOutOfBoundsError | If the size of the terminal window is too small








