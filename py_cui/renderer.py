"""
File containing the py_cui renderer. It is used to draw all of the onscreen widgets and items.

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""

import curses
import py_cui
import py_cui.colors


class Renderer:
    """
    Main renderer class used for drawing widgets to the terminal. Has helper functions for drawing the borders, cursor,
    and text required for the cui.
    
    All of the functions supplied by the renderer class should only be used internally.
    """

    def __init__(self, root, stdscr):
        self.root = root
        self.stdscr = stdscr
        self.color_rules = []


    def set_bold(self):
        """ Sets bold draw mode """

        self.stdscr.attron(curses.A_BOLD)

    def unset_bold(self):
        """ Unsets bold draw mode """

        self.stdscr.attroff(curses.A_BOLD)

    def set_color_rules(self, color_rules):
        """ Sets current color rules """

        self.color_rules = color_rules


    def set_color_mode(self, color_mode):
        """ Sets the output color mode """

        self.stdscr.attron(curses.color_pair(color_mode))


    def unset_color_mode(self, color_mode):
        """ Unsets the output color mode """

        self.stdscr.attroff(curses.color_pair(color_mode))


    def reset_cursor(self, widget, fill=True):
        """
        Positions the cursor at the bottom right of the selected widget
        
        Parameters
        ----------
        widget : py_cui.widgets.Widget
            widget for which to reset cursor
        fill : bool
            a flag that tells the renderer if the widget is filling its grid space, or not (ex. Textbox vs textblock)
        """
        
        if fill:
            cursor_y = widget.start_y + widget.height - widget.pady - 1
            cursor_x = widget.start_x + widget.width - 2*widget.padx + 1
        else:
            cursor_y = widget.start_y + int(widget.height / 2) + 2
            cursor_x = widget.start_x + widget.width - 2*widget.padx + 1
        try:
            self.stdscr.move(cursor_y, cursor_x)
        except:
            self.stdscr.move(0,0)


    def draw_cursor(self, cursor_y, cursor_x):
        """ Draws the cursor at a particular location """

        self.stdscr.move(cursor_y, cursor_x)


    def draw_border(self, widget, fill=True, with_title=True):
        """
        Draws border around widget

        Parameters
        ----------
        fill : bool
            a flag that tells the renderer if the widget is filling its grid space, or not (ex. Textbox vs textblock)
        with_title : bool
            flag that tells whether or not to draw widget title
        """

        if widget.selected:
            self.stdscr.attron(curses.A_BOLD)

        if fill:
            border_y_start = widget.start_y + widget.pady
            border_y_stop = widget.start_y + widget.height - widget.pady - 1
        else:
            border_y_start = widget.start_y + int(widget.height / 2)
            border_y_stop = border_y_start + 2

        self.draw_border_top(widget, border_y_start, with_title)
        for i in range(border_y_start + 1, border_y_stop):
            self.draw_blank_row(widget, i)
        self.draw_border_bottom(widget, border_y_stop)

        if widget.selected:
            self.stdscr.attroff(curses.A_BOLD)


    def draw_border_top(self, widget, y, with_title):
        """ Internal function for drawing top of border """

        if not with_title or (len(widget.title) + 4 >= widget.width - 2 * widget.padx):
            self.stdscr.addstr(y, widget.start_x + widget.padx, '+{}+'.format('-'*(widget.width-2 - 2*widget.padx)))
        else:
            self.stdscr.addstr(y, widget.start_x + widget.padx, '+--{}{}+'.format(widget.title, '-' * (widget.width - 4 - 2*widget.padx - len(widget.title))))


    def draw_border_bottom(self, widget, y):
        """ Internal function for drawing bottom of border """

        self.stdscr.addstr(y, widget.start_x + widget.padx, '+{}+'.format('-'*(widget.width-2 - 2*widget.padx)))


    def draw_blank_row(self, widget, y):
        """ Internal function for drawing a blank row """

        self.stdscr.addstr(y, widget.start_x + widget.padx, '|{}|'.format(' ' *(widget.width-2 - 2*widget.padx)))


    def get_render_text(self, widget, line, centered, bordered, start_pos):
        """ Internal function that computes the scope of the text that should be drawn """

        render_text_length = widget.width - (2 * widget.padx)
        if bordered:
            render_text_length = render_text_length - 4
        if len(line) - start_pos < render_text_length:
            if centered:
                render_text = '{}'.format(line[start_pos:].center(render_text_length, ' '))
            else:
                render_text = '{}{}'.format(line[start_pos:], ' ' * (render_text_length - len(line[start_pos:])))
        else:
            render_text = line[start_pos:start_pos + render_text_length]
        render_text_fragments = self.generate_text_color_fragments(widget, line, render_text)
        return render_text_fragments


    def generate_text_color_fragments(self, widget, line, render_text):
        """ Function that applies color rules to text, dividing them if match is found """

        text_fragments_list = []

        fragments = [[render_text, widget.color]]
        for color_rule in self.color_rules:
            fragments, match = color_rule.generate_fragments(widget, line, render_text)
            if match:
                return fragments

        return fragments


    def draw_text(self, widget, line, y, centered = False, bordered = True, selected = False, start_pos = 0):
        """
        Function that draws widget text.

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
        start_pos : int
            position to start rendering the text from.
        """

        render_text = self.get_render_text(widget, line, centered, bordered, start_pos)
        current_start_x = widget.start_x + widget.padx
        if widget.selected:
            self.stdscr.attron(curses.A_BOLD)

        if bordered:
            self.stdscr.addstr(y, widget.start_x + widget.padx, '|')
            current_start_x = current_start_x + 2

        if widget.selected:
            self.stdscr.attroff(curses.A_BOLD)

        # Each text elem is a list with [text, color]
        for text_elem in render_text:
            if text_elem[1] != widget.color:
                self.set_color_mode(text_elem[1])

            if selected:
                self.stdscr.attron(curses.A_BOLD)

            self.stdscr.addstr(y, current_start_x, text_elem[0])
            current_start_x = current_start_x + len(text_elem[0])

            if selected:
                self.stdscr.attroff(curses.A_BOLD)

            if text_elem[1] != widget.color:
                self.unset_color_mode(text_elem[1])

        if widget.selected:
            self.stdscr.attron(curses.A_BOLD)

        if bordered:
            self.stdscr.addstr(y, widget.start_x + widget.width - 2 * widget.padx, '|')

        if widget.selected:
            self.stdscr.attroff(curses.A_BOLD)
