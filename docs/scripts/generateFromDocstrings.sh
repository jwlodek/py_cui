#!/bin/bash

#Simple bash script for generating markdown documentation from docstrings

if [ ! -d "markdoc" ]
then
git clone https://github.com/jwlodek/markdoc
fi
cd markdoc
python3 markdoc.py ../../py_cui/__init__.py ../DocstringGenerated/PyCUI.md
python3 markdoc.py ../../py_cui/colors.py ../DocstringGenerated/Colors.md
python3 markdoc.py ../../py_cui/grid.py ../DocstringGenerated/Grid.md
python3 markdoc.py ../../py_cui/widgets.py ../DocstringGenerated/Widgets.md
python3 markdoc.py ../../py_cui/widget_set.py ../DocstringGenerated/WidgetSet.md
python3 markdoc.py ../../py_cui/renderer.py ../DocstringGenerated/Renderer.md
python3 markdoc.py ../../py_cui/popups.py ../DocstringGenerated/Popups.md