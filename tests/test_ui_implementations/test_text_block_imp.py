import pytest # noqa

import py_cui


def test_move_right(SCROLLTEXTBLOCK):
    text_box = SCROLLTEXTBLOCK('Hello World')
    text_box._move_right()
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    assert text_x == 1
    assert cursor_x == 43


def test_move_left_side(SCROLLTEXTBLOCK):
    text_box = SCROLLTEXTBLOCK('Hello World')
    for _ in range(0, 5):
        text_box._move_right()
    text_box._move_left()
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    max_left, _ = text_box.get_cursor_limits_horizontal()
    assert text_x == 4
    assert cursor_x == (max_left + 5 - 1)


def test_clear(SCROLLTEXTBLOCK):
    text_box = SCROLLTEXTBLOCK('Hello World')
    text_box.clear()
    assert text_box.get() == '\n'
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    assert text_x == 0
    assert cursor_x == 42


def test_get_initial(SCROLLTEXTBLOCK):
    text_box = SCROLLTEXTBLOCK('Hello World\nSecond Line')
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    max_left, max_right = text_box.get_cursor_limits_horizontal()
    assert text_x == 0
    assert cursor_x == 42
    assert text_box.get() == 'Hello World\nSecond Line\n'
    assert max_left == 42
    assert max_right == 117


def test_insert_char(SCROLLTEXTBLOCK):
    text_box = SCROLLTEXTBLOCK('Hello World')
    text_box._insert_char(py_cui.keys.KEY_D_UPPER)
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    max_left, _ = text_box.get_cursor_limits_horizontal()
    assert text_box.get_current_line() == 'DHello World'
    assert cursor_x == max_left + 1
    assert text_x == 1


def test_handle_backspace(SCROLLTEXTBLOCK):
    text_box = SCROLLTEXTBLOCK('Hello World')
    for _ in range(0, 2):
        text_box._move_right()
    text_box._handle_backspace()
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    max_left, _ = text_box.get_cursor_limits_horizontal()
    assert cursor_x == max_left + 1
    assert text_x == 1
    assert text_box.get_current_line() == 'Hllo World'


def test_handle_backspace_startline(SCROLLTEXTBLOCK):
    text_box = SCROLLTEXTBLOCK('Hello\n World')
    text_box._move_down()
    text_box._handle_backspace()
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    max_left, _ = text_box.get_cursor_limits_horizontal()
    assert cursor_x == max_left + 5
    assert text_x == 5
    assert text_box.get_current_line() == 'Hello World'


def test_get_edited(SCROLLTEXTBLOCK):
    text_box = SCROLLTEXTBLOCK('Hello World')
    for _ in range(0, 3):
        text_box._move_right()
    text_box._handle_backspace()
    text_box._insert_char(py_cui.keys.KEY_A_LOWER)
    text_box._insert_char(py_cui.keys.KEY_E_UPPER)
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    max_left, _ = text_box.get_cursor_limits_horizontal()
    assert cursor_x == max_left + 4
    assert text_x == 4
    assert text_box.get_current_line() == 'HeaElo World'


def test_jump_to_start(SCROLLTEXTBLOCK):
    text_box = SCROLLTEXTBLOCK('Hello World')
    for _ in range(0, 4):
        text_box._move_right()
    text_box._handle_home()
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    assert text_box.get_current_line() == 'Hello World'
    assert text_x == 0
    assert cursor_x == 42


def test_jump_to_end(SCROLLTEXTBLOCK):
    text_box = SCROLLTEXTBLOCK('Hello World')
    text_box._handle_end()
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    max_left, _ = text_box.get_cursor_limits_horizontal()
    assert text_x == 11
    assert cursor_x == max_left + 11


