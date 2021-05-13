#!/bin/bash

PYTHONPATH=$(pwd)/randomizer

python3 -m pip install -r requirements.txt -r requirements-dev.txt
pyinstaller -F -i ico/randomizer.ico -n randomizer randomizer/__main__.py
