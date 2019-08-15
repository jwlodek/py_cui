import termbox

OUTPUT_NORMAL = termbox.OUTPUT_NORMAL
OUTPUT_256 = termbox.OUTPUT_256

class PyGUI:

    def __init__(self, output_mode):
        self.views = []
        self.current_view = None
        self.managers = []
        self.keybindings = []
        self.max_x = 0
        self.max_y = 0
        self.output_mode = output_mode

        self.background_color = termbox.BLACK
        self.foreground_color = termbox.WHITE

        self.ASCII = False
        self.input_esc = False
        self.cursor = False
        self.highlight = False
        self.mouse = False


    def close(self):
        termbox.