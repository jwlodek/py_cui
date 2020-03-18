"""Module containing the py_cui renderer. It is used to draw all of the onscreen widgets and items.

@author:    Jakub Wlodek  
@created:   12-Aug-2019
"""

import curses
import py_cui
import py_cui.colors


class Renderer:
    """Main renderer class used for drawing widgets to the terminal.
    
    Has helper functions for drawing the borders, cursor,
    and text required for the cui. All of the functions supplied by the renderer class should only be used internally.

    Attributes
    ----------
    root : py_cui.PyCUI
        The parent window
    stdscr : standard cursor
        The cursor with which renderer draws text
    color_rules : list of py_cui.colors.ColorRule
        List of currently loaded rules to apply during drawing
    """

    def __init__(self, root, stdscr):
        """Constructor for renderer object
        """

        self.__root         = root
        self.__stdscr       = stdscr
        self.__color_rules  = []

        # Define widget border characters
        self.__border_characters = {
            'UP_LEFT'       : '+',
            'UP_RIGHT'      : '+',
            'DOWN_LEFT'     : '+',
            'DOWN_RIGHT'    : '+',
            'HORIZONTAL'    : '-',
            'VERTICAL'      : '|'
        }


    def _set_border_renderer_chars(self, border_char_set):
        """Function that sets the border characters for widgets

        Parameters
        ----------
        border_characters : Dict of str to str
            The border characters as specified by user
        """

        self.__border_characters['UP_LEFT'   ] = border_char_set['UP_LEFT'   ]
        self.__border_characters['UP_RIGHT'  ] = border_char_set['UP_RIGHT'  ]
        self.__border_characters['DOWN_LEFT' ] = border_char_set['DOWN_LEFT' ]
        self.__border_characters['DOWN_RIGHT'] = border_char_set['DOWN_RIGHT']
        self.__border_characters['HORIZONTAL'] = border_char_set['HORIZONTAL']
        self.__border_characters['VERTICAL'  ] = border_char_set['VERTICAL'  ]


    def _set_bold(self):
        """Sets bold draw mode
        """

        self.__stdscr.attron(curses.A_BOLD)


    def _unset_bold(self):
        """Unsets bold draw mode
        """

        self.__stdscr.attroff(curses.A_BOLD)


    def _set_color_rules(self, color_rules):
        """Sets current color rules

        Parameters
        ----------
        color_rules : List[py_cui.colors.ColorRule]
            List of currently loaded rules to apply during drawing
        """

        self.__color_rules = color_rules


    def _set_color_mode(self, color_mode):
        """Sets the output color mode

        Parameters
        ----------
        color_mode : int
            Color code to apply during drawing
        """

        self.__stdscr.attron(curses.color_pair(color_mode))


    def _unset_color_mode(self, color_mode):
        """Unsets the output color mode

        Parameters
        ----------
        color_mode : int
            Color code to unapply during drawing
        """

        self.__stdscr.attroff(curses.color_pair(color_mode))


    def _reset_cursor(self, widget, fill=True):
        """Positions the cursor at the bottom right of the selected widget
        
        Parameters
        ----------
        widget : py_cui.widgets.Widget
            widget for which to reset cursor
        fill : bool
            a flag that tells the renderer if the widget is filling its grid space, or not (ex. Textbox vs textblock)
        """

        padx, pady       = widget._get_padding()
        pady, start_y    = widget._get_start_position()
        height, _     = widget._get_dimensions()
        
        if fill:
            cursor_y = widget.start_y + widget.height - widget.pady - 1
            cursor_x = widget.start_x + widget.width - 2*widget.padx + 1
        else:
            cursor_y = widget.start_y + int(widget.height / 2) + 2
            cursor_x = widget.start_x + widget.width - 2*widget.padx + 1
        try:
            self.__stdscr.move(cursor_y, cursor_x)
        except:
            self.__stdscr.move(0,0)


    def _draw_cursor(self, cursor_y, cursor_x):
        """Draws the cursor at a particular location
        
        Parameters
        ----------
        cursor_x, cursor_y : int
            x, y coordinates where to draw the cursor
        """

        self.__stdscr.move(cursor_y, cursor_x)


    def _draw_border(self, widget, fill=True, with_title=True):
        """Draws ascii border around widget

        Parameters
        ----------
        widget : py_cui.widgets.Widget
            The widget being drawn
        fill : bool
            a flag that tells the renderer if the widget is filling its grid space, or not (ex. Textbox vs textblock)
        with_title : bool
            flag that tells whether or not to draw widget title
        """

        _, pady       = widget._get_padding()
        _, start_y    = widget._get_start_position()
        height, _     = widget._get_dimensions()

        if widget.is_selected():
            self.__stdscr.attron(curses.A_BOLD)

        if fill:
            border_y_start = start_y + pady
            border_y_stop = start_y + height - pady - 1
        else:
            border_y_start = start_y + int(height / 2)
            border_y_stop = border_y_start + 2

        self.__draw_border_top(widget, border_y_start, with_title)
        for i in range(border_y_start + 1, border_y_stop):
            self.__draw_blank_row(widget, i)
        self.__draw_border_bottom(widget, border_y_stop)

        if widget.is_selected():
            self.__stdscr.attroff(curses.A_BOLD)


    def __draw_border_top(self, widget, y, with_title):
        """Internal function for drawing top of border

        Parameters
        ----------
        widget : py_cui.widgets.Widget
            The widget being drawn
        y : int
            the terminal row (top down) on which to draw the text
        with_title : bool
            Flag that tells renderer if title should be superimposed into border.
        """

        padx, _       = widget.get_padding()
        start_x, _    = widget.get_start_position()
        _, width      = widget.get_dimensions()
        title         = widget.get_title()

        if not with_title or (len(title) + 4 >= width - 2 * padx):
            render_text = '{}{}{}'.format(  self.__border_characters['UP_LEFT'], 
                                            self.__border_characters['HORIZONTAL'] * (width - 2 - 2 * padx), 
                                            self.__border_characters['UP_RIGHT'])
            self.__stdscr.addstr(y, start_x + padx, render_text)
        else:
            render_text = '{}{} {} {}{}'.format(self.__border_characters['UP_LEFT'], 
                                                2 * self.__border_characters['HORIZONTAL'], 
                                                widget.title, 
                                                self.__border_characters['HORIZONTAL'] * (width - 6 - 2 * padx - len(title)), 
                                                self.__border_characters['UP_RIGHT'])
            self.__stdscr.addstr(y, start_x + padx, render_text)


    def __draw_border_bottom(self, widget, y):
        """Internal function for drawing bottom of border
        
        Parameters
        ----------
        widget : py_cui.widgets.Widget
            The widget being drawn
        y : int
            the terminal row (top down) on which to draw the text
        """

        padx, _       = widget.get_padding()
        start_x, _    = widget.get_start_position()
        _, width      = widget.get_dimensions()

        render_text = '{}{}{}'.format(  self.__border_characters['DOWN_LEFT'], 
                                        self.__border_characters['HORIZONTAL'] * (width - 2 - 2 * padx), 
                                        self.__border_characters['DOWN_RIGHT'])
        self.__stdscr.addstr(y, start_x + padx, render_text)


    def __draw_blank_row(self, widget, y):
        """Internal function for drawing a blank row
        
        Parameters
        ----------
        widget : py_cui.widgets.Widget
            The widget being drawn
        y : int
            the terminal row (top down) on which to draw the text
        """

        padx, _       = widget.get_padding()
        start_x, _    = widget.get_start_position()
        _, width      = widget.get_dimensions()

        render_text = '{}{}{}'.format(  self.__border_characters['VERTICAL'], 
                                        ' ' * (width - 2 - 2 * padx), 
                                        self.__border_characters['VERTICAL'])
        self.__stdscr.addstr(y, start_x + padx, render_text)


    def __get_render_text(self, widget, line, centered, bordered, start_pos):
        """Internal function that computes the scope of the text that should be drawn
        
        Parameters
        ----------
        widget : py_cui.widgets.Widget
            The widget being drawn
        line : str
            the line of text being drawn
        centered : bool
            flag to set if the text should be centered
        bordered : bool
            a flag to set if the text should be bordered
        start_pos : int
            position to start rendering the text from.

        Returns
        -------
        render_text : str
            The text shortened to fit within given space
        """

        padx, _       = widget.get_padding()
        _, width      = widget.get_dimensions()

        render_text_length = width - (2 * padx)

        if bordered:
            render_text_length = render_text_length - 4

        if len(line) - start_pos < render_text_length:
            if centered:
                render_text = '{}'.format(  line[start_pos:].center(render_text_length, 
                                            ' '))
            else:
                render_text = '{}{}'.format(line[start_pos:], 
                                            ' ' * (render_text_length - len(line[start_pos:])))
        else:
            render_text = line[start_pos:start_pos + render_text_length]

        render_text_fragments = self.__generate_text_color_fragments(widget, line, render_text)
        return render_text_fragments


    def __generate_text_color_fragments(self, widget, line, render_text):
        """Function that applies color rules to text, dividing them if match is found
        
        Parameters
        ----------
        widget : py_cui.widgets.Widget
            The widget being drawn
        line : str
            the line of text being drawn
        render_text : str
            The text shortened to fit within given space
        
        Returns
        -------
        fragments : list of [int, str]
            list of text - color code combinations to write
        """

        fragments = [[render_text, widget.get_color()]]
        for color_rule in self.__color_rules:
            fragments, match = color_rule.generate_fragments(widget, line, render_text)
            if match:
                return fragments

        return fragments


    def _draw_text(self, widget, line, y, centered = False, bordered = True, selected = False, start_pos = 0):
        """Function that draws widget text.

        Parameters
        ----------
        widget : py_cui.widgets.Widget
            The widget being drawn
        line : str
            the line of text being drawn
        y : int
            the terminal row (top down) on which to draw the text
        centered : bool
            flag to set if the text should be centered
        bordered : bool
            a flag to set if the text should be bordered
        selected : bool
            Flag that tells renderer if widget is selected.
        start_pos : int
            position to start rendering the text from.
        """

        padx, _       = widget.get_padding()
        start_x, _    = widget.get_start_position()

        render_text = self.__get_render_text(widget, line, centered, bordered, start_pos)
        current_start_x = start_x + padx
        if widget.selected:
            self.__stdscr.attron(curses.A_BOLD)

        if bordered:
            self.__stdscr.addstr(y, start_x + padx, self.__border_characters['VERTICAL'])
            current_start_x = current_start_x + 2

        if widget.selected:
            self.__stdscr.attroff(curses.A_BOLD)

        # Each text elem is a list with [text, color]
        for text_elem in render_text:
            if text_elem[1] != widget.get_color():
                self._set_color_mode(text_elem[1])

            if selected:
                self.__stdscr.attron(curses.A_BOLD)

            self.__stdscr.addstr(y, current_start_x, text_elem[0])
            current_start_x = current_start_x + len(text_elem[0])

            if selected:
                self.__stdscr.attroff(curses.A_BOLD)

            if text_elem[1] != widget.get_color():
                self._unset_color_mode(text_elem[1])

        if widget.is_selected():
            self.__stdscr.attron(curses.A_BOLD)

        if bordered:
            self.__stdscr.addstr(y, widget.start_x + widget.width - 2 * widget.padx, self.__border_characters['VERTICAL'])

        if widget.is_selected():
            self.__stdscr.attroff(curses.A_BOLD)
