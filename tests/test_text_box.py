import pytest

import py_cui

grid_test = py_cui.grid.Grid(10, 10, 100, 100)

def test_move_right():
    text_box = py_cui.widgets.TextBox('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World', False)
    text_box.move_right()
    assert text_box.cursor_text_pos == 1
    assert text_box.cursor_x == 13


def test_move_left_side():
    text_box = py_cui.widgets.TextBox('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World', False)
    temp = text_box.cursor_x
    text_box.cursor_x = text_box.cursor_x + 5
    text_box.cursor_text_pos = 5
    text_box.move_left()
    assert text_box.cursor_text_pos == 4
    assert text_box.cursor_x == (temp + 5 - 1)


def test_clear():
    text_box = py_cui.widgets.TextBox('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World', False)
    text_box.clear()
    assert text_box.get() == ''
    assert text_box.cursor_text_pos == 0
    assert text_box.cursor_x == 12


def test_get_initial():
    text_box = py_cui.widgets.TextBox('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World', False)
    assert text_box.cursor_text_pos == 0
    assert text_box.cursor_x == 12
    assert text_box.get() == 'Hello World'
    assert text_box.cursor_max_left == 12
    assert text_box.cursor_max_right == 27


def test_insert_char():
    text_box = py_cui.widgets.TextBox('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World', False)
    text_box.insert_char(py_cui.keys.KEY_D_UPPER)
    assert text_box.get() == 'DHello World'
    assert text_box.cursor_x == text_box.cursor_max_left + 1
    assert text_box.cursor_text_pos == 1


def test_erase_char():
    text_box = py_cui.widgets.TextBox('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World', False)
    for i in range(0,2):
        text_box.move_right()
    text_box.erase_char()
    assert text_box.cursor_x == text_box.cursor_max_left + 1
    assert text_box.cursor_text_pos == 1
    assert text_box.get() == 'Hllo World'


def test_get_edited():
    text_box = py_cui.widgets.TextBox('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World', False)
    for i in range(0, 3):
        text_box.move_right()
    text_box.erase_char()
    text_box.insert_char(py_cui.keys.KEY_A_LOWER)
    text_box.insert_char(py_cui.keys.KEY_E_UPPER)
    assert text_box.cursor_x == text_box.cursor_max_left + 4
    assert text_box.cursor_text_pos == 4
    assert text_box.get() == 'HeaElo World'


def test_jump_to_start():
    text_box = py_cui.widgets.TextBox('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World', False)
    for i in range(0, 4):
        text_box.move_right()
    text_box.jump_to_start()
    assert text_box.get() == 'Hello World'
    assert text_box.cursor_text_pos == 0
    assert text_box.cursor_x == 12


def test_jump_to_end():
    text_box = py_cui.widgets.TextBox('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World', False)
    text_box.jump_to_end()
    assert text_box.cursor_text_pos == 11
    assert text_box.cursor_x == text_box.cursor_max_left + 11


def test_move_right_overflow():
    text_box = py_cui.widgets.TextBox('id', 'Test', grid_test, 1, 1, 1, 1, 1, 0 , 'Hello World!!!', False)
    for i in range(0, 20):
        text_box.move_right()
    assert text_box.cursor_text_pos == 14
    assert text_box.cursor_x == text_box.cursor_max_left + 5


def test_move_left_overflow():
    text_box = py_cui.widgets.TextBox('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World', False)
    text_box.move_left()
    assert text_box.cursor_text_pos == 0
    assert text_box.cursor_x == 12


def test_set_text():
    text_box = py_cui.widgets.TextBox('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World', False)
    for i in range(0, 7):
        text_box.move_right()
    text_box.set_text('Hi')
    assert text_box.get() == 'Hi'
    assert text_box.cursor_text_pos == 2
    assert text_box.cursor_x == text_box.cursor_max_left + 2
