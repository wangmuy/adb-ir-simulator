@echo off

set /p tvip="请输入电视端IP或串号: "
monkeyrunner.bat "%~dp0\ir.py" %tvip%