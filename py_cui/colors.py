"""
File containing all error types for py_cui

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""

# TODO - these are currently not very intuitive or efficient


import py_cui
import re


class ColorRule:

    def __init__(self, regex, color, rule_type, match_type, region, include_whitespace):
        self.regex = regex
        self.color = color
        self.rule_type = rule_type
        self.match_type = match_type
        self.region = region
        self.include_whitespace = include_whitespace

    def check_match(self, line):
        temp = line
        if not self.include_whitespace:
            temp = temp.strip()
        if self.rule_type == 'startswith':
            if temp.startswith(self.regex):
                return True
        elif self.rule_type == 'endswith':
            if temp.endswith(self.regex):
                return True
        elif self.rule_type == 'notstartswith':
            if temp.startswith(self.regex):
                return False
            return True
        elif self.rule_type == 'notendswith':
            if temp.endswith(self.regex):
                return False
            return True
        elif self.rule_type == 'contains':
            if re.search(self.regex, line) is not None:
                return True
        return False


    def generate_fragments_regex(self, widget, render_text):
        fragments = []
        matches = re.findall(self.regex, render_text)
        current_render_text = render_text
        for match in matches:
            temp = current_render_text.split(match, 1)
            if len(temp) == 2:
                fragments.append([temp[0], widget.color])
                fragments.append([match, self.color])
                current_render_text = temp[1]
        fragments.append([current_render_text, widget.color])

        return fragments


    def split_text_on_region(self, widget, render_text):

        fragments = []
        if self.region[0] != 0:
            fragments.append([render_text[0:self.region[0]], widget.color])
        fragments.append([render_text[self.region[0]:self.region[1]], self.color])
        fragments.append([render_text[self.region[1]:], widget.color])
        return fragments



# THE FUNCTIONS BELOW GET LISTS OF COLOR RULES TO APPLY LANGUAGE SYNTAX HIGHLIGHTING
# FOR py_cui TEXT. RUN widget.add_color_rules(py_cui.colors.get_LANGUAGE_highlighting_rules())
# To get lanuage syntax highlighting.

# DO NOT WORK YET

#def get_python_highlighting_rules():
#    color_rules = []
#    python_keywords = ['class', 'pass', 'raise', 'def', 'import', 'if', 'for', 'as', 'else', 'elif', 'return', 'for', 'in', 'and', 'or', ]
#    python_constants = ['True', 'False', 'None']
#    #python_strings = ['".*"', "'.*'"]
#    color_rules.append(ColorRule(python_keywords, py_cui.CYAN_ON_BLACK, 'contains', 'regex', None, False))
#    color_rules.append(ColorRule(python_constants, py_cui.MAGENTA_ON_BLACK, 'contains', 'regex', None, False))
#    color_rules.append(ColorRule(['#'], py_cui.RED_ON_BLACK, 'startswith', 'line', None, False))
#    color_rules.append(ColorRule(['"""'], py_cui.GREEN_ON_BLACK, 'block', 'block', None, False))
#    #color_rules.append(ColorRule(python_strings, py_cui.GREEN_ON_BLACK, 'contains', 'line', None, False))
#    return color_rules