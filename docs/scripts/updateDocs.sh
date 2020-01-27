#!/bin/bash

cd ../../..
if [ ! -d "py_cui-docs" ]
then
git clone https://github.com/jwlodek/py_cui-docs
else
rm -rf py_cui-docs
git clone https://github.com/jwlodek/py_cui-docs
fi
cd py_cui
python3 -m mkdocs build -d ../py_cui-docs
cd ../py_cui-docs
git add -A
DATE=$(date)
git commit -m "Update py_cui docs $DATE"
git push
