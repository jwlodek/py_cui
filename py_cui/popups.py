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

    def __init__(self, root, title, text, color, renderer):
        """ Constructor for popup class """

        self.root = root
        self.title = title
        self.text = text
        self.color = color
        self.start_x = int(self.root.width / 4)
        self.start_y = int(self.root.height / 3)
        self.stop_x = int(3 * self.root.width / 4)
        self.stop_y = int(2 * self.root.height / 3)
        self.height = self.stop_y - self.start_y
        self.width = self.stop_x - self.start_x
        self.padx = 1
        self.pady = 0
        self.renderer = renderer
        self.selected = True


    def handle_key_press(self, key_pressed):
        """ Must be implemented by subclass """

        pass


    def draw(self, stdscr):
        """ Must be implemented by subclass """
        self.renderer.set_color_mode(self.color)
        target_y = int(self.stop_y - self.start_y / 2)
        """
        width = self.stop_x - self.start_x
        render_text = self.text
        if len(render_text) > (self.stop_x - self.start_x - 4):
            render_text = render_text[:(self.stop_x - self.start_x - 7)] + '...'

        render_title = self.title
        if len(render_title)> (self.stop_x - self.start_x - 4):
            render_title = render_title[:(self.stop_x - self.start_x - 7)] + '...'

        """
        self.renderer.set_bold()
        self.renderer.draw_border(self, with_title=False)
        self.renderer.draw_text(self, self.title, target_y - 2, centered=True)
        self.renderer.draw_text(self, self.text, target_y, centered=True)
        self.renderer.unset_color_mode(self.color)
        self.renderer.unset_bold()
        self.renderer.reset_cursor(self)



class MessagePopup(Popup):

    def __init__(self, root, title, text, color, renderer):
        super().__init__(root, title, text, color, renderer)
        

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

    def __init__(self, root, title, text, color, command, renderer):
        super().__init__(root, title, text, color, renderer)
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
    def __init__(self, root, title, color, command, renderer):
        super().__init__(root, title, '', color, renderer)
        self.text = ''
        self.command = command
        self.cursor_x = self.start_x + 2 + self.padx
        self.cursor_text_pos = 0
        self.cursor_max_left = self.cursor_x
        self.cursor_max_right = self.start_x + self.width - 1 -self.pady
        self.cursor_y = self.start_y + int(self.height / 2) + 1
        self.viewport_width = self.cursor_max_right - self.cursor_max_left


    def set_text(self, text):
        """ Sets the value of the text. Overwrites existing text """

        self.text = text
        if self.cursor_text_pos > len(self.text):
            diff = self.cursor_text_pos - len(self.text)
            self.cursor_text_pos = len(self.text)
            self.cursor_x = self.cursor_x - diff

    def get(self):
        """ Gets value of the text in the textbox """

        return self.text


    def clear(self):
        """ Clears the text in the textbox """

        self.cursor_x = self.cursor_max_left
        self.cursor_text_pos = 0
        self.text = ''


    def move_left(self):
        """ Shifts the cursor the the left. Internal use only """

        if  self.cursor_text_pos > 0:
            if self.cursor_x > self.cursor_max_left:
                self.cursor_x = self.cursor_x - 1
            self.cursor_text_pos = self.cursor_text_pos - 1


    def move_right(self):
        """ Shifts the cursor the the right. Internal use only """
        if self.cursor_text_pos < len(self.text):
            if self.cursor_x < self.cursor_max_right:
                self.cursor_x = self.cursor_x + 1
            self.cursor_text_pos = self.cursor_text_pos + 1

    def insert_char(self, key_pressed):
        """ Inserts char at cursor position. Internal use only """
        self.text = self.text[:self.cursor_text_pos] + chr(key_pressed) + self.text[self.cursor_text_pos:]
        if len(self.text) < self.viewport_width:
            self.cursor_x = self.cursor_x + 1
        self.cursor_text_pos = self.cursor_text_pos + 1


    def jump_to_start(self):
        """ Jumps to the start of the textbox """

        self.cursor_x = self.start_x + self.padx + 2
        self.cursor_text_pos = 0


    def jump_to_end(self):
        """ Jumps to the end to the textbox """

        self.cursor_text_pos = len(self.text)
        self.cursor_x = self.start_x + self.padx + 2 + self.cursor_text_pos


    def erase_char(self):
        """ Erases character at textbox cursor """

        if self.cursor_text_pos > 0:
            self.text = self.text[:self.cursor_text_pos - 1] + self.text[self.cursor_text_pos:]
            if len(self.text) < self.width - 2 * self.padx - 4:
                self.cursor_x = self.cursor_x - 1
            self.cursor_text_pos = self.cursor_text_pos - 1



    def handle_key_press(self, key_pressed):
        """ Override of base handle key press function """

        valid_pressed = False
        if key_pressed == py_cui.keys.KEY_ENTER:
            self.ret_val = self.text
            valid_pressed = True

        if valid_pressed:
            self.root.close_popup()
            if self.command is not None:
                self.command(self.ret_val)
            else:
                self.root.show_warning_popup('No Command Specified', 'The Yes/No popup had no specified command')

        if key_pressed == py_cui.keys.KEY_LEFT_ARROW:
            self.move_left()
        elif key_pressed == py_cui.keys.KEY_RIGHT_ARROW:
            self.move_right()
        elif key_pressed == py_cui.keys.KEY_BACKSPACE:
            self.erase_char()
        elif key_pressed == py_cui.keys.KEY_HOME:
            self.jump_to_start()
        elif key_pressed == py_cui.keys.KEY_END:
            self.jump_to_end()
        elif key_pressed > 31 and key_pressed < 128:
            self.insert_char(key_pressed)

    def draw(self, stdscr):
        """ Override of base draw function """

        self.renderer.set_color_mode(self.color)
        self.renderer.draw_text(self, self.title, self.cursor_y - 2, bordered=False)
        self.renderer.draw_border(self, fill=False, with_title=False)
        render_text = self.text
        if len(self.text) > self.width - 2 * self.padx - 4:
            end = len(self.text) - (self.width - 2 * self.padx - 4)
            if self.cursor_text_pos < end:
                render_text = self.text[self.cursor_text_pos:self.cursor_text_pos + (self.width - 2 * self.padx - 4)]
            else:
                render_text = self.text[end:]
        self.renderer.draw_text(self, render_text, self.cursor_y, selected=self.selected)

        if self.selected:
            self.renderer.draw_cursor(self.cursor_y, self.cursor_x)
        else:
            self.renderer.reset_cursor(self, fill=False)
        self.renderer.unset_color_mode(self.color)


