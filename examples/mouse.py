import py_cui
import py_cui.keys as KEYS


class MouseApp:

    def __init__(self, root: py_cui.PyCUI):

        # Initialize our two widgets, a button and a mous press log
        self.root = root
        self.button_presser = self.root.add_button('Press Me!', 0, 0)
        self.mouse_press_log = self.root.add_text_block('Mouse Presses', 1, 0, row_span=2)

        # This demonstrates how you can get mouse press coordinates to a mouse press event function
        # You may pass in either a no-parameter function or one with two parameters as the second argument
        # to add_mouse_command. If it is detected as one with two parameters, the function will be ran with
        # the x, y coordinates of the press in terminal characters as the input.
        self.button_presser.add_mouse_command(KEYS.LEFT_MOUSE_CLICK, self.print_left_press_with_coords)

        # Demonstration of how to add mouse commands for remaining left click events
        self.button_presser.add_mouse_command(KEYS.LEFT_MOUSE_DBL_CLICK, lambda: self.mouse_press_log.set_text('Left Double\n' + self.mouse_press_log.get()))
        self.button_presser.add_mouse_command(KEYS.LEFT_MOUSE_PRESSED, lambda: self.mouse_press_log.set_text('Left Pressed\n' + self.mouse_press_log.get()))
        self.button_presser.add_mouse_command(KEYS.LEFT_MOUSE_RELEASED, lambda: self.mouse_press_log.set_text('Left Released\n' + self.mouse_press_log.get()))
        self.button_presser.add_mouse_command(KEYS.LEFT_MOUSE_TRPL_CLICK, lambda: self.mouse_press_log.set_text('Left Triple\n' + self.mouse_press_log.get()))


        self.button_presser.add_mouse_command(KEYS.MIDDLE_MOUSE_CLICK, lambda: self.mouse_press_log.set_text('Middle Single\n' + self.mouse_press_log.get()))
        self.button_presser.add_mouse_command(KEYS.MIDDLE_MOUSE_DBL_CLICK, lambda: self.mouse_press_log.set_text('Middle Double\n' + self.mouse_press_log.get()))
        self.button_presser.add_mouse_command(KEYS.MIDDLE_MOUSE_PRESSED, lambda: self.mouse_press_log.set_text('Middle Pressed\n' + self.mouse_press_log.get()))
        self.button_presser.add_mouse_command(KEYS.MIDDLE_MOUSE_RELEASED, lambda: self.mouse_press_log.set_text('Middle Released\n' + self.mouse_press_log.get()))
        self.button_presser.add_mouse_command(KEYS.MIDDLE_MOUSE_TRPL_CLICK, lambda: self.mouse_press_log.set_text('Middle Triple\n' + self.mouse_press_log.get()))

        # Demonstration of how to add mouse commands for remaining right click events
        self.button_presser.add_mouse_command(KEYS.RIGHT_MOUSE_CLICK, lambda: self.mouse_press_log.set_text('Right Single\n' + self.mouse_press_log.get()))
        self.button_presser.add_mouse_command(KEYS.RIGHT_MOUSE_DBL_CLICK, lambda: self.mouse_press_log.set_text('Right Double\n' + self.mouse_press_log.get()))
        self.button_presser.add_mouse_command(KEYS.RIGHT_MOUSE_PRESSED, lambda: self.mouse_press_log.set_text('Right Pressed\n' + self.mouse_press_log.get()))
        self.button_presser.add_mouse_command(KEYS.RIGHT_MOUSE_RELEASED, lambda: self.mouse_press_log.set_text('Right Released\n' + self.mouse_press_log.get()))
        self.button_presser.add_mouse_command(KEYS.RIGHT_MOUSE_TRPL_CLICK, lambda: self.mouse_press_log.set_text('Right Triple\n' + self.mouse_press_log.get()))


        # Two scroll menus demonstrating how to handle drag and drop functionality with py_cui
        self.drag_from = self.root.add_scroll_menu('Drag From', 0, 1, row_span=3)
        self.drag_to = self.root.add_scroll_menu('Drag To', 0, 2, row_span=3)

        self.drag_from.add_mouse_command(KEYS.LEFT_MOUSE_PRESSED, self.drag)
        self.drag_to.add_mouse_command(KEYS.LEFT_MOUSE_RELEASED, self.drop)

        self.drag_from.add_item_list(['Drag Me', 'Drop Me Too'])

        self.current_clipboard_elem = None



    def drag(self):
        self.current_clipboard_elem = self.drag_from.get()


    def drop(self):
        self.drag_to.add_item(self.current_clipboard_elem)
        self.drag_from.remove_item(self.current_clipboard_elem)
        self.current_clipboard_elem = None


    def print_left_press_with_coords(self, x, y):

        self.mouse_press_log.set_text(f'Left Single w/ coords {x}, {y}\n' + self.mouse_press_log.get())



root = py_cui.PyCUI(3, 3)
MouseApp(root)
root.start()