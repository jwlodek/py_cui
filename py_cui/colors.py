"""
File containing all error types for py_cui

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""


import py_cui
import re


class ColorRule:

    def __init__(self, regex_list, color, rule_type, match_type, region, include_whitespace):
        self.regex_list = regex_list
        self.color = color
        self.rule_type = rule_type
        self.match_type = match_type
        self.region = region
        self.include_whitespace = include_whitespace


    def add_regex(self, regex):
        self.regex_list.append(regex)


    def add_regex_list(self, regex_list):
        self.regex_list = self.regex_list + regex_list




    def match_starts_with(self, line):
        color_region_list = []
        temp = line
        if not self.include_whitespace:
            temp = temp.strip()
        for regex in self.regex_list:
            if temp.startswith(regex):
                color_region_list.append([self.color])


    def check_match(self, line):
        temp = line
        if not self.include_whitespace:
            temp = temp.strip()
        if self.rule_type == 'startswith':
            for regex in self.regex_list:
                if temp.startswith(regex):
                    return True
        elif self.rule_type == 'endswith':
            for regex in self.regex_list:
                if temp.endswith(regex):
                    return True
        elif self.rule_type == 'notstartswith':
            for regex in self.regex_list:
                if temp.startswith(regex):
                    return False
            return True
        elif self.rule_type == 'notendswith':
            for regex in self.regex_list:
                if temp.startswith(regex):
                    return False
            return True
        elif self.rule_type == 'contains':
            for regex in self.regex_list:
                if regex in temp:
                    return True
        return False


    def split_text_on_region(self, widget, render_text):

        fragments = []
        if self.region[0] != 0:
            fragments.append([render_text[0:self.region[0], widget.color, [0, self.region[0]]]])
        fragments.append([render_text[self.region[0]:self.region[1]], self.color, self.region])
        fragments.append([render_text[self.region[1]:], widget.color, [self.region[1], len(render_text)]])
        return fragments

# THE FUNCTIONS BELOW GET LISTS OF COLOR RULES TO APPLY LANGUAGE SYNTAX HIGHLIGHTING
# FOR py_cui TEXT. RUN widget.add_color_rules(py_cui.colors.get_LANGUAGE_highlighting_rules())
# To get lanuage syntax highlighting.

def get_python_highlighting_rules():
    color_rules = []
    python_keywords = ['def', 'import', 'if', 'for', 'as', 'else', 'elif', 'return', 'for', 'in', 'and', 'or']
    python_constants = ['True', 'False', 'None']
    python_strings = ['".*"', "'.*'"]
    color_rules.append(ColorRule(python_keywords, py_cui.CYAN_ON_BLACK, 'contains', 'regex', None, False))
    color_rules.append(ColorRule(python_constants, py_cui.MAGENTA_ON_BLACK, 'contains', 'regex', None, False))
    color_rules.append(ColorRule(['#'], py_cui.RED_ON_BLACK, 'startswith', 'line', None, False))
    color_rules.append(ColorRule(python_strings, py_cui.GREEN_ON_BLACK, 'contains', 'line', None, False))