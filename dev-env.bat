@echo off
echo Activating Python virtual environment...
call .venv\Scripts\activate.bat
set PYTHONPATH=src;%PYTHONPATH%
echo Virtual environment activated!
echo Python path includes src directory
cmd /k
