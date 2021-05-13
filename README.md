# Randomizer
Randomizer for specific Roms I want to hack

## How to Run
This randomizer supports both 64 bit Windows and Linux distrobutions. Unfortunately, I'm too poor and stubborn to afford a Mac, so I cannot compile for OS X. If you do want to build for MAC, you can try runnign the steps from the `DEVELOPING` section below. Since I use `pyinstaller` and `python`, it should be platform independent for the most part.

### Installing on Windows
1. [Download the source code](https://github.com/HighSaltLevels/Randomizer/archive/refs/tags/0.0.1.zip) and unzip it into any working directory that you want to use.

1. Open up a file explorer and navigate to the unzipped folder.

1. Double click on `install.bat` to pull down the binary file and set up your configuration files.

1. Move the binary (`randomizer-Win-x86_64.exe`) to a desired location to run this program from (like the Desktop).

1. To run, just double click the binary.

### Installing on Linux
1. Clone the repository with git using http or ssh

 - HTTP: `git clone https://github.com/HighSaltLevels/Randomizer.git`
 - SSH: `git clone git@github.com:HighSaltLevels/Randomizer.git`

1. `cd` into the project directory, and run `./install.sh`

1. The binary gets installed to `~/.local/bin` so if it is not in your `PATH` variable, you may want to append it or install it as `root` into `/usr/bin`

## Developing

The easiest way to run this locally is to create a python virtual environment, install the dependencies, and run the package directly.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 randomizer
```

If you would like to build your own binary, you can use `./build.sh` for Linux and `./build.bat` for Windows.
