# File containing the Grid Class.


The grid is currently the only supported layout manager for py_cui

@author:Jakub Wlodek
@created: 12-Aug-2019


# Grid 

``` python 
 class Grid 
```

Class representing the CUI gri.

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     num_rows | int |         Number of grid rows | 
|     num_columns | int |         Number of grid columns | 
|     height | int |         The height in characters of the terminal window | 
|     width | int |         The width in characters of the terminal window | 
|     offset_y | int |         The number of additional characters found by height mod rows | 
|     offset_x | int |         The number of additional characters found by width mod columns | 
|     row_height | int |         The number of characters in a single grid row | 
|     column_width | int |         The number of characters in a single grid column     | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| set_num_rows | Sets the grid row siz. | 
| set_num_cols | Sets the grid column siz. | 
| update_grid_height_width | Update grid height and width. Allows for on-the-fly size editin. | 
 
 

### set_num_rows

``` python 
    set_num_rows(num_rows) 
```


Sets the grid row siz.



| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         num_rows | int |             New number of grid rows | 


### set_num_cols

``` python 
    set_num_cols(num_columns) 
```


Sets the grid column siz.



| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         num_columns | int |             New number of grid columns         | 


### update_grid_height_width

``` python 
    update_grid_height_width(height, width) 
```


Update grid height and width. Allows for on-the-fly size editin.



| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         height | int |             The height in characters of the terminal window | 
|         width | int |             The width in characters of the terminal window | 
