import pytest

import py_cui

import pytest

import py_cui

grid_test = py_cui.grid.Grid(3, 3, 120, 120)

def test_move_right():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World')
    text_box.move_right()
    assert text_box.cursor_text_pos_x == 1
    assert text_box.cursor_x == 43


def test_move_left_side():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World')
    temp = text_box.cursor_x
    text_box.cursor_x = text_box.cursor_x + 5
    text_box.cursor_text_pos_x = 5
    text_box.move_left()
    assert text_box.cursor_text_pos_x == 4
    assert text_box.cursor_x == (temp + 5 - 1)


def test_clear():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World')
    text_box.clear()
    assert text_box.get() == '\n'
    assert text_box.cursor_text_pos_x == 0
    assert text_box.cursor_x == 42


def test_get_initial():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World\nSecond Line')
    assert text_box.cursor_text_pos_x == 0
    assert text_box.cursor_x == 42
    assert text_box.get() == 'Hello World\nSecond Line\n'
    assert text_box.cursor_max_left == 42
    assert text_box.cursor_max_right == 117


def test_insert_char():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World')
    text_box.insert_char(py_cui.keys.KEY_D_UPPER)
    assert text_box.get_current_line() == 'DHello World'
    assert text_box.cursor_x == text_box.cursor_max_left + 1
    assert text_box.cursor_text_pos_x == 1


def test_handle_backspace():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World')
    for i in range(0,2):
        text_box.move_right()
    text_box.handle_backspace()
    assert text_box.cursor_x == text_box.cursor_max_left + 1
    assert text_box.cursor_text_pos_x == 1
    assert text_box.get_current_line() == 'Hllo World'


def test_handle_backspace_startline():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello\n World')
    text_box.move_down()
    text_box.handle_backspace()
    assert text_box.cursor_x == text_box.cursor_max_left + 5
    assert text_box.cursor_text_pos_x == 5
    assert text_box.get_current_line() == 'Hello World'


def test_get_edited():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World')
    for i in range(0, 3):
        text_box.move_right()
    text_box.handle_backspace()
    text_box.insert_char(py_cui.keys.KEY_A_LOWER)
    text_box.insert_char(py_cui.keys.KEY_E_UPPER)
    assert text_box.cursor_x == text_box.cursor_max_left + 4
    assert text_box.cursor_text_pos_x == 4
    assert text_box.get_current_line() == 'HeaElo World'


def test_jump_to_start():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World')
    for i in range(0, 4):
        text_box.move_right()
    text_box.handle_home()
    assert text_box.get_current_line() == 'Hello World'
    assert text_box.cursor_text_pos_x == 0
    assert text_box.cursor_x == 42


def test_jump_to_end():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World')
    text_box.handle_end()
    assert text_box.cursor_text_pos_x == 11
    assert text_box.cursor_x == text_box.cursor_max_left + 11


def test_move_right_overflow():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 1, 1, 0 , 'Helloasdasdfasdfsadf Worasdcascaadcasdcdascasdcasdcadscld!!!')
    for i in range(0, 50):
        text_box.move_right()
    assert text_box.cursor_text_pos_x == 50
    assert text_box.cursor_x == text_box.cursor_max_left + text_box.width - 2 * text_box.padx - 3


def test_move_left_overflow():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World')
    text_box.move_left()
    assert text_box.cursor_text_pos_x == 0
    assert text_box.cursor_x == 42


def test_set_text():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World')
    for i in range(0, 7):
        text_box.move_right()
    text_box.set_text('Hi')
    assert text_box.get_current_line() == 'Hi'
    assert text_box.cursor_text_pos_x == 0
    assert text_box.cursor_x == text_box.cursor_max_left


def test_move_down():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World\nTest')
    for i in range(0, 8):
        text_box.move_right()
    text_box.move_down()
    assert text_box.get_current_line() == "Test"
    assert text_box.cursor_text_pos_x == 4
    assert text_box.cursor_x == text_box.cursor_max_left + 4


def test_move_up_limit():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World\nTest')
    text_box.move_up()
    assert text_box.get_current_line() == "Hello World"
    assert text_box.cursor_text_pos_x == 0
    assert text_box.cursor_x == text_box.cursor_max_left


def test_move_up():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello\nTest 12234567')
    text_box.move_down()
    for i in range(0, 8):
        text_box.move_right()
    text_box.move_up()
    assert text_box.get_current_line() == "Hello"
    assert text_box.cursor_text_pos_x == 5
    assert text_box.cursor_x == text_box.cursor_max_left + 5


def test_handle_delete_inline():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World')
    for i in range(0, 2):
        text_box.move_right()
    text_box.handle_delete()
    assert text_box.get_current_line() == 'Helo World'
    assert text_box.cursor_text_pos_x == 2
    assert text_box.cursor_x == text_box.cursor_max_left + 2


def test_handle_delete_endline():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello\nWorld')
    for i in range(0, 5):
        text_box.move_right()
    text_box.handle_delete()
    assert text_box.get_current_line() == 'HelloWorld'
    assert text_box.cursor_text_pos_x == 5
    assert text_box.cursor_x == text_box.cursor_max_left + 5


def test_enter_endline():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello\nWorld')
    for i in range(0, 5):
        text_box.move_right()
    text_box.handle_newline()
    assert text_box.get_current_line() == ''
    assert text_box.cursor_text_pos_x == 0
    assert text_box.cursor_x == text_box.cursor_max_left


def test_enter_inline():
    text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', grid_test, 1, 1, 1, 2, 1, 0 , 'Hello World')
    for i in range(0, 5):
        text_box.move_right()
    text_box.handle_newline()
    assert text_box.get_current_line() == ' World'
    assert text_box.cursor_text_pos_x == 0
    assert text_box.cursor_x == text_box.cursor_max_left
