"""Module containing the py_cui renderer. It is used to draw all of the onscreen ui_elements and items.
"""

# Author:    Jakub Wlodek
# Created:   12-Aug-2019

import curses
import py_cui
import py_cui.colors


class Renderer:
    """Main renderer class used for drawing ui_elements to the terminal.
    
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

    def __init__(self, root, stdscr, logger):
        """Constructor for renderer object
        """

        self._root         = root
        self._stdscr       = stdscr
        self._color_rules  = []
        self._logger       = logger

        # Define ui_element border characters
        self._border_characters = {
            'UP_LEFT'       : '+',
            'UP_RIGHT'      : '+',
            'DOWN_LEFT'     : '+',
            'DOWN_RIGHT'    : '+',
            'HORIZONTAL'    : '-',
            'VERTICAL'      : '|'
        }


    def _set_border_renderer_chars(self, border_char_set):
        """Function that sets the border characters for ui_elements

        Parameters
        ----------
        border_characters : Dict of str to str
            The border characters as specified by user
        """

        self._border_characters['UP_LEFT'   ] = border_char_set['UP_LEFT'   ]
        self._border_characters['UP_RIGHT'  ] = border_char_set['UP_RIGHT'  ]
        self._border_characters['DOWN_LEFT' ] = border_char_set['DOWN_LEFT' ]
        self._border_characters['DOWN_RIGHT'] = border_char_set['DOWN_RIGHT']
        self._border_characters['HORIZONTAL'] = border_char_set['HORIZONTAL']
        self._border_characters['VERTICAL'  ] = border_char_set['VERTICAL'  ]


    def _set_bold(self):
        """Sets bold draw mode
        """

        self._stdscr.attron(curses.A_BOLD)


    def _unset_bold(self):
        """Unsets bold draw mode
        """

        self._stdscr.attroff(curses.A_BOLD)


    def set_color_rules(self, color_rules):
        """Sets current color rules

        Parameters
        ----------
        color_rules : List[py_cui.colors.ColorRule]
            List of currently loaded rules to apply during drawing
        """

        self._color_rules = color_rules


    def set_color_mode(self, color_mode):
        """Sets the output color mode

        Parameters
        ----------
        color_mode : int
            Color code to apply during drawing
        """

        self._stdscr.attron(curses.color_pair(color_mode))


    def unset_color_mode(self, color_mode):
        """Unsets the output color mode

        Parameters
        ----------
        color_mode : int
            Color code to unapply during drawing
        """

        self._stdscr.attroff(curses.color_pair(color_mode))


    def reset_cursor(self, ui_element, fill=True):
        """Positions the cursor at the bottom right of the selected element
        
        Parameters
        ----------
        ui_element : py_cui.ui.UIElement
            ui element for which to reset cursor
        fill : bool
            a flag that tells the renderer if the element is filling its grid space, or not (ex. Textbox vs textblock)
        """

        padx, pady       = ui_element.get_padding()
        start_x, start_y = ui_element.get_start_position()
        height, width    = ui_element.get_absolute_dimensions()
        
        if fill:
            cursor_y = start_y + height - pady - 1
            cursor_x = start_x + width - 2 * padx + 1
        else:
            cursor_y = start_y + int(height / 2) + 2
            cursor_x = start_x + width - 2 * padx + 1
        try:
            self._stdscr.move(cursor_y, cursor_x)
        except:
            self._stdscr.move(0,0)


    def draw_cursor(self, cursor_y, cursor_x):
        """Draws the cursor at a particular location
        
        Parameters
        ----------
        cursor_x, cursor_y : int
            x, y coordinates where to draw the cursor
        """

        self._stdscr.move(cursor_y, cursor_x)


    def draw_border(self, ui_element, fill=True, with_title=True):
        """Draws ascii border around ui element

        Parameters
        ----------
        ui_element : py_cui.ui.UIElement
            The ui_element being drawn
        fill : bool
            a flag that tells the renderer if the ui_element is filling its grid space, or not (ex. Textbox vs textblock)
        with_title : bool
            flag that tells whether or not to draw ui_element title
        """

        _, pady       = ui_element.get_padding()
        _, start_y    = ui_element.get_start_position()
        height, _     = ui_element.get_absolute_dimensions()

        if ui_element.is_selected():
            self._set_bold()

        if fill:
            border_y_start = start_y + pady
            border_y_stop = start_y + height - pady - 1
        else:
            border_y_start = start_y + int(height / 2)
            border_y_stop = border_y_start + 2

        self._draw_border_top(ui_element, border_y_start, with_title)
        for i in range(border_y_start + 1, border_y_stop):
            self._draw_blank_row(ui_element, i)
        self._draw_border_bottom(ui_element, border_y_stop)

        if ui_element.is_selected():
            self._unset_bold()


    def _draw_border_top(self, ui_element, y, with_title):
        """Internal function for drawing top of border

        Parameters
        ----------
        ui_element : py_cui.ui.UIElement
            The ui_element being drawn
        y : int
            the terminal row (top down) on which to draw the text
        with_title : bool
            Flag that tells renderer if title should be superimposed into border.
        """

        padx, _       = ui_element.get_padding()
        start_x, _    = ui_element.get_start_position()
        _, width      = ui_element.get_absolute_dimensions()
        title         = ui_element.get_title()

        if not with_title or (len(title) + 4 >= width - 2 * padx):
            render_text = '{}{}{}'.format(  self._border_characters['UP_LEFT'], 
                                            self._border_characters['HORIZONTAL'] * (width - 2 - 2 * padx), 
                                            self._border_characters['UP_RIGHT'])
            self._stdscr.addstr(y, start_x + padx, render_text)
        else:
            render_text = '{}{} {} {}{}'.format(self._border_characters['UP_LEFT'], 
                                                2 * self._border_characters['HORIZONTAL'], 
                                                title, 
                                                self._border_characters['HORIZONTAL'] * (width - 6 - 2 * padx - len(title)), 
                                                self._border_characters['UP_RIGHT'])
            self._stdscr.addstr(y, start_x + padx, render_text)


    def _draw_border_bottom(self, ui_element, y):
        """Internal function for drawing bottom of border
        
        Parameters
        ----------
        ui_element : py_cui.ui.UIElement
            The ui_element being drawn
        y : int
            the terminal row (top down) on which to draw the text
        """

        padx, _       = ui_element.get_padding()
        start_x, _    = ui_element.get_start_position()
        _, width      = ui_element.get_absolute_dimensions()

        render_text = '{}{}{}'.format(  self._border_characters['DOWN_LEFT'], 
                                        self._border_characters['HORIZONTAL'] * (width - 2 - 2 * padx), 
                                        self._border_characters['DOWN_RIGHT'])
        self._stdscr.addstr(y, start_x + padx, render_text)


    def _draw_blank_row(self, ui_element, y):
        """Internal function for drawing a blank row
        
        Parameters
        ----------
        ui_element : py_cui.ui.UIElement
            The ui_element being drawn
        y : int
            the terminal row (top down) on which to draw the text
        """

        padx, _       = ui_element.get_padding()
        start_x, _    = ui_element.get_start_position()
        _, width      = ui_element.get_absolute_dimensions()

        render_text = '{}{}{}'.format(  self._border_characters['VERTICAL'], 
                                        ' ' * (width - 2 - 2 * padx), 
                                        self._border_characters['VERTICAL'])
        self._stdscr.addstr(y, start_x + padx, render_text)


    def _get_render_text(self, ui_element, line, centered, bordered, start_pos):
        """Internal function that computes the scope of the text that should be drawn
        
        Parameters
        ----------
        ui_element : py_cui.ui.UIElement
            The ui_element being drawn
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

        padx, _       = ui_element.get_padding()
        _, width      = ui_element.get_absolute_dimensions()

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

        render_text_fragments = self._generate_text_color_fragments(ui_element, line, render_text)
        return render_text_fragments


    def _generate_text_color_fragments(self, ui_element, line, render_text):
        """Function that applies color rules to text, dividing them if match is found
        
        Parameters
        ----------
        ui_element : py_cui.ui.UIElement
            The ui_element being drawn
        line : str
            the line of text being drawn
        render_text : str
            The text shortened to fit within given space
        
        Returns
        -------
        fragments : list of [int, str]
            list of text - color code combinations to write
        """

        fragments = [[render_text, ui_element.get_color()]]
        for color_rule in self._color_rules:
            fragments, match = color_rule.generate_fragments(ui_element, line, render_text)
            if match:
                return fragments

        return fragments


    def draw_text(self, ui_element, line, y, centered = False, bordered = True, selected = False, start_pos = 0):
        """Function that draws ui_element text.

        Parameters
        ----------
        ui_element : py_cui.ui.UIElement
            The ui_element being drawn
        line : str
            the line of text being drawn
        y : int
            the terminal row (top down) on which to draw the text
        centered : bool
            flag to set if the text should be centered
        bordered : bool
            a flag to set if the text should be bordered
        selected : bool
            Flag that tells renderer if ui_element is selected.
        start_pos : int
            position to start rendering the text from.
        """

        padx, _       = ui_element.get_padding()
        _, width      = ui_element.get_absolute_dimensions()
        start_x, _    = ui_element.get_start_position()

        render_text = self._get_render_text(ui_element, line, centered, bordered, start_pos)
        current_start_x = start_x + padx
        if ui_element.is_selected():
            self._set_bold()

        if bordered:
            self._stdscr.addstr(y, start_x + padx, self._border_characters['VERTICAL'])
            current_start_x = current_start_x + 2

        if ui_element.is_selected():
            self._unset_bold()

        # Each text elem is a list with [text, color]
        for text_elem in render_text:
            if text_elem[1] != ui_element.get_color():
                self.set_color_mode(text_elem[1])

            if selected:
                self._set_bold()

            self._stdscr.addstr(y, current_start_x, text_elem[0])
            current_start_x = current_start_x + len(text_elem[0])

            if selected:
                self._unset_bold()

            if text_elem[1] != ui_element.get_color():
                self.unset_color_mode(text_elem[1])

        if ui_element.is_selected():
            self._set_bold()

        if bordered:
            self._stdscr.addstr(y, start_x + width - 2 * padx, self._border_characters['VERTICAL'])

        if ui_element.is_selected():
            self._unset_bold()
