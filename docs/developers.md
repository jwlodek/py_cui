# Documentation for py_cui Developers

This page contains information on writing new widgets and popups, as well as anything else required for developers and contributors for py_cui.

### Adding a new Widget

We will walk through the steps of adding a new widget to py_cui (in this case a scroll menu) in order to demonstrate this process.


**Step One - Extend the Widget Class**

Your first step when writing a new widget is to create a class in `py_cui/widgets.py` that extends the base `Widget` class. For our `ScrollMenu` example:

```Python
class ScrollMenu(Widget):

    def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady):
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)

    def handle_key_press(self, key_pressed):

        super().handle_key_press(key_pressed)

    def draw(self):

        super().draw()
```
The `handle_key_press` and `draw` functions must be extended for your new widget. You may leave the `handle_key_press` as above, if you don't require any keybindings for the widget. The `draw` function must extended, as the base class does no drawing itself, instead just setting up color rules.

**Step Two - Add additional class variables**

Next, add any variables that your widget may require on top of the base `Widget` class variables. In our case, it will be the selected item index, a list of menu items, and an integer representing the top item visible (in case the menu scrolls down). We also add some functions for getting and setting these variables.

```Python
def __init__(self, id, title, grid, row, column, row_span, column_span, padx, pady):
    super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)
    self.top_view = 0
    self.selected_item = 0
    self.view_items = []


def clear(self):
    """ Clears all items from the Scroll Menu """

    self.view_items = []
    self.selected_item = 0
    self.top_view = 0


def add_item_list(self, item_list):

    for item in item_list:
        self.add_item(item)


def remove_selected_item(self):

    if len(self.view_items) == 0:
        return
    del self.view_items[self.selected_item]
    if self.selected_item >= len(self.view_items):
        self.selected_item = self.selected_item - 1


def get_item_list(self):

    return self.view_items


def get(self):

    if len(self.view_items) > 0:
        return self.view_items[self.selected_item]
    return None
```

**Step 3 - Add Key Bindings**

Next, add any default key bindings you wish to have for the widget when in focus mode. In the case of the scroll menu, we wish for the arrow keys to scroll up and down, so we extend the `handle_key_press` function:
```Python
def scroll_up(self):

    if self.selected:
        if self.top_view > 0:
            self.top_view = self.top_view - 1
        if self.selected_item > 0:
            self.selected_item = self.selected_item - 1


def scroll_down(self):

    if self.selected:
        if self.selected_item < len(self.view_items) - 1:
            self.selected_item = self.selected_item + 1
        if self.selected_item > self.top_view + self.height - (2 * self.pady) - 3:
            self.top_view = self.top_view + 1


def handle_key_press(self, key_pressed):

    super().handle_key_press(key_pressed)
    if key_pressed == py_cui.keys.KEY_UP_ARROW:
        self.scroll_up()
    if key_pressed == py_cui.keys.KEY_DOWN_ARROW:
        self.scroll_down()
```
Note that the way default key bindings are added are simply `if` statements, which happen after the `super()` call. The `scroll_up()` and `scroll_down()` functions simply contain the logic for editing the viewport for the menu.

**Step 4 - implement the Draw function**

In the draw function, you must use the `self.renderer` object to render your widget to the screen. In our case, we want a border around the menu widget, and we also want to draw menu items that are within our viewport. The key renderer functions we will use are:
```Python
self.renderer.draw_border(self)
```
which will draw a border around the widget space, and 
```Python
self.renderer.draw_text(self, text, y_position)
```
which will draw the text in the y_position. For our scroll menu, we would write the following:
```Python
def draw(self):

    super().draw()
    # sets the color mode
    self.renderer.set_color_mode(self.color)
    # draws border around widget
    self.renderer.draw_border(self)
    # will store the current y-position
    counter = self.pady + 1
    line_counter = 0
    for line in self.view_items:
        # Until we reach viewport start, increment counter
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
    # reset default colors
    self.renderer.unset_color_mode(self.color)
    # reset cursor should be called at the end of every draw function
    self.renderer.reset_cursor(self)
```

**Step 5 - add a function to `__init__.py` to add the widget**

Finally, add a function to `__init__.py` that will add the widget to the CUI. In our case we write the following:
```Python
def add_scroll_menu(self, title, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0):

    id = 'Widget{}'.format(len(self.widgets.keys()))
    new_scroll_menu = widgets.ScrollMenu(id, title, self.grid, row, column, row_span, column_span, padx, pady)
    self.widgets[id] = new_scroll_menu
    if self.selected_widget is None:
        self.set_selected_widget(id)
    return new_scroll_menu
```
The function must:
* Create an id titled 'Widget####' where #### is replaced with the number of widget
* Add the widget to the PyCUI widgets dict with the ID as a key
* If there is no selected widget, make this new widget the selected one
* Return a reference to the widget

**That's it!**

Your widget is now ready to be added to the CUI!

### Adding a new Popup

This documentation section is incomplete. Feel free to [expand me](https://github.com/jwlodek/py_cui/pulls).

### Working on the renderer

This documentation section is incomplete. Feel free to [expand me](https://github.com/jwlodek/py_cui/pulls).

### Working on color rules

This documentation section is incomplete. Feel free to [expand me](https://github.com/jwlodek/py_cui/pulls).