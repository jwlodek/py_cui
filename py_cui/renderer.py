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

    def draw_border(self, widget):
        self.draw_border_top(widget)
        for i in range(widget.start_y + widget.pad_y + 1, widget.start_y + widget.height - widget.pady - 1):
            self.draw_blank_row(widget, i)
        self.stdscr.addstr(widget.start_y + widget.height - widget.pady - 1, widget.start_x + widget.padx, '+{}+'.format('-'*(widget.width-2 - widget.padx)))


    def draw_border_top(self, widget, with_title=True):
        if not with_title or (len(widget.title) + 4 >= widget.width - 2 * widget.padx):
            self.stdscr.addstr(widget.start_y + widget.pady, widget.start_x + widget.padx, '+{}+'.format('-'*(widget.width-2 - widget.padx)))
        else:
            self.stdscr.addstr(widget.start_y + widget.pady, widget.start_x + widget.padx, '+--{}{}+'.format(widget.title, '-' * (widget.width - 4 - widget.padx - len(widget.title))))


    def draw_blank_row(self, widget, y):

        self.stdscr.addstr(y, widget.start_x + widget.padx, '|{}|'.format(' ' *(widget.width-2 - widget.padx)))


    def draw_text(self, widget, line, y, centered = False, bordered = True):
        if centered and bordered:
            render_text = '|{}|'.format(line.center(widget.width - (2 * widget.padx) - 2, ' '))
        elif centered and not bordered:
            render_text = '{}'.format(line.center(widget.width - (2 * widget.padx), ' '))
        elif not centered and bordered:
            render_text = '| {}{}|'.format(line, ' ' * (widget.width-3 - widget.padx - len(line)))
        else:
            render_text = '{}{}'.format(line, ' ' * (widget.width - widget.padx -len(line)))
        self.stdscr.addstr(y, widget.start_x + widget.padx, render_text)