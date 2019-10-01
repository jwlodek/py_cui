import pytest
import py_cui

"""
TODO: This test file is probably overkill
"""

def test_status_bar():
    bar = py_cui.statusbar.StatusBar('Hello', py_cui.WHITE_ON_BLACK)
    assert bar.text == 'Hello'
    bar.set_text('Test')
    assert bar.text == 'Test'