import pytest # noqa

import py_cui.grid as grid
import py_cui.widgets as widgets
import py_cui.errors as err



# grid spot width should be 6 x 6, with an overlap of 2 chars on the edges
"""
test_grid_over = grid.Grid(3, 3, 20, 20, logger)
test_cell_over_A = widgets.Widget('5', 'Test Over A',
                                  test_grid_over, 2, 0, 1, 1, 1, 0, logger)
test_cell_over_B = widgets.Widget('6', 'Test Over B',
                                  test_grid_over, 0, 2, 1, 1, 1, 0, logger)
test_cell_over_C = widgets.Widget('7', 'Test Over C',
                                  test_grid_over, 2, 2, 1, 1, 1, 0, logger)
"""


def test_illegal_create_1(GRID, LOGGER):
    test_grid = GRID(5, 7, 90, 210)
    try:
        _ = widgets.Widget('8', 'Test E', None, 0, 5, 1, 1, 1, 0, LOGGER)
        assert False
    except err.PyCUIMissingParentError:
        assert True


def test_illegal_create_2(GRID, LOGGER):
    test_grid = GRID(5, 7, 90, 210)
    try:
        _ = widgets.Widget('9', 'Test E',
                           test_grid, 6, 8, 1, 1, 1, 0, LOGGER)
        assert False
    except err.PyCUIOutOfBoundsError:
        assert True


def test_illegal_create_3(GRID, LOGGER):
    test_grid = GRID(5, 7, 90, 210)
    try:
        _ = widgets.Widget('10', 'Test E',
                           test_grid, 4, 0, 3, 1, 1, 0, LOGGER)
        assert False
    except err.PyCUIOutOfBoundsError:
        assert True


def test_illegal_create_4(GRID, LOGGER):
    test_grid = GRID(5, 7, 90, 210)
    try:
        _ = widgets.Widget('11', 'Test E',
                           test_grid, 0, 6, 1, 2, 1, 0, LOGGER)
        assert False
    except err.PyCUIOutOfBoundsError:
        assert True


def test_get_start_position(CUSTOMWIDGET):

    test_cell_A = CUSTOMWIDGET('1', 'Test A', 0, 0, 1, 1)
    test_cell_B = CUSTOMWIDGET('2', 'Test B', 3, 4, 2, 1)
    test_cell_C = CUSTOMWIDGET('3', 'Test C', 1, 2, 1, 3)
    test_cell_D = CUSTOMWIDGET('4', 'Test D -----------------------------------', 0, 0, 1, 1)

    xA, yA = test_cell_A.get_start_position()
    xB, yB = test_cell_B.get_start_position()
    xC, yC = test_cell_C.get_start_position()
    xD, yD = test_cell_D.get_start_position()
    assert xA == -1 and yA == 1
    assert xB == 119 and yB == 55
    assert xC == 59 and yC == 19
    assert xD == -1 and yD == 1


def test_get_absolute_dims_simple(CUSTOMWIDGET):

    test_cell_A = CUSTOMWIDGET('1', 'Test A', 0, 0, 1, 1)
    test_cell_B = CUSTOMWIDGET('2', 'Test B', 3, 4, 2, 1)
    test_cell_C = CUSTOMWIDGET('3', 'Test C', 1, 2, 1, 3)
    test_cell_D = CUSTOMWIDGET('4', 'Test D -----------------------------------', 0, 0, 1, 1)

    hA, wA = test_cell_A.get_absolute_dimensions()
    hB, wB = test_cell_B.get_absolute_dimensions()
    hC, wC = test_cell_C.get_absolute_dimensions()
    hD, wD = test_cell_D.get_absolute_dimensions()
    assert wA == 30 and hA == 18
    assert wB == 30 and hB == 36
    assert wC == 90 and hC == 18
    assert wD == 30 and hD == 18


def test_create_with_overlap():
    pass
    # assert test_cell_over_A.overlap_y == 2
    # assert test_cell_over_B.overlap_x == 1
    # assert test_cell_over_C.overlap_x == 1
    # assert test_cell_over_C.overlap_y == 2


def test_get_absolute_dims_overlap():
    # TODO need to fix this unit test
    return
    # wA, hA = test_cell_over_A.get_absolute_dimensions()
    # wB, hB = test_cell_over_B.get_absolute_dimensions()
    # wC, hC = test_cell_over_C.get_absolute_dimensions()
    # assert wA == 6 and hA == 8
    # assert wB == 8 and hB == 6
    # assert wC == 8 and hC == 8
