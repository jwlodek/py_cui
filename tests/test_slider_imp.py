import pytest

import py_cui
import py_cui.debug as dbg

logger = dbg.PyCUILogger('PYCUI TEST')

grid_test = py_cui.grid.Grid(10, 10, 100, 100, logger)


def test_initial_values_base():
    slider = py_cui.widgets.Slider('id', 'slider', grid_test, 1, 1, 1, 2, 1, 0,
                                   logger, 0, 100, 5, 30)

    assert slider.get_slider_value() == 30
    assert slider.update_slider_value(1) == 35
    assert slider.update_slider_value(-1) == 30


def test_min_value():
    slider = py_cui.widgets.Slider('id', 'slider', grid_test, 1, 1, 1, 2, 1, 0,
                                   logger, 10, 220, 5, 30)

    idx = 0
    while idx < 100:
        slider.update_slider_value(-1)
        idx += 1
    # min value
    assert slider.get_slider_value() == 10


def test_min_value_fail():
    # min 10
    # max 90
    # step 4
    # initial 65
    slider = py_cui.widgets.Slider('id', 'slider', grid_test, 1, 1, 1, 2, 1, 0,
                                   logger, 10, 90, 4, 65)

    idx = 0
    while idx < 4:
        slider.update_slider_value(-1)
        idx += 1
    # min value
    assert slider.get_slider_value() != 10


def test_max_value():
    slider = py_cui.widgets.Slider('id', 'slider', grid_test, 1, 1, 1, 2, 1, 0,
                                   logger, 10, 220, 5, 30)
    idx = 0
    while idx < 100:
        print(idx)
        slider.update_slider_value(1)
        idx += 1
    # min value
    assert slider.get_slider_value() == 220


def test_change_step():
    # min 10
    # max 90
    # step 4
    # initial 65
    slider = py_cui.widgets.Slider('id', 'slider', grid_test, 1, 1, 1, 2, 1, 0,
                                   logger, 10, 90, 4, 65)

    _cur = slider.get_slider_value()
    assert _cur == 65

    slider.update_slider_value(-1)
    _cur_1 = slider.get_slider_value()
    assert _cur_1 == 61

    slider.set_slider_step(22)
    assert slider._step == 22

    slider.update_slider_value(-1)
    _cur_2 = slider.get_slider_value()
    assert _cur_2 == 39

    _cur_3 = slider.update_slider_value(-1)
    _cur_3 = slider.update_slider_value(-1)
    assert _cur_3 == 10


def test_wrong_inital_value():
    with pytest.raises(Exception):
        py_cui.widgets.Slider('id', 'slider', grid_test, 1,
                              1, 1, 2, 1, 0, logger, 10, 90, 4, 165)
