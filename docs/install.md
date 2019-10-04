### Installation

The easiest way to install py_cui is to use `pip`. You may simply run:
```
pip install py_cui
```
and the library should install along with all dependancies. If you are working on a machine where `pip` defaults to the `Python 2` version, replace `pip` with `pip3`.

There is no Python 2 support for `py_cui`, you will need a version of Python 3.4+ in order to use it. It may function with lower versions of Python 3, but it has not been tested on them.

Alternatively, if you wish to avoid using pip, you may install from this repository:

```
git clone https://github.com/jwlodek/py_cui
cd py_cui
pip install .
```
This will use pip to install from the sources in the git repository. If you wish to avoid installing altogether, you may copy an example from the `examples/` directory into the root `py_cui` directory, and run it with python3. Note that in this case you are required to install the dependancies yourself, which are `curses` on UNIX (should be included with python3) and `windows-curses` on windows, which can be installed with `pip`.

### Running Unit Tests

Unit tests for `py_cui` are written for pytest. Simply clone the repository, and run `pytest` in the root directory:
```
git clone https://github.com/jwlodek/py_cui
cd py_cui
pytest
```

These tests are also run on Travis-CI each time a new commit is pushed to the upstream repository.

### Running Examples

To run examples, install py_cui, enter the `examples/` directory, and run them with python3. For example, to run `todo_list_example.py`:
```
cd examples
python3 todo_list_example.py
```
Feel free to take a look at the `Examples` section of this documentation for more details.