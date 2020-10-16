import pytest

import py_cui
import py_cui.debug as dbg
import py_cui.grid



@pytest.fixture
def LOGGER():
    return dbg.PyCUILogger('PYCUI TEST')


@pytest.fixture
def RENDERER(request, LOGGER):
    return py_cui.renderer.Renderer(None, None, LOGGER)


@pytest.fixture
def GRID(request, LOGGER):

    def _GRID(rows, cols, height, width):

        return py_cui.grid.Grid(rows, cols, height, width, LOGGER)

    return _GRID


@pytest.fixture
def DUMMYWIDGET(request, GRID, LOGGER):

    dummy_grid = GRID(3, 3, 30, 30)
    return py_cui.widgets.Widget('1', 'Test', dummy_grid, 1, 1, 1, 1, 1, 0, LOGGER)


@pytest.fixture
def CUSTOMWIDGET(request, GRID, LOGGER):

    def _CUSTOMWIDGET(id, name, row, col, rowspan, colspan):
        test_grid = GRID(5, 7, 90, 210)
        return py_cui.widgets.Widget(id, name, test_grid, row, col, rowspan, colspan, 1, 0, LOGGER)
    
    return _CUSTOMWIDGET


@pytest.fixture
def PYCUI():

    def _PYCUI(rows, cols, height, width):
        return py_cui.PyCUI(rows, cols, simulated_terminal=[height, width])

    return _PYCUI


@pytest.fixture
def WIDGETSET(request, LOGGER):

    def _WIDGETSET(rows, cols, height, width):
        return py_cui.widget_set.WidgetSet(rows, cols, LOGGER, simulated_terminal=[height, width])

    return _WIDGETSET


@pytest.fixture
def SCROLLMENU(request, GRID, LOGGER):

    test_grid = GRID(10, 10, 100, 100)
    scroll = py_cui.widgets.ScrollMenu('1', 'Scroll', test_grid, 0, 0, 1, 1, 1, 0, LOGGER)
    scroll.selected = True

    return scroll


@pytest.fixture
def CHECKBOXMENU(request, GRID, LOGGER):

    test_grid = GRID(10, 10, 100, 100)
    scroll = py_cui.widgets.CheckBoxMenu('1', 'Scroll', test_grid, 0, 0, 1, 1, 1, 0, LOGGER, 'X')
    scroll.selected = True

    return scroll


@pytest.fixture
def TEXTBOX(request, GRID, LOGGER):
    
    def _TEXTBOX(text='Hello World', row=1, col=1, rowspan=1, colspan=2):
        test_grid = GRID(10,10,100,100)
        text_box = py_cui.widgets.TextBox('id', 'Test', test_grid,
                                            row, col, rowspan, colspan, 1, 0, LOGGER,
                                            text, False)
        return text_box
    
    return _TEXTBOX


@pytest.fixture
def SCROLLTEXTBLOCK(request, GRID, LOGGER):

    def _SCROLLTEXTBLOCK(text, row=1, col=1, row_span=1, col_span=2):

        test_grid = GRID(3, 3, 120, 120)
        text_box = py_cui.widgets.ScrollTextBlock('id', 'Test', test_grid,
                                                    row, col, row_span, col_span, 1, 0,
                                                    LOGGER, text)
        return text_box

    return _SCROLLTEXTBLOCK


@pytest.fixture
def COLORRULE(request, LOGGER):

    def _COLORRULE(text, rule_type, match_type, color_A=py_cui.RED_ON_BLACK, color_B=py_cui.RED_ON_BLACK, region=None, whitespace=False):

        color_rule = py_cui.colors.ColorRule(text, color_A, color_B, rule_type, match_type, region, whitespace, LOGGER)
        return color_rule

    return _COLORRULE