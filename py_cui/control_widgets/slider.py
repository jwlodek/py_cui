import py_cui.ui
import py_cui.widgets
import py_cui.popups


class SliderImplementation(py_cui.ui.UIImplementation):
    pass


class SliderWidget(py_cui.widgets.Widget, SliderImplementation):
    pass


class SliderPopup(py_cui.popups.Popup, SliderImplementation):
    pass