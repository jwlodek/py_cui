---
description: |
    API documentation for modules: py_cui, py_cui.colors, py_cui.errors, py_cui.grid, py_cui.keybinding, py_cui.popups, py_cui.renderer, py_cui.statusbar, py_cui.widget_set, py_cui.widgets.

lang: en

classoption: oneside
geometry: margin=1in
papersize: a4

linkcolor: blue
links-as-notes: true
---


    
# Module `py_cui` {#py_cui}

A python library for creating command line based user interfaces.

@author:    Jakub Wlodek
@created:   12-Aug-2019



    
## Sub-modules

* [py_cui.colors](#py_cui.colors)
* [py_cui.errors](#py_cui.errors)
* [py_cui.grid](#py_cui.grid)
* [py_cui.keybinding](#py_cui.keybinding)
* [py_cui.popups](#py_cui.popups)
* [py_cui.renderer](#py_cui.renderer)
* [py_cui.statusbar](#py_cui.statusbar)
* [py_cui.widget_set](#py_cui.widget_set)
* [py_cui.widgets](#py_cui.widgets)



    
## Functions


    
### Function `fit_text` {#py_cui.fit_text}



    
> `def fit_text(width, text, center=False)`


Helper function to fit text within a given width. Used to fix issue with status/title bar text
being too long and crashing the CUI

###### Parameters

**`width`** :&ensp;`int`
:   width of window in characters


**`text`** :&ensp;`str`
:   input text


**`center`** :&ensp;`Boolean`
:   flag to center text

###### Returns

`text` `fixed` `depending` `on` `width`
:   &nbsp;




    
## Classes


    
### Class `PyCUI` {#py_cui.PyCUI}



> `class PyCUI(num_rows, num_cols, auto_focus_buttons=True, exit_key=113)`


Main user interface class for py_cui. To create a user interface, you must first
create an instance of this class, and then add cells + widgets to it.

#### Attributes

**`cursor_x`**, **`cursor_y`** :&ensp;`int`
:   absolute position of the cursor in the CUI


**[`py_cui.grid`](#py_cui.grid)** :&ensp;[`Grid`](#py_cui.grid.Grid)
:   The main layout manager for the CUI


**`cells`** :&ensp;`list` of `py_cui.cell.Cell`
:   list of cells in the grid


**`title_bar`** :&ensp;[`StatusBar`](#py_cui.statusbar.StatusBar)
:   a status bar object that gets drawn at the top of the CUI


**`status_bar`** :&ensp;[`StatusBar`](#py_cui.statusbar.StatusBar)
:   a status bar object that gets drawn at the bottom of the CUI


**`keybindings`** :&ensp;`list` of `py_cui.keybinding.KeyBinding`
:   list of keybindings to check against in the main CUI loop


**`height`**, **`width`** :&ensp;`int`
:   height of the terminal in characters, width of terminal in characters


**`exit_key`** :&ensp;`key_code`
:   a key code for a key that exits the CUI

#### Methods

start()
    starts the CUI once all of the widgets have been added. Note that you cannot
    add more widgets once this has been run
add_status_bar(text : str, foreground_color : color, background_color : color)
    function that adds a status bar widget to the CUI








    
#### Methods


    
##### Method `add_block_label` {#py_cui.PyCUI.add_block_label}



    
> `def add_block_label(self, title, row, column, row_span=1, column_span=1, padx=1, pady=0)`


Function that adds a new label to the CUI grid


    
##### Method `add_button` {#py_cui.PyCUI.add_button}



    
> `def add_button(self, title, row, column, row_span=1, column_span=1, padx=1, pady=0, command=None)`


Function that adds a new button to the CUI grid


    
##### Method `add_checkbox_menu` {#py_cui.PyCUI.add_checkbox_menu}



    
> `def add_checkbox_menu(self, title, row, column, row_span=1, column_span=1, padx=1, pady=0, checked_char='X')`


Function that adds a new checkbox menu to the CUI grid


    
##### Method `add_key_command` {#py_cui.PyCUI.add_key_command}



    
> `def add_key_command(self, key, command)`


Function that adds a keybinding to the CUI when in overview mode


    
##### Method `add_label` {#py_cui.PyCUI.add_label}



    
> `def add_label(self, title, row, column, row_span=1, column_span=1, padx=1, pady=0)`


Function that adds a new label to the CUI grid


    
##### Method `add_scroll_menu` {#py_cui.PyCUI.add_scroll_menu}



    
> `def add_scroll_menu(self, title, row, column, row_span=1, column_span=1, padx=1, pady=0)`


Function that adds a new scroll menu to the CUI grid


    
##### Method `add_text_block` {#py_cui.PyCUI.add_text_block}



    
> `def add_text_block(self, title, row, column, row_span=1, column_span=1, padx=1, pady=0, initial_text='')`


Function that adds a new text box to the CUI grid


    
##### Method `add_text_box` {#py_cui.PyCUI.add_text_box}



    
> `def add_text_box(self, title, row, column, row_span=1, column_span=1, padx=1, pady=0, initial_text='')`


Function that adds a new text box to the CUI grid


    
##### Method `apply_widget_set` {#py_cui.PyCUI.apply_widget_set}



    
> `def apply_widget_set(self, new_widget_set)`


Function that can be used to replace all widgets in a py_cui with those of a different widget set


    
##### Method `check_if_neighbor_exists` {#py_cui.PyCUI.check_if_neighbor_exists}



    
> `def check_if_neighbor_exists(self, row, column, row_span, col_span, direction)`


Function that checks if widget has neighbor in specified cell. Used for navigating CUI


    
##### Method `close_popup` {#py_cui.PyCUI.close_popup}



    
> `def close_popup(self)`


Closes the popup, and resets focus


    
##### Method `display_window_warning` {#py_cui.PyCUI.display_window_warning}



    
> `def display_window_warning(self, stdscr, error_info)`


Function that prints some basic error info if there is an error with the CUI


    
##### Method `draw` {#py_cui.PyCUI.draw}



    
> `def draw(self, stdscr)`


Main CUI draw loop called by start()


    
##### Method `draw_status_bars` {#py_cui.PyCUI.draw_status_bars}



    
> `def draw_status_bars(self, stdscr, height, width)`


Draws status bar and title bar


    
##### Method `draw_widgets` {#py_cui.PyCUI.draw_widgets}



    
> `def draw_widgets(self)`


Function that draws all of the widgets to the screen


    
##### Method `get_widget_set` {#py_cui.PyCUI.get_widget_set}



    
> `def get_widget_set(self)`


Gets widget set object from current widgets.


    
##### Method `handle_key_presses` {#py_cui.PyCUI.handle_key_presses}



    
> `def handle_key_presses(self, key_pressed)`


Function that handles all main loop key presses.


    
##### Method `increment_loading_bar` {#py_cui.PyCUI.increment_loading_bar}



    
> `def increment_loading_bar(self)`


Increments progress bar if loading bar popup is open


    
##### Method `initialize_colors` {#py_cui.PyCUI.initialize_colors}



    
> `def initialize_colors(self)`


Function for initialzing curses colors. Called when CUI is first created.


    
##### Method `initialize_widget_renderer` {#py_cui.PyCUI.initialize_widget_renderer}



    
> `def initialize_widget_renderer(self)`


Function that creates the renderer object that will draw each widget


    
##### Method `lose_focus` {#py_cui.PyCUI.lose_focus}



    
> `def lose_focus(self)`


Function that forces py_cui out of focus mode. After popup is called, focus is lost


    
##### Method `refresh_height_width` {#py_cui.PyCUI.refresh_height_width}



    
> `def refresh_height_width(self, height, width)`


Function that updates the height and width of the CUI based on terminal window size


    
##### Method `set_selected_widget` {#py_cui.PyCUI.set_selected_widget}



    
> `def set_selected_widget(self, widget_id)`


Function that sets the selected cell for the CUI

###### Parameters

**`cell_title`** :&ensp;`str`
:   the title of the cell



    
##### Method `set_status_bar_text` {#py_cui.PyCUI.set_status_bar_text}



    
> `def set_status_bar_text(self, text)`


Sets the status bar text when in overview mode


    
##### Method `set_title` {#py_cui.PyCUI.set_title}



    
> `def set_title(self, title)`


Sets the title bar text


    
##### Method `show_error_popup` {#py_cui.PyCUI.show_error_popup}



    
> `def show_error_popup(self, title, text)`


Shows an error popup


    
##### Method `show_loading_bar_popup` {#py_cui.PyCUI.show_loading_bar_popup}



    
> `def show_loading_bar_popup(self, title, num_items)`


Shows loading bar popup. Use 'increment_loading_bar' to show progress


    
##### Method `show_loading_icon_popup` {#py_cui.PyCUI.show_loading_icon_popup}



    
> `def show_loading_icon_popup(self, title, message)`


Shows a loading icon popup


    
##### Method `show_menu_popup` {#py_cui.PyCUI.show_menu_popup}



    
> `def show_menu_popup(self, title, menu_items, command, run_command_if_none=False)`


Shows a yes/no popup.

The 'command' parameter must be a function with a single boolean parameter


    
##### Method `show_message_popup` {#py_cui.PyCUI.show_message_popup}



    
> `def show_message_popup(self, title, text)`


Shows a message popup


    
##### Method `show_text_box_popup` {#py_cui.PyCUI.show_text_box_popup}



    
> `def show_text_box_popup(self, title, command)`


Shows a yes/no popup.

The 'command' parameter must be a function with a single boolean parameter


    
##### Method `show_warning_popup` {#py_cui.PyCUI.show_warning_popup}



    
> `def show_warning_popup(self, title, text)`


Shows a warning popup


    
##### Method `show_yes_no_popup` {#py_cui.PyCUI.show_yes_no_popup}



    
> `def show_yes_no_popup(self, title, command)`


Shows a yes/no popup.

The 'command' parameter must be a function with a single boolean parameter


    
##### Method `start` {#py_cui.PyCUI.start}



    
> `def start(self)`


Function that starts the CUI


    
##### Method `stop` {#py_cui.PyCUI.stop}



    
> `def stop(self, callback=None)`


Function that stops the CUI, and fires the callback function. Callback must be a no arg method


    
##### Method `stop_loading_popup` {#py_cui.PyCUI.stop_loading_popup}



    
> `def stop_loading_popup(self)`


Leaves loading state, and closes popup. Must be called by user to escape loading.




    
# Module `py_cui.colors` {#py_cui.colors}

File containing all error types for py_cui

@author:    Jakub Wlodek
@created:   12-Aug-2019






    
## Classes


    
### Class `ColorRule` {#py_cui.colors.ColorRule}



> `class ColorRule(regex, color, rule_type, match_type, region, include_whitespace)`











    
#### Methods


    
##### Method `check_match` {#py_cui.colors.ColorRule.check_match}



    
> `def check_match(self, line)`


Checks if the color rule matches a line


    
##### Method `generate_fragments` {#py_cui.colors.ColorRule.generate_fragments}



    
> `def generate_fragments(self, widget, line, render_text)`





    
##### Method `generate_fragments_regex` {#py_cui.colors.ColorRule.generate_fragments_regex}



    
> `def generate_fragments_regex(self, widget, render_text)`


Splits text into fragments based on regular expression


    
##### Method `split_text_on_region` {#py_cui.colors.ColorRule.split_text_on_region}



    
> `def split_text_on_region(self, widget, render_text)`


Splits text into fragments based on region




    
# Module `py_cui.errors` {#py_cui.errors}

File containing all error types for py_cui

@author:    Jakub Wlodek
@created:   12-Aug-2019






    
## Classes


    
### Class `PyCUIError` {#py_cui.errors.PyCUIError}



> `class PyCUIError(*args, **kwargs)`


General error



    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `PyCUIMissingChildError` {#py_cui.errors.PyCUIMissingChildError}



> `class PyCUIMissingChildError(*args, **kwargs)`


Error for when child widget is None or invalid



    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `PyCUIMissingParentError` {#py_cui.errors.PyCUIMissingParentError}



> `class PyCUIMissingParentError(*args, **kwargs)`


Error for when parent widget is None or invalid



    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `PyCUIOutOfBoundsError` {#py_cui.errors.PyCUIOutOfBoundsError}



> `class PyCUIOutOfBoundsError(*args, **kwargs)`


Error for when widget or text goes off of the py_cui grid



    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)








    
# Module `py_cui.grid` {#py_cui.grid}

File containing the Grid Class. The grid is currently the only
supported layout manager for py_cui

@author:    Jakub Wlodek
@created:   12-Aug-2019






    
## Classes


    
### Class `Grid` {#py_cui.grid.Grid}



> `class Grid(num_rows, num_columns, height, width)`











    
#### Methods


    
##### Method `set_num_cols` {#py_cui.grid.Grid.set_num_cols}



    
> `def set_num_cols(self, num_columns)`


Sets the grid column size


    
##### Method `set_num_rows` {#py_cui.grid.Grid.set_num_rows}



    
> `def set_num_rows(self, num_rows)`


Sets the grid row size


    
##### Method `update_grid_height_width` {#py_cui.grid.Grid.update_grid_height_width}



    
> `def update_grid_height_width(self, height, width)`


Update grid height and width. Allows for on-the-fly size editing




    
# Module `py_cui.keybinding` {#py_cui.keybinding}

File containing constants and helper functions for dealing with keys

@author:    Jakub Wlodek
@created:   12-Aug-2019





    
## Functions


    
### Function `get_ascii_from_char` {#py_cui.keybinding.get_ascii_from_char}



    
> `def get_ascii_from_char(char)`





    
### Function `get_char_from_ascii` {#py_cui.keybinding.get_char_from_ascii}



    
> `def get_char_from_ascii(key_num)`








    
# Module `py_cui.popups` {#py_cui.popups}

File containing classes for all popups used by py_cui

@author:    Jakub Wlodek
@created:   12-Aug-2019






    
## Classes


    
### Class `LoadingBarPopup` {#py_cui.popups.LoadingBarPopup}



> `class LoadingBarPopup(root, title, num_items, color, renderer)`


Base popup class. Contains constructor and initial definitions for key_press and draw
Unlike widgets, they do not have a set grid cell, they are simply centered in the view
frame

#### Attributes

**`root`** :&ensp;`PyCUI`
:   the root py_cui window


**`title`**, **`text`** :&ensp;`str`
:   The message title and text


**`color`** :&ensp;`int`
:   The py_cui color code


**`start_x`**, **`start_y`** :&ensp;`int`
:   top left corner of the popup


**`stop_x`**, **`stop_y`** :&ensp;`int`
:   bottom right corner of the popup

#### Methods

handle_key_press()
    Implemented by each subclass, handles key presses
draw()
    Implemented by each subclass, draws the popup to the terminal

Constructor for popup class



    
#### Ancestors (in MRO)

* [py_cui.popups.Popup](#py_cui.popups.Popup)






    
### Class `LoadingIconPopup` {#py_cui.popups.LoadingIconPopup}



> `class LoadingIconPopup(root, title, message, color, renderer)`


Base popup class. Contains constructor and initial definitions for key_press and draw
Unlike widgets, they do not have a set grid cell, they are simply centered in the view
frame

#### Attributes

**`root`** :&ensp;`PyCUI`
:   the root py_cui window


**`title`**, **`text`** :&ensp;`str`
:   The message title and text


**`color`** :&ensp;`int`
:   The py_cui color code


**`start_x`**, **`start_y`** :&ensp;`int`
:   top left corner of the popup


**`stop_x`**, **`stop_y`** :&ensp;`int`
:   bottom right corner of the popup

#### Methods

handle_key_press()
    Implemented by each subclass, handles key presses
draw()
    Implemented by each subclass, draws the popup to the terminal

Constructor for popup class



    
#### Ancestors (in MRO)

* [py_cui.popups.Popup](#py_cui.popups.Popup)






    
### Class `MenuPopup` {#py_cui.popups.MenuPopup}



> `class MenuPopup(root, items, title, color, command, renderer, run_command_if_none)`


A scroll menu widget. Allows for creating a scrollable list of items of which one is selectable. Analogous to a RadioButton 

Constructor for popup class



    
#### Ancestors (in MRO)

* [py_cui.popups.Popup](#py_cui.popups.Popup)






    
#### Methods


    
##### Method `draw` {#py_cui.popups.MenuPopup.draw}



    
> `def draw(self)`


Overrides base class draw function


    
##### Method `get` {#py_cui.popups.MenuPopup.get}



    
> `def get(self)`


Function that gets the selected item from the scroll menu

###### Returns

**`item`** :&ensp;`str`
:   selected item, or None if there are no items in the menu



    
##### Method `handle_key_press` {#py_cui.popups.MenuPopup.handle_key_press}



    
> `def handle_key_press(self, key_pressed)`


Override of base handle key press function


    
##### Method `scroll_down` {#py_cui.popups.MenuPopup.scroll_down}



    
> `def scroll_down(self)`


Function that scrolls the view down in the scroll menu


    
##### Method `scroll_up` {#py_cui.popups.MenuPopup.scroll_up}



    
> `def scroll_up(self)`


Function that scrolls the view up in the scroll menu


    
### Class `MessagePopup` {#py_cui.popups.MessagePopup}



> `class MessagePopup(root, title, text, color, renderer)`


Base popup class. Contains constructor and initial definitions for key_press and draw
Unlike widgets, they do not have a set grid cell, they are simply centered in the view
frame

#### Attributes

**`root`** :&ensp;`PyCUI`
:   the root py_cui window


**`title`**, **`text`** :&ensp;`str`
:   The message title and text


**`color`** :&ensp;`int`
:   The py_cui color code


**`start_x`**, **`start_y`** :&ensp;`int`
:   top left corner of the popup


**`stop_x`**, **`stop_y`** :&ensp;`int`
:   bottom right corner of the popup

#### Methods

handle_key_press()
    Implemented by each subclass, handles key presses
draw()
    Implemented by each subclass, draws the popup to the terminal

Constructor for popup class



    
#### Ancestors (in MRO)

* [py_cui.popups.Popup](#py_cui.popups.Popup)






    
### Class `Popup` {#py_cui.popups.Popup}



> `class Popup(root, title, text, color, renderer)`


Base popup class. Contains constructor and initial definitions for key_press and draw
Unlike widgets, they do not have a set grid cell, they are simply centered in the view
frame

#### Attributes

**`root`** :&ensp;`PyCUI`
:   the root py_cui window


**`title`**, **`text`** :&ensp;`str`
:   The message title and text


**`color`** :&ensp;`int`
:   The py_cui color code


**`start_x`**, **`start_y`** :&ensp;`int`
:   top left corner of the popup


**`stop_x`**, **`stop_y`** :&ensp;`int`
:   bottom right corner of the popup

#### Methods

handle_key_press()
    Implemented by each subclass, handles key presses
draw()
    Implemented by each subclass, draws the popup to the terminal

Constructor for popup class




    
#### Descendants

* [py_cui.popups.MessagePopup](#py_cui.popups.MessagePopup)
* [py_cui.popups.YesNoPopup](#py_cui.popups.YesNoPopup)
* [py_cui.popups.TextBoxPopup](#py_cui.popups.TextBoxPopup)
* [py_cui.popups.MenuPopup](#py_cui.popups.MenuPopup)
* [py_cui.popups.LoadingIconPopup](#py_cui.popups.LoadingIconPopup)
* [py_cui.popups.LoadingBarPopup](#py_cui.popups.LoadingBarPopup)





    
#### Methods


    
##### Method `draw` {#py_cui.popups.Popup.draw}



    
> `def draw(self)`


Must be implemented by subclass


    
##### Method `handle_key_press` {#py_cui.popups.Popup.handle_key_press}



    
> `def handle_key_press(self, key_pressed)`


Must be implemented by subclass


    
### Class `TextBoxPopup` {#py_cui.popups.TextBoxPopup}



> `class TextBoxPopup(root, title, color, command, renderer)`


Base popup class. Contains constructor and initial definitions for key_press and draw
Unlike widgets, they do not have a set grid cell, they are simply centered in the view
frame

#### Attributes

**`root`** :&ensp;`PyCUI`
:   the root py_cui window


**`title`**, **`text`** :&ensp;`str`
:   The message title and text


**`color`** :&ensp;`int`
:   The py_cui color code


**`start_x`**, **`start_y`** :&ensp;`int`
:   top left corner of the popup


**`stop_x`**, **`stop_y`** :&ensp;`int`
:   bottom right corner of the popup

#### Methods

handle_key_press()
    Implemented by each subclass, handles key presses
draw()
    Implemented by each subclass, draws the popup to the terminal

Constructor for popup class



    
#### Ancestors (in MRO)

* [py_cui.popups.Popup](#py_cui.popups.Popup)






    
#### Methods


    
##### Method `clear` {#py_cui.popups.TextBoxPopup.clear}



    
> `def clear(self)`


Clears the text in the textbox


    
##### Method `draw` {#py_cui.popups.TextBoxPopup.draw}



    
> `def draw(self)`


Override of base draw function


    
##### Method `erase_char` {#py_cui.popups.TextBoxPopup.erase_char}



    
> `def erase_char(self)`


Erases character at textbox cursor


    
##### Method `get` {#py_cui.popups.TextBoxPopup.get}



    
> `def get(self)`


Gets value of the text in the textbox


    
##### Method `handle_key_press` {#py_cui.popups.TextBoxPopup.handle_key_press}



    
> `def handle_key_press(self, key_pressed)`


Override of base handle key press function


    
##### Method `insert_char` {#py_cui.popups.TextBoxPopup.insert_char}



    
> `def insert_char(self, key_pressed)`


Inserts char at cursor position. Internal use only


    
##### Method `jump_to_end` {#py_cui.popups.TextBoxPopup.jump_to_end}



    
> `def jump_to_end(self)`


Jumps to the end to the textbox


    
##### Method `jump_to_start` {#py_cui.popups.TextBoxPopup.jump_to_start}



    
> `def jump_to_start(self)`


Jumps to the start of the textbox


    
##### Method `move_left` {#py_cui.popups.TextBoxPopup.move_left}



    
> `def move_left(self)`


Shifts the cursor the the left. Internal use only


    
##### Method `move_right` {#py_cui.popups.TextBoxPopup.move_right}



    
> `def move_right(self)`


Shifts the cursor the the right. Internal use only


    
##### Method `set_text` {#py_cui.popups.TextBoxPopup.set_text}



    
> `def set_text(self, text)`


Sets the value of the text. Overwrites existing text


    
### Class `YesNoPopup` {#py_cui.popups.YesNoPopup}



> `class YesNoPopup(root, title, text, color, command, renderer)`


Base popup class. Contains constructor and initial definitions for key_press and draw
Unlike widgets, they do not have a set grid cell, they are simply centered in the view
frame

#### Attributes

**`root`** :&ensp;`PyCUI`
:   the root py_cui window


**`title`**, **`text`** :&ensp;`str`
:   The message title and text


**`color`** :&ensp;`int`
:   The py_cui color code


**`start_x`**, **`start_y`** :&ensp;`int`
:   top left corner of the popup


**`stop_x`**, **`stop_y`** :&ensp;`int`
:   bottom right corner of the popup

#### Methods

handle_key_press()
    Implemented by each subclass, handles key presses
draw()
    Implemented by each subclass, draws the popup to the terminal

Constructor for popup class



    
#### Ancestors (in MRO)

* [py_cui.popups.Popup](#py_cui.popups.Popup)








    
# Module `py_cui.renderer` {#py_cui.renderer}

File containing the py_cui renderer. It is used to draw all of the onscreen widgets and items.

@author:    Jakub Wlodek
@created:   12-Aug-2019






    
## Classes


    
### Class `Renderer` {#py_cui.renderer.Renderer}



> `class Renderer(root, stdscr)`


Main renderer class used for drawing widgets to the terminal. Has helper functions for drawing the borders, cursor,
and text required for the cui.

All of the functions supplied by the renderer class should only be used internally.








    
#### Methods


    
##### Method `draw_blank_row` {#py_cui.renderer.Renderer.draw_blank_row}



    
> `def draw_blank_row(self, widget, y)`


Internal function for drawing a blank row


    
##### Method `draw_border` {#py_cui.renderer.Renderer.draw_border}



    
> `def draw_border(self, widget, fill=True, with_title=True)`


Draws border around widget

###### Parameters

**`fill`** :&ensp;`bool`
:   a flag that tells the renderer if the widget is filling its grid space, or not (ex. Textbox vs textblock)


**`with_title`** :&ensp;`bool`
:   flag that tells whether or not to draw widget title



    
##### Method `draw_border_bottom` {#py_cui.renderer.Renderer.draw_border_bottom}



    
> `def draw_border_bottom(self, widget, y)`


Internal function for drawing bottom of border


    
##### Method `draw_border_top` {#py_cui.renderer.Renderer.draw_border_top}



    
> `def draw_border_top(self, widget, y, with_title)`


Internal function for drawing top of border


    
##### Method `draw_cursor` {#py_cui.renderer.Renderer.draw_cursor}



    
> `def draw_cursor(self, cursor_y, cursor_x)`


Draws the cursor at a particular location


    
##### Method `draw_text` {#py_cui.renderer.Renderer.draw_text}



    
> `def draw_text(self, widget, line, y, centered=False, bordered=True, selected=False, start_pos=0)`


Function that draws widget text.

###### Parameters

**`widget`** :&ensp;[`Widget`](#py_cui.widgets.Widget)
:   The widget being drawn


**`line`** :&ensp;`str`
:   the line of text being drawn


**`y`** :&ensp;`int`
:   the terminal row (top down) on which to draw the text


**`centered`** :&ensp;`bool`
:   flag to set if the text should be centered


**`bordered`** :&ensp;`bool`
:   a flag to set if the text should be bordered


**`start_pos`** :&ensp;`int`
:   position to start rendering the text from.



    
##### Method `generate_text_color_fragments` {#py_cui.renderer.Renderer.generate_text_color_fragments}



    
> `def generate_text_color_fragments(self, widget, line, render_text)`


Function that applies color rules to text, dividing them if match is found


    
##### Method `get_render_text` {#py_cui.renderer.Renderer.get_render_text}



    
> `def get_render_text(self, widget, line, centered, bordered, start_pos)`


Internal function that computes the scope of the text that should be drawn


    
##### Method `reset_cursor` {#py_cui.renderer.Renderer.reset_cursor}



    
> `def reset_cursor(self, widget, fill=True)`


Positions the cursor at the bottom right of the selected widget

###### Parameters

**`widget`** :&ensp;[`Widget`](#py_cui.widgets.Widget)
:   widget for which to reset cursor


**`fill`** :&ensp;`bool`
:   a flag that tells the renderer if the widget is filling its grid space, or not (ex. Textbox vs textblock)



    
##### Method `set_bold` {#py_cui.renderer.Renderer.set_bold}



    
> `def set_bold(self)`


Sets bold draw mode


    
##### Method `set_color_mode` {#py_cui.renderer.Renderer.set_color_mode}



    
> `def set_color_mode(self, color_mode)`


Sets the output color mode


    
##### Method `set_color_rules` {#py_cui.renderer.Renderer.set_color_rules}



    
> `def set_color_rules(self, color_rules)`


Sets current color rules


    
##### Method `unset_bold` {#py_cui.renderer.Renderer.unset_bold}



    
> `def unset_bold(self)`


Unsets bold draw mode


    
##### Method `unset_color_mode` {#py_cui.renderer.Renderer.unset_color_mode}



    
> `def unset_color_mode(self, color_mode)`


Unsets the output color mode




    
# Module `py_cui.statusbar` {#py_cui.statusbar}

File containing class for the status bar

TODO: File can probably be abstracted away - probably doesn't need a class

@author:    Jakub Wlodek
@created:   12-Aug-2019






    
## Classes


    
### Class `StatusBar` {#py_cui.statusbar.StatusBar}



> `class StatusBar(text, color)`


Very simple class representing a status bar

#### Attributes

**`text`** :&ensp;`str`
:   status bar text


**`color`** :&ensp;`py_cui.COLOR`
:   color to display the statusbar


Constructor for statusbar








    
#### Methods


    
##### Method `set_text` {#py_cui.statusbar.StatusBar.set_text}



    
> `def set_text(self, text)`


Sets the statusbar text




    
# Module `py_cui.widget_set` {#py_cui.widget_set}

File containing class that abstracts a collection of widgets. It can be used to swap between collections
of widgets in a py_cui

@Author: Jakub Wlodek
@Created 05-Oct-2019






    
## Classes


    
### Class `WidgetSet` {#py_cui.widget_set.WidgetSet}



> `class WidgetSet(num_rows, num_cols)`











    
#### Methods


    
##### Method `add_block_label` {#py_cui.widget_set.WidgetSet.add_block_label}



    
> `def add_block_label(self, title, row, column, row_span=1, column_span=1, padx=1, pady=0)`


Function that adds a new label to the CUI grid


    
##### Method `add_button` {#py_cui.widget_set.WidgetSet.add_button}



    
> `def add_button(self, title, row, column, row_span=1, column_span=1, padx=1, pady=0, command=None)`


Function that adds a new button to the CUI grid


    
##### Method `add_checkbox_menu` {#py_cui.widget_set.WidgetSet.add_checkbox_menu}



    
> `def add_checkbox_menu(self, title, row, column, row_span=1, column_span=1, padx=1, pady=0, checked_char='X')`


Function that adds a new checkbox menu to the CUI grid


    
##### Method `add_key_command` {#py_cui.widget_set.WidgetSet.add_key_command}



    
> `def add_key_command(self, key, command)`


Function that adds a keybinding to the CUI when in overview mode


    
##### Method `add_label` {#py_cui.widget_set.WidgetSet.add_label}



    
> `def add_label(self, title, row, column, row_span=1, column_span=1, padx=1, pady=0)`


Function that adds a new label to the CUI grid


    
##### Method `add_scroll_menu` {#py_cui.widget_set.WidgetSet.add_scroll_menu}



    
> `def add_scroll_menu(self, title, row, column, row_span=1, column_span=1, padx=1, pady=0)`





    
##### Method `add_text_block` {#py_cui.widget_set.WidgetSet.add_text_block}



    
> `def add_text_block(self, title, row, column, row_span=1, column_span=1, padx=1, pady=0, initial_text='')`


Function that adds a new text box to the CUI grid


    
##### Method `add_text_box` {#py_cui.widget_set.WidgetSet.add_text_box}



    
> `def add_text_box(self, title, row, column, row_span=1, column_span=1, padx=1, pady=0, initial_text='')`


Function that adds a new text box to the CUI grid


    
##### Method `set_selected_widget` {#py_cui.widget_set.WidgetSet.set_selected_widget}



    
> `def set_selected_widget(self, widget_id)`


Function that sets the selected cell for the CUI

###### Parameters

**`cell_title`** :&ensp;`str`
:   the title of the cell





    
# Module `py_cui.widgets` {#py_cui.widgets}

File contatining all core widget classes for py_cui. Widgets are the basic
building blocks of a user interface made with py_cui. This file contains classes for:

* Base Widget class
* Label
* Block Label
* Scroll Menu
* Checkbox Menu
* Button
* TextBox
* Text Block

Additional widgets should be added in as additional_widgets/$WIDGET_NAME.py, importing this
file and extending the base Widget class, or if appropriate one of the other core widgets.

@author:    Jakub Wlodek
@created:   12-Aug-2019






    
## Classes


    
### Class `BlockLabel` {#py_cui.widgets.BlockLabel}



> `class BlockLabel(id, title, grid, row, column, row_span, column_span, padx, pady)`


A Variation of the label widget that renders a block of text



    
#### Ancestors (in MRO)

* [py_cui.widgets.Widget](#py_cui.widgets.Widget)






    
#### Methods


    
##### Method `draw` {#py_cui.widgets.BlockLabel.draw}



    
> `def draw(self)`


Override base draw class. Center text and draw it


    
### Class `Button` {#py_cui.widgets.Button}



> `class Button(id, title, grid, row, column, row_span, column_span, padx, pady, command)`


Basic button widget. Allows for running a command function on Enter



    
#### Ancestors (in MRO)

* [py_cui.widgets.Widget](#py_cui.widgets.Widget)






    
#### Methods


    
##### Method `draw` {#py_cui.widgets.Button.draw}



    
> `def draw(self)`


Override of base class draw function


    
##### Method `handle_key_press` {#py_cui.widgets.Button.handle_key_press}



    
> `def handle_key_press(self, key_pressed)`


Override of base class, adds ENTER listener that runs the button's command


    
### Class `CheckBoxMenu` {#py_cui.widgets.CheckBoxMenu}



> `class CheckBoxMenu(id, title, grid, row, column, row_span, column_span, padx, pady, checked_char)`


Extension of ScrollMenu that allows for multiple items to be selected at once.



    
#### Ancestors (in MRO)

* [py_cui.widgets.ScrollMenu](#py_cui.widgets.ScrollMenu)
* [py_cui.widgets.Widget](#py_cui.widgets.Widget)






    
#### Methods


    
##### Method `add_item` {#py_cui.widgets.CheckBoxMenu.add_item}



    
> `def add_item(self, item_text)`


Adds item to Checkbox


    
##### Method `add_item_list` {#py_cui.widgets.CheckBoxMenu.add_item_list}



    
> `def add_item_list(self, item_list)`


Adds list of items to the checkbox


    
##### Method `get` {#py_cui.widgets.CheckBoxMenu.get}



    
> `def get(self)`


Gets list of selected items from the checkbox


    
##### Method `handle_key_press` {#py_cui.widgets.CheckBoxMenu.handle_key_press}



    
> `def handle_key_press(self, key_pressed)`


Override of key presses. First, run the superclass function, scrolling should still work. Adds Enter command to toggle selection


    
##### Method `mark_item_as_checked` {#py_cui.widgets.CheckBoxMenu.mark_item_as_checked}



    
> `def mark_item_as_checked(self, text)`


Function that marks an item as selected


    
### Class `Label` {#py_cui.widgets.Label}



> `class Label(id, title, grid, row, column, row_span, column_span, padx, pady)`


The most basic subclass of Widget. Simply displays one centered row of text



    
#### Ancestors (in MRO)

* [py_cui.widgets.Widget](#py_cui.widgets.Widget)






    
#### Methods


    
##### Method `draw` {#py_cui.widgets.Label.draw}



    
> `def draw(self)`


Override base draw class. Center text and draw it


    
### Class `ScrollMenu` {#py_cui.widgets.ScrollMenu}



> `class ScrollMenu(id, title, grid, row, column, row_span, column_span, padx, pady)`


A scroll menu widget. Allows for creating a scrollable list of items of which one is selectable. Analogous to a RadioButton



    
#### Ancestors (in MRO)

* [py_cui.widgets.Widget](#py_cui.widgets.Widget)


    
#### Descendants

* [py_cui.widgets.CheckBoxMenu](#py_cui.widgets.CheckBoxMenu)





    
#### Methods


    
##### Method `add_item` {#py_cui.widgets.ScrollMenu.add_item}



    
> `def add_item(self, item_text)`


Adds an item to the menu.

###### Parameters

**`item_text`** :&ensp;`str`
:   The text for the item



    
##### Method `add_item_list` {#py_cui.widgets.ScrollMenu.add_item_list}



    
> `def add_item_list(self, item_list)`


Adds a list of items to the scroll menu.

###### Parameters

**`item_list`** :&ensp;`list` of `str`
:   list of strings to add as items to the scrollmenu



    
##### Method `clear` {#py_cui.widgets.ScrollMenu.clear}



    
> `def clear(self)`


Clears all items from the Scroll Menu


    
##### Method `draw` {#py_cui.widgets.ScrollMenu.draw}



    
> `def draw(self)`


Overrides base class draw function


    
##### Method `get` {#py_cui.widgets.ScrollMenu.get}



    
> `def get(self)`


Function that gets the selected item from the scroll menu

###### Returns

**`item`** :&ensp;`str`
:   selected item, or None if there are no items in the menu



    
##### Method `get_item_list` {#py_cui.widgets.ScrollMenu.get_item_list}



    
> `def get_item_list(self)`


Function that gets list of items in a scroll menu

###### Returns

**`item_list`** :&ensp;`list` of `str`
:   list of items in the scrollmenu



    
##### Method `handle_key_press` {#py_cui.widgets.ScrollMenu.handle_key_press}



    
> `def handle_key_press(self, key_pressed)`


Override base class function. UP_ARROW scrolls up, DOWN_ARROW scrolls down


    
##### Method `remove_selected_item` {#py_cui.widgets.ScrollMenu.remove_selected_item}



    
> `def remove_selected_item(self)`


Function that removes the selected item from the scroll menu.


    
##### Method `scroll_down` {#py_cui.widgets.ScrollMenu.scroll_down}



    
> `def scroll_down(self)`


Function that scrolls the view down in the scroll menu


    
##### Method `scroll_up` {#py_cui.widgets.ScrollMenu.scroll_up}



    
> `def scroll_up(self)`


Function that scrolls the view up in the scroll menu


    
### Class `ScrollTextBlock` {#py_cui.widgets.ScrollTextBlock}



> `class ScrollTextBlock(id, title, grid, row, column, row_span, column_span, padx, pady, initial_text)`


Widget for editing large multi-line blocks of text



    
#### Ancestors (in MRO)

* [py_cui.widgets.Widget](#py_cui.widgets.Widget)






    
#### Methods


    
##### Method `clear` {#py_cui.widgets.ScrollTextBlock.clear}



    
> `def clear(self)`


Function that clears the text block


    
##### Method `draw` {#py_cui.widgets.ScrollTextBlock.draw}



    
> `def draw(self)`


Override of base class draw function


    
##### Method `get` {#py_cui.widgets.ScrollTextBlock.get}



    
> `def get(self)`


Gets all of the text in the textblock and returns it


    
##### Method `get_current_line` {#py_cui.widgets.ScrollTextBlock.get_current_line}



    
> `def get_current_line(self)`


Returns the line on which the cursor currently resides


    
##### Method `handle_backspace` {#py_cui.widgets.ScrollTextBlock.handle_backspace}



    
> `def handle_backspace(self)`


Function that handles recieving backspace characters in the text


    
##### Method `handle_delete` {#py_cui.widgets.ScrollTextBlock.handle_delete}



    
> `def handle_delete(self)`


Function that handles recieving a delete keypress


    
##### Method `handle_end` {#py_cui.widgets.ScrollTextBlock.handle_end}



    
> `def handle_end(self)`


Function that handles recieving an end keypress


    
##### Method `handle_home` {#py_cui.widgets.ScrollTextBlock.handle_home}



    
> `def handle_home(self)`


Function that handles recieving a home keypress


    
##### Method `handle_key_press` {#py_cui.widgets.ScrollTextBlock.handle_key_press}



    
> `def handle_key_press(self, key_pressed)`


Override of base class handle key press function


    
##### Method `handle_newline` {#py_cui.widgets.ScrollTextBlock.handle_newline}



    
> `def handle_newline(self)`


Function that handles recieving newline characters in the text


    
##### Method `insert_char` {#py_cui.widgets.ScrollTextBlock.insert_char}



    
> `def insert_char(self, key_pressed)`


Function that handles recieving a character


    
##### Method `move_down` {#py_cui.widgets.ScrollTextBlock.move_down}



    
> `def move_down(self)`


Function that moves the cursor/text position one location down


    
##### Method `move_left` {#py_cui.widgets.ScrollTextBlock.move_left}



    
> `def move_left(self)`


Function that moves the cursor/text position one location to the left


    
##### Method `move_right` {#py_cui.widgets.ScrollTextBlock.move_right}



    
> `def move_right(self)`


Function that moves the cursor/text position one location to the right


    
##### Method `move_up` {#py_cui.widgets.ScrollTextBlock.move_up}



    
> `def move_up(self)`


Function that moves the cursor/text position one location up


    
##### Method `set_text` {#py_cui.widgets.ScrollTextBlock.set_text}



    
> `def set_text(self, text)`


Function that sets the text for the textblock. Note that this will overwrite any existing text 

###### Parameters

**`text`** :&ensp;`str`
:   text to write into text block



    
##### Method `set_text_line` {#py_cui.widgets.ScrollTextBlock.set_text_line}



    
> `def set_text_line(self, text)`


Function that sets the current line's text. Meant only for internal use


    
##### Method `write` {#py_cui.widgets.ScrollTextBlock.write}



    
> `def write(self, text)`


Function used for writing text to the text block


    
### Class `TextBox` {#py_cui.widgets.TextBox}



> `class TextBox(id, title, grid, row, column, row_span, column_span, padx, pady, initial_text)`


Widget for entering small single lines of text



    
#### Ancestors (in MRO)

* [py_cui.widgets.Widget](#py_cui.widgets.Widget)






    
#### Methods


    
##### Method `clear` {#py_cui.widgets.TextBox.clear}



    
> `def clear(self)`


Clears the text in the textbox


    
##### Method `draw` {#py_cui.widgets.TextBox.draw}



    
> `def draw(self)`


Override of base draw function


    
##### Method `erase_char` {#py_cui.widgets.TextBox.erase_char}



    
> `def erase_char(self)`


Erases character at textbox cursor


    
##### Method `get` {#py_cui.widgets.TextBox.get}



    
> `def get(self)`


Gets value of the text in the textbox


    
##### Method `handle_key_press` {#py_cui.widgets.TextBox.handle_key_press}



    
> `def handle_key_press(self, key_pressed)`


Override of base handle key press function


    
##### Method `insert_char` {#py_cui.widgets.TextBox.insert_char}



    
> `def insert_char(self, key_pressed)`


Inserts char at cursor position. Internal use only


    
##### Method `jump_to_end` {#py_cui.widgets.TextBox.jump_to_end}



    
> `def jump_to_end(self)`


Jumps to the end to the textbox


    
##### Method `jump_to_start` {#py_cui.widgets.TextBox.jump_to_start}



    
> `def jump_to_start(self)`


Jumps to the start of the textbox


    
##### Method `move_left` {#py_cui.widgets.TextBox.move_left}



    
> `def move_left(self)`


Shifts the cursor the the left. Internal use only


    
##### Method `move_right` {#py_cui.widgets.TextBox.move_right}



    
> `def move_right(self)`


Shifts the cursor the the right. Internal use only


    
##### Method `set_text` {#py_cui.widgets.TextBox.set_text}



    
> `def set_text(self, text)`


Sets the value of the text. Overwrites existing text


    
##### Method `update_height_width` {#py_cui.widgets.TextBox.update_height_width}



    
> `def update_height_width(self)`


Need to update all cursor positions on resize


    
### Class `Widget` {#py_cui.widgets.Widget}



> `class Widget(id, title, grid, row, column, row_span, column_span, padx, pady, selectable=True)`


Top Level Widget Base Class




    
#### Descendants

* [py_cui.widgets.Label](#py_cui.widgets.Label)
* [py_cui.widgets.BlockLabel](#py_cui.widgets.BlockLabel)
* [py_cui.widgets.ScrollMenu](#py_cui.widgets.ScrollMenu)
* [py_cui.widgets.Button](#py_cui.widgets.Button)
* [py_cui.widgets.TextBox](#py_cui.widgets.TextBox)
* [py_cui.widgets.ScrollTextBlock](#py_cui.widgets.ScrollTextBlock)





    
#### Methods


    
##### Method `add_key_command` {#py_cui.widgets.Widget.add_key_command}



    
> `def add_key_command(self, key, command)`


Maps a keycode to a function that will be executed when in focus mode

###### Parameters

**`key`** :&ensp;`py_cui.keys.KEY`
:   ascii keycode used to map the key


**`command`** :&ensp;`function` `without` `args`
:   a non-argument function or lambda function to execute if in focus mode and key is pressed



    
##### Method `add_text_color_rule` {#py_cui.widgets.Widget.add_text_color_rule}



    
> `def add_text_color_rule(self, regex, color, rule_type, match_type='line', region=[0, 1], include_whitespace=False)`


Forces renderer to draw text using given color if text_condition_function returns True

###### Parameters

**`rule_type`** :&ensp;`string`
:   A supported color rule type


**`regex`** :&ensp;`str`
:   A string to check against the line for a given rule type


**`color`** :&ensp;`int`
:   a supported py_cui color value


**`match_entire_line`** :&ensp;`bool`
:   if true, if regex fits rule type, entire line will be colored. If false, only matching text



    
##### Method `assign_renderer` {#py_cui.widgets.Widget.assign_renderer}



    
> `def assign_renderer(self, renderer)`


Function that assigns a renderer object to the widget (Meant for internal usage only)


    
##### Method `draw` {#py_cui.widgets.Widget.draw}



    
> `def draw(self)`


Base class draw class that checks if renderer is valid. Should be called with super().draw() in overrides


    
##### Method `get_absolute_dims` {#py_cui.widgets.Widget.get_absolute_dims}



    
> `def get_absolute_dims(self)`


Gets the absolute dimensions of the widget in characters


    
##### Method `get_absolute_position` {#py_cui.widgets.Widget.get_absolute_position}



    
> `def get_absolute_position(self)`


Gets the absolute position of the widget in characters


    
##### Method `get_help_text` {#py_cui.widgets.Widget.get_help_text}



    
> `def get_help_text(self)`


Returns help text


    
##### Method `handle_key_press` {#py_cui.widgets.Widget.handle_key_press}



    
> `def handle_key_press(self, key_pressed)`


Base class function that handles all assigned key presses.
When overwriting this function, make sure to add a super().handle_key_press(key_pressed) call,
as this is required for user defined key command support


    
##### Method `is_row_col_inside` {#py_cui.widgets.Widget.is_row_col_inside}



    
> `def is_row_col_inside(self, row, col)`


Checks if a particular row + column is inside the widget area


    
##### Method `set_focus_text` {#py_cui.widgets.Widget.set_focus_text}



    
> `def set_focus_text(self, text)`


Function that sets the text of the status bar on focus for a particular widget


    
##### Method `set_selected_color` {#py_cui.widgets.Widget.set_selected_color}



    
> `def set_selected_color(self, color)`


Sets the selected color for the widget


    
##### Method `set_standard_color` {#py_cui.widgets.Widget.set_standard_color}



    
> `def set_standard_color(self, color)`


Sets the standard color for the widget


    
##### Method `update_height_width` {#py_cui.widgets.Widget.update_height_width}



    
> `def update_height_width(self)`


Function that refreshes position and dimensons on resize. If necessary, make sure required widget attributes updated here as well.

