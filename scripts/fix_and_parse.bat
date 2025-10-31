@echo off
cd /d "%~dp0\.."
echo Fixing encoding in precommit_errors.txt...
python scripts\fix_encoding.py
echo.
echo Now parsing errors...
python scripts\parse_precommit_errors.py
pause
