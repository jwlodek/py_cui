"""Module containing constants and helper functions for dealing with keys.
"""

# Author:    Jakub Wlodek
# Created:   12-Aug-2019


from sys import platform
import curses

# Some simple helper functions

def get_ascii_from_char(char):
    """Function that converts ascii code to character

    Parameters
    ----------
    char : character
        character to convert to ascii
    
    Returns
    -------
    ascii_code : int
        Ascii code of character
    """

    return ord(char)


def get_char_from_ascii(key_num):
    """Function that converts a character to an ascii code

    Parameters
    ----------
    ascii_code : int
        Ascii code of character

    Returns
    -------
    char : character
        character converted from ascii
    """

    if key_num is None:
        return None

    return chr(key_num)


# Supported py_cui keys
KEY_ENTER       = get_ascii_from_char('\n')
# Escape character is ascii #27
KEY_ESCAPE      = 27
KEY_SPACE       = get_ascii_from_char(' ')
KEY_DELETE      = curses.KEY_DC
KEY_TAB         = get_ascii_from_char('\t')

# Arrow Keys
KEY_UP_ARROW    = curses.KEY_UP
KEY_DOWN_ARROW  = curses.KEY_DOWN
KEY_LEFT_ARROW  = curses.KEY_LEFT
KEY_RIGHT_ARROW = curses.KEY_RIGHT


if platform == 'linux' or platform == 'darwin':
    
    # Modified arrow keys
    KEY_SHIFT_LEFT  = 393
    KEY_SHIFT_RIGHT = 402
    KEY_SHIFT_UP    = 337
    KEY_SHIFT_DOWN  = 336
    
    KEY_CTRL_LEFT   = 560
    KEY_CTRL_RIGHT  = 545
    KEY_CTRL_UP     = 566
    KEY_CTRL_DOWN   = 525

elif platform == 'win32':

    KEY_SHIFT_LEFT  = 391
    KEY_SHIFT_RIGHT = 400
    KEY_SHIFT_UP    = 547
    KEY_SHIFT_DOWN  = 548
    
    KEY_CTRL_LEFT   = 443
    KEY_CTRL_RIGHT  = 444
    KEY_CTRL_UP     = 480
    KEY_CTRL_DOWN   = 481


ARROW_KEYS = [KEY_UP_ARROW, KEY_DOWN_ARROW, KEY_LEFT_ARROW, KEY_RIGHT_ARROW]


# Page navigation keys
KEY_PAGE_UP     = curses.KEY_PPAGE
KEY_PAGE_DOWN   = curses.KEY_NPAGE
KEY_HOME        = curses.KEY_HOME
KEY_END         = curses.KEY_END


# Standard letter keys
KEY_A_LOWER     = get_ascii_from_char('a')
KEY_B_LOWER     = get_ascii_from_char('b')
KEY_C_LOWER     = get_ascii_from_char('c')
KEY_D_LOWER     = get_ascii_from_char('d')
KEY_E_LOWER     = get_ascii_from_char('e')
KEY_F_LOWER     = get_ascii_from_char('f')
KEY_G_LOWER     = get_ascii_from_char('g')
KEY_H_LOWER     = get_ascii_from_char('h')
KEY_I_LOWER     = get_ascii_from_char('i')
KEY_J_LOWER     = get_ascii_from_char('j')
KEY_K_LOWER     = get_ascii_from_char('k')
KEY_L_LOWER     = get_ascii_from_char('l')
KEY_M_LOWER     = get_ascii_from_char('m')
KEY_N_LOWER     = get_ascii_from_char('n')
KEY_O_LOWER     = get_ascii_from_char('o')
KEY_P_LOWER     = get_ascii_from_char('p')
KEY_Q_LOWER     = get_ascii_from_char('q')
KEY_R_LOWER     = get_ascii_from_char('r')
KEY_S_LOWER     = get_ascii_from_char('s')
KEY_T_LOWER     = get_ascii_from_char('t')
KEY_U_LOWER     = get_ascii_from_char('u')
KEY_V_LOWER     = get_ascii_from_char('v')
KEY_W_LOWER     = get_ascii_from_char('w')
KEY_X_LOWER     = get_ascii_from_char('x')
KEY_Y_LOWER     = get_ascii_from_char('y')
KEY_Z_LOWER     = get_ascii_from_char('z')