def test_move_right_overflow(SCROLLTEXTBLOCK):
    demo = 'Helloasdasdfasdfsadf Worasdcascaadcasdcdascasdcasdcadscld!!!'
    text_box = SCROLLTEXTBLOCK(demo, col_span=1)
    for _ in range(0, 50):
        text_box._move_right()
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    max_left, _ = text_box.get_cursor_limits_horizontal()
    _, width = text_box.get_absolute_dimensions()
    padx, _ = text_box.get_padding()
    assert text_x == 50
    assert cursor_x == max_left + width - 2 * padx - 3


def test_move_left_overflow(SCROLLTEXTBLOCK):
    text_box = SCROLLTEXTBLOCK('Hello World')

    text_box._move_left()
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    assert text_x == 0
    assert cursor_x == 42


def test_set_text(SCROLLTEXTBLOCK):
    text_box = SCROLLTEXTBLOCK('Hello World')

    for _ in range(0, 7):
        text_box._move_right()
    text_box.set_text('Hi')
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    max_left, _ = text_box.get_cursor_limits_horizontal()
    assert text_box.get_current_line() == 'Hi'
    assert text_x == 0
    assert cursor_x == max_left


def test_move_down(SCROLLTEXTBLOCK):
    text_box = SCROLLTEXTBLOCK('Hello World\nTest')

    for _ in range(0, 8):
        text_box._move_right()
    text_box._move_down()
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    max_left, _ = text_box.get_cursor_limits_horizontal()
    assert text_box.get_current_line() == "Test"
    assert text_x == 4
    assert cursor_x == max_left + 4


def test_move_up_limit(SCROLLTEXTBLOCK):
    text_box = SCROLLTEXTBLOCK('Hello World\nTest')

    text_box._move_up()
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    max_left, _ = text_box.get_cursor_limits_horizontal()
    assert text_box.get_current_line() == "Hello World"
    assert text_x == 0
    assert cursor_x == max_left


def test_move_up(SCROLLTEXTBLOCK):
    text_box = SCROLLTEXTBLOCK('Hello\nTest 12234567')

    text_box._move_down()
    for _ in range(0, 8):
        text_box._move_right()
    text_box._move_up()
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    max_left, _ = text_box.get_cursor_limits_horizontal()
    assert text_box.get_current_line() == "Hello"
    assert text_x == 5
    assert cursor_x == max_left + 5


def test_handle_delete_inline(SCROLLTEXTBLOCK):
    text_box = SCROLLTEXTBLOCK('Hello World')

    for _ in range(0, 2):
        text_box._move_right()
    text_box._handle_delete()
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    max_left, _ = text_box.get_cursor_limits_horizontal()
    assert text_box.get_current_line() == 'Helo World'
    assert text_x == 2
    assert cursor_x == max_left + 2


def test_handle_delete_endline(SCROLLTEXTBLOCK):
    text_box = SCROLLTEXTBLOCK('Hello\nWorld')

    for _ in range(0, 5):
        text_box._move_right()
    text_box._handle_delete()
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    max_left, _ = text_box.get_cursor_limits_horizontal()
    assert text_box.get_current_line() == 'HelloWorld'
    assert text_x == 5
    assert cursor_x == max_left + 5


def test_enter_endline(SCROLLTEXTBLOCK):
    text_box = SCROLLTEXTBLOCK('Hello\nWorld')

    for _ in range(0, 5):
        text_box._move_right()
    text_box._handle_newline()
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    max_left, _ = text_box.get_cursor_limits_horizontal()
    assert text_box.get_current_line() == ''
    assert text_x == 0
    assert cursor_x == max_left


def test_enter_inline(SCROLLTEXTBLOCK):
    text_box = SCROLLTEXTBLOCK('Hello World')

    for _ in range(0, 5):
        text_box._move_right()
    text_box._handle_newline()
    cursor_x, _ = text_box.get_abs_cursor_position()
    text_x, _ = text_box.get_cursor_text_pos()
    max_left, _ = text_box.get_cursor_limits_horizontal()
    assert text_box.get_current_line() == ' World'
    assert text_x == 0
    assert cursor_x == max_left
