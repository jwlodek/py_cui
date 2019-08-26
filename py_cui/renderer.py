"""
File containing the py_cui renderer. It is used to draw all of the onscreen widgets and items.

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""

import curses

class Renderer:

    def __init__(self, root, stdscr):
        self.root = root
        self.stdscr = stdscr


    def set_color_mode(self, color_mode):

        self.stdscr.attron(curses.color_pair(color_mode))

    def unset_color_mode(self, color_mode):

        self.stdscr.attroff(curses.color_pair(color_mode))

    def reset_cursor(self, widget, fill=True):
        
        if fill:
            cursor_y = widget.start_y + widget.height - widget.pady - 1
            cursor_x = widget.start_x + widget.width - widget.padx + 1
        else:
            cursor_y = widget.start_y + int(widget.height / 2) + 2
            cursor_x = widget.start_x + widget.width - widget.padx + 1

        self.stdscr.move(cursor_y, cursor_x)

    def draw_cursor(self, cursor_y, cursor_x):

        self.stdscr.move(cursor_y, cursor_x)

    def draw_border(self, widget, fill=True, with_title=True):
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


    def draw_border_top(self, widget, y, with_title):
        if not with_title or (len(widget.title) + 4 >= widget.width - 2 * widget.padx):
            self.stdscr.addstr(y, widget.start_x + widget.padx, '+{}+'.format('-'*(widget.width-2 - widget.padx)))
        else:
            self.stdscr.addstr(y, widget.start_x + widget.padx, '+--{}{}+'.format(widget.title, '-' * (widget.width - 4 - widget.padx - len(widget.title))))

    def draw_border_bottom(self, widget, y):
        self.stdscr.addstr(y, widget.start_x + widget.padx, '+{}+'.format('-'*(widget.width-2 - widget.padx)))

    def draw_blank_row(self, widget, y):

        self.stdscr.addstr(y, widget.start_x + widget.padx, '|{}|'.format(' ' *(widget.width-2 - widget.padx)))


    def draw_text(self, widget, line, y, centered = False, bordered = True):
        if centered and bordered:
            render_text = '|{}|'.format(line.center(widget.width - widget.padx - 2, ' '))
        elif centered and not bordered:
            render_text = '{}'.format(line.center(widget.width - widget.padx, ' '))
        elif not centered and bordered:
            render_text = '| {}{}|'.format(line, ' ' * (widget.width-3 - widget.padx - len(line)))
        else:
            render_text = '{}{}'.format(line, ' ' * (widget.width - widget.padx -len(line)))
        self.stdscr.addstr(y, widget.start_x + widget.padx, render_text)