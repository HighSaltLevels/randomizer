#!/bin/bash

PYTHONPATH=$(pwd)/randomizer
SITE_PACKAGES=$(python3 -c 'import sysconfig; print(sysconfig.get_paths()["platlib"])')
echo "Using site-packages location: ${SITE_PACKAGES}"

python3 -m pip install -r requirements.txt -r requirements-dev.txt
pyinstaller -w -F \
    -p "$(pwd)/randomizer" \
    -n randomizer \
    -i ico/randomizer.ico \
    --add-data "${SITE_PACKAGES}/qt_material/:qt_material/" \
    randomizer/__main__.py
