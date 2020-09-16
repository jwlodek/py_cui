# Using colors in a py_cui

Colors in `py_cui` based interfaces are handled by widget level color choices, or by text color rules. In the case of widget coloring, you may use the `Widget.set_color` function, and pass in one of the supported color pairs. Color rules on the other hand are assigned to widgets, and relate to the text drawn within the widget. 

### Supported Colors

All colors in the `py_cui` library are represented as pairs, a foreground and background color. Below is a list of supported colors:

* Black
* White
* Red
* Green
* Blue
* Magenta
* Yellow
* Cyan

Each of these colors can either be a foreground or background color, in any combination. To access a specific color pair, use py_cui.FOREGROUND_ON_BACKGROUND.
For example, a simple white on black classic terminal color would be `py_cui.WHITE_ON_BLACK`. This is also the default color for all UI elements.

### UI Element Color Customization

You may set three individual color attributes for UI elements, in addition to more complex color rules described below. You may set the following:

* Border Color
* Text Color
* Selected Text Color

Overall UI color is applied by default to all three attributes, unless one is specifically set. Use the dedicated getter/setter methods for UI element
objects to adjust these attributes.

### Using Color Rules

In addition to setting the default color for certain UI elements, in many cases it is important to gain a more fine control over
widget coloration, and color rules aim to achive this by allowing for defining color logic depending on matches against regular
expressions.

There are several possible color rules that can be added to a py_cui widget, and these are classified under:

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

In addition, if your widget uses selected text and you wish for it to apply a different color in that case, an additional parameter is 
passed into the `add_text_color_rule` function, namely: `selected_color=py_cui.GREEN_ON_WHITE`, specifying the color of the match 
in the event that text is selected. This is important, for example, for color rules applied to scroll menus, since the current position in
the menu is rendered as "selected" text.
