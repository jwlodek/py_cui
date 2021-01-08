"""
The most basic possible use case for py_cui

@author:    Jakub Wlodek
@created:   12-Aug-2019
"""

# Import the lib
import py_cui

# create the CUI object. Will have a 3 by 3 grid with indexes from 0,0 to 2,2
root = py_cui.PyCUI(3, 3)

# Add a label to the center of the CUI in the 1,1 grid position
root.add_label('Hello py_cui!!!', 1, 1)

# Start/Render the CUI
root.start()
