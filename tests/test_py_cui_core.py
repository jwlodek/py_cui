import pytest
import py_cui
print(py_cui.__path__)

def test_fit_text():
    out = py_cui.fit_text(7, 'Hello World')
    assert out == 'He...'

def test_fit_text_center():
    out = py_cui.fit_text(10, 'HI', center=True)
    assert out == '   HI    '