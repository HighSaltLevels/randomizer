@ECHO off

ECHO "Fetching Release 0.4.1"
curl.exe -L https://github.com/HighSaltLevels/Randomizer/releases/download/0.4.1/randomizer-Win-x86_64.exe -o randomizer.exe >NUL 2>&1 

ECHO "Done. You can start up the randomizer which is in this current directory."
PAUSE
