

class Keybinding:

    def __init__(self, view_name, key, rune, handler_function):
        self.view_name = view_name
        self.key = key
        self.rune = rune
        self.handler_function = handler_function

    def match_key_press(self, key, rune):
        return self.key == key and self.rune == rune

    def match_view(self, view):
        if len(self.view_name) == 0:
            return True
        else:
            return view is not None and self.view_name == view.view_name

    