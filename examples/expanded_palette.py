"""A simple example demonstrating how to add additional colors to your UI past the defaults.

@author:    Jakub Wlodek
@created:   17-Apr-2023
"""


import py_cui

root = py_cui.PyCUI(3, 3)

# The default colors created for you by py_cui are essentially every foreground/background
# combination using the default basic 8 colors: White, Black, Blue, Red, Green, Yellow, Cyan, and Magenta.

# For conveniance, these color pairs have variables that can be used as shortcuts, ex. py_cui.colors.GREEN_ON_BLACK will allow
# for green text on a black background.

# These default colors make up 56 foreground/background combinations. In total, py_cui allows for up to 256 (in supported terminals).
# The remaining 200 foreground/background pairs can be customized with the below function calls.


# The add_color_pair function takes two arguments, a foreground color, and a background color, each being a number from 0-255.
# The default colors have codes: 0 - BLACK, 1- RED, 2 - GREEN, 3 - YELLOW, 4 - BLUE, 5 - MAGENTA, 6 - CYAN, 7 - WHITE.
# 208 represents a shade of orange in my terminal emulator.

ORANGE_ON_BLACK = root.add_color_pair(208, 0)


# Additional color codes can depend on the terminal emulator, however, the below program can help identifying them.
# It will print (on a black background), the code for each of the 256 supported colors - in the respective color.
# The above number (203) was printed orange in my terminal emulator (gnome-terminal). So (208, 0) will be orange on a black background.
"""
import curses

def show_color_codes(stdscr):
    key = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()

    for i in range(256):
        curses.init_pair(i+1, i, 0)

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        xpos = 0
        ypos = 0
        for i in range(256):
            temp = int(i / 25)
            if temp > ypos:
                ypos += 1
                xpos = 0
            stdscr.addstr(ypos, xpos, " ", curses.color_pair(0))
            stdscr.addstr(ypos, xpos + 1, str(i), curses.color_pair(i))
            stdscr.addstr(ypos, xpos + 1 + len(str(i)), " ", curses.color_pair(0))
            xpos = xpos + len(str(i)) + 2

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        key = stdscr.getch()

def main():
    curses.wrapper(show_color_codes)

if __name__ == "__main__":
    main()
"""


# Add a label to the center of the CUI in the 1,1 grid position
label = root.add_label('Hello py_cui in a non-standard color!!!', 1, 1)
label.set_color(ORANGE_ON_BLACK)

# Start/Render the CUI
root.start()
