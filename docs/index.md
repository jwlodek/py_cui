<div align="center">
    <img src="assets/py_cui_logo_new.svg" alt="PyCUI" width=300px>
</div>

<div align="center">
    <p><strong><br/>A library for creating CUI/TUI interfaces with pre-built widgets in python.</strong></p>
    <p>Easily build text-based user interfaces on both Linux and Windows.</p>
    <a href="#">
        <img src="https://github.com/jwlodek/py_cui/workflows/tests/badge.svg?branch=master" alt="Automated Test+Build Status">
    </a>
    <a href="https://pepy.tech/project/py-cui">
        <img src="https://pepy.tech/badge/py-cui" alt="Download Counter">
    </a>
    <a href="https://badge.fury.io/py/py-cui">
        <img src="https://badge.fury.io/py/py-cui.svg" alt="PyPI Version">
    </a>
    <a href="#">
        <img src="https://img.shields.io/github/license/jwlodek/py_cui.svg" alt="License">
    </a>
</div>

---

# py_cui

`py_cui` is a python library meant to simplify writing console user interfaces in python. It relies on `curses`, which is traditionally unix-specific, however, you may use the [windows-curses](https://github.com/zephyrproject-rtos/windows-curses) module to run `py_cui` on windows.

The main advantage `py_cui` has over typical text-based user interface builders is that it relies on widgets and a grid layout manager like most traditional graphical user interfaces. You may define a grid size, and then drop predefined widgets onto it into specific grid locations. Widgets can also be stretched accross multiple grid rows and columns. If you've ever made a Tkinter GUI, you will feel right at home.

If you would like to contribute, feel free to make an issue or pull request after reading through the `CONTRIBUTING.md` file.

## Examples

Below are some screenshots and gifs of programs written with py_cui. Additional (simpler) examples are available in the `examples/` directory of this repository.

**py_cui_2048 - A command line version of the classic 2048 game**

[py_cui_2048](https://github.com/jwlodek/py_cui_2048) is a demo of using `py_cui` to build simple CUI games and applications. The entire game was made in under 400 lines of code.
<p align="center">
    <img src="assets/py2048-demo.gif">
</p>

**recoverpy - A TUI that allows for recovering lost or deleted files**

[recoverpy](https://github.com/PabloLec/recoverpy) is a utility for recovering files on linux. It will search through every inode to find your requested file block.

<p align="center">
    <img src="assets/recoverpy-demo.gif">
</p>

**pyautogit - A command line interface for managing git repositories**

[pyautogit](https://github.com/jwlodek/pyautogit) is the first larger scale project written in `py_cui`. Feel free to use it as a guide to programming with `py_cui`.
<p align="center">
    <img src="assets/pyautogit-demo.gif">
</p>

## Powered by py_cui

Below is a table of python projects developed with the help of `py_cui`. If you've made something, feel free to make a pull request to add it!

Project | Description
--------|-------------
[pypodcasts](https://github.com/jwlodek/pypodcasts) | A TUI for listening to and managing podcast feeds. (Coming Soon)
[pyautogit](https://github.com/jwlodek/pyautogit) | A command line UI for interfacing with git features for multiple repositories.
[recoverpy](https://github.com/PabloLec/recoverpy) | A CUI for recovering overwritten or deleted data on linux.
[py_cui_2048](https://github.com/jwlodek/py_cui_2048) | A CUI version of the classic 2048 game.
[unipkg](https://github.com/jwlodek/unipkg) | A CUI interface for managing all installed package managers on your system. (In-Progress)
[CUIAudioPlayer](https://github.com/jupiterbjy/CUIAudioPlayer) | A TUI for playing back audio files in a variety of formats.
[tinypub](https://github.com/HakierGrzonzo/tinyPub) | A console-based ebook reader.
[hue-tui](https://github.com/channel-42/hue-tui) | A CUI controlling for Philips Hue lights.
[mini-radio-player](https://github.com/wdog/mini-radio-player-pycui) | A terminal based radio interface for linux.

## License

BSD 3-Clause License

Copyright (c) 2019-2021, Jakub Wlodek