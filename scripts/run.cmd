@echo off
set "PYTHONPATH=%~dp0..\src"
python "%~dp0..\app\main.py" %*
