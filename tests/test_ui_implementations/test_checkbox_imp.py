import pytest # noqa

import py_cui

elems = ["Elem0", "Elem1", "Elem2", "Elem3", "Elem4"]


def test_is_empty(CHECKBOXMENU):
    scroll = CHECKBOXMENU
    assert scroll.is_empty()
    scroll.add_item_list(elems)
    assert not scroll.is_empty()
    scroll.clear()


def test_add_item_list(CHECKBOXMENU):
    scroll = CHECKBOXMENU
    scroll.add_item_list(elems)
    counter = 0
    for item in scroll.get_item_list():
        assert item == elems[counter]
        counter = counter + 1
    assert scroll.get_selected_item_index() == 0
    assert scroll.get() == "Elem0"
    for item in scroll._selected_item_dict.keys():
        assert not scroll._selected_item_dict[item]
    scroll.clear()


def test_mark_item(CHECKBOXMENU):
    scroll = CHECKBOXMENU
    scroll.add_item_list(elems)
    scroll.set_selected_item_index(1)
    assert scroll.get() == "Elem1"
    print(scroll._selected_item_dict)
    scroll.mark_item_as_checked(scroll.get())
    print(scroll._selected_item_dict)
    assert scroll._selected_item_dict[scroll.get()]
    scroll.clear()
