[← ← ←](../../../#installation)
# Detailed Installation Instructions
## 1. Ensure Python3 and Pip are installed.
Run ``python3 --version``. If you get an "comand not found" error, [install Python3](https://www.python.org/) and ensure it's on Path.

Run ``pip --version``. If you get an "comand not found" error, [install Pip](https://pypi.org/project/pip/) and ensure it's on Path.

## 2. [Download this repo](https://github.com/lewisforbes/ug5-project/archive/refs/heads/main.zip) and unzip the files.

## 3. Install dependencies
Open the unzipped folder in the terminal ([windows instructions](https://www.wikihow.com/Open-a-Folder-in-Cmd)). 

Run ``dir``. 
- If you see ``ug5-project-main``, run ``cd ug5-project-main && dir``. Go to next bullet.
- If you see ``main.py`` (among other things), proceed.

Run ``python3 main.py``. 

Follow instructions to install required dependencies, which include Pip packages and [Pandoc](https://pandoc.org/).[^1]
[^1]: Installing Pandoc this way installs it for use only in this program, not system wide. It is fully uninstalled by deleting the folder containing the program's code.

## 4. Check installation was succesful.
The program is installed when the following message occurs after runnning `python3 main.py`:

```
> python3 main.py
----------------------------------
All installation requirements met.
----------------------------------
Run `python3 main.py -h` for usage information.
```

