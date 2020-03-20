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
    """

    def __init__(self, regex, color, rule_type, match_type, region, include_whitespace, logger):
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
        
        self._regex            = regex
        self._color            = color
        self._rule_type        = rule_type
        self._match_type       = match_type
        self._region           = region

        if self._region is not None:
            if self._region[0] > self._region[1]:
                temp = region[0]
                self._region[0] = self._region[1]
                self._region[1] = temp

        self._include_whitespace   = include_whitespace
        self._logger               = logger


    def _check_match(self, line):
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
        if not self._include_whitespace:
            temp = temp.strip()
        if self._rule_type == 'startswith':
            if temp.startswith(self._regex):
                return True
        elif self._rule_type == 'endswith':
            if temp.endswith(self._regex):
                return True
        elif self._rule_type == 'notstartswith':
            if temp.startswith(self._regex):
                return False
            return True
        elif self._rule_type == 'notendswith':
            if temp.endswith(self._regex):
                return False
            return True
        elif self._rule_type == 'contains':
            if re.search(self._regex, line) is not None:
                return True
        return False


    def _generate_fragments_regex(self, widget, render_text):
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
        matches = re.findall(self._regex, render_text)
        current_render_text = render_text
        for match in matches:
            temp = current_render_text.split(match, 1)
            if len(temp) == 2:
                fragments.append([temp[0], widget.color])
                fragments.append([match, self._color])
                current_render_text = temp[1]
        fragments.append([current_render_text, widget.color])

        return fragments


    def _split_text_on_region(self, widget, render_text):
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
        if self._region is None or len(render_text) < self._region[0]:
            return [[render_text, widget.color]]
        elif len(render_text) < self._region[1]:
            self._region[1] = len(render_text)
        if self._region[0] != 0:
            fragments.append([render_text[0:self._region[0]], widget.color])
        fragments.append([render_text[self._region[0]:self._region[1]], self._color])
        fragments.append([render_text[self._region[1]:], widget.color])

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
        fragments : List[List[str, color]]
            the render text split into fragments of strings paired with colors
        matched : bool
            Boolean output saying if a match was found in the line.
        """

        match       = self._check_match(line)
        fragments   = [[render_text, widget.color]]
        
        if match:

            if self._match_type == 'line':
                fragments = [[render_text, self._color]]
            elif self._match_type == 'regex':
                fragments = self._generate_fragments_regex(widget, render_text)
            elif self._match_type == 'region':
                fragments = self._split_text_on_region(widget, render_text)
        
            self._logger.info('Generated fragments: {}'.format(fragments))
        
        return fragments, match