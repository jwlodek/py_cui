"""
File containing all error types for py_cui

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""


import py_cui
import re


class ColorRule:

    def __init__(self, regex, color, rule_type, match_type, region, include_whitespace):
        self.regex = regex
        self.color = color
        self.rule_type = rule_type
        self.match_type = match_type
        self.region = region
        if self.region is not None:
            if self.region[0] > self.region[1]:
                temp = region[0]
                self.region[0] = self.region[1]
                self.region[1] = temp
        self.include_whitespace = include_whitespace


    def check_match(self, line):
        """ Checks if the color rule matches a line """

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
        """ Splits text into fragments based on regular expression """

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
        """ Splits text into fragments based on region """

        fragments = []
        if self.region is None or len(render_text) < self.region[1]:
            return [[render_text, widget.color]]
        if self.region[0] != 0:
            fragments.append([render_text[0:self.region[0]], widget.color])
        fragments.append([render_text[self.region[0]:self.region[1]], self.color])
        fragments.append([render_text[self.region[1]:], widget.color])
        return fragments


    def generate_fragments(self, widget, line, render_text):

        match = self.check_match(line)
        if match:

            if self.match_type == 'line':
                return [[render_text, self.color]], True
            elif self.match_type == 'regex':
                return self.generate_fragments_regex(widget, render_text), True
            elif self.match_type == 'region':
                return self.split_text_on_region(widget, render_text), True
    
        return [[render_text, widget.color]], False