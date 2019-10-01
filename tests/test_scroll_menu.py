import pytest

import py_cui


grid_test = py_cui.grid.Grid(10, 10, 100, 100)

scroll = py_cui.widgets.ScrollMenu('1', 'Scroll', grid_test, 0, 0, 1, 1, 1, 0)
scroll.selected = True

elems = ["Elem0","Elem1","Elem2","Elem3","Elem4"]

def test_add_item_list():
    scroll.add_item_list(elems)
    counter = 0
    for item in scroll.get_item_list():
        assert item == elems[counter]
        counter = counter + 1
    assert scroll.selected_item == 0
    assert scroll.get() == "Elem0"
    scroll.clear()

def test_scroll_up():
    scroll.add_item_list(elems)
    scroll.scroll_up()
    assert scroll.selected_item == 0
    assert scroll.get() == "Elem0"
    scroll.selected_item = 2
    assert scroll.get() == "Elem2"
    scroll.scroll_up()
    assert scroll.selected_item == 1
    assert scroll.get() == "Elem1"
    scroll.clear()

def test_scroll_down():
    scroll.add_item_list(elems)
    scroll.scroll_down()
    assert scroll.selected_item == 1
    assert scroll.get() == "Elem1"
    scroll.selected_item = 4
    assert scroll.get() == "Elem4"
    scroll.scroll_down()
    assert scroll.selected_item == 4
    assert scroll.get() == "Elem4"
    scroll.clear()


def test_empty_scroll_menu():
    scroll.clear()
    assert scroll.get() is None
    assert scroll.selected_item == 0
    scroll.scroll_up()
    assert scroll.selected_item == 0 and scroll.get() is None
    scroll.scroll_down()
    assert scroll.selected_item == 0 and scroll.get() is None