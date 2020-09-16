import pytest # noqa
import py_cui
from py_cui.colors import ColorRule
import py_cui.debug as dbg

# Initialize debug logger
logger = dbg.PyCUILogger('PYCUI TEST')

# Some test strings
test_string_A = "Hello world, etc 123 @ testing @ ++-- Test"
test_string_B = "     Test string number two Space"
test_string_C = "Hi"

# Initialize a dummy grid, widget, and color rules
dummy_grid = py_cui.grid.Grid(3, 3, 30, 30, logger)
dummy_widget = py_cui.widgets.Widget('1', 'Test', dummy_grid,
                                     1, 1, 1, 1, 1, 0, logger)

color_rule_A = ColorRule('@.*@', py_cui.RED_ON_BLACK, py_cui.RED_ON_BLACK,
                         'contains', 'regex', None, False, logger)

color_rule_B = ColorRule('Test', py_cui.RED_ON_BLACK, py_cui.RED_ON_BLACK,
                         'startswith', 'line', None, False, logger)

color_rule_C = ColorRule('Space', py_cui.RED_ON_BLACK, py_cui.RED_ON_BLACK,
                         'endswith', 'regex', None,   False, logger)

color_rule_D = ColorRule('Test', py_cui.RED_ON_BLACK, py_cui.RED_ON_BLACK,
                         'notstartswith', 'region', [3, 5], False, logger)

color_rule_E = ColorRule('Test', py_cui.RED_ON_BLACK, py_cui.RED_ON_BLACK,
                         'notendswith', 'line', None, False, logger)


def test_check_match():
    assert color_rule_A._check_match(test_string_A) is True
    assert color_rule_B._check_match(test_string_A) is False
    assert color_rule_C._check_match(test_string_A) is False
    assert color_rule_D._check_match(test_string_A) is True
    assert color_rule_E._check_match(test_string_A) is False

    assert color_rule_A._check_match(test_string_B) is False
    assert color_rule_B._check_match(test_string_B) is True
    assert color_rule_C._check_match(test_string_B) is True
    assert color_rule_D._check_match(test_string_B) is False
    assert color_rule_E._check_match(test_string_B) is True

    assert color_rule_A._check_match(test_string_C) is False
    assert color_rule_B._check_match(test_string_C) is False
    assert color_rule_C._check_match(test_string_C) is False
    assert color_rule_D._check_match(test_string_C) is True
    assert color_rule_E._check_match(test_string_C) is True


def test_generate_fragments_A():

    fragments, match = color_rule_A.generate_fragments(dummy_widget,
                                                       test_string_A,
                                                       test_string_A)
    assert match is True
    assert len(fragments) == 3
    assert fragments[0][0] == "Hello world, etc 123 "
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK
    assert fragments[1][0] == "@ testing @"
    assert fragments[1][1] == py_cui.RED_ON_BLACK
    assert fragments[2][0] == " ++-- Test"
    assert fragments[2][1] == py_cui.WHITE_ON_BLACK

    fragments, match = color_rule_A.generate_fragments(dummy_widget,
                                                       test_string_B,
                                                       test_string_B)
    assert match is False
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_B
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK

    fragments, match = color_rule_A.generate_fragments(dummy_widget,
                                                       test_string_C,
                                                       test_string_C)
    assert match is False
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_C
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK


def test_generate_fragments_B():

    fragments, match = color_rule_B.generate_fragments(dummy_widget,
                                                       test_string_A,
                                                       test_string_A)
    assert match is False
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_A
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK

    fragments, match = color_rule_B.generate_fragments(dummy_widget,
                                                       test_string_B,
                                                       test_string_B)
    assert match is True
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_B
    assert fragments[0][1] == py_cui.RED_ON_BLACK

    fragments, match = color_rule_B.generate_fragments(dummy_widget,
                                                       test_string_C,
                                                       test_string_C)
    assert match is False
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_C
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK


def test_generate_fragments_C():
    fragments, match = color_rule_C.generate_fragments(dummy_widget,
                                                       test_string_A,
                                                       test_string_A)
    assert match is False
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_A
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK

    fragments, match = color_rule_C.generate_fragments(dummy_widget,
                                                       test_string_B,
                                                       test_string_B)
    assert match is True
    assert len(fragments) == 3
    assert fragments[0][0] == "     Test string number two "
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK
    assert fragments[1][0] == "Space"
    assert fragments[1][1] == py_cui.RED_ON_BLACK
    assert fragments[2][0] == ''
    assert fragments[2][1] == py_cui.WHITE_ON_BLACK

    fragments, match = color_rule_C.generate_fragments(dummy_widget,
                                                       test_string_C,
                                                       test_string_C)
    assert match is False
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_C
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK


def test_generate_fragments_D():
    fragments, match = color_rule_D.generate_fragments(dummy_widget,
                                                       test_string_A,
                                                       test_string_A)
    assert match is True
    assert len(fragments) == 3
    assert fragments[0][0] == "Hel"
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK
    assert fragments[1][0] == "lo"
    assert fragments[1][1] == py_cui.RED_ON_BLACK
    assert fragments[2][0] == " world, etc 123 @ testing @ ++-- Test"
    assert fragments[2][1] == py_cui.WHITE_ON_BLACK

    fragments, match = color_rule_D.generate_fragments(dummy_widget,
                                                       test_string_B,
                                                       test_string_B)
    assert match is False
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_B
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK

    fragments, match = color_rule_D.generate_fragments(dummy_widget,
                                                       test_string_C,
                                                       test_string_C)
    # In this case we match, but our input is too small
    # for region to be accounted for, so should return
    assert match is True
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_C
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK


def test_generate_fragments_E():
    fragments, match = color_rule_E.generate_fragments(dummy_widget,
                                                       test_string_A,
                                                       test_string_A)
    assert match is False
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_A
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK

    fragments, match = color_rule_E.generate_fragments(dummy_widget,
                                                       test_string_B,
                                                       test_string_B)
    assert len(fragments) == 1
    assert match is True
    assert fragments[0][0] == test_string_B
    assert fragments[0][1] == py_cui.RED_ON_BLACK

    fragments, match = color_rule_E.generate_fragments(dummy_widget,
                                                       test_string_C,
                                                       test_string_C)
    assert match is True
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_C
    assert fragments[0][1] == py_cui.RED_ON_BLACK
