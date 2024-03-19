[← ← ←](../../../#installation)
# Detailed Installation Instructions
## 1. Ensure Python3 and Pip are installed.
Run ``python3 --version``. If you get an "comand not found" error, [install Python3](https://www.python.org/) and ensure it's on Path.

Run ``pip --version``. If you get an "comand not found" error, [install Pip](https://pypi.org/project/pip/) and ensure it's on Path.

## 2. [Download this repo](https://github.com/lewisforbes/Quiz-Whiz/archive/refs/heads/main.zip) and unzip the files.

## 3. Install dependencies
Open the unzipped folder in the terminal ([windows instructions](https://www.wikihow.com/Open-a-Folder-in-Cmd)). 

Run ``python3 main.py``. 
If you get a ``No such file or directory`` error, you do not have the correct folder open in the terminal.

Follow instructions to install required dependencies:

- If the required Pip packages are not installed, the program will prompt you to install them. Type `yes` to proceed.
- If Pandoc[^1] is not installed, the program will ask you to install it. Type `yes` to proceed.

[^1]: Installing [Pandoc](https://pandoc.org/) this way installs it for use only in this program, not system wide. It is fully uninstalled by deleting the folder containing the program's code.


## 4. Check installation was succesful.
The program is installed when the following message occurs after runnning `python3 main.py`:

```
> python3 main.py
----------------------------------
All installation requirements met.
----------------------------------
Run `python3 main.py -h` for usage information.
```

