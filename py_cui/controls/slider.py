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
                f'initial value must be between {self._min_val} and {self._max_val}')


    def set_bar_char(self, char):
        """
        Updates the character used to represent the slider bar.

        Parameters
        ----------
        char : str
            Character to represent progressive bar.
        """

        assert len(char) == 1, f"char should contain exactly one character, got {len(char)} instead."
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

        if self._cur_val < self._min_val:
            self._cur_val = self._min_val

        elif self._cur_val > self._max_val:
            self._cur_val = self._max_val

        return self._cur_val


    def get_slider_value(self):
        """
        Returns current slider value.

        Returns
        -------
        self._cur_val: float
            Current slider value.
        """

        return self._cur_val


    def set_slider_step(self, step):
        """
        Changes the step value.

        Parameters
        ----------
        step : int
            Step size of the slider.
        """

        self._step = step


class SliderWidget(py_cui.widgets.Widget, SliderImplementation):
    """
    Widget for a Slider

    Parameters
    ----------
    min_val : int
        Lowest value of the slider
    max_val: int
        Highest value of the slider
    step : int
        Increment from low to high value
    init_val:
        Initial value of the slider
    """

    def __init__(self, id, title, grid, row, column, row_span, column_span,
                 padx, pady, logger, min_val, max_val, step, init_val):

        SliderImplementation.__init__(self, min_val, max_val, init_val, step, logger)

        py_cui.widgets.Widget.__init__(self, id, title, grid, row, column,
                                       row_span, column_span, padx,
                                       pady, logger, selectable=True)

        self._title_enabled = True
        self._border_enabled = True
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
        """Aligns widget height to middle. default configuration.
        """
        self._alignment = "mid"


    def align_to_bottom(self):
        """Aligns widget height to bottom.
        """
        self._alignment = "btm"


    def _custom_draw_with_border(self, start_y: int, content: str):
        """
        Custom method made from renderer.draw_border to support alignment for bordered variants.

        Parameters
        ----------
        start_y : int
            border's Y-axis starting coordination
        content: str
            string to be drawn inside the border
        """

        # having closer reference allow faster access. More dot access means more scopes to search for.
        renderer = self.get_renderer()
        ui_element = self

        renderer.set_color_mode(ui_element.get_border_color())

        if ui_element.is_selected():
            renderer._set_bold()
            renderer._draw_border_top(ui_element, start_y, False)

            renderer.draw_text(ui_element, content, start_y + 1, selected=True, bordered=True)
            renderer._set_bold()

            renderer._draw_border_bottom(ui_element, start_y + 2)
            renderer._unset_bold()
        else:
            renderer._draw_border_top(ui_element, start_y, False)
            renderer.draw_text(ui_element, content, start_y + 1, selected=False, bordered=True)
            renderer._draw_border_bottom(ui_element, start_y + 2)

        renderer.unset_color_mode(ui_element.get_border_color())


    def _generate_bar(self, width: int) -> str:
        """
        Internal implementation to generate progression bar.

        Parameters
        ----------
        width : int
            Width of bar in character length.

        Returns
        -------
        progress: str
            progressive bar string  with length of width.
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
        """Override of base class draw function.
        """

        super()._draw()
        self._renderer.set_color_mode(self._color)

        height, width = self.get_absolute_dimensions()
        visual_height = (2 if self._border_enabled else 0) + (1 if self._title_enabled else 0)

        if self._alignment == "top":
            text_y_pos = self._start_y
        elif self._alignment == "mid":
            text_y_pos = self._start_y + ((height - visual_height) // 2)
        else:
            text_y_pos = self._start_y + height - visual_height - 1

        if self._title_enabled:
            self._renderer.draw_text(
                self, self.get_title(), text_y_pos, selected=self.is_selected(), bordered=False
            )
            text_y_pos += 1

        if self._border_enabled:
            width -= 6
            self._custom_draw_with_border(text_y_pos, self._generate_bar(width))
        else:
            width -= 2
            self._renderer.draw_text(
                self, self._generate_bar(width), text_y_pos, selected=self.is_selected(), bordered=False
            )

        self._renderer.unset_color_mode(self._color)


    def _handle_key_press(self, key_pressed):
        """
        LEFT_ARROW decreases value, RIGHT_ARROW increases.

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
