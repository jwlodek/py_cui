import pytest # noqa
import py_cui

# Some test strings
test_string_A = "Hello world, etc 123 @ testing @ ++-- Test"
test_string_B = "     Test string number two Space"
test_string_C = "Hi"


def gen_color_rule_examples(rule_gen):
    color_rule_examples = []
    color_rule_examples.append(rule_gen('@.*@', 'contains', 'regex'))
    color_rule_examples.append(rule_gen('Test', 'startswith', 'line'))
    color_rule_examples.append(rule_gen('Space', 'endswith', 'regex'))
    color_rule_examples.append(rule_gen('Test', 'notstartswith', 'region', region=[3,5]))
    color_rule_examples.append(rule_gen('Test', 'notendswith', 'line'))

    return color_rule_examples


def test_check_match(COLORRULE):
    rules = gen_color_rule_examples(COLORRULE)
    
    assert rules[0]._check_match(test_string_A) is True
    assert rules[1]._check_match(test_string_A) is False
    assert rules[2]._check_match(test_string_A) is False
    assert rules[3]._check_match(test_string_A) is True
    assert rules[4]._check_match(test_string_A) is False

    assert rules[0]._check_match(test_string_B) is False
    assert rules[1]._check_match(test_string_B) is True
    assert rules[2]._check_match(test_string_B) is True
    assert rules[3]._check_match(test_string_B) is False
    assert rules[4]._check_match(test_string_B) is True

    assert rules[0]._check_match(test_string_C) is False
    assert rules[1]._check_match(test_string_C) is False
    assert rules[2]._check_match(test_string_C) is False
    assert rules[3]._check_match(test_string_C) is True
    assert rules[4]._check_match(test_string_C) is True


def test_generate_fragments_contains_regex(COLORRULE, DUMMYWIDGET):
    rules = gen_color_rule_examples(COLORRULE)

    fragments, match = rules[0].generate_fragments(DUMMYWIDGET,
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

    fragments, match = rules[0].generate_fragments(DUMMYWIDGET,
                                                       test_string_B,
                                                       test_string_B)
    assert match is False
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_B
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK

    fragments, match = rules[0].generate_fragments(DUMMYWIDGET,
                                                       test_string_C,
                                                       test_string_C)
    assert match is False
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_C
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK


def test_generate_fragments_startswith_line(COLORRULE, DUMMYWIDGET):
    rules = gen_color_rule_examples(COLORRULE)

    fragments, match = rules[1].generate_fragments(DUMMYWIDGET,
                                                       test_string_A,
                                                       test_string_A)
    assert match is False
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_A
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK

    fragments, match = rules[1].generate_fragments(DUMMYWIDGET,
                                                       test_string_B,
                                                       test_string_B)
    assert match is True
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_B
    assert fragments[0][1] == py_cui.RED_ON_BLACK

    fragments, match = rules[1].generate_fragments(DUMMYWIDGET,
                                                       test_string_C,
                                                       test_string_C)
    assert match is False
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_C
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK


def test_generate_fragments_endswith_regex(COLORRULE, DUMMYWIDGET):
    rules = gen_color_rule_examples(COLORRULE)

    fragments, match = rules[2].generate_fragments(DUMMYWIDGET,
                                                       test_string_A,
                                                       test_string_A)
    assert match is False
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_A
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK

    fragments, match = rules[2].generate_fragments(DUMMYWIDGET,
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

    fragments, match = rules[2].generate_fragments(DUMMYWIDGET,
                                                       test_string_C,
                                                       test_string_C)
    assert match is False
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_C
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK


def test_generate_fragments_notstartswith_region(COLORRULE, DUMMYWIDGET):
    rules = gen_color_rule_examples(COLORRULE)

    fragments, match = rules[3].generate_fragments(DUMMYWIDGET,
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

    fragments, match = rules[3].generate_fragments(DUMMYWIDGET,
                                                       test_string_B,
                                                       test_string_B)
    assert match is False
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_B
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK

    fragments, match = rules[3].generate_fragments(DUMMYWIDGET,
                                                       test_string_C,
                                                       test_string_C)
    # In this case we match, but our input is too small
    # for region to be accounted for, so should return
    assert match is True
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_C
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK


def test_generate_fragments_notendswith_line(COLORRULE, DUMMYWIDGET):
    rules = gen_color_rule_examples(COLORRULE)

    fragments, match = rules[4].generate_fragments(DUMMYWIDGET,
                                                       test_string_A,
                                                       test_string_A)
    assert match is False
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_A
    assert fragments[0][1] == py_cui.WHITE_ON_BLACK

    fragments, match = rules[4].generate_fragments(DUMMYWIDGET,
                                                       test_string_B,
                                                       test_string_B)
    assert len(fragments) == 1
    assert match is True
    assert fragments[0][0] == test_string_B
    assert fragments[0][1] == py_cui.RED_ON_BLACK

    fragments, match = rules[4].generate_fragments(DUMMYWIDGET,
                                                       test_string_C,
                                                       test_string_C)
    assert match is True
    assert len(fragments) == 1
    assert fragments[0][0] == test_string_C
    assert fragments[0][1] == py_cui.RED_ON_BLACK
