#!/bin/bash

PYTHONPATH=$(pwd)/randomizer

python3 -m pip install -r requirements.txt -r requirements-dev.txt
pyinstaller -w -F \
    -p "$(pwd)/randomizer" \
    -n randomizer \
    -i ico/randomizer.ico \
    randomizer/__main__.py
