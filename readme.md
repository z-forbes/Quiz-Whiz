This program facilitates the creation of quiz questions for Moodle and Learn Ultra.

![overview diagram](docs/overview.png)

# Installation
1. Ensure [Python3](https://www.python.org/) and [Pip](https://pypi.org/project/pip/) are installed.
2. [Download this repo](https://github.com/lewisforbes/ug5-project/archive/refs/heads/main.zip) and unzip the files.
3. Run `python3 main.py` to install dependancies.
4. If you see `All installation requirements met.` the program is ready to be used!

### [Detailed installation instructions here](docs/installation.md)

# Full Usage
- [Basic question formatting](docs/basic_formatting.md)
- [Advanced formatting](docs/advanced_formatting.md)
- [Complete usage details](docs/complete_usage.md)

# Basic Usage

At its simplist, the program is run through the command line as follows:

`python3 main.py path/to/input.md --VLE`

Where `--VLE` is either `--learn` or `--moodle`, and `path/to/input.md` is the filepath to an input file of the correct format.

An example input file might look something like:

```
# What colour is the sky at night?

- Pink
- ^Black
- Green

# Alan Turing was a famous pianist.

- False
```

Which creates the following questions on Learn:

![Example questions on Learn](docs/learn_example_qs.png)

