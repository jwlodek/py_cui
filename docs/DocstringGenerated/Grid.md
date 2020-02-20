# grid

File containing the Grid Class.



The grid is currently the only supported layout manager for py_cui

@author:    Jakub Wlodek  
@created:   12-Aug-2019




## Grid

```python
class Grid
```

Class representing the CUI grid




#### Attributes

 Attribute  | Type  | Doc
-----|----------|----------|-----
 num_rows  |  int | Number of grid rows
 num_columns  |  int | Number of grid columns
 height  |  int | The height in characters of the terminal window
 width  |  int | The width in characters of the terminal window
 offset_y  |  int | The number of additional characters found by height mod rows
 offset_x  |  int | The number of additional characters found by width mod columns
 row_height  |  int | The number of characters in a single grid row
 column_width  |  int | The number of characters in a single grid column

#### Methods

 Method  | Doc
-----|----------|-----
 set_num_rows | Sets the grid row size
 set_num_cols | Sets the grid column size
 update_grid_height_width | Update grid height and width. Allows for on-the-fly size editing




### __init__

```python
def __init__(self, num_rows, num_columns, height, width)
```

Constructor for the Grid class




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 num_rows  |  int | Number of grid rows
 num_columns  |  int | Number of grid columns
 height  |  int | The height in characters of the terminal window
 width  |  int | The width in characters of the terminal window





### set_num_rows

```python
def set_num_rows(self, num_rows)
```

Sets the grid row size




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 num_rows  |  int | New number of grid rows
 Raises | ------
 error  |  PyCUIOutOfBoundsError | If the size of the terminal window is too small





### set_num_cols

```python
def set_num_cols(self, num_columns)
```

Sets the grid column size




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 num_columns  |  int | New number of grid columns
 Raises | ------
 error  |  PyCUIOutOfBoundsError | If the size of the terminal window is too small





### update_grid_height_width

```python
def update_grid_height_width(self, height, width)
```

Update grid height and width. Allows for on-the-fly size editing




#### Parameters

 Parameter  | Type  | Doc
-----|----------|----------|-----
 height  |  int | The height in characters of the terminal window
 width  |  int | The width in characters of the terminal window
 Raises | ------
 error  |  PyCUIOutOfBoundsError | If the size of the terminal window is too small








