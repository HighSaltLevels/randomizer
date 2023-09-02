# Randomizer
Randomizer for specific Roms I want to hack. Currently supports
 - Fire Emblem 6
 - Fire Emblem 7
 - Fire Emblem 8

## Please Help Report Bugs

Check out out the [list of known issues](KNOWN_BUGS.md) to see if your issue is listed there. Also, have a look at this [list of strange behavior](STRANGE_BEHAVIOR.md) in case your issue is something caused by a known difference in behavior due to things changed by this randomizer. If you find any potential bugs, please raise an issue on this project and document it.

## How to Run
This randomizer supports both 64 bit Windows and Linux distrobutions. Unfortunately, I'm too poor and stubborn to afford a Mac, so I cannot compile for OS X. If you do want to build for MAC, you can try runnign the steps from the `DEVELOPING` section below. Since I use `pyinstaller` and `python`, it should be platform independent for the most part.

### Installation
1. [Go to the Releases page](https://github.com/HighSaltLevels/randomizer/releases) of this project.

1. Download the appropriate binary for your system.

The release contains a standalone binary so there is no need to install this or any other package. Just execute it :)

## Developing

### Running
The easiest way to run this locally is to create a python virtual environment, install the dependencies, and run the package directly.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 randomizer
```

### Testing
Assuming you've already created and activated a python virtual environment:
```bash
python3 -m pip install -r requirements-dev.txt
./run_tests.sh
```

### Building a Binary

Use `./build.sh` for Linux and `./build.bat` for Windows.

It's also worth noting that I use [qt-material](https://github.com/UN-GCPDS/qt-material) to build the stylesheets in the final binary, and I purposefully remove the `font-size` from `material.css.template` so that I can set my own variable font sizes. If you don't do this manually, then all of the labels will be a set size and they won't look like headers.
