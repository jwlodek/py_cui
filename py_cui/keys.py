"""Module containing constants and helper functions for dealing with keys.

@author:    Jakub Wlodek  
@created:   12-Aug-2019
"""

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
    
    return chr(key_num)


# Supported py_cui keys
KEY_ENTER       = get_ascii_from_char('\n')
# Escape character is ascii #27
KEY_ESCAPE      = 27
KEY_SPACE       = get_ascii_from_char(' ')
KEY_DELETE      = curses.KEY_DC
KEY_TAB         = get_ascii_from_char('\t')
KEY_UP_ARROW    = curses.KEY_UP
KEY_DOWN_ARROW  = curses.KEY_DOWN
KEY_LEFT_ARROW  = curses.KEY_LEFT
KEY_RIGHT_ARROW = curses.KEY_RIGHT
KEY_PAGE_UP     = curses.KEY_PPAGE
KEY_PAGE_DOWN   = curses.KEY_NPAGE
KEY_F1          = curses.KEY_F1
KEY_F2          = curses.KEY_F2
KEY_F3          = curses.KEY_F3
KEY_F4          = curses.KEY_F4
KEY_F5          = curses.KEY_F5
KEY_F6          = curses.KEY_F6
KEY_F7          = curses.KEY_F7
KEY_F8          = curses.KEY_F8
KEY_HOME        = curses.KEY_HOME
KEY_END         = curses.KEY_END
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

# Pressing backspace returns 8 on windows?
if platform == 'win32':
    KEY_BACKSPACE   = 8
else:
    KEY_BACKSPACE   = curses.KEY_BACKSPACE


ARROW_KEYS = [KEY_UP_ARROW, KEY_DOWN_ARROW, KEY_LEFT_ARROW, KEY_RIGHT_ARROW]