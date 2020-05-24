import pytest # noqa
import py_cui
import py_cui.debug as dbg

logger = dbg.PyCUILogger('PYCUI TEST')

test_string_A = "Hello world, etc 123 @ testing @ ++-- Test"
test_string_B = "     Test string number two Space"
test_string_C = "Hi"

dummy_grid = py_cui.grid.Grid(3, 3, 30, 30, logger)
dummy_widget = py_cui.widgets.Widget('1', 'Test', dummy_grid,
                                     1, 1, 1, 1, 1, 0, logger)
dummy_renderer = py_cui.renderer.Renderer(None, None, logger)


def test_dummy_grid():
    row_height, column_width = dummy_grid.get_cell_dimensions()
    start_x, start_y = dummy_widget.get_start_position()
    height, width = dummy_widget.get_absolute_dimensions()
    assert row_height == 10
    assert column_width == 10
    assert start_x == 9
    assert start_y == 11
    assert height == 10
    assert width == 10


def test_get_render_text_A():
    render_fragment = dummy_renderer._get_render_text(dummy_widget,
                                                      test_string_A,
                                                      False, False, 0)
    assert render_fragment[0][0] == "Hello wo"
    render_fragment = dummy_renderer._get_render_text(dummy_widget,
                                                      test_string_A,
                                                      True, False, 0)
    assert render_fragment[0][0] == "Hello wo"
    render_fragment = dummy_renderer._get_render_text(dummy_widget,
                                                      test_string_A,
                                                      False, True, 0)
    assert render_fragment[0][0] == "Hell"
    render_fragment = dummy_renderer._get_render_text(dummy_widget,
                                                      test_string_A,
                                                      True, True, 0)
    assert render_fragment[0][0] == "Hell"


def test_get_render_text_B():
    render_fragment = dummy_renderer._get_render_text(dummy_widget,
                                                      test_string_B,
                                                      False, False, 0)
    assert render_fragment[0][0] == "     Tes"
    render_fragment = dummy_renderer._get_render_text(dummy_widget,
                                                      test_string_B,
                                                      True, False, 0)
    assert render_fragment[0][0] == "     Tes"
    render_fragment = dummy_renderer._get_render_text(dummy_widget,
                                                      test_string_B,
                                                      False, True, 0)
    assert render_fragment[0][0] == "    "
    render_fragment = dummy_renderer._get_render_text(dummy_widget,
                                                      test_string_B,
                                                      True, True, 0)
    assert render_fragment[0][0] == "    "


def test_get_render_text_C():
    render_fragment = dummy_renderer._get_render_text(dummy_widget,
                                                      test_string_C,
                                                      False, False, 0)
    assert render_fragment[0][0] == "Hi      "
    render_fragment = dummy_renderer._get_render_text(dummy_widget,
                                                      test_string_C,
                                                      True, False, 0)
    assert render_fragment[0][0] == "   Hi   "
    render_fragment = dummy_renderer._get_render_text(dummy_widget,
                                                      test_string_C,
                                                      False, True, 0)
    assert render_fragment[0][0] == "Hi  "
    render_fragment = dummy_renderer._get_render_text(dummy_widget,
                                                      test_string_C,
                                                      True, True, 0)
    assert render_fragment[0][0] == " Hi "
