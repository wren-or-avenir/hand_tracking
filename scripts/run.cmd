@echo off
call conda activate hand_tracking
set "PYTHONPATH=%~dp0..\src"
python "%~dp0..\app\main.py" %*
