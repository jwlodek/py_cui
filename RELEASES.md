# py_cui Releases

This file will contain a changelog for all release versions of py_cui.

## v0.1.3 - Feb ??, 2021

This release adds filedialog popup support, a significant overhaul of the slider widget, overhaul of testing, scroll menu improvements, and minor bugfixes

### Features Added

* New popup - Filedialog popup allows for seamlessly asking user to select a file, directory, or a save location.
* Slider widget improved, adding options for alignment, as well as 
* Allow for border color to be set for in-focus and out of focus seperately
* Test overhaul to use pytest fixtures. Modernized pytest structure
* Version auto-detection during packaging process
* Example improvements + bugfixes
* IDE annotations added to examples
* Cyrillic input support for textboxes
* Avoid drawing bolded black on white - produces illegible results on many terminals
* Add custom exceptions for un

### Issues Fixed

* #49
* #68
* #75
* #57
* #61
* #86
* #64
* #88
* #90

### Breaking Changes

The slider widget has had some changes to the outer facing API. No other breaking changes were made.


## v0.1.2 - Sep 15, 2020

Next iterative release of `py_cui`. This release fixes some minor issues with the old version, adds form and slider popups and widgets, expands color and key options, and makes performance improvements.

### Features Added

* Huge performance improvement. Only redraw changed areas of screen.
* Functions to allow setting timeout for waiting for user input to refresh. Allows for editing values in second thread and seeing them update without having to interact with the UI
* Many new Colors added (56 total combinations, up from 10)
* Many new keys supported (Modifiers + letters, some special keys)
* Support for setting widget cycling keys for navigating between widgets even when in focus mode. (Defaults to Ctrl + left/right arrow keys).
* Support for a slider widget added.
* Form entry popup added. Allows for asking for several fields of input
* Greatly expanded coloration options. Can now individually set border color, text color, and selected text color

### Issues Fixed

* #54 
* #46 
* #50 
* #63
* #60 

### Breaking Changes

No breaking changes were made to the outer-facing API in this PR. Internally, certain functions had arguments added, but externally these are treated as keyword arguments.

## v0.1.1 - May 23, 2020

Next iterative release of `py_cui`, meant to add some requested functionality and improvements, particularly for scroll and checkbox menu widgets. Also adds mouse click support 

### Features Added

* Create `CheckBoxMenuImplementation` class
* Allow menu items to receive objects as well as strings
* Add additional default keys for faster menu navigation
* Mouse click support
* Fix bug with block label widget centering
* Fix some minor encapsulation issues

### Issues Fixed

* #44 
* #45 
* #16 
* #51 

### Breaking Changes

The only (minor) breaking change in this release is the change in the scoping of the title bar variable in the root PyCUI class. Most applications should not be affected, unless referencing the variable directly, instead of through getters/setters.

## v0.1.0 - Apr 18, 2020

First alpha release of `py_cui`, adds many requested features, but has some minor breaking changes, that shouldn't affect many programs.

### Features Added

* Add logging support for debug purposes
* Improve code reuse, restructure widget and popup classes
* Add set of central base classes for UI elements and implementations
* Move CI/CD to github actions
* Fix bug with window resize with widget sets on `win32`
* Improve error handling in main draw loop
* Improved widget navigation
* Fix `KEY_BACKSPACE` on MacOS
* Add ability to run in simulated terminal to improve testing capabilities

### Issues fixed

* #40 
* #38 
* #36 
* #35 
* #27 
* #21 

### Breaking Changes

* WidgetSet objects should no longer be directly created, but instead should be spawned with the `create_new_widget_set` function.
* Many internal variable name changes, are now accessible via getter and setter methods. Any instances where direct access to internal variables was made may be broken, but can easily be replaced without functionality loss with getter/setter alternatives

## v0.0.3 - Mar 10, 2020

Next iterative release of `py_cui`

### Features Added

* Custom border characters. You may now use non-ascii unicode border characters (`toggle_unicode_borders`)
* TextBox password option. You may now enable password protection on standard textboxes
* Improved doc generation

### Bug Fixes/Improvements

* Navigation between widgets that are not directly adjacent improved
* Missing `DELETE` key functionality added for textbox and textbox popup
* Removed redundant docstrings
* Mark checked option fixed for checkbox menu widget
* Loading bar now will always be correct size
* Add loading animation to loading bar

## v0.0.2 - Feb 19, 2020

Next iterative release of `py_cui`

### Features Added
* label.toggle_border() for showing label borders

### Bug Fixes
* `move_focus` command should work correctly
* Fix issue with windows installs
* Improve doc auto-generation
* Improve docs in code and examples
* Fix incorrect use of function in `move_focus`

## v0.0.1 - Feb 19, 2020

Initial pre-release version of `py_cui`. 

### Features Added
* Collection of default widgets
* Popup support
* Loading icon support
* Ability to switch between windows
* Ascii based interface renderer
* Basic text color options
* Grid layout manager
* Automated CI/CD unit testing with TravisCI

### Known Issues
* Windows version does not seem to pull `windows-curses` from pypi automatically
* `move_focus` does not reset status bar text
* Docs are incomplete

### Future Plans
* Improved layout management
* More intuitive color rule definition
* `py_cui_constructor` helper script for building `py_cui` interface templates
* Code cleanup and bug fixes