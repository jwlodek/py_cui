import pytest
import py_cui


test_string_A = "Hello world, etc 123 @ testing @ ++-- Test"
test_string_B = "     Test string number two Space"
test_string_C = "Hi"

dummy_grid = py_cui.grid.Grid(3,3,30,30)
dummy_widget = py_cui.widgets.Widget('1', 'Test', dummy_grid, 1,1,1,1,1,0)
dummy_renderer = py_cui.renderer.Renderer(None, None)


def test_dummy_grid():
    assert dummy_grid.row_height == 10
    assert dummy_grid.column_width == 10
    assert dummy_widget.start_x == 9
    assert dummy_widget.start_y == 11
    assert dummy_widget.height == 10
    assert dummy_widget.width == 10

def test_get_render_text_A():
    render_fragment = dummy_renderer.get_render_text(dummy_widget, test_string_A, False, False, 0)
    assert render_fragment[0][0] == "Hello wo"
    render_fragment = dummy_renderer.get_render_text(dummy_widget, test_string_A, True, False, 0)
    assert render_fragment[0][0] == "Hello wo"
    render_fragment = dummy_renderer.get_render_text(dummy_widget, test_string_A, False, True, 0)
    assert render_fragment[0][0] == "Hell"
    render_fragment = dummy_renderer.get_render_text(dummy_widget, test_string_A, True, True, 0)
    assert render_fragment[0][0] == "Hell"

def test_get_render_text_B():
    render_fragment = dummy_renderer.get_render_text(dummy_widget, test_string_B, False, False, 0)
    assert render_fragment[0][0] == "     Tes"
    render_fragment = dummy_renderer.get_render_text(dummy_widget, test_string_B, True, False, 0)
    assert render_fragment[0][0] == "     Tes"
    render_fragment = dummy_renderer.get_render_text(dummy_widget, test_string_B, False, True, 0)
    assert render_fragment[0][0] == "    "
    render_fragment = dummy_renderer.get_render_text(dummy_widget, test_string_B, True, True, 0)
    assert render_fragment[0][0] == "    "

def test_get_render_text_C():
    render_fragment = dummy_renderer.get_render_text(dummy_widget, test_string_C, False, False, 0)
    assert render_fragment[0][0] == "Hi      "
    render_fragment = dummy_renderer.get_render_text(dummy_widget, test_string_C, True, False, 0)
    assert render_fragment[0][0] == "   Hi   "
    render_fragment = dummy_renderer.get_render_text(dummy_widget, test_string_C, False, True, 0)
    assert render_fragment[0][0] == "Hi  "
    render_fragment = dummy_renderer.get_render_text(dummy_widget, test_string_C, True, True, 0)
    assert render_fragment[0][0] == " Hi "