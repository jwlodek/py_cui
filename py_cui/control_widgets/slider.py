import py_cui.ui
import py_cui.widgets
import py_cui.popups


class SliderImplementation(py_cui.ui.UIImplementation):

    _bar_char = '#'

    def __init__(self, min_val, max_val, init_val, step, logger):
        super().__init__(logger)

        self._min_val = min_val
        self._max_val = max_val
        self._cur_val = init_val
        self._step = step

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

        self.title_enabled = False
        self.border_enabled = False
        self.display_value = True
        self.fine_step = False


    def _draw(self):
        """Override of base class draw function
        """

        super()._draw()
        self._renderer.set_color_mode(self._color)

        text_y_pos = self._start_y + int(self._height / 2)

        # screen length of the slider bar
        height, width = self.get_absolute_dimensions()
        width -= 2

        if self.border_enabled:
            # Bordered, either entitled or not titled
            self._renderer.draw_border(self, fill=False, with_title=self.title_enabled)
            text_y_pos += 1
            width -= 4

        elif self.title_enabled:
            # Entitled borderless
            self._renderer.draw_text(self, self.get_title(), text_y_pos, bordered=False)
            text_y_pos += 1

        progress = self._bar_char * int((width * self._cur_val) / self._max_val)

        if self.display_value:
            rounded_str_val = str(int(self._cur_val))
            progress = progress[: -len(rounded_str_val)] + rounded_str_val

        self._renderer.draw_text(self,
                                 progress,
                                 text_y_pos,
                                 centered=False,
                                 bordered=self.border_enabled
                                 )

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
