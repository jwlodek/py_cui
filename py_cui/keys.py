"""Module containing constants and helper functions for dealing with keys.

@author:    Jakub Wlodek, Ellis Wright (telday)
@created:   12-Aug-2019
"""

from sys import platform
from typing import Callable
import curses
import enum

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


class Key(enum.Enum):
    # KeysSupported py_cui keys
    ENTER       = get_ascii_from_char('\n')
    #Esccape character is ascii #27
    ESCAPE      = 27
    SPACE       = get_ascii_from_char(' ')
    DELETE      = curses.KEY_DC
    TAB         = get_ascii_from_char('\t')
    UP_ARROW    = curses.KEY_UP
    DOWN_ARROW  = curses.KEY_DOWN
    LEFT_ARROW  = curses.KEY_LEFT
    RIGHT_ARROW = curses.KEY_RIGHT
    PAGE_UP     = curses.KEY_PPAGE
    PAGE_DOWN   = curses.KEY_NPAGE
    F1          = curses.KEY_F1
    F2          = curses.KEY_F2
    F3          = curses.KEY_F3
    F4          = curses.KEY_F4
    F5          = curses.KEY_F5
    F6          = curses.KEY_F6
    F7          = curses.KEY_F7
    F8          = curses.KEY_F8
    HOME        = curses.KEY_HOME
    END         = curses.KEY_END
    A_LOWER     = get_ascii_from_char('a')
    B_LOWER     = get_ascii_from_char('b')
    C_LOWER     = get_ascii_from_char('c')
    D_LOWER     = get_ascii_from_char('d')
    E_LOWER     = get_ascii_from_char('e')
    F_LOWER     = get_ascii_from_char('f')
    G_LOWER     = get_ascii_from_char('g')
    H_LOWER     = get_ascii_from_char('h')
    I_LOWER     = get_ascii_from_char('i')
    J_LOWER     = get_ascii_from_char('j')
    K_LOWER     = get_ascii_from_char('k')
    L_LOWER     = get_ascii_from_char('l')
    M_LOWER     = get_ascii_from_char('m')
    N_LOWER     = get_ascii_from_char('n')
    O_LOWER     = get_ascii_from_char('o')
    P_LOWER     = get_ascii_from_char('p')
    Q_LOWER     = get_ascii_from_char('q')
    R_LOWER     = get_ascii_from_char('r')
    S_LOWER     = get_ascii_from_char('s')
    T_LOWER     = get_ascii_from_char('t')
    U_LOWER     = get_ascii_from_char('u')
    V_LOWER     = get_ascii_from_char('v')
    W_LOWER     = get_ascii_from_char('w')
    X_LOWER     = get_ascii_from_char('x')
    Y_LOWER     = get_ascii_from_char('y')
    Z_LOWER     = get_ascii_from_char('z')
    A_UPPER     = get_ascii_from_char('A')
    B_UPPER     = get_ascii_from_char('B')
    C_UPPER     = get_ascii_from_char('C')
    D_UPPER     = get_ascii_from_char('D')
    E_UPPER     = get_ascii_from_char('E')
    F_UPPER     = get_ascii_from_char('F')
    G_UPPER     = get_ascii_from_char('G')
    H_UPPER     = get_ascii_from_char('H')
    I_UPPER     = get_ascii_from_char('I')
    J_UPPER     = get_ascii_from_char('J')
    K_UPPER     = get_ascii_from_char('K')
    L_UPPER     = get_ascii_from_char('L')
    M_UPPER     = get_ascii_from_char('M')
    N_UPPER     = get_ascii_from_char('N')
    O_UPPER     = get_ascii_from_char('O')
    P_UPPER     = get_ascii_from_char('P')
    Q_UPPER     = get_ascii_from_char('Q')
    R_UPPER     = get_ascii_from_char('R')
    S_UPPER     = get_ascii_from_char('S')
    T_UPPER     = get_ascii_from_char('T')
    U_UPPER     = get_ascii_from_char('U')
    V_UPPER     = get_ascii_from_char('V')
    W_UPPER     = get_ascii_from_char('W')
    X_UPPER     = get_ascii_from_char('X')
    Y_UPPER     = get_ascii_from_char('Y')
    Z_UPPER     = get_ascii_from_char('Z')

    BACKSPACE   = 8 if platform == 'win32' else curses.KEY_BACKSPACE


class KeyMap(object):
    def __init__(self):
        self._bindings = dict()

    def bind_key(self, /, key: Key, *, definition: Callable=None, old: Key=None):
        """Binds a key to either a function or a key that previously had a binding

        Parameters
        ----------
        key : Key
            The new key to bind
        definition : Callable
            The function to bind
        old : Key
            The already bound key to bind to
        """
        if not isinstance(key, Key):
            raise ValueError(f"{key} is an invalid value for key")
        if old and old.value not in self._bindings:
            raise ValueError(f"{old} is not in the bindings list, cannot bind to it")
        if not old and not definition:
            raise ValueError(f"Either old or definition must be defined")
        if old and definition:
            raise ValueError(f"Cannot bind to both a key and a callable")
        if old:
            self._bindings[key.value] = self._bindings[old.value]
        else:
            self._bindings[key.value] = (definition, key)
    
    def execute(self, key: Key):
        if not isinstance(key, Key):
            raise ValueError(f"{key} is an invalid value for key")
        elif key.value not in self._bindings.keys():
            return

        self._bindings[key.value][0](self._bindings[key.value][1])

    def unbind(self, key: Key):
        """Unbinds a key from the map

        Parameters
        ----------
        key : Key
            The key to unbind
        """
        while key.value in self._bindings:
            del self._bindings[key.value]
    
    def __add__(self, value):
        if not isinstance(value, self.__class__):
            raise ValueError(f"Cannot add a KeyMap and {value.__class__} type")
        else:
            k = KeyMap()
            k._bindings = {**value._binings, **self._bindings}
            return k

class RawKeyMap(object):
    def __init__(self, char_range: range):
        self.char_range = char_range
        self.definition = None

    def add_definition(self, definition):
        self.definition = definition

    def execute(self, key: int):
        if key in self.char_range and self.definition:
            self.definition(key)
