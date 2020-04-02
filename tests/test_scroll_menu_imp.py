import pytest

import py_cui
import py_cui.debug as dbg

logger = dbg.PyCUILogger('PYCUI TEST')

grid_test = py_cui.grid.Grid(10, 10, 100, 100, logger)

scroll = py_cui.widgets.ScrollMenu('1', 'Scroll', grid_test, 0, 0, 1, 1, 1, 0, logger)
scroll.selected = True

elems = ["Elem0","Elem1","Elem2","Elem3","Elem4"]


def test_add_item_list():
    scroll.add_item_list(elems)
    counter = 0
    for item in scroll.get_item_list():
        assert item == elems[counter]
        counter = counter + 1
    assert scroll.get_selected_item() == 0
    assert scroll.get() == "Elem0"
    scroll.clear()


def test_scroll_up():
    scroll.add_item_list(elems)
    scroll._scroll_up()
    assert scroll.get_selected_item() == 0
    assert scroll.get() == "Elem0"
    scroll.set_selected_item(2)
    assert scroll.get() == "Elem2"
    scroll._scroll_up()
    assert scroll.get_selected_item() == 1
    assert scroll.get() == "Elem1"
    scroll.clear()


def test_scroll_down():
    scroll.add_item_list(elems)
    scroll._scroll_down(scroll.get_viewport_height())
    assert scroll.get_selected_item() == 1
    assert scroll.get() == "Elem1"
    scroll.set_selected_item(4)
    assert scroll.get() == "Elem4"
    scroll._scroll_down(scroll.get_viewport_height())
    assert scroll.get_selected_item() == 4
    assert scroll.get() == "Elem4"
    scroll.clear()


def test_empty_scroll_menu():
    scroll.clear()
    assert scroll.get() is None
    assert scroll.get_selected_item() == 0
    scroll._scroll_up()
    assert scroll.get_selected_item() == 0 and scroll.get() is None
    scroll._scroll_down(scroll.get_viewport_height())
    assert scroll.get_selected_item() == 0 and scroll.get() is None