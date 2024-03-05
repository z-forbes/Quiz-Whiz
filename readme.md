This program facilitates the creation of quiz questions for Moodle and Learn Ultra.

![overview diagram](docs/overview.png)

# Installation
1. Ensure [Python3](https://www.python.org/) and [Pip](https://pypi.org/project/pip/) are installed.
2. [Download this repo](https://github.com/lewisforbes/ug5-project/archive/refs/heads/main.zip) and unzip the files.
3. Run `python3 main.py` to install dependancies.
4. If you see `All installation requirements met.` the program is ready to be used!

### [Detailed installation instructions here](docs/installation.md)

# Full Usage Contents
- [Question formatting](docs/question_types.md)
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

Input files are markdown files of the following format...
## Input File Structure
Files consist of questions separated by one or more blank lines:

```
[question1]

[question2]

[question3]
```


## Additional Formatting
### Images
Images can be included in most questions, although Learn will reject images placed in certain locations. 
They can be either local or from the web. If local, images will be encoded in base 64 to be uploaded.

They are included as follows `![alt text](path_to_image){width=_px}`. Size information inside `{}` is optional, see the [Pandoc documentation](https://pandoc.org/MANUAL.html#extension-link_attributes) for details. 

### Comments
Comments are included by starting a line with '//'.

### Newlines
Where permitted, newlines are copied from markdown file to output. Newlines can also be added using `>>>`, useful when adding newlines to titles.

The following are equivalent:
```
#  Question Title
Description line 1
Description line 2
```
```
# Question Title
Description line 1>>>Description line 2
```
