from program.Quiz import Quiz
from program.utils import *
import program.Question as Question

########
# MAIN #
########
# input: filepath of input file
# output: Quiz
def parse_input(fpath):
    output = Quiz()
    f = safe_open(fpath, "r")

    q_current = []
    Progress.reset()
    f_empty = True
    for line in f:
        if f_empty and line.strip()!="": # first condition for efficiency
            f_empty = False
        if line[0]=="#": # first line of question
            if len(q_current)!=0: # if not first question
                if q_current[-1]=="":
                    q_current = q_current[:-1] # remove final newline separating question
                output.add_q(parse_question(q_current))
                q_current = []
        
        to_add = line
        if line[-1]=="\n":
            to_add = line[:-1]
        q_current.append(to_add)

    if f_empty:
        error(f"Input file '{os.path.basename(fpath)}' is empty.")
    output.add_q(parse_question(q_current)) # add final q
    Progress.reset()              
    return output

# input: array of relevant lines for one question from input file
# output: Question
def parse_question(q_lines):
    Progress.parse_update()
    split_q = split_on_blank(q_lines, space_is_blank=False)
    pre_answers = split_q[0] # question (and description)
    if pre_answers[0][0]!="#":
        error("All questions must begin with '#'.") # called on first question only

    answers = shrink_answers(split_q[1])
    verify_answers(answers) # ensures answers are of plausable format
    q_class = find_q_class(answers)
    parsed_answers = q_class.parse_answers(answers)

    q = q_class(answers=parsed_answers, question=get_line_content(pre_answers[0]))
    if len(pre_answers)>1:
        desc = ""
        # format multiline description
        for l in pre_answers[1:]:
            desc+=l+"\n"
        q.set_description(desc[:-1]) # trailing \n removed
 
    return q


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
        if a=="":
            error("Blank line found in answers/description. Add a space to the line to include blank line.")
        if a[0]=="-" or type(force_type(a[0]))==int: # starts with - or int
            if current != "":
                current = current[:-1] # remove trailing newline
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


# checks every answer starts with bullet or every answer starts with list index (X.) 
# answers: raw, shrunk answers
# throws error if bad, does nothing if good
def verify_answers(answers):
    msg = 'Incorrect answer format...\n"{}"'
    num_pat = "[0-9]+\."
    patterns = ["-", num_pat]
    for a_i, a in enumerate(answers):
        if not " " in a:
            error(msg.format(a))
        bullet = a.split(" ")[0]
        for p in patterns[:]:
            if not re.match(p, bullet):
                patterns.remove(p)
            if patterns==[]:
                error(msg.format(a))
            if patterns==[num_pat] and bullet.split(".")[0]!=str(a_i+1):
                error(msg.format(a)+"\n(Numbers not sequential and starting from 1.)")