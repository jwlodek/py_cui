import pytest

import py_cui.grid as grid
import py_cui.errors as err


test_grid_A = grid.Grid(3, 3, 800, 600)

test_grid_B = grid.Grid(1, 1, 10, 10)

test_grid_C = grid.Grid(5, 5, 100, 150)


def test_init():
    assert test_grid_A.row_height == 266
    assert test_grid_A.column_width == 200
    assert test_grid_B.row_height == 10
    assert test_grid_B.column_width == 10
    assert test_grid_C.row_height == 20
    assert test_grid_C.column_width == 30


def test_set_num_rows_illegal():
    try:
        test_grid_B.set_num_rows(4, 4)
        assert False
    except err.PyCUIOutOfBoundsError:
        assert True


def test_set_num_rows_legal():
    test_grid_C.set_num_rows(10)
    assert test_grid_C.row_height == 10
    assert test_grid_C.column_width == 30

def test_set_num_cols_illegal():
    try:
        test_grid_A.set_num_cols(300)
        assert False
    except err.PyCUIOutOfBoundsError:

    
