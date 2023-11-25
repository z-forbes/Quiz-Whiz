from Quiz import Quiz
from utils import *

def parse_input(fpath):
    output = Quiz()

    f = open(fpath, "r")
    q_current = []
    for line in f:
        if line[0]=="#":
            if len(q_current)!=0:
                output.add_q(parse_question(q_current))
                q_current = []
                
        q_current.append(line.strip())


def parse_question(q_lines):
    tmp = remove_blanks(split_on_blank(q_lines))
    q_desc = tmp[0]
    answers = tmp[0]

    output = parse_answers(answers) # returns a Question
    output.question = q_desc[0]
    if len(q_desc)==2:
        output.description = q_desc[1]

    return output
    
def parse_answers(answers):
    if answers==None:
        return None
    
    # check for cloze
    for a in answers:
        if not type(force_type(a[0]))==int:
            break
        parse_cloze_answers(answers)
    
    for a in answers:
        if not "///" in a:
            break
        parse_match_answers(answers)

    parse_basic_answers(answers)



parse_input("input/example.md")
