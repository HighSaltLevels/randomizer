#!/bin/bash

PYTHONPATH=$(pwd)/randomizer coverage run --omit=./randomizer/__main__.py --source=randomizer -m pytest tests
if [ $? != 0 ]; then
    echo "One or more tests failed!"
    exit 1
fi

coverage report -m
