import pytest # noqa
import py_cui


test_string_A = "Hello world, etc 123 @ testing @ ++-- Test"
test_string_B = "     Test string number two Space"
test_string_C = "Hi"


def test_dummy_grid(DUMMYWIDGET, RENDERER):
    row_height, column_width = DUMMYWIDGET._grid.get_cell_dimensions()
    start_x, start_y = DUMMYWIDGET.get_start_position()
    height, width = DUMMYWIDGET.get_absolute_dimensions()
    assert row_height == 10
    assert column_width == 10
    assert start_x == 9
    assert start_y == 11
    assert height == 10
    assert width == 10


def test_get_render_text_A(DUMMYWIDGET, RENDERER):
    render_fragment = RENDERER._get_render_text(DUMMYWIDGET,
                                                      test_string_A,
                                                      False, False, False, 0)
    assert render_fragment[0][0] == "Hello wo"
    render_fragment = RENDERER._get_render_text(DUMMYWIDGET,
                                                      test_string_A,
                                                      True, False, False, 0)
    assert render_fragment[0][0] == "Hello wo"
    render_fragment = RENDERER._get_render_text(DUMMYWIDGET,
                                                      test_string_A,
                                                      False, True, False, 0)
    assert render_fragment[0][0] == "Hell"
    render_fragment = RENDERER._get_render_text(DUMMYWIDGET,
                                                      test_string_A,
                                                      True, True, False, 0)
    assert render_fragment[0][0] == "Hell"


def test_get_render_text_B(DUMMYWIDGET, RENDERER):
    render_fragment = RENDERER._get_render_text(DUMMYWIDGET,
                                                      test_string_B,
                                                      False, False, False, 0)
    assert render_fragment[0][0] == "     Tes"
    render_fragment = RENDERER._get_render_text(DUMMYWIDGET,
                                                      test_string_B,
                                                      True, False, False, 0)
    assert render_fragment[0][0] == "     Tes"
    render_fragment = RENDERER._get_render_text(DUMMYWIDGET,
                                                      test_string_B,
                                                      False, True, False, 0)
    assert render_fragment[0][0] == "    "
    render_fragment = RENDERER._get_render_text(DUMMYWIDGET,
                                                      test_string_B,
                                                      True, True,False,  0)
    assert render_fragment[0][0] == "    "


def test_get_render_text_C(DUMMYWIDGET, RENDERER):
    render_fragment = RENDERER._get_render_text(DUMMYWIDGET,
                                                      test_string_C,
                                                      False, False, False, 0)
    assert render_fragment[0][0] == "Hi      "
    render_fragment = RENDERER._get_render_text(DUMMYWIDGET,
                                                      test_string_C,
                                                      True, False, False, 0)
    assert render_fragment[0][0] == "   Hi   "
    render_fragment = RENDERER._get_render_text(DUMMYWIDGET,
                                                      test_string_C,
                                                      False, True, False, 0)
    assert render_fragment[0][0] == "Hi  "
    render_fragment = RENDERER._get_render_text(DUMMYWIDGET,
                                                      test_string_C,
                                                      True, True, False, 0)
    assert render_fragment[0][0] == " Hi "
