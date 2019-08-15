import pycui.errors

class Cell:

    def __init__(self, chr, background_color, foreground_color):
        self.chr = chr
        self.background_color = background_color
        self.foreground_color = foreground_color


class ViewLine:

    def __init__(self, n_lines_x, n_lines_y, line):
        self.n_lines_x = n_lines_x
        self.n_lines_y = n_lines_y
        self.line = line




class View:


    def __init__(self, name, x0, y0, x1, y1, output_mode):
        self.name = name
        self.coordinates = [[x0, y0],[x1, y1]]
        self.origin_x = 0
        self.origin_y = 0
        self.cursor_x = 0
        self.cursor_y = 0
        self.lines = []
        self.read_offset = 0
        self.read_cache = ''
        self.background_color = 'black'
        self.foreground_color = 'white'

        self.selected_background = 'green'
        self.selected_foreground = 'black'

        self.editable = False

        self.editor = DefaultEditor
        self.tainted = True
        self.ei = newEscapeInterpreter(output_mode)

        self.overwrite = False

        self.highlight = False
        self.frame = True
        self.wrap = False
        self.autoscroll = False

        self.title = 'None'
        self.mask = 0


    def get_view_size(self):
        return self.coordinates[1][0] - self.coordinates[0][0] - 1, self.coordinates[1][1] - self.coordinates[0][1] -1


    def get_view_name(self):
        return self.name


    def check_point_in_view(self, x, y):
        maxX, maxY = self.get_view_size()
        return not (x < 0 or x >= maxX or y < 0 or y >= maxY)


    def set_rune(self, x, y, rune):
        if not self.check_point_in_view(x, y):
            raise pycui.errors.PyCUIOutOfBoundsError
        if self.highlight:
            _, rune_y, err = self.real_position(x, y)
            if err is not None:
                return err
            _, rune_cursor_y, err = self.real_position(x, y)
            if err is not None:
                return err
        foreground_color = self.selected_foreground
        background_color = self.selected_background
        # here need to set the cell color



    def set_cursor(self, x, y):
        if not self.check_point_in_view(x, y):
            raise pycui.errors.PyCUIOutOfBoundsError

        self.cursor_x = x
        self.cursor_y = y


    def get_cursor(self):
        return self.cursor_x, self.cursor_y


    def set_origin(self, x, y):
        
        if not self.check_point_in_view(x,y):
            raise pycui.errors.PyCUIOutOfBoundsError

        self.origin_x = x
        self.origin_y = y


    def get_origin(self):
        return self.origin_x, self.origin_y



    def write(self, in_bytes):
        self.tainted = True

        for char in in_bytes:
            if char == '\n':
                self.lines.append([])
            elif char == '\r':
                num_lines = len(self.lines)
                if num_lines > 0:
                    del self.lines[-1]
            else:
                cells = self.parse_input(char)
                num_lines = len(self.lines)
                if num_lines == 0:
                    self.lines.append([])
                self.lines[-1].append(cells)
        return len(in_bytes)


    def parse_input(self, char):
        cells = []
        try:
            is_escape, err = self.ei.parse_one(char)
        except PyCUIError:
            for rune in self.ei.runes:
                cell = Cell(char, self.background_color, self.foreground_color)
                cells.append(cell)
            self.ei.reset()
            return cells
        if is_escape:
            return None
        cell = Cell(char, self.ei.background_color, self.ei.foreground_color)
        cells.append(cell)
        return cells


    def line_to_str(self, line):
        out_str = ''
        for cell in line:
            out_str = out_str + cell.chr
        return out_str


    def read(self):
        if sel.read_offset == 0:
            self.read_cache = self.Buffer()
        if self.read_offset < len(self.read_cache):
            

    def rewind(self):
        self.read_offset = 0



    def draw(self):
        max_x, max_y = self.get_view_size()

        if self.wrap:
            if max_x == 0:
                raise pycui.errors.PyCUIOutOfBoundsError
            self.origin_x = 0
        if self.tainted:
            self.view_lines = []
            counter = 0
            for line in self.lines:
                if self.wrap:
                    if len(line) < self.max_x:
                        view_line = ViewLine(0, counter, line)
                        self.view_lines.append(view_line)
                        continue
                    else:
                        n = 0
                        while n <= len(line):
                            if len(line[n:]) <= max_x:
                                view_line = ViewLine(n, counter, line[n:]) 
                                self.view_lines.append(view_line)
                            else:
                                view_line = ViewLine(n, counter, line[n:n+max_x])
                                self.view_lines.append(view_line)
                            n = n+max_x
                else:
                    view_line = ViewLine(0, counter, line)
                    self.view_lines.append(view_line)
                counter = counter + 1
            self.tainted = False

        if self.autoscroll and len(self.view_lines) > max_y:
            self.origin_y = len(self.view_lines) - max_y

        y = 0
        counter = 0
        for view_line in self.view_lines:
            if counter < self.origin_y:
                continue
            if y >= max_y:
                break
            x = 0
            counter_x = 0
            for rune in view_line.line:
                if counter_x < self.origin_x:
                    continue
                if x >= max_x:
                    break
                foreground_color = rune.foreground_color
                background_color = rune.background_color
                
                self.set_rune(x, y, rune.chr, foreground_color, background_color)
                x = x + 1
                counter_x = counter_x + 1
            y = y + 1
            counter = counter + 1


    def real_position(self, view_x, view_y):
        actual_x = self.origin_x + view_x
        actual_y = self.origin_y + view_y
        if actual_x < 0 or actual_y < 0:
            raise pycui.errors.PyCUIOutOfBoundsError
        
        if len(self.view_lines) == 0:
            return actual_x, actual_y
        
        if actual_y < len(self.view_lines):
            view_line = self.view_lines[actual_y]
            x = view_line.n_lines_x + actual_x
            y = view_line.n_lines_y
        else:
            view_line = self.view_lines[-1]
            x = actual_x
            y = view_line.n_lines_y + actual_y - len(self.view_lines) + 1
        return x, y


    def clear(self):
        self.tainted = True
        self.lines = []
        self.view_lines = []
        self.read_offset = 0
        self.clear_runes()

    def clear_runes(self):
        max_x, max_y = self.get_view_size()
        for x in range(max_x):
            for y in range(max_y):
                # set_cell(self.coordinates[0][0] + x + 1, self.coordinates[0][1] + y + 1, ' ', self.foreground, self.background)
        

    def buffer_lines(self):
        out_lines = []
        for line in self.lines:
            out_str = self.line_to_str(line)
            out_lines.append(out_str)
        return out_lines


    def buffer(self):
        out_str = ''
        for line in self.lines:
            out_str = out_str + self.line_to_str(line) + '\n'
        return out_str

    def view_buffer_lines(self):
        out_lines = []
        for line in self.view_lines:
            out_str = self.line_to_str(line)
            out_lines.append(out_str)
        return out_lines


    def view_buffer(self):
        out_str = ''
        for line in self.view_lines:
            out_str = out_str + self.line_to_str(line) + '\n'
        return out_str


    def line(self, y):
        _, y, err = self.real_position(0, y)
        if not self.check_point_in_view(0, y):
            raise pycui.errors.PyCUIOutOfBoundsError
        return self.line_to_str(self.lines[y])


    def word(self, x, y):
        x, y = self.real_position(x, y)
        if not self.check_point_in_view(x, y):
            raise pycui.errors.PyCUIOutOfBoundsError
        line_str = self.line_to_str(self.lines[y])
        line_str = line_str[:x]
        words = line_str.split(' ')
        return words[0]

