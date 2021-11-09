#!/bin/bash

PYTHONPATH=$(pwd)/randomizer coverage run --source=randomizer -m pytest tests
if [ $? != 0 ]; then
    echo "One or more tests failed!"
    exit 1
fi

coverage report -m
