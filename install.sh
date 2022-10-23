#!/bin/bash

RELEASE=$(curl -s https://api.github.com/repos/highsaltlevels/randomizer/releases/latest | jq .assets[0].browser_download_url | tr -d \") 2>/dev/null 1>/dev/null
if [[ $? -ne 0 ]] ; then
    echo "jq not found or properly installed. Will attempt to parse without jq"
    RELEASE=$(curl -s https://api.github.com/repos/highsaltlevels/randomizer/releases/latest | grep "browser_download_url" | cut -d : -f 2,3 | tr -d \" | grep -i linux)
fi

echo "Pulling release $RELEASE"
mkdir ~/.local/bin 2>/dev/null 1>/dev/null
wget -O ~/.local/bin/randomizer $RELEASE 2>/dev/null
if [[ $? -ne 0 ]] ; then
    echo "Error trying to retrieve $RELEASE"
    exit 1
fi
chmod +x ~/.local/bin/randomizer

echo $PATH | grep -q "\.local/bin"
if [[ $? -ne 0 ]] ; then
    echo
    echo "WARNING:"
    echo "Did not find '.local/bin' in your PATH variable."
    echo "You can either append it to your PATH variable by running:"
    echo '"export PATH=${PATH}:.local/bin"'
    echo "Or you can just install the application as root with:"
    echo '"sudo mv ~/.local/bin/randomizer /usr/bin/randomizer"'
fi
