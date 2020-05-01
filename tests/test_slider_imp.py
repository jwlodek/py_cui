import pytest

import py_cui
import py_cui.debug as dbg
import py_cui.control_widgets.slider as slider


logger = dbg.PyCUILogger('PYCUI TEST')

grid_test = py_cui.grid.Grid(10, 10, 100, 100, logger)


def test_initial_values_base():
    test_slider = slider.SliderWidget('id', 'slider', grid_test, 1, 1, 1, 2,
                                      1, 0, logger, 0, 100, 5, 30)

    assert test_slider.get_slider_value() == 30
    assert test_slider.update_slider_value(1) == 35
    assert test_slider.update_slider_value(-1) == 30


def test_min_value():
    test_slider = slider.SliderWidget('id', 'slider', grid_test, 1, 1, 1, 2,
                                      1, 0, logger, 10, 220, 5, 30)

    idx = 0
    while idx < 100:
        test_slider.update_slider_value(-1)
        idx += 1
    # min value
    assert test_slider.get_slider_value() == 10


def test_min_value_fail():
    # min 10
    # max 90
    # step 4
    # initial 65
    test_slider = slider.SliderWidget('id', 'slider', grid_test, 1, 1, 1, 2,
                                      1, 0, logger, 10, 90, 4, 65)

    idx = 0
    while idx < 4:
        test_slider.update_slider_value(-1)
        idx += 1
    # min value
    assert test_slider.get_slider_value() != 10


def test_max_value():
    test_slider = slider.SliderWidget('id', 'slider', grid_test, 1, 1, 1, 2, 1, 0,
                                      logger, 10, 220, 5, 30)
    idx = 0
    while idx < 100:
        print(idx)
        test_slider.update_slider_value(1)
        idx += 1
    # min value
    assert test_slider.get_slider_value() == 220


def test_change_step():
    # min 10
    # max 90
    # step 4
    # initial 65
    test_slider = slider.SliderWidget('id', 'slider', grid_test, 1, 1, 1, 2,
                                      1, 0, logger, 10, 90, 4, 65)

    _cur = test_slider.get_slider_value()
    assert _cur == 65

    test_slider.update_slider_value(-1)
    _cur_1 = test_slider.get_slider_value()
    assert _cur_1 == 61

    test_slider.set_slider_step(22)
    assert test_slider._step == 22

    test_slider.update_slider_value(-1)
    _cur_2 = test_slider.get_slider_value()
    assert _cur_2 == 39

    _cur_3 = test_slider.update_slider_value(-1)
    _cur_3 = test_slider.update_slider_value(-1)
    assert _cur_3 == 10


def test_wrong_inital_value():
    with pytest.raises(Exception):
        slider.SliderWidget('id', 'slider', grid_test, 1,
                            1, 1, 2, 1, 0, logger, 10, 90, 4, 165)
