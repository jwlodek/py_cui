# File containing color rule class and any color-rendering related function


@author:Jakub Wlodek
@created: 12-Aug-2019


# ColorRule 

``` python 
 class ColorRule 
```

Class representing a text color rendering rul.

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     regex | str |         A python 're' module string | 
|     color | int |         A valid color value. Ex. py_cui.WHITE_ON_BLACK | 
|     rule_type | str |         String representing rule type. ['startswith', 'endswith', 'notstartswith', 'notendswith', 'contains'] | 
|     match_type | str |         String representing the match type. ['line', 'regex', 'region'] | 
|     region | [int, int] |         Start and end positions for the coloring, None if match_type != 'region' | 
|     include_whitespace | bool |         Flag to determine whether to strip whitespace before matching. | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| check_match | Checks if the color rule matches a lin. | 
| generate_fragments_regex | Splits text into fragments based on regular expressio. | 
| split_text_on_region | Splits text into fragments based on regio. | 
| generate_fragments | Splits text into fragments if matched line to rege. | 
 
 

### check_match

``` python 
    check_match(line) 
```


Checks if the color rule matches a lin.



| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         line | str |             The input line of text to try to match the rule against | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         matched | bool |             True if a match was found, false otherwise | 


### generate_fragments_regex

``` python 
    generate_fragments_regex(widget, render_text) 
```


Splits text into fragments based on regular expressio.



| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         widget | py_cui.Widget |             Widget containing the render text | 
|         render_text | str |             text being rendered | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         fragments | list of lists of [str, color] |             the render text split into fragments of strings paired with colors | 


### split_text_on_region

``` python 
    split_text_on_region(widget, render_text) 
```


Splits text into fragments based on regio.



| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         widget | py_cui.Widget |             Widget containing the render text | 
|         render_text | str |             text being rendered | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         fragments | list of lists of [str, color] |             the render text split into fragments of strings paired with colors | 


### generate_fragments

``` python 
    generate_fragments(widget, line, render_text) 
```


Splits text into fragments if matched line to rege.



| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         widget | py_cui.Widget |             Widget containing the render text | 
|         line | str |             the line to match | 
|         render_text | str |             text being rendered | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         fragments | list of lists of [str, color] |             the render text split into fragments of strings paired with colors | 
|         matched | bool |             Boolean output saying if a match was found in the line. | 
