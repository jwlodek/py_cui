#!/bin/bash

#Simple bash script for generating markdown documentation from docstrings

if [ ! -d "npdoc2md" ]
then
git clone https://github.com/jwlodek/npdoc2md
fi
cd npdoc2md
python3 npdoc2md.py -i ../../../py_cui -o ../../DocstringGenerated -s statusbar.py errors.py
cd ..
rm -rf npdoc2md
cd ../DocstringGenerated
rm Controls.md
rm Dialogs.md
mkdir Dialogs
mkdir Controls
mv Slider.md Controls/.
mv Filedialog.md Dialogs/.
mv Form.md Dialogs/.