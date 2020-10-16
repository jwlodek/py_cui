import pytest

import py_cui


def test_initial_values_base(SLIDER):
    test_slider = SLIDER(minval=0, maxval=100, step=5)

    assert test_slider.get_slider_value() == 30
    assert test_slider.update_slider_value(1) == 35
    assert test_slider.update_slider_value(-1) == 30


def test_min_value(SLIDER):
    test_slider = SLIDER(maxval=220, step=5)

    idx = 0
    while idx < 100:
        test_slider.update_slider_value(-1)
        idx += 1
    # min value
    assert test_slider.get_slider_value() == 10


def test_min_value_fail(SLIDER):
    # min 10
    # max 90
    # step 4
    # initial 65
    test_slider = SLIDER(init_val=65)

    idx = 0
    while idx < 4:
        test_slider.update_slider_value(-1)
        idx += 1
    # min value
    assert test_slider.get_slider_value() != 10


def test_max_value(SLIDER):
    test_slider = SLIDER(maxval=220, step=5)
    idx = 0
    while idx < 100:
        print(idx)
        test_slider.update_slider_value(1)
        idx += 1
    # min value
    assert test_slider.get_slider_value() == 220


def test_change_step(SLIDER):
    # min 10
    # max 90
    # step 4
    # initial 65
    test_slider = SLIDER(init_val=65)

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


def test_wrong_inital_value(SLIDER):
    with pytest.raises(py_cui.errors.PyCUIInvalidValue):
        _ = SLIDER(init_val=165)
