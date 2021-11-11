@ECHO off

ECHO "Fetching Release 0.3.2"
curl.exe -L https://github.com/HighSaltLevels/Randomizer/releases/download/0.3.2/randomizer-Win-x86_64.exe -o randomizer.exe >NUL 2>&1 

ECHO "Fetching and setting configuration files"
MKDIR "%userprofile%\.config\randomizer" >NUL 2>&1
curl.exe -L https://github.com/HighSaltLevels/Randomizer/raw/master/config/spec.yml -o "%userprofile%\.config\randomizer\spec.yml" >NUL 2>&1
curl.exe -L https://github.com/HighSaltLevels/Randomizer/raw/master/config/FE7.yml -o "%userprofile%\.config\randomizer\FE7.yml" >NUL 2>&1
curl.exe -L https://github.com/HighSaltLevels/Randomizer/raw/master/config/FE8.yml -o "%userprofile%\.config\randomizer\FE8.yml" >NUL 2>&1
curl.exe -L https://github.com/HighSaltLevels/Randomizer/raw/master/config/FE7.sav -o "%userprofile%\.config\randomizer\FE7.sav" >NUL 2>&1
curl.exe -L https://github.com/HighSaltLevels/Randomizer/raw/master/ico/randomizer.ico -o "%userprofile%\.config\randomizer\randomizer.ico" >NUL 2>&1

ECHO "Done. You can start up the randomizer which is in this current directory."
PAUSE