class MenuPopup(Popup):
    """ A scroll menu widget. Allows for creating a scrollable list of items of which one is selectable. Analogous to a RadioButton """

    def __init__(self, root, items, title, command, color, renderer):
        super().__init__(root, title, '', color, renderer)
        self.top_view = 0
        self.selected_item = 0
        self.view_items = items
        self.command = command


    def scroll_up(self):
        """ Function that scrolls the view up in the scroll menu """

        if self.selected:
            if self.top_view > 0:
                self.top_view = self.top_view - 1
            if self.selected_item > 0:
                self.selected_item = self.selected_item - 1


    def scroll_down(self):
        """ Function that scrolls the view down in the scroll menu """

        if self.selected:
            if self.selected_item < len(self.view_items) - 1:
                self.selected_item = self.selected_item + 1
            if self.selected_item > self.top_view + self.height - (2 * self.pady) - 3:
                self.top_view = self.top_view + 1


    def get(self):
        """
        Function that gets the selected item from the scroll menu

        Returns
        -------
        item : str
            selected item, or None if there are no items in the menu
        """
        
        if len(self.view_items) > 0:
            return self.view_items[self.selected_item]
        return None


    def handle_key_press(self, key_pressed):
        """ Override of base handle key press function """

        valid_pressed = False
        if key_pressed == py_cui.keys.KEY_ENTER:
            self.ret_val = self.get()
            valid_pressed = True

        if valid_pressed:
            self.root.close_popup()
            if self.command is not None:
                self.command(self.ret_val)
            else:
                self.root.show_warning_popup('No Command Specified', 'The Yes/No popup had no specified command')
        
        if key_pressed == py_cui.keys.KEY_UP_ARROW:
            self.scroll_up()
        if key_pressed == py_cui.keys.KEY_DOWN_ARROW:
            self.scroll_down()


    def draw(self):
        """ Overrides base class draw function """

        self.renderer.set_color_mode(self.color)
        self.renderer.draw_border(self)
        counter = self.pady + 1
        line_counter = 0
        for line in self.view_items:
            if line_counter < self.top_view:
                line_counter = line_counter + 1
            else:
                if counter >= self.height - self.pady - 1:
                    break
                if line_counter == self.selected_item:
                    self.renderer.draw_text(self, line, self.start_y + counter, selected=True)
                else:
                    self.renderer.draw_text(self, line, self.start_y + counter)
                counter = counter + 1
                line_counter = line_counter + 1
        self.renderer.unset_color_mode(self.color)
        self.renderer.reset_cursor(self)


class LoadingIconPopup(Popup):
    def __init__(self, root, title, message, color, renderer):
        super().__init__(root, title, '{} ... \\'.format(message), color, renderer)
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
    def __init__(self, root, title, num_items, color, renderer):
        super().__init__(root, title, '{} (0/{})'.format('-' * num_items, num_items), color, renderer)
        self.num_items = num_items
        self.completed_items = 0

    def draw(self, stdscr):
        width = self.stop_x - self.start_x
        bar_width = 2 * int(width / 3)
        items_per_bar_block = self.num_items / bar_width
        if bar_width > self.num_items:
            bar_width = self.num_items
            items_per_bar_block = 1
        if self.completed_items == self.num_items:
            self.root.stop_loading_popup()

        completed_blocks = int(self.completed_items / items_per_bar_block)
        non_completed_blocks = bar_width - completed_blocks
        #self.title = '{}, {}, {}, {}, {}'.format(width, bar_width, items_per_bar_block, completed_blocks, non_completed_blocks)

        self.text = '{}{} ({}/{})'.format('#' * completed_blocks, '-' * non_completed_blocks, self.completed_items, self.num_items)
        super().draw(stdscr)
