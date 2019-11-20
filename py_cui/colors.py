"""File containing color rule class and any color-rendering related functions

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""


import py_cui
import re


class ColorRule:
    """Class representing a text color rendering rule

    Attributes
    ----------
    regex : str
        A python 're' module string
    color : int
        A valid color value. Ex. py_cui.WHITE_ON_BLACK
    rule_type : str
        String representing rule type. ['startswith', 'endswith', 'notstartswith', 'notendswith', 'contains']
    match_type : str
        String representing the match type. ['line', 'regex', 'region']
    region : [int, int]
        Start and end positions for the coloring, None if match_type != 'region'
    include_whitespace : bool
        Flag to determine whether to strip whitespace before matching.

    Methods
    -------
    check_match()
        Function that checks if the regex given matches the input line given the rule type
    generate_fragments_regex()
        Splits text into color coded renderable fragments based on regular expression
    split_text_on_region()
        Splits text into color coded renderable fragments based on region
    generate_fragments()
        Checks match of rule with line, then splits render_text into fragments if required
    """

    def __init__(self, regex, color, rule_type, match_type, region, include_whitespace):
        """Constructor for ColorRule object
            
        Parameters
        ----------
        regex : str
            A python 're' module string
        color : int
            A valid color value. Ex. py_cui.WHITE_ON_BLACK
        rule_type : str
            String representing rule type. ['startswith', 'endswith', 'notstartswith', 'notendswith', 'contains']
        match_type : str
            String representing the match type. ['line', 'regex', 'region']
        region : [int, int]
            Start and end positions for the coloring, None if match_type != 'region'
        include_whitespace : bool
            Flag to determine whether to strip whitespace before matching.
        """
        
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
        """Checks if the color rule matches a line
        
        Parameters
        ----------
        line : str
            The input line of text to try to match the rule against

        Returns
        -------
        matched : bool
            True if a match was found, false otherwise
        """

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
        """Splits text into fragments based on regular expression
        
        Parameters
        ----------
        widget : py_cui.Widget
            Widget containing the render text
        render_text : str
            text being rendered

        Returns
        -------
        fragments : list of lists of [str, color]
            the render text split into fragments of strings paired with colors
        """

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
        """Splits text into fragments based on region
        
        Parameters
        ----------
        widget : py_cui.Widget
            Widget containing the render text
        render_text : str
            text being rendered

        Returns
        -------
        fragments : list of lists of [str, color]
            the render text split into fragments of strings paired with colors
        """

        fragments = []
        if self.region is None or len(render_text) < self.region[0]:
            return [[render_text, widget.color]]
        elif len(render_text) < self.region[1]:
            self.region[1] = len(render_text)
        if self.region[0] != 0:
            fragments.append([render_text[0:self.region[0]], widget.color])
        fragments.append([render_text[self.region[0]:self.region[1]], self.color])
        fragments.append([render_text[self.region[1]:], widget.color])
        return fragments


    def generate_fragments(self, widget, line, render_text):
        """Splits text into fragments if matched line to regex
        
        Parameters
        ----------
        widget : py_cui.Widget
            Widget containing the render text
        line : str
            the line to match
        render_text : str
            text being rendered

        Returns
        -------
        fragments : list of lists of [str, color]
            the render text split into fragments of strings paired with colors
        matched : bool
            Boolean output saying if a match was found in the line.
        """

        match = self.check_match(line)
        if match:

            if self.match_type == 'line':
                return [[render_text, self.color]], True
            elif self.match_type == 'regex':
                return self.generate_fragments_regex(widget, render_text), True
            elif self.match_type == 'region':
                return self.split_text_on_region(widget, render_text), True
    
        return [[render_text, widget.color]], False