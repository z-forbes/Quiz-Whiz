@echo off
setlocal

REM Deleting folders
rd /s /q "test_inputs"
rd /s /q "inputs"
rd /s /q "output"
rd /s /q "example_outputs"
rd /s /q "program\__pycache__"

REM Deleting files
del "test.py"

REM Deleting self
del "cleanup.bat"

echo Folders and file deleted successfully.

endlocal
