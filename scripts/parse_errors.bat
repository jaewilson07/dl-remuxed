@echo off
cd /d "%~dp0\.."
python scripts\parse_precommit_errors.py
pause
