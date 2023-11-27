from Quiz import Quiz
from utils import *
import Question


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

    output.add_q(parse_question(q_current))
    
    return output


def parse_question(q_lines):
    tmp = split_on_blank(q_lines)
    pre_answers = remove_blanks(tmp[0])
    answers = remove_blanks(tmp[1])

    q_class = find_q_class(answers)
    parsed_answers = q_class.parse_answers(answers)

    # output = q_class().set_answers(parsed_answers).set_question(get_line_content(pre_answers[0]))
    output = q_class(answers=parsed_answers, question=get_line_content(pre_answers[0]))
    if len(pre_answers)==2:
        output.set_description(pre_answers[1])

    return output
    
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
