@ECHO off

python -m pip install -r requirements.txt -r requirements-dev.txt

set PYTHONPATH="%PYTHONPATH%:%CD%\randomizer"
python -c "import sysconfig; print(sysconfig.get_paths()['platlib'])" > .site_packages
for /f %%i in (.site_packages) do set SITE_PACKAGES=%%i

pyinstaller -w -p "%CD%\randomizer" -F -n randomizer -i ico\randomizer.ico --add-data "config/FE7.sav;config/FE7.sav" randomizer\__main__.py
