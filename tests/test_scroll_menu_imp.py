import pytest # noqa

import py_cui


elems = ["Elem0", "Elem1", "Elem2", "Elem3", "Elem4"]


def test_add_item_list(SCROLLMENU):
    scroll = SCROLLMENU
    scroll.add_item_list(elems)
    counter = 0
    for item in scroll.get_item_list():
        assert item == elems[counter]
        counter = counter + 1
    assert scroll.get_selected_item_index() == 0
    assert scroll.get() == "Elem0"
    scroll.clear()


def test_scroll_up(SCROLLMENU):
    scroll = SCROLLMENU
    scroll.add_item_list(elems)
    scroll._scroll_up()
    assert scroll.get_selected_item_index() == 0
    assert scroll.get() == "Elem0"
    scroll.set_selected_item_index(2)
    assert scroll.get() == "Elem2"
    scroll._scroll_up()
    assert scroll.get_selected_item_index() == 1
    assert scroll.get() == "Elem1"
    scroll.clear()


def test_scroll_down(SCROLLMENU):
    scroll = SCROLLMENU
    scroll.add_item_list(elems)
    scroll._scroll_down(scroll.get_viewport_height())
    assert scroll.get_selected_item_index() == 1
    assert scroll.get() == "Elem1"
    scroll.set_selected_item_index(4)
    assert scroll.get() == "Elem4"
    scroll._scroll_down(scroll.get_viewport_height())
    assert scroll.get_selected_item_index() == 4
    assert scroll.get() == "Elem4"
    scroll.clear()


def test_empty_scroll_menu(SCROLLMENU):
    scroll = SCROLLMENU
    scroll.clear()
    assert scroll.get() is None
    assert scroll.get_selected_item_index() == 0
    scroll._scroll_up()
    assert scroll.get_selected_item_index() == 0 and scroll.get() is None
    scroll._scroll_down(scroll.get_viewport_height())
    assert scroll.get_selected_item_index() == 0 and scroll.get() is None


def test_goto_end(SCROLLMENU):
    scroll = SCROLLMENU
    scroll.add_item_list(elems)
    scroll.set_selected_item_index(0)
    scroll._jump_to_bottom(scroll.get_viewport_height())
    assert scroll.get_selected_item_index() == 4
    scroll.clear()


def test_goto_start(SCROLLMENU):
    scroll = SCROLLMENU
    scroll.add_item_list(elems)
    scroll.set_selected_item_index(4)
    assert scroll.get() == "Elem4"
    scroll._jump_to_top()
    assert scroll.get_selected_item_index() == 0
    assert scroll.get() == "Elem0"
    scroll.clear()


def test_jump_down(SCROLLMENU):
    scroll = SCROLLMENU
    scroll.add_item_list(elems)
    scroll.set_selected_item_index(0)
    scroll._jump_down(scroll.get_viewport_height())
    assert scroll.get_selected_item_index() == 4
    scroll.clear()


def test_jump_up(SCROLLMENU):
    scroll = SCROLLMENU
    scroll.add_item_list(elems)
    scroll.set_selected_item_index(4)
    assert scroll.get() == "Elem4"
    scroll._jump_up()
    assert scroll.get_selected_item_index() == 0
    assert scroll.get() == "Elem0"
    scroll.clear()
