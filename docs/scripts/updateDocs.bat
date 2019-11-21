@echo OFF

cd ..\..\..
if exist py_cui-docs goto DOCSEXIST
git clone https://github.com/jwlodek/py_cui-docs
:DOCSEXIST
cd py_cui
git pull
py -m mkdocs build -d ..\py_cui-docs
cd ..\py_cui-docs
git add -A
git commit -m "Update py_cui docs %date%"
git push