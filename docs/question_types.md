This program can create 6 different question types:

- [Multiple Choice](#multiple-choice)
- [True/False](#truefalse)
- [Numeric](#numeric)
- [Multiple Choice](#multiple-choice) 

## <ins>Multiple Choice
In these questions, students are asked to select correct answers from a list. Although, there can be any number of *correct* answers, including zero, there must be at least 2 answers total for Learn to accept the question.

### Basic Example
```
# Which of the following are programming languages?

- ^Python
- French
- Swahili
- ^Haskell
```
### Full Skeleton
```
# Question Title
optional question description

- answer 1
second line of answer 1
- ^answer 2 (this is a correct answerr)
- ^answer 3 (this is a correct answer correct)
second line of answer 3
- answer 4
```

## <ins>True/False
Although these can be equivalently expressed as multiple choice questions, they are more concisely written in as True/False questions. 
The boolean answer is case-insensitive.

### Basic Example
```
# Tracklocross is a cycling discipline.

- True
```

### Full Skeleton
```
# Question Title
optional question description

- false
```

## <ins>Numeric
These have a numerical answer and a threshold outlining what counts as a correct answer.

### Basic Example
```
# How tall is is Mt. Everest in metres? (answers within 100m of correct height accepted)

- 8849 [100]

```

## <ins>Full Skeleton
```
# Question Title
optional question description

- answer [threshold]
```

## <ins>Fill in the Blanks
These require numbers, not dashes, as bullets.

### Basic Example
```
# The [] is the powerhouse of the [].

- mitochondria
- cell
```

### Complete Skeleton
```
# Question Title with [] some [] blanks [].
optional question description

1. first blank
2. second blank
3. third blank
```

## <ins>Match
### Basic Example
```
# Match the penguins to their homes:

- Fairy penguins///New Zealand
- Emperor penguins///Antarctica
- Magellanic///Patagonia
```


### Complete Skeleton
```
# Question Title
optional question description

- pair 1 first item///pair 1 second item
- pair 2 first item///pair 2 second item
- pair 3 first item///pair 3 second item
```

## <ins>Essay
Essay quesions have optional 'placeholders' instead of descriptions.
## <ins>Basic Example
```
# Write 400 words on the history of Speed Garage.
```

### Full Skeleton
```
# Question Title
optional question placeholder
```