# Shift modified (Uppercase) letters
KEY_A_UPPER     = get_ascii_from_char('A')
KEY_B_UPPER     = get_ascii_from_char('B')
KEY_C_UPPER     = get_ascii_from_char('C')
KEY_D_UPPER     = get_ascii_from_char('D')
KEY_E_UPPER     = get_ascii_from_char('E')
KEY_F_UPPER     = get_ascii_from_char('F')
KEY_G_UPPER     = get_ascii_from_char('G')
KEY_H_UPPER     = get_ascii_from_char('H')
KEY_I_UPPER     = get_ascii_from_char('I')
KEY_J_UPPER     = get_ascii_from_char('J')
KEY_K_UPPER     = get_ascii_from_char('K')
KEY_L_UPPER     = get_ascii_from_char('L')
KEY_M_UPPER     = get_ascii_from_char('M')
KEY_N_UPPER     = get_ascii_from_char('N')
KEY_O_UPPER     = get_ascii_from_char('O')
KEY_P_UPPER     = get_ascii_from_char('P')
KEY_Q_UPPER     = get_ascii_from_char('Q')
KEY_R_UPPER     = get_ascii_from_char('R')
KEY_S_UPPER     = get_ascii_from_char('S')
KEY_T_UPPER     = get_ascii_from_char('T')
KEY_U_UPPER     = get_ascii_from_char('U')
KEY_V_UPPER     = get_ascii_from_char('V')
KEY_W_UPPER     = get_ascii_from_char('W')
KEY_X_UPPER     = get_ascii_from_char('X')
KEY_Y_UPPER     = get_ascii_from_char('Y')
KEY_Z_UPPER     = get_ascii_from_char('Z')


LOWERCASE_LETTER_KEYS = list(range(97, 123))
UPPERCASE_LETTER_KEYS = list(range(65, 91))
LETTER_KEYS = UPPERCASE_LETTER_KEYS + LOWERCASE_LETTER_KEYS


# Control Keys
KEY_CTRL_A      = 1
KEY_CTRL_B      = 2
KEY_CTRL_C      = 3
KEY_CTRL_D      = 4
KEY_CTRL_E      = 5
KEY_CTRL_F      = 6
KEY_CTRL_G      = 7
KEY_CTRL_H      = 8
KEY_CTRL_I      = 9
KEY_CTRL_J      = 10
KEY_CTRL_K      = 11
KEY_CTRL_L      = 12
KEY_CTRL_M      = 13
KEY_CTRL_N      = 14
KEY_CTRL_O      = 15
KEY_CTRL_P      = 16
KEY_CTRL_Q      = 17
KEY_CTRL_R      = 18
KEY_CTRL_S      = 19
KEY_CTRL_T      = 20
KEY_CTRL_U      = 21
KEY_CTRL_V      = 22
KEY_CTRL_W      = 23
KEY_CTRL_X      = 24
KEY_CTRL_Y      = 25
KEY_CTRL_Z      = 26

CTRL_MODIFIED_LETTERS = list(range(1,27))

_ALT_MODIFIER = 0
if platform == 'win32':
    _ALT_MODIFIER = 320

