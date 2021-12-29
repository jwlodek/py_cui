# colors

Module containing color rule class and any color-rendering related functions and variables



#### Classes

 Class  | Doc
-----|-----
 ColorRule | Class representing a text color rendering rule




## ColorRule

```python
class ColorRule
```

Class representing a text color rendering rule




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 regex  |  str | A python 're' module string
 color  |  int | A valid color value. Ex. py_cui.WHITE_ON_BLACK
 rule_type  |  str | String representing rule type. ['startswith', 'endswith', 'notstartswith', 'notendswith', 'contains']
 match_type  |  str | String representing the match type. ['line', 'regex', 'region']
 region  |  [int, int] | Start and end positions for the coloring, None if match_type != 'region'
 include_whitespace  |  bool | Flag to determine whether to strip whitespace before matching.

#### Methods

 Method  | Doc
-----|-----
 _check_match | Checks if the color rule matches a line
 _generate_fragments_regex | Splits text into fragments based on regular expression
 _split_text_on_region | Splits text into fragments based on region
 generate_fragments | Splits text into fragments if matched line to regex




### __init__

```python
def __init__(self, regex: str, color: int, selected_color: int, rule_type: str, match_type: str, region: List[int], include_whitespace: bool, logger)
```

Constructor for ColorRule object




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 regex  |  str | A python 're' module string
 color  |  int | A valid color value. Ex. py_cui.WHITE_ON_BLACK
 selected_color  |  int | Color to use if rule matched but selected modifier is applied
 rule_type  |  str | String representing rule type. ['startswith', 'endswith', 'notstartswith', 'notendswith', 'contains']
 match_type  |  str | String representing the match type. ['line', 'regex', 'region']
 region  |  [int, int] | Start and end positions for the coloring, None if match_type != 'region'
 include_whitespace  |  bool | Flag to determine whether to strip whitespace before matching.





### _check_match

```python
def _check_match(self, line: str) -> bool
```

Checks if the color rule matches a line




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 line  |  str | The input line of text to try to match the rule against

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 matched  |  bool | True if a match was found, false otherwise





### _generate_fragments_regex

```python
def _generate_fragments_regex(self, widget: Union['py_cui.widgets.Widget','py_cui.ui.UIElement'], render_text:str, selected) -> List[List[Union[int,str]]]
```

Splits text into fragments based on regular expression




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 widget  |  py_cui.Widget | Widget containing the render text
 render_text  |  str | text being rendered

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 fragments  |  list of lists of [str, color] | the render text split into fragments of strings paired with colors





### _split_text_on_region

```python
def _split_text_on_region(self, widget: Union['py_cui.widgets.Widget','py_cui.ui.UIElement'], render_text: str, selected) -> List[List[Union[str,int]]]:   # renderer._generate_text_color_fragments passes a uielement and not a widge
```

Splits text into fragments based on region




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 widget  |  py_cui.Widget | Widget containing the render text
 render_text  |  str | text being rendered

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 fragments  |  list of lists of [str, color] | the render text split into fragments of strings paired with colors





### generate_fragments

```python
def generate_fragments(self, widget: Union['py_cui.widgets.Widget','py_cui.ui.UIElement'], line: str, render_text: str, selected=False) -> Tuple[List[List[Union[str,int]]],bool]
```

Splits text into fragments if matched line to regex




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 widget  |  py_cui.Widget | Widget containing the render text
 line  |  str | the line to match
 render_text  |  str | text being rendered

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 fragments  |  List[List[str, color]] | the render text split into fragments of strings paired with colors
 matched  |  bool | Boolean output saying if a match was found in the line.








