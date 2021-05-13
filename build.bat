@ECHO off

python -m pip install -r requirements.txt -r requirements-dev.txt

set PYTHONPATH="%PYTHONPATH%:%CD%\randomizer"
pyinstaller -w -p "%CD%\randomizer" -F -n randomizer -i ico\randomizer.ico randomizer\__main__.py
