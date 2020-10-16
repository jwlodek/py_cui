import pytest # noqa

import py_cui


def test_move_right(TEXTBOX):
    text_box = TEXTBOX()
    text_box._move_right()
    cursor_x, _ = text_box.get_cursor_position()
    assert text_box.get_cursor_text_pos() == 1
    assert cursor_x == 13


def test_move_left_side(TEXTBOX):
    text_box = TEXTBOX()
    for _ in range(0, 5):
        text_box._move_right()
    text_box._move_left()
    cursor_x, _ = text_box.get_cursor_position()
    max_left, _ = text_box.get_cursor_limits()
    assert text_box.get_cursor_text_pos() == 4
    assert cursor_x == (max_left + 5 - 1)


def test_clear(TEXTBOX):
    text_box = TEXTBOX()
    text_box.clear()
    cursor_x, _ = text_box.get_cursor_position()
    assert text_box.get() == ''
    assert text_box.get_cursor_text_pos() == 0
    assert cursor_x == 12


def test_get_initial(TEXTBOX):
    text_box = TEXTBOX()
    cursor_x, _ = text_box.get_cursor_position()
    max_left, max_right = text_box.get_cursor_limits()
    assert text_box.get_cursor_text_pos() == 0
    assert cursor_x == 12
    assert text_box.get() == 'Hello World'
    assert max_left == 12
    assert max_right == 27


def test_insert_char(TEXTBOX):
    text_box = TEXTBOX()
    text_box._insert_char(py_cui.keys.KEY_D_UPPER)
    cursor_x, _ = text_box.get_cursor_position()
    max_left, _ = text_box.get_cursor_limits()
    assert text_box.get() == 'DHello World'
    assert cursor_x == max_left + 1
    assert text_box.get_cursor_text_pos() == 1


def test_erase_char(TEXTBOX):
    text_box = TEXTBOX()
    for _ in range(0, 2):
        text_box._move_right()
    text_box._erase_char()
    cursor_x, _ = text_box.get_cursor_position()
    max_left, _ = text_box.get_cursor_limits()
    assert cursor_x == max_left + 1
    assert text_box.get_cursor_text_pos() == 1
    assert text_box.get() == 'Hllo World'


def test_get_edited(TEXTBOX):
    text_box = TEXTBOX()
    for _ in range(0, 3):
        text_box._move_right()
    text_box._erase_char()
    text_box._insert_char(py_cui.keys.KEY_A_LOWER)
    text_box._insert_char(py_cui.keys.KEY_E_UPPER)
    cursor_x, _ = text_box.get_cursor_position()
    max_left, _ = text_box.get_cursor_limits()
    assert cursor_x == max_left + 4
    assert text_box.get_cursor_text_pos() == 4
    assert text_box.get() == 'HeaElo World'


def test_jump_to_start(TEXTBOX):
    text_box = TEXTBOX()
    for _ in range(0, 4):
        text_box._move_right()
    text_box._jump_to_start()
    assert text_box.get() == 'Hello World'
    assert text_box.get_cursor_text_pos() == 0
    cursor_x, _ = text_box.get_cursor_position()
    assert cursor_x == 12


def test_jump_to_end(TEXTBOX):
    text_box = TEXTBOX()
    text_box._jump_to_end()
    cursor_x, _ = text_box.get_cursor_position()
    max_left, _ = text_box.get_cursor_limits()
    assert text_box.get_cursor_text_pos() == 11
    assert cursor_x == max_left + 11


def test_move_right_overflow(TEXTBOX):
    text_box = TEXTBOX(text='Hello World!!!', colspan=1)
    for _ in range(0, 20):
        text_box._move_right()
    assert text_box.get_cursor_text_pos() == 14
    cursor_x, _ = text_box.get_cursor_position()
    max_left, _ = text_box.get_cursor_limits()
    assert cursor_x == max_left + 5


def test_move_left_overflow(TEXTBOX):
    text_box = TEXTBOX()
    text_box._move_left()
    assert text_box.get_cursor_text_pos() == 0
    cursor_x, _ = text_box.get_cursor_position()
    assert cursor_x == 12


def test_set_text(TEXTBOX):
    text_box = TEXTBOX()
    for _ in range(0, 7):
        text_box._move_right()
    text_box.set_text('Hi')
    assert text_box.get() == 'Hi'

    assert text_box.get_cursor_text_pos() == 2
    cursor_x, _ = text_box.get_cursor_position()
    max_left, _ = text_box.get_cursor_limits()
    assert cursor_x == max_left + 2
