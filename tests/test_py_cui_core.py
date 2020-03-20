import pytest
import py_cui
import py_cui.keys

def test_fit_text():
    out = py_cui.fit_text(7, 'Hello World')
    assert out == 'He...'

def test_fit_text_center():
    out = py_cui.fit_text(10, 'HI', center=True)
    assert out == '   HI    '

# Define a test CUI with a 30 by 100 simulated terminal
def test_create():
    test_cui = py_cui.PyCUI(4, 5, simulated_terminal=[30, 100])
    assert test_cui._height == 26
    assert test_cui._width == 100
    assert test_cui._title_bar.get_text().strip() == 'PyCUI Window'
    assert test_cui._simulated_terminal == [30, 100]
    assert test_cui._exit_key == py_cui.keys.KEY_Q_LOWER


def test_add_scroll_menu():
    test_cui = py_cui.PyCUI(4, 5, simulated_terminal=[30, 100])
    test_cui.add_scroll_menu('Demo', 1, 1)
    assert len(test_cui.get_widgets().keys()) == 1
    for key in test_cui.get_widgets().keys():
        assert key == 'Widget0'
        break
    widget = test_cui.get_widgets()['Widget0']
    assert isinstance(widget, py_cui.widgets.ScrollMenu)
    assert widget.get_id() == 'Widget0'
    row, col = widget.get_grid_cell()
    assert row == 1
    assert col == 1


def test_add_checkbox_menu():
    test_cui = py_cui.PyCUI(4, 5, simulated_terminal=[30, 100])
    test_cui.add_checkbox_menu('Demo', 1, 1)
    assert len(test_cui.get_widgets().keys()) == 1
    for key in test_cui.get_widgets().keys():
        assert key == 'Widget0'
        break
    widget = test_cui.get_widgets()['Widget0']
    assert isinstance(widget, py_cui.widgets.CheckBoxMenu)
    assert widget.get_id() == 'Widget0'
    row, col = widget.get_grid_cell()
    assert row == 1
    assert col == 1

def test_add_label():
    test_cui = py_cui.PyCUI(4, 5, simulated_terminal=[30, 100])
    test_cui.add_label('Demo', 1, 1)
    assert len(test_cui.get_widgets().keys()) == 1
    for key in test_cui.get_widgets().keys():
        assert key == 'Widget0'
        break
    widget = test_cui.get_widgets()['Widget0']
    assert isinstance(widget, py_cui.widgets.Label)
    assert widget.get_id() == 'Widget0'
    row, col = widget.get_grid_cell()
    assert row == 1
    assert col == 1


def test_add_block_label():
    test_cui = py_cui.PyCUI(4, 5, simulated_terminal=[30, 100])
    test_cui.add_block_label('Demo', 1, 1)
    assert len(test_cui.get_widgets().keys()) == 1
    for key in test_cui.get_widgets().keys():
        assert key == 'Widget0'
        break
    widget = test_cui.get_widgets()['Widget0']
    assert isinstance(widget, py_cui.widgets.BlockLabel)
    assert widget.get_id() == 'Widget0'
    row, col = widget.get_grid_cell()
    assert row == 1
    assert col == 1


def test_add_text_box():
    test_cui = py_cui.PyCUI(4, 5, simulated_terminal=[30, 100])
    test_cui.add_text_box('Demo', 1, 1)
    assert len(test_cui.get_widgets().keys()) == 1
    for key in test_cui.get_widgets().keys():
        assert key == 'Widget0'
        break
    widget = test_cui.get_widgets()['Widget0']
    assert isinstance(widget, py_cui.widgets.TextBox)
    assert widget.get_id() == 'Widget0'
    row, col = widget.get_grid_cell()
    assert row == 1
    assert col == 1


def test_add_button():
    test_cui = py_cui.PyCUI(4, 5, simulated_terminal=[30, 100])
    test_cui.add_button('Demo', 1, 1)
    assert len(test_cui.get_widgets().keys()) == 1
    for key in test_cui.get_widgets().keys():
        assert key == 'Widget0'
        break
    widget = test_cui.get_widgets()['Widget0']
    assert isinstance(widget, py_cui.widgets.Button)
    assert widget.get_id() == 'Widget0'
    row, col = widget.get_grid_cell()
    assert row == 1
    assert col == 1


def test_add_text_block():
    test_cui = py_cui.PyCUI(4, 5, simulated_terminal=[30, 100])
    test_cui.add_text_block('Demo', 1, 1)
    assert len(test_cui.get_widgets().keys()) == 1
    for key in test_cui.get_widgets().keys():
        assert key == 'Widget0'
        break
    widget = test_cui.get_widgets()['Widget0']
    assert isinstance(widget, py_cui.widgets.ScrollTextBlock)
    assert widget.get_id() == 'Widget0'
    row, col = widget.get_grid_cell()
    assert row == 1
    assert col == 1