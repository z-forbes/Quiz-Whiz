from Quiz import Quiz
from utils import *
import Question

########
# MAIN #
########
# input: filepath of input file
# output: Quiz
def parse_input(fpath):
    output = Quiz()

    f = open(fpath, "r")
    q_current = []
    for line in f:
        if line[0]=="#": # first line of question
            if len(q_current)!=0: # if not first question
                output.add_q(parse_question(q_current))
                q_current = []
        
        to_add = line
        if line[-1]=="\n":
            to_add = line[:-1]
        q_current.append(to_add)

    output.add_q(parse_question(q_current)) # add final q
    return output

# input: array of relevant lines for one question from input file
# output: Question
def parse_question(q_lines):
    tmp = split_on_blank(q_lines)
    pre_answers = remove_blanks(tmp[0]) # question (and description)
    answers = shrink_answers(remove_blanks(tmp[1]))

    q_class = find_q_class(answers) 
    parsed_answers = q_class.parse_answers(answers)

    output = q_class(answers=parsed_answers, question=get_line_content(pre_answers[0]))
    if len(pre_answers)>1:
        desc = ""
        # format multiline description
        for l in pre_answers[1:]:
            desc+=l+"\n"
        output.set_description(desc[:-1]) # trailing \n removed

    return output


###########
# HELPERS #
###########

# deals with multiline answers
# example input: answers=["- hello", "world", "-learn", "ultra"]
# example output: ["-hello\nworld", "-learn\nultra"]
def shrink_answers(answers):
    if answers == None or len(answers)==0:
        return answers
    output = []
    current = ""
    for a in answers:
        if a[0]=="-" or type(force_type(a[0]))==int: # var a starts with - or int
            if current != "":
                current = current[:-1]
                output.append(current)
                current = ""
        current += a + "\n"

    current = current[:-1]
    output.append(current)
    return output

# finds the Question class (not QType) from its answers    
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

    if Question.Num.is_num(answers):
        return Question.Num
    
    return Question.Basic
