import py_cui.ui
import py_cui.widgets
import py_cui.popups


class SliderImplementation(py_cui.ui.UIImplementation):

    def set_bar_char(self,char):
        self._bar_char = char

    def update_slider_value(self, direction):
        """ set the value of the slider - increment decrement
        """
        # direction , 1 raise value, -1 lower value
        self._cur_val += (direction * self._step)
        if (self._cur_val <= self._min_val):
            self._cur_val = self._min_val
        if (self._cur_val >= self._max_val):
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
    Attributes
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
    _bar_char = '#'

    def __init__(self, id, title, grid, row, column, row_span, column_span,
                 padx, pady, logger, min_val, max_val, step, init_val):

        super().__init__(id, title, grid, row, column,
                         row_span, column_span, padx, pady, logger,
                         selectable=True)

        self._min_val = min_val
        self._max_val = max_val
        self._cur_val = init_val
        self._step = step

        if self._cur_val < self._min_val or self._cur_val > self._max_val:
            raise Exception('initial value must be between {} and {}'
                            .format(self._min_val, self._max_val))

    def _draw(self):

        super()._draw()
        self._renderer.set_color_mode(self._color)
        target_y = self._start_y + int(self._height / 2)

        # simple normalize width:
        # ratio between screen bar width and bar interval
        fact = (self._max_val - self._min_val) / (self._width - 4)
        # screen length of the slider bar
        _len = int((self._cur_val - self._min_val) / fact)
        # append percentual
        _bar_length = _len - len(str(self._max_val))

        _bar = " " + self._bar_char * _bar_length + str(self._cur_val)

        self._renderer.draw_text(self,
                                 _bar,
                                 target_y,
                                 centered=False,
                                 bordered=False
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
