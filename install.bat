@ECHO off

ECHO "Fetching Release 0.0.2"
curl.exe -L https://github.com/HighSaltLevels/Randomizer/releases/download/0.0.2/randomizer-Win-x86_64.exe -o randomizer-Win-x86-64.exe 

ECHO "Setting configuration files"
MKDIR "%userprofile%\.config\randomizer" >NUL 2>&1
COPY "ico\randomizer.ico" "%userprofile%\.config\randomizer\" >NUL 2>&1
COPY "config\FE8.yml" "%userprofile%\.config\randomizer\" >NUL 2>&1

ECHO "done."
PAUSE