# Alt-modified keys
KEY_ALT_A       = 97 + _ALT_MODIFIER
KEY_ALT_B       = 98 + _ALT_MODIFIER
KEY_ALT_C       = 99 + _ALT_MODIFIER
KEY_ALT_D       = 100 + _ALT_MODIFIER
KEY_ALT_E       = 101 + _ALT_MODIFIER
KEY_ALT_F       = 102 + _ALT_MODIFIER
KEY_ALT_G       = 103 + _ALT_MODIFIER
KEY_ALT_H       = 104 + _ALT_MODIFIER
KEY_ALT_I       = 105 + _ALT_MODIFIER
KEY_ALT_J       = 106 + _ALT_MODIFIER
KEY_ALT_K       = 107 + _ALT_MODIFIER
KEY_ALT_L       = 108 + _ALT_MODIFIER
KEY_ALT_M       = 109 + _ALT_MODIFIER
KEY_ALT_N       = 110 + _ALT_MODIFIER
KEY_ALT_O       = 111 + _ALT_MODIFIER
KEY_ALT_P       = 112 + _ALT_MODIFIER
KEY_ALT_Q       = 113 + _ALT_MODIFIER
KEY_ALT_R       = 114 + _ALT_MODIFIER
KEY_ALT_S       = 115 + _ALT_MODIFIER
KEY_ALT_T       = 116 + _ALT_MODIFIER
KEY_ALT_U       = 117 + _ALT_MODIFIER
KEY_ALT_V       = 118 + _ALT_MODIFIER
KEY_ALT_W       = 119 + _ALT_MODIFIER
KEY_ALT_X       = 120 + _ALT_MODIFIER
KEY_ALT_Y       = 121 + _ALT_MODIFIER
KEY_ALT_Z       = 122 + _ALT_MODIFIER

# Function keys
KEY_F0          = curses.KEY_F0
KEY_F1          = curses.KEY_F1
KEY_F2          = curses.KEY_F2
KEY_F3          = curses.KEY_F3
KEY_F4          = curses.KEY_F4
KEY_F5          = curses.KEY_F5
KEY_F6          = curses.KEY_F6
KEY_F7          = curses.KEY_F7
KEY_F8          = curses.KEY_F8
KEY_F9          = curses.KEY_F9
KEY_F10         = curses.KEY_F10
KEY_F11         = curses.KEY_F11
KEY_F12         = curses.KEY_F12


# Number keys
KEY_0 = get_ascii_from_char('0')
KEY_1 = get_ascii_from_char('1')
KEY_2 = get_ascii_from_char('2')
KEY_3 = get_ascii_from_char('3')
KEY_4 = get_ascii_from_char('4')
KEY_5 = get_ascii_from_char('5')
KEY_6 = get_ascii_from_char('6')
KEY_7 = get_ascii_from_char('7')
KEY_8 = get_ascii_from_char('8')
KEY_9 = get_ascii_from_char('9')

# Array storing number keys
NUMBER_KEYS = [KEY_0, KEY_1, KEY_2, KEY_3, KEY_4, KEY_5, KEY_6, KEY_7, KEY_8, KEY_9]
ALPHANUMERIC_KEYS = LETTER_KEYS + NUMBER_KEYS

# Mouse click events
LEFT_MOUSE_CLICK        = curses.BUTTON1_CLICKED
LEFT_MOUSE_DBL_CLICK    = curses.BUTTON1_DOUBLE_CLICKED
LEFT_MOUSE_TRPL_CLICK   = curses.BUTTON1_TRIPLE_CLICKED
LEFT_MOUSE_PRESSED      = curses.BUTTON1_PRESSED
LEFT_MOUSE_RELEASED     = curses.BUTTON1_RELEASED

RIGHT_MOUSE_CLICK        = curses.BUTTON3_CLICKED
RIGHT_MOUSE_DBL_CLICK    = curses.BUTTON3_DOUBLE_CLICKED
RIGHT_MOUSE_TRPL_CLICK   = curses.BUTTON3_TRIPLE_CLICKED
RIGHT_MOUSE_PRESSED      = curses.BUTTON3_PRESSED
RIGHT_MOUSE_RELEASED     = curses.BUTTON3_RELEASED

MOUSE_EVENTS = [LEFT_MOUSE_CLICK, LEFT_MOUSE_DBL_CLICK, LEFT_MOUSE_TRPL_CLICK, LEFT_MOUSE_PRESSED, LEFT_MOUSE_RELEASED,
                RIGHT_MOUSE_CLICK, RIGHT_MOUSE_DBL_CLICK, RIGHT_MOUSE_TRPL_CLICK, RIGHT_MOUSE_PRESSED, RIGHT_MOUSE_RELEASED]

# Pressing backspace returns 8 on windows?
if platform == 'win32':
    KEY_BACKSPACE   = 8
# Adds support for 'delete/backspace' key on OSX
elif platform == 'darwin':
    KEY_BACKSPACE   = 127
else:
    KEY_BACKSPACE   = curses.KEY_BACKSPACE

