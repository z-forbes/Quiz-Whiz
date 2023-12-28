from Quiz import Quiz
from utils import *
import Question

# parses a file of the correct format
# returns Quiz object
# fpath: filepath of input file 
def parse_input(fpath):
    output = Quiz()

    f = open(fpath, "r")
    q_current = []
    for line in f:
        if line[0]=="#":
            if len(q_current)!=0:
                output.add_q(parse_question(q_current))
                q_current = []
        
        to_add = line
        if line[-1]=="\n":
            to_add = line[:-1]
        q_current.append(to_add)

    output.add_q(parse_question(q_current))
    return output


# parses a raw question from an input file
# q_lines: the raw lines relating to one question
# returns Question object
def parse_question(q_lines):
    tmp = split_on_blank(q_lines)
    pre_answers = remove_blanks(tmp[0])
    answers = fix_answers(remove_blanks(tmp[1]))

    q_class = find_q_class(answers) 
    parsed_answers = q_class.parse_answers(answers)

    output = q_class(answers=parsed_answers, question=get_line_content(pre_answers[0]))
    if len(pre_answers)>1:
        desc = ""
        for l in pre_answers[1:]:
            desc+=l+"\n"
        output.set_description(desc[:-1])

    # duplicate newlines in answer/question text because of markdown
    # L = "\n\n"
    # output.question = output.question.replace("\n", L)
    # output.description = output.description.replace("\n", L) 
    # output.set_answers_bodies([a.replace("\n", L) for a in output.get_answers_bodies()])
    return output


# fixes multiline answers
# example input: ["- hello", "world", "-learn", "ultra"]
# example output: ["-hello\nworld", "-learn\nultra"]
def fix_answers(answers):
    if answers == None or len(answers)==0:
        return answers
    output = []
    current = ""
    for a in answers:
        if a[0]=="-" or type(force_type(a[0]))==int: # a starts with - or int
            if current != "":
                current = current[:-1]
                output.append(current)
                current = ""
        current += a + "\n"

    current = current[:-1]
    output.append(current)
    return output



# returns the Question subclass of given raw answers
# answers: array of answers for a question
def find_q_class(answers): 
    for a in answers:
        if not type(force_type(a[0]))==int:
            break
        # only reached if no break
        return Question.Cloze

    for a in answers:
        if not "///" in a:
            break
        # only reached if no break
        return Question.Match

    return Question.Basic
