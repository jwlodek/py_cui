# PyCUI Installation

You may install `py_cui` via pip (use `pip3` if python 2 and 3 are installed side by side)

```
pip install py-cui
```

Make sure to run as root/sudo as required. Note that the library is titled `py_cui`, but the name of the pypi package is `py-cui`, though in most cases, installing with 

```
pip install py_cui
```

should work OK.

If you would like to use `py_cui` directly from source, clone this repository with:

```
git clone https://github.com/jwlodek/py_cui
```

Then build/install with `pip`:

```
cd py_cui
pip install .
```

If you would like to try it out without installing, first make sure that `curses` is installed (`windows-curses` if on windows), and then copy one of the example files into the top directory. You may then simply run it with `python3`.

### Developer Installation

Additional packages can be used by `py_cui` developers to help with debugging and other issues. For these, you may use pip:

```
pip install -r requirements_dev.txt
```

It is also recommended to use a virtual environment to develop `py_cui`:

```
mkdir venv
cd venv
python3 -m venv .
source bin/activate
```

Development packages are as follows:

Package | Used For
-----|-----
`pytest` | Unit testing
`pytest-cov` | Code coverage stats
`flake8` | Style checking
`npdoc2md` | Docstring to Markdown documentation auto-conversion

### Running Examples

To run examples, install py_cui, enter the `examples/` directory, and run them with python3. For example, to run `todo_list_example.py`:
```
cd examples
python3 todo_list_example.py
```
Feel free to take a look at the `Examples` section of this documentation for more details.