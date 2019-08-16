# py_cui

A **py**thon library for creating **c**ommand line **u**ser **i**nterfaces.

### What is it and why is it?

`py_cui` is a python library meant to simplify writing command line user interfaces in python. It relies on the `curses` module, which is traditionally a unix-specific python module, however during my tests the [windows-curses]() module will allow `py_cui` to run on windows.

The main advantage `py_cui` has over traditional command line user interfaces is that it relies on widgets and a grid layout manager like most traditional Graphical User interfaces. You may define a grid size, and then drop predefined widgets onto it into specific grid locations. Widgets can also be stretched accross multiple grid rows and columns.

This system allows for very simple interface construction. If you've ever made a Tkinter GUI, you will feel right at home.

Do I think that `py_cui` will replace traditional GUIs? No, I'm not crazy. But as someone who loves working in the terminal this was a fun project to work on, and I've already made some useful programs using it. I hope someone else can make something cool with it as well, and if you do, feel free to let me know about it! I'd love to add a "Built with `py_cui`" section to this README.

If you would like to contribute, feel free to make an issue or pull request after reading through the `CONTRIBUTING.md` file.

### Writing a PyCUI

Basic usage of `py_cui` starts with creating a PyCUI object, and specifiying it's grid size. Keep in mind that grid cell height and width will be measured in characters, so there is a lower limit on legal grid size. Create this object with:
```
root = py_cui.PyCUI(7, 9)
```
The above line will create a UI with 7 rows and 9 columns. Then, add widgets with the different add commands:
```
label = root.add_label('Label Text', 0, 0)
button = root.add_button('Button Text', 1, 2, column_span=2, command=my_function)
...
```
for a full list of available widgets and how to add them, check on the examples or the documentation [here]().

`py_cui` also has support for custom key bindings for both the overview mode and focused mode, as well as some basic popup support.

### Using a PyCUI

There are some basic rules that apply to all `py_cui` based interfaces. There are three key operating modes - overview mode, focus mode, and popup mode. 

**Overview Mode**

In overview mode, you may move around the widgets in the UI with the arrow keys, and you may enter focus mode and/or press buttons depending on if the `auto_focus_buttons` flag is set. This mode is the overall control mode for the UI

**Focus Mode**

When in focus mode, you enter into a particular widget (For example a text box.). Each widget has some predefined basic controls, such as arrow keys to scroll in a `ScrollCell`. You may also add keybindings to functions for each particular widget. These keybindings will only apply to a widget if it is in focus mode. Enter focus mode by navigating to a widget in overview mode and hitting the `Enter` key. Return to overview mode from focus mode by pressing `Escape`.

**Popup Mode**

Popup mode simply displays a popup over the rest of the UI. You may exit popup mode by pressing `Space`, `Enter`, or `Escape`.

### Installation

You may install `py_cui` via pip:
```
pip install py_cui
```
Make sure to run as root/sudo as required.

If you would like to use `py_cui` directly from source, clone this repository with:
```
git clone https://github.com/jwlodek/py_cui
```
Then build/install with `setup.py`:
```
python3 setup.py install
```
If you would like to try it out without installing, first make sure that `curses` is installed (`windows-curses` if on windows), and then copy one of the example files into the top directory. You may then simply run it with `python3`.

### Unit Tests

`py_cui` unit tests are written for `pytest`. Make sure `pytest` is installed, and simply run
```
pytest
```
in the root directory to run all unit tests.

### License

BSD 3-Clause License

Copyright (c) 2019, Jakub Wlodek