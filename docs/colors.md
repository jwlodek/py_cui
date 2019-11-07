# Using colors in a py_cui

Colors in `py_cui` based interfaces are handled wither by widget level color choices, or by text color rules. In the case of widget coloring, you may set the `Widget.color` attribute to one of the supported color pairs. Color rules on the other hand are assigned to widgets, and relate to the text drawn within the widget. 

### Supported Colors

All colors in the `py_cui` library are represented as pairs, a foreground and background color. Below is a list of supported color pairs:

Color Pair | Foreground (Text) Color | Background Color
----------------|-|-
WHITE_ON_BLACK   | WHITE | BLACK
BLACK_ON_GREEN   |BLACK |GREEN
BLACK_ON_WHITE   |BLACK | WHITE
WHITE_ON_RED     |WHITE|RED
YELLOW_ON_BLACK  |YELLOW |BLACK
RED_ON_BLACK     |RED|BLACK
CYAN_ON_BLACK    |CYAN|BLACK
MAGENTA_ON_BLACK |MAGENTA|BLACK
GREEN_ON_BLACK   |GREEN|BLACK
BLUE_ON_BLACK    |BLUE|BLACK

### Using Color Rules

There are severl possible color rules that can be added to a py_cui widget, and these are classified under:
* Rule Type - How we attempt to match a text line with a given regular expression
* Match Type - How the resulting matched text is rendered

**Rule Types**

Rule Type | Explanation
-|-
startswith | check if string starts with regex
endswith | check if string ends with regex
notstartswith | check if string doesn't start with regex
notendswith | check if string doesn't end with regex
contains | check if regex is contained within line

**Match Type**

Match Type | Explanation
-|-
line | Color the entire line given color if matched
region | Color specified region if matched. For example a region of (0,3) would color the first 3 characters
regex | Color the matched regex only

**Examples**

```
self.text_block.add_text_color_rule('+', py_cui.GREEN_ON_BLACK, 'startswith')
```
In the above example, all lines that start with a '+' symbol will be green. The default match type is line, meaning that the entire line will be colored in the event of a rule match.

```
self.menu.add_text_color_rule('?', py_cui.GREEN_ON_BLACK, 'notstartswith', match_type='region', region=[0,3], include_whitespace=True)
```
For this color rule, all lines that don't start with a `?` will have their first three characters colored green.

```
self.text_block.add_text_color_rule('@.*@', py_cui.CYAN_ON_BLACK, 'contains', match_type='regex')
```
The above color rule will color all matches of @ ... @ cyan in the text of the textblock.
