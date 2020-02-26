#!/bin/bash

#Simple bash script for generating markdown documentation from docstrings

if [ ! -d "npdoc2md" ]
then
git clone https://github.com/jwlodek/npdoc2md
fi
cd npdoc2md
python3 npdoc2md.py ../../../py_cui ../../DocstringGenerated -i statusbar.py errors.py