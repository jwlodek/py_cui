"""Module containing color rule class and any color-rendering related functions and variables
"""

# Author:    Jakub Wlodek
# Created:   12-Aug-2019


import py_cui
import curses
import re


# Curses color configuration - curses colors automatically work as pairs, so it was easiest to
# create these values as pairs off the bat to be selected.
# Format is FOREGROUND_ON_BACKGROUND

# Black background colors
WHITE_ON_BLACK      = 1
YELLOW_ON_BLACK     = 2
RED_ON_BLACK        = 3
CYAN_ON_BLACK       = 4
MAGENTA_ON_BLACK    = 5
GREEN_ON_BLACK      = 6
BLUE_ON_BLACK       = 7

# Green background colors
BLACK_ON_GREEN      = 8
WHITE_ON_GREEN      = 9
YELLOW_ON_GREEN     = 10
RED_ON_GREEN        = 11
CYAN_ON_GREEN       = 12
MAGENTA_ON_GREEN    = 13
BLUE_ON_GREEN       = 14

# White background colors
BLACK_ON_WHITE      = 15
YELLOW_ON_WHITE     = 16
RED_ON_WHITE        = 17
CYAN_ON_WHITE       = 18
GREEN_ON_WHITE      = 19
MAGENTA_ON_WHITE    = 20
BLUE_ON_WHITE       = 21

# Red background colors
WHITE_ON_RED        = 22
BLACK_ON_RED        = 23
YELLOW_ON_RED       = 24
CYAN_ON_RED         = 25
GREEN_ON_RED        = 26
BLUE_ON_RED         = 27
MAGENTA_ON_RED      = 28

# Cyan background colors
WHITE_ON_CYAN       = 29
BLACK_ON_CYAN       = 30
RED_ON_CYAN         = 31
YELLOW_ON_CYAN      = 32
MAGENTA_ON_CYAN     = 33
GREEN_ON_CYAN       = 34
BLUE_ON_CYAN        = 35

# Yellow background colors
BLACK_ON_YELLOW     = 36
WHITE_ON_YELLOW     = 37
RED_ON_YELLOW       = 38
GREEN_ON_YELLOW     = 39
BLUE_ON_YELLOW      = 40
CYAN_ON_YELLOW      = 41
MAGENTA_ON_YELLOW   = 42

# Magenta background colors
BLACK_ON_MAGENTA    = 43
WHITE_ON_MAGENTA    = 44
RED_ON_MAGENTA      = 45
GREEN_ON_MAGENTA    = 46
BLUE_ON_MAGENTA     = 47
YELLOW_ON_MAGENTA   = 48
CYAN_ON_MAGENTA     = 49

# Blue background colors
BLACK_ON_BLUE       = 50
WHITE_ON_BLUE       = 51
RED_ON_BLUE         = 52
GREEN_ON_BLUE       = 53
YELLOW_ON_BLUE      = 54
CYAN_ON_BLUE        = 55
MAGENTA_ON_BLUE     = 56

# Map the color pair variables to the appropriate curses colors.
# This is used as a part of CUI startup to initialize color options in curses.
_COLOR_MAP = {
    WHITE_ON_BLACK      : (curses.COLOR_WHITE, curses.COLOR_BLACK),
    YELLOW_ON_BLACK     : (curses.COLOR_YELLOW, curses.COLOR_BLACK),
    RED_ON_BLACK        : (curses.COLOR_RED, curses.COLOR_BLACK),
    CYAN_ON_BLACK       : (curses.COLOR_CYAN, curses.COLOR_BLACK),
    MAGENTA_ON_BLACK    : (curses.COLOR_MAGENTA, curses.COLOR_BLACK),
    GREEN_ON_BLACK      : (curses.COLOR_GREEN, curses.COLOR_BLACK),
    BLUE_ON_BLACK       : (curses.COLOR_BLUE, curses.COLOR_BLACK),
    BLACK_ON_GREEN      : (curses.COLOR_BLACK, curses.COLOR_GREEN),
    WHITE_ON_GREEN      : (curses.COLOR_WHITE, curses.COLOR_GREEN),
    YELLOW_ON_GREEN     : (curses.COLOR_YELLOW, curses.COLOR_GREEN),
    RED_ON_GREEN        : (curses.COLOR_RED, curses.COLOR_GREEN),
    CYAN_ON_GREEN       : (curses.COLOR_CYAN, curses.COLOR_GREEN),
    MAGENTA_ON_GREEN    : (curses.COLOR_MAGENTA, curses.COLOR_GREEN),
    BLUE_ON_GREEN       : (curses.COLOR_BLUE, curses.COLOR_GREEN),
    BLACK_ON_WHITE      : (curses.COLOR_BLACK, curses.COLOR_WHITE),
    YELLOW_ON_WHITE     : (curses.COLOR_YELLOW, curses.COLOR_WHITE),
    RED_ON_WHITE        : (curses.COLOR_RED, curses.COLOR_WHITE),
    CYAN_ON_WHITE       : (curses.COLOR_CYAN, curses.COLOR_WHITE),
    GREEN_ON_WHITE      : (curses.COLOR_GREEN, curses.COLOR_WHITE),
    MAGENTA_ON_WHITE    : (curses.COLOR_MAGENTA, curses.COLOR_WHITE),
    BLUE_ON_WHITE       : (curses.COLOR_BLUE, curses.COLOR_WHITE),
    WHITE_ON_RED        : (curses.COLOR_WHITE, curses.COLOR_RED),
    BLACK_ON_RED        : (curses.COLOR_BLACK, curses.COLOR_RED),
    YELLOW_ON_RED       : (curses.COLOR_YELLOW, curses.COLOR_RED),
    CYAN_ON_RED         : (curses.COLOR_CYAN, curses.COLOR_RED),
    GREEN_ON_RED        : (curses.COLOR_GREEN, curses.COLOR_RED),
    BLUE_ON_RED         : (curses.COLOR_BLUE, curses.COLOR_RED),
    MAGENTA_ON_RED      : (curses.COLOR_MAGENTA, curses.COLOR_RED),
    WHITE_ON_CYAN       : (curses.COLOR_WHITE, curses.COLOR_CYAN),
    BLACK_ON_CYAN       : (curses.COLOR_BLACK, curses.COLOR_CYAN),
    RED_ON_CYAN         : (curses.COLOR_RED, curses.COLOR_CYAN),
    YELLOW_ON_CYAN      : (curses.COLOR_YELLOW, curses.COLOR_CYAN),
    MAGENTA_ON_CYAN     : (curses.COLOR_MAGENTA, curses.COLOR_CYAN),
    GREEN_ON_CYAN       : (curses.COLOR_GREEN, curses.COLOR_CYAN),
    BLUE_ON_CYAN        : (curses.COLOR_BLUE, curses.COLOR_CYAN),
    BLACK_ON_YELLOW     : (curses.COLOR_BLACK, curses.COLOR_YELLOW),
    WHITE_ON_YELLOW     : (curses.COLOR_WHITE, curses.COLOR_YELLOW),
    RED_ON_YELLOW       : (curses.COLOR_RED, curses.COLOR_YELLOW),
    GREEN_ON_YELLOW     : (curses.COLOR_GREEN, curses.COLOR_YELLOW),
    BLUE_ON_YELLOW      : (curses.COLOR_BLUE, curses.COLOR_YELLOW),
    CYAN_ON_YELLOW      : (curses.COLOR_CYAN, curses.COLOR_YELLOW),
    MAGENTA_ON_YELLOW   : (curses.COLOR_MAGENTA, curses.COLOR_YELLOW),
    BLACK_ON_MAGENTA    : (curses.COLOR_BLACK, curses.COLOR_MAGENTA),
    WHITE_ON_MAGENTA    : (curses.COLOR_WHITE, curses.COLOR_MAGENTA),
    RED_ON_MAGENTA      : (curses.COLOR_RED, curses.COLOR_MAGENTA),
    GREEN_ON_MAGENTA    : (curses.COLOR_GREEN, curses.COLOR_MAGENTA),
    BLUE_ON_MAGENTA     : (curses.COLOR_BLUE, curses.COLOR_MAGENTA),
    YELLOW_ON_MAGENTA   : (curses.COLOR_YELLOW, curses.COLOR_MAGENTA),
    CYAN_ON_MAGENTA     : (curses.COLOR_CYAN, curses.COLOR_MAGENTA),
    BLACK_ON_BLUE       : (curses.COLOR_BLACK, curses.COLOR_BLUE),
    WHITE_ON_BLUE       : (curses.COLOR_WHITE, curses.COLOR_BLUE),
    RED_ON_BLUE         : (curses.COLOR_RED, curses.COLOR_BLUE),
    GREEN_ON_BLUE       : (curses.COLOR_GREEN, curses.COLOR_BLUE),
    YELLOW_ON_BLUE      : (curses.COLOR_YELLOW, curses.COLOR_BLUE),
    CYAN_ON_BLUE        : (curses.COLOR_CYAN, curses.COLOR_BLUE),
    MAGENTA_ON_BLUE     : (curses.COLOR_MAGENTA, curses.COLOR_BLUE),
}


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

    def __init__(self, regex, color, selected_color, rule_type, match_type, region, include_whitespace, logger):
        """Constructor for ColorRule object
            
        Parameters
        ----------
        regex : str
            A python 're' module string
        color : int
            A valid color value. Ex. py_cui.WHITE_ON_BLACK
        selected_color : int
            Color to use if rule matched but selected modifier is applied
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
        self._selected_color   = selected_color
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


    def _generate_fragments_regex(self, widget, render_text, selected):
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
                if selected:
                    fragments.append([temp[0], widget.get_selected_color()])
                    fragments.append([match, self._selected_color])
                else:
                    fragments.append([temp[0], widget.get_color()])
                    fragments.append([match, self._color])
                current_render_text = temp[1]

        if selected:
            fragments.append([current_render_text, widget.get_selected_color()])
        else:
            fragments.append([current_render_text, widget.get_color()])

        return fragments


    def _split_text_on_region(self, widget, render_text, selected):
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
            if selected:
                return [[render_text, widget.get_selected_color()]]
            else:
                return [[render_text, widget.get_color()]]
        elif len(render_text) < self._region[1]:
            self._region[1] = len(render_text)
        
        if self._region[0] != 0:
            if selected:
                fragments.append([render_text[0:self._region[0]], widget.get_selected_color()])
            else:
                fragments.append([render_text[0:self._region[0]], widget.get_color()])
        
        if selected:
            fragments.append([render_text[self._region[0]:self._region[1]], self._selected_color])
            fragments.append([render_text[self._region[1]:], widget.get_selected_color()])
        else:
            fragments.append([render_text[self._region[0]:self._region[1]], self._color])
            fragments.append([render_text[self._region[1]:], widget.get_color()])

        return fragments


    def generate_fragments(self, widget, line, render_text, selected=False):
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
        if selected:
            fragments = [[render_text, widget.get_selected_color()]]
        else:
            fragments = [[render_text, widget.get_color()]]
        
        if match:

            if self._match_type == 'line':
                if selected:
                    fragments = [[render_text, self._selected_color]]
                else:
                    fragments = [[render_text, self._color]]
            elif self._match_type == 'regex':
                fragments = self._generate_fragments_regex(widget, render_text, selected)
            elif self._match_type == 'region':
                fragments = self._split_text_on_region(widget, render_text, selected)
        
            self._logger.debug(f'Generated fragments: {fragments}')
        
        return fragments, match