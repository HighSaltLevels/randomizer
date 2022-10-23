#!/bin/bash

ICON=$1
if [ -z ${ICON} ]; then
    echo "Usage:"
    echo "./tools/make_png.sh <Path-to-PNG-file>"
    exit 1
fi

python3 -c "f = open('${ICON}', 'rb'); data=f.read(); print('ICON = ', end=''); print(data); f.close()" > randomizer/icon.py
