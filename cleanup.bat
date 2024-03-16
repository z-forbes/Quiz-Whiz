@echo off
setlocal

REM Deleting folders
rd /s /q "test_inputs"
rd /s /q "inputs"
rd /s /q "output"

REM Deleting file
del "test.py"

REM Deleting self
del "cleanup.bat"

echo Folders and file deleted successfully.

endlocal
