import py_cui.ui
import py_cui.widgets
import py_cui.popups


class SliderImplementation(py_cui.ui.UIImplementation):

    def __init__(self, min_val, max_val, init_val, step, logger):
        super().__init__(logger)

        self._min_val = min_val
        self._max_val = max_val
        self._cur_val = init_val
        self._step = step

        self._bar_char = "#"

        if self._cur_val < self._min_val or self._cur_val > self._max_val:
            raise py_cui.errors.PyCUIInvalidValue(
                'initial value must be between {} and {}'
                .format(self._min_val, self._max_val))


    def set_bar_char(self, char):
        """Updates the character used to represent the slider bar
        """

        self._bar_char = char


    def update_slider_value(self, offset: int) -> float:
        """
        Steps up or down the value in offset fashion.

        Parameters
        ----------
        offset : int
            Number of steps to increase or decrease the slider value.

        Returns
        -------
        self._cur_val: float
            Current slider value.

        """

        # direction , 1 raise value, -1 lower value
        self._cur_val += (offset * self._step)

        if self._cur_val <= self._min_val:
            self._cur_val = self._min_val

        if self._cur_val >= self._max_val:
            self._cur_val = self._max_val

        return self._cur_val


    def get_slider_value(self):
        """return current slider value
        """
        return self._cur_val


    def set_slider_step(self,step):
        """change step value
        """
        self._step = step


class SliderWidget(py_cui.widgets.Widget, SliderImplementation):
    """Widget for a Slider
    """

    """
    Parameters
    ----------
    _min_val : int
        Lowest value of the slider
    _max_val: int
        Highest value of the slider
    _step : int
        Increment from low to high value
    _cur_val:
        Current value of the slider

    """

    def __init__(self, id, title, grid, row, column, row_span, column_span,
                 padx, pady, logger, min_val, max_val, step, init_val):

        SliderImplementation.__init__(self, min_val, max_val, init_val, step, logger)

        py_cui.widgets.Widget.__init__(self, id, title, grid, row, column,
                                       row_span, column_span, padx,
                                       pady, logger, selectable=True)

        self._title_enabled = False
        self._border_enabled = False
        self._display_value = True
        self._alignment = "mid"
        self.set_help_text("Focus mode on Slider. Use left/right to adjust value. Esc to exit.")


    def toggle_title(self):
        """Toggles visibility of the widget's name.
        """

        self._title_enabled = not self._title_enabled


    def toggle_border(self):
        """Toggles visibility of the widget's border.
        """

        self._border_enabled = not self._border_enabled


    def toggle_value(self):
        """Toggles visibility of the widget's current value in integer.
        """

        self._display_value = not self._display_value


    def align_to_top(self):
        """Aligns widget height to top.
        """
        self._alignment = "top"


    def align_to_middle(self):
        """Aligns widget height to middle, default option.
        """
        self._alignment = "mid"


    def align_to_bottom(self):
        """Aligns widget height to bottom.
        """
        self._alignment = "btm"


    def _draw(self):
        """Override of base class draw function
        """

        super()._draw()
        self._renderer.set_color_mode(self._color)

        text_y_pos = self._start_y + int(self._height / 2)

        height, width = self.get_absolute_dimensions()
        width -= 2

        # Bordered, either entitled or not titled
        if self._border_enabled:
            self._renderer.draw_border(self, fill=False, with_title=self._title_enabled)
            text_y_pos += 1
            width -= 4

        # Entitled borderless
        elif self._title_enabled:
            self._renderer.draw_text(self, self.get_title(), text_y_pos, bordered=False)
            text_y_pos += 1

        # Compensate length in case for negative values
        if self._display_value:
            min_string = str(self._min_val)
            width -= len(min_string)

        progress = self._bar_char * int((width * (self._cur_val - self._min_val)) / (self._max_val - self._min_val))

        # Compensate length for current value
        if self._display_value:
            str_current = str(int(self._cur_val))
            progress = (self._bar_char * len(min_string) + progress)[: -len(str_current)] + str_current

        self._renderer.draw_text(self, progress, text_y_pos, centered=False, bordered=self._border_enabled)
        self._renderer.unset_color_mode(self._color)


    def _handle_key_press(self, key_pressed):
        """LEFT_ARROW decrease value, RIGHT_ARROW increase.

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """

        super()._handle_key_press(key_pressed)
        if key_pressed == py_cui.keys.KEY_LEFT_ARROW:
            self.update_slider_value(-1)
        if key_pressed == py_cui.keys.KEY_RIGHT_ARROW:
            self.update_slider_value(1)


class SliderPopup(py_cui.popups.Popup, SliderImplementation):
    pass
