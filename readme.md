This program facilitates the creation of quiz questions for Moodle and Learn Ultra. 

It is run through the command line as follows:

`python3 main.py input [--moodle] [--learn] [--output OUTPUT] [--debug] [--no_colour] [--add_nums | --remove_nums]`

Where...

```
Required:
  input                         Path of input file/directory

At least one required:
  --moodle, -m                  Produce Moodle output.
  --learn, -l                   Produce Mearn output.

Independent options:
  --output OUTPUT, -o OUTPUT    Path of output directory. Default "output/".

  --debug, -d                   Show detailed error messages.

  --no_colour, -nc              Doesn't output colour to terminal.

Mutually exclusive options:
  --add_nums, -an               Adds question numbers to input file(s).
  --remove_nums, -rn            Undos action of --add_nums.
```


Input files are markdown files of the following format...
## Input File Structure
Files consist of questions separated by one or more blank lines:

```
[question1]

[question2]

[question3]
```

## Question Types
There are 6 different question types, each with a different format.

### Multiple Choice
In these questions, students are asked to select correct answers from a list. Although, there can be any number of *correct* answers, including zero, there must be at least 2 answers total for Learn to accept the question.

```
# Question Title
optional question description

- answer 1
second line of answer 1
- ^answer 2 (correct)
- ^answer 3 (correct)
second line of answer 3
- answer 4
```

### True/False
Although these can be equivalently expressed as multiple choice questions, they are more concisely written in as True/False questions. 
Note the boolean answer is case-insensitive.

```
# Question Title
optional question description

- false
```

### Numeric
Note that the square brackets are required around the threshold

```
# Question Title
optional question description

- answer [threshold]
```

### Cloze
Note that the number of blanks in the question and answer must be the same.

```
# Question Title with [] some [] blanks [].
optional question description

1. first blank
2. second blank
3. third blank
```

### Match
```
# Question Title
optional question description

- pair 1 first item///pair 1 second item
- pair 2 first item///pair 2 second item
- pair 3 first item///pair 3 second item
```

### Essay
Essay quesions do not have descriptions.
```
# Question Title
optional question placeholder
```

## Images
Images can be included in most questions, although Learn will reject images placed in certain locations. 
They can be either local or from the web. If local, images will be encoded in base 64 to be uploaded.

They are included as follows `![alt text](path_to_image)`

## Comments
Comments are included by starting a line with '//'.
