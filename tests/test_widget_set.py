import pytest # noqa
import py_cui
from py_cui.widget_set import WidgetSet

import py_cui.debug as dbg

logger = dbg.PyCUILogger('widget_set.WidgetSet TEST')


def test_create():
    test_widget_set = WidgetSet(4, 5, logger, simulated_terminal=[30, 100])
    assert test_widget_set._simulated_terminal == [30, 100]
    assert test_widget_set._height == 26
    assert test_widget_set._width == 100


def test_add_scroll_menu():
    test_widget_set = WidgetSet(4, 5, logger, simulated_terminal=[30, 100])
    test_widget_set.add_scroll_menu('Demo', 1, 1)
    assert len(test_widget_set.get_widgets().keys()) == 1
    for key in test_widget_set.get_widgets().keys():
        assert key == 'Widget0'
        break
    widget = test_widget_set.get_widgets()['Widget0']
    assert isinstance(widget, py_cui.widgets.ScrollMenu)
    assert widget.get_id() == 'Widget0'
    row, col = widget.get_grid_cell()
    assert row == 1
    assert col == 1


def test_add_checkbox_menu():
    test_widget_set = WidgetSet(4, 5, logger, simulated_terminal=[30, 100])
    test_widget_set.add_checkbox_menu('Demo', 1, 1)
    assert len(test_widget_set.get_widgets().keys()) == 1
    for key in test_widget_set.get_widgets().keys():
        assert key == 'Widget0'
        break
    widget = test_widget_set.get_widgets()['Widget0']
    assert isinstance(widget, py_cui.widgets.CheckBoxMenu)
    assert widget.get_id() == 'Widget0'
    row, col = widget.get_grid_cell()
    assert row == 1
    assert col == 1


def test_add_label():
    test_widget_set = WidgetSet(4, 5, logger, simulated_terminal=[30, 100])
    test_widget_set.add_label('Demo', 1, 1)
    assert len(test_widget_set.get_widgets().keys()) == 1
    for key in test_widget_set.get_widgets().keys():
        assert key == 'Widget0'
        break
    widget = test_widget_set.get_widgets()['Widget0']
    assert isinstance(widget, py_cui.widgets.Label)
    assert widget.get_id() == 'Widget0'
    row, col = widget.get_grid_cell()
    assert row == 1
    assert col == 1


def test_add_block_label():
    test_widget_set = WidgetSet(4, 5, logger, simulated_terminal=[30, 100])
    test_widget_set.add_block_label('Demo', 1, 1)
    assert len(test_widget_set.get_widgets().keys()) == 1
    for key in test_widget_set.get_widgets().keys():
        assert key == 'Widget0'
        break
    widget = test_widget_set.get_widgets()['Widget0']
    assert isinstance(widget, py_cui.widgets.BlockLabel)
    assert widget.get_id() == 'Widget0'
    row, col = widget.get_grid_cell()
    assert row == 1
    assert col == 1


def test_add_text_box():
    test_widget_set = WidgetSet(4, 5, logger, simulated_terminal=[30, 100])
    test_widget_set.add_text_box('Demo', 1, 1)
    assert len(test_widget_set.get_widgets().keys()) == 1
    for key in test_widget_set.get_widgets().keys():
        assert key == 'Widget0'
        break
    widget = test_widget_set.get_widgets()['Widget0']
    assert isinstance(widget, py_cui.widgets.TextBox)
    assert widget.get_id() == 'Widget0'
    row, col = widget.get_grid_cell()
    assert row == 1
    assert col == 1


def test_add_button():
    test_widget_set = WidgetSet(4, 5, logger, simulated_terminal=[30, 100])
    test_widget_set.add_button('Demo', 1, 1)
    assert len(test_widget_set.get_widgets().keys()) == 1
    for key in test_widget_set.get_widgets().keys():
        assert key == 'Widget0'
        break
    widget = test_widget_set.get_widgets()['Widget0']
    assert isinstance(widget, py_cui.widgets.Button)
    assert widget.get_id() == 'Widget0'
    row, col = widget.get_grid_cell()
    assert row == 1
    assert col == 1


def test_add_text_block():
    test_widget_set = WidgetSet(4, 5, logger, simulated_terminal=[30, 100])
    test_widget_set.add_text_block('Demo', 1, 1)
    assert len(test_widget_set.get_widgets().keys()) == 1
    for key in test_widget_set.get_widgets().keys():
        assert key == 'Widget0'
        break
    widget = test_widget_set.get_widgets()['Widget0']
    assert isinstance(widget, py_cui.widgets.ScrollTextBlock)
    assert widget.get_id() == 'Widget0'
    row, col = widget.get_grid_cell()
    assert row == 1
    assert col == 1
