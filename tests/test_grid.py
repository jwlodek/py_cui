import pytest # noqa

import py_cui.grid as grid
import py_cui.errors as err
import py_cui.debug as dbg

logger = dbg.PyCUILogger('PYCUI TEST')

test_grid_A = grid.Grid(3, 3, 800,  600, logger)
test_grid_B = grid.Grid(1, 1, 10,   10,  logger)
test_grid_C = grid.Grid(5, 5, 100,  150, logger)


def test_init():
    row_height, col_width = test_grid_A.get_cell_dimensions()
    assert row_height == 266
    assert col_width == 200
    row_height, col_width = test_grid_B.get_cell_dimensions()
    assert row_height == 10
    assert col_width == 10
    row_height, col_width = test_grid_C.get_cell_dimensions()
    assert row_height == 20
    assert col_width == 30


def test_set_num_rows_illegal():
    try:
        test_grid_B.set_num_rows(4)
        assert False
    except err.PyCUIOutOfBoundsError:
        assert True


def test_set_num_rows_legal():
    test_grid_C.set_num_rows(10)
    row_height, col_width = test_grid_C.get_cell_dimensions()
    assert row_height == 10
    assert col_width == 30


def test_set_num_cols_illegal():
    try:
        test_grid_A.set_num_cols(300)
        assert False
    except err.PyCUIOutOfBoundsError:
        assert True


def test_set_num_cols_legal():
    test_grid_C.set_num_cols(10)
    _, col_width = test_grid_C.get_cell_dimensions()
    assert col_width == 15


def test_update_height_width_illegal_1():
    try:
        test_grid_A.update_grid_height_width(9, 10)
        assert False
    except err.PyCUIOutOfBoundsError:
        assert True


def test_update_height_width_illegal_2():
    try:
        test_grid_C.update_grid_height_width(30, 15)
        assert False
    except err.PyCUIOutOfBoundsError:
        assert True


def test_update_height_width_legal():
    test_grid_A.update_grid_height_width(300, 900)
    row_height, col_width = test_grid_A.get_cell_dimensions()
    assert col_width == 300
    assert row_height == 100
