"""
File containing classes for all popups used by py_cui

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""

# required library imports
import curses
import py_cui
import py_cui.errors


class Popup:
    """
    Base popup class. Contains constructor and initial definitions for key_press and draw
    Unlike widgets, they do not have a set grid cell, they are simply centered in the view
    frame

    Attributes
    ----------
    root : PyCUI
        the root py_cui window
    title, text : str
        The message title and text
    color : int
        The py_cui color code
    start_x, start_y : int
        top left corner of the popup
    stop_x, stop_y : int
        bottom right corner of the popup

    Methods
    -------
    handle_key_press()
        Implemented by each subclass, handles key presses
    draw()
        Implemented by each subclass, draws the popup to the terminal
    """

    def __init__(self, root, title, text, color):
        """ Constructor for popup class """

        self.root = root
        self.title = title
        self.text = text
        self.color = color
        self.start_x = int(self.root.width / 4)
        self.start_y = int(self.root.height / 3)
        self.stop_x = int(3 * self.root.width / 4)
        self.stop_y = int(2 * self.root.height / 3)

        # ret_val not used. Need to try and find a way to return values from popups
        self.ret_val = None


    def handle_key_press(self, key_pressed):
        """ Must be implemented by subclass """

        pass


    def draw(self, stdscr):
        """ Must be implemented by subclass """

        stdscr.attron(curses.color_pair(self.color))
        target_y = int(self.stop_y - self.start_y / 2)
        width = self.stop_x - self.start_x
        render_text = self.text
        if len(render_text) > (self.stop_x - self.start_x - 4):
            render_text = render_text[:(self.stop_x - self.start_x - 7)] + '...'

        render_title = self.title
        if len(render_title)> (self.stop_x - self.start_x - 4):
            render_title = render_title[:(self.stop_x - self.start_x - 7)] + '...'

        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(self.start_y, self.start_x, '+-{}-+'.format('-' * (width - 4 )))
        for i in range(self.start_y + 1, target_y - 2):
            stdscr.addstr(i, self.start_x, '|{}|'.format(' ' * (width - 2)))
        stdscr.addstr(target_y - 2, self.start_x, '|{}|'.format(render_title.center(width - 2, ' ')))
        stdscr.addstr(target_y - 1, self.start_x, '|{}|'.format(' ' * (width - 2)))
        stdscr.addstr(target_y, self.start_x, '|{}|'.format(render_text.center(width - 2, ' ')))
        for i in range(target_y + 1, self.stop_y):
            stdscr.addstr(i, self.start_x, '|{}|'.format(' ' * (width - 2)))
        stdscr.addstr(self.stop_y, self.start_x, '+-{}-+'.format('-' * (width - 4)))
        stdscr.attroff(curses.color_pair(self.color))
        stdscr.attroff(curses.A_BOLD)


class MessagePopup(Popup):

    def __init__(self, root, title, text, color):
        super().__init__(root, title, text, color)
        

    def handle_key_press(self, key_pressed):
        if (key_pressed == 10 or key_pressed == 32 or key_pressed == 27):
            self.root.close_popup()

    def draw(self, stdscr):
        super().draw(stdscr)


###########################################################
#
# Below popups require some form of blocking + return,
# which I cannot yet figure out. TODO
#
# UNIMPLEMENTED
#
###########################################################



class YesNoPopup(Popup):

    def __init__(self, root, title, text, color, command):
        super().__init__(root, title, text, color)
        self.command = command

    def handle_key_press(self, key_pressed):
        valid_pressed = False
        if key_pressed == py_cui.keys.KEY_Y_LOWER or key_pressed == py_cui.keys.KEY_Y_UPPER:
            self.ret_val = True
            valid_pressed = True
        elif key_pressed == py_cui.keys.KEY_N_UPPER or key_pressed == py_cui.keys.KEY_N_LOWER:
            self.ret_val = False
            valid_pressed = True

        if valid_pressed:
            self.root.close_popup()
            if self.command is not None:
                self.command(self.ret_val)
            else:
                self.root.show_warning_popup('No Command Specified', 'The Yes/No popup had no specified command')


    def draw(self, stdscr):
        super().draw(stdscr)



class TextBoxPopup(Popup):
    pass


class MenuPopup(Popup):
    pass


class LoadingIconPopup(Popup):
    def __init__(self, root, title, message, color):
        super().__init__(root, title, '{} ... \\'.format(message), color)
        self.loading_icons = ['\\', '|', '/', '-']
        self.icon_counter = 0
        self.message = message

    def draw(self, stdscr):
        self.text = '{} ... {}'.format(self.message, self.loading_icons[self.icon_counter])
        self.icon_counter = self.icon_counter + 1
        if self.icon_counter == len(self.loading_icons):
            self.icon_counter = 0
        super().draw(stdscr)


class LoadingBarPopup(Popup):
    def __init__(self, root, title, num_items, color):
        super().__init__(root, title, '{} (0/{})'.format('-' * num_items, num_items), color)
        self.loading_icons = ['\\', '|', '/', '-']
        self.icon_counter = 0
        self.num_items = num_items
        self.completed_items = 0

    def draw(self, stdscr):
        if self.completed_items == self.num_items:
            self.root.stop_loading_popup()

        self.text = '{}{} ({}/{})'.format('#' * self.completed_items, '-' * (self.num_items - self.completed_items), self.completed_items, self.num_items)
        super().draw(stdscr)
