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
        """Toggles visibility of the widget's border. Enabling this will disable the alignment.
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


    def _custom_draw_border(self, start_y: int):
        """Custom method made from renderer.draw_border to support alignment for bordered variants.

        Parameters
        ----------
        start_y : int
            border's Y-axis starting coordination
        """

        start_y = start_y
        renderer = self.get_renderer()
        ui_element = self

        if ui_element.is_selected():
            renderer._set_bold()

        renderer.set_color_mode(ui_element.get_border_color())

        renderer._draw_border_top(ui_element, start_y, False)
        renderer._draw_blank_row(ui_element, start_y + 1)
        renderer._draw_border_bottom(ui_element, start_y + 2)

        renderer.unset_color_mode(ui_element.get_border_color())

        if ui_element.is_selected():
            renderer._unset_bold()


    def _generate_bar(self, width: int) -> str:
        """Internal implementation to generate progression bar

        Parameters
        ----------
        width : int
            Width of bar in character length.
        """
        if self._display_value:
            min_string = str(self._min_val)
            value_str = str(int(self._cur_val))

            width -= len(min_string)

            bar = self._bar_char * int((width * (self._cur_val - self._min_val)) / (self._max_val - self._min_val))
            progress = (self._bar_char * len(min_string) + bar)[: -len(value_str)] + value_str
        else:
            progress = self._bar_char * int((width * (self._cur_val - self._min_val)) / (self._max_val - self._min_val))

        return progress


    def _draw(self):
        """Override of base class draw function
        """

        super()._draw()
        self._renderer.set_color_mode(self._color)

        height, width = self.get_absolute_dimensions()
        width -= 6

        visual_height = (2 if self._border_enabled else 0) + (1 if self._title_enabled else 0)

        if self._alignment == "top":
            text_y_pos = self._start_y
        elif self._alignment == "mid":
            text_y_pos = self._start_y + ((height - visual_height) // 2)
        else:
            text_y_pos = self._start_y + height - visual_height - 1

        if self._title_enabled:
            self._renderer.draw_text(self, self.get_title(), text_y_pos, bordered=False)
            text_y_pos += 1

        if self._border_enabled:
            self._custom_draw_border(self, text_y_pos)
            self._renderer.draw_text(self, self._generate_bar(width), text_y_pos + 1, bordered=True)
        else:
            self._renderer.draw_text(self, self._generate_bar(width), text_y_pos, bordered=False)

        self._renderer.unset_color_mode(self._color)


    def _handle_key_press(self, key_pressed):
        """LEFT_ARROW decreases value, RIGHT_ARROW increases.

        Parameters
        ----------
        key_pressed : int
            key code of pressed key
        """

        super()._handle_key_press(key_pressed)
        if key_pressed == py_cui.keys.KEY_LEFT_ARROW:
            self.update_slider_value(-1)
        if key_pressed == py_cui.keys.KEY_RIGHT_ARROW:
            self.update_slider_value(1)


class SliderPopup(py_cui.popups.Popup, SliderImplementation):
    pass
