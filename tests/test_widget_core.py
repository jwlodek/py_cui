import pytest

import py_cui.grid as grid
import py_cui.widgets as widgets
import py_cui.errors as err


test_grid = grid.Grid(5, 7, 90, 210)
test_cell_A = widgets.Widget('1', 'TestA', test_grid, 0, 0, 1, 1, 1, 0)
test_cell_B = widgets.Widget('2', 'Test B', test_grid, 3, 4, 2, 1, 1, 0)
test_cell_C = widgets.Widget('3', 'Test C', test_grid, 1, 2, 1, 3, 1, 0)
test_cell_D = widgets.Widget('4', 'Test D -----------------------------------', test_grid, 0, 0, 1, 1, 1, 0)


# grid spot width should be 6 x 6, with an overlap of 2 chars on the edges
test_grid_over = grid.Grid(3, 3, 20, 20)
test_cell_over_A = widgets.Widget('5', 'Test Over A', test_grid_over, 2, 0, 1, 1, 1, 0)
test_cell_over_B = widgets.Widget('6', 'Test Over B', test_grid_over, 0, 2, 1, 1, 1, 0)
test_cell_over_C = widgets.Widget('7', 'Test Over C', test_grid_over, 2, 2, 1, 1, 1, 0)



def test_illegal_create_1():
    try:
        test_cell_E = widgets.Widget('8', 'Test E', None, 0, 5, 1, 1, 1, 0)
        assert False
    except err.PyCUIMissingParentError:
        assert True


def test_illegal_create_2():
    try:
        test_cell_E = widgets.Widget('9', 'Test E', test_grid, 6, 8, 1, 1, 1, 0)
        assert False
    except err.PyCUIOutOfBoundsError:
        assert True


def test_illegal_create_3():
    try:
        test_cell_E = widgets.Widget('10', 'Test E', test_grid, 4, 0, 3, 1, 1, 0)
        assert False
    except err.PyCUIOutOfBoundsError:
        assert True

def test_illegal_create_4():
    try:
        test_cell_E = widgets.Widget('11', 'Test E', test_grid, 0, 6, 1, 2, 1, 0)
        assert False
    except err.PyCUIOutOfBoundsError:
        assert True


def test_get_absolute_position():
    xA, yA = test_cell_A.get_absolute_position()
    xB, yB = test_cell_B.get_absolute_position()
    xC, yC = test_cell_C.get_absolute_position()
    xD, yD = test_cell_D.get_absolute_position()
    assert xA == 0 and yA == 2
    assert xB == 120 and yB == 56
    assert xC == 60 and yC == 20
    assert xD == 0 and yD == 2


def test_get_absolute_dims_simple():
    wA, hA = test_cell_A.get_absolute_dims()
    wB, hB = test_cell_B.get_absolute_dims()
    wC, hC = test_cell_C.get_absolute_dims()
    wD, hD = test_cell_D.get_absolute_dims()
    assert wA == 30 and hA == 18
    assert wB == 30 and hB == 36
    assert wC == 90 and hC == 18
    assert wD == 30 and hD == 18


def test_create_with_overlap():
    assert test_cell_over_A.overlap_y == 2
    assert test_cell_over_B.overlap_x == 1
    assert test_cell_over_C.overlap_x == 1 and test_cell_over_C.overlap_y == 2


def test_get_absolute_dims_overlap():
    #TODO need to fix this unit test
    return
    wA, hA = test_cell_over_A.get_absolute_dims()
    wB, hB = test_cell_over_B.get_absolute_dims()
    wC, hC = test_cell_over_C.get_absolute_dims()
    assert wA == 6 and hA == 8
    assert wB == 8 and hB == 6
    assert wC == 8 and hC == 8