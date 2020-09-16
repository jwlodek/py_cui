# Usage

In this section we discuss some universal usage rules common to all `py_cui` based interfaces.

### py_cui Operation Modes

Each `py_cui` based interface has three operation modes: overview mode, focus mode, and popup mode.

**Overview Mode**

In overview mode, you use your arrow keys to navigate between widgets. While in overview mode you may also press buttons by hovering over them and pressing Enter, or you may enter focus mode on a widget by hovering over it and pressing Enter. In addition, any keybindings you add to the root `PyCUI` object will be accessible while in overview mode. Also while in overview mode, by default the `q` key is used to quit. To cycle through widgets you can also use Ctrl + Left/Right arrow keys.

**Focus mode**

Once you enter focus mode on a particular widget, different keybindings apply. These vary from widget to widget, but the Esc key always returns to overview mode. Also, any keybindings assigned to the in-focus widget will be honored here.

**Popup Mode**

During popup mode, no keybindings are accepted by default. Certain popups allow for certain keys to close or interact with them however. When in popup mode no CUI widgets or overview are accessible. If a widget was in focus when popup mode is initiated, focus is lost.