# Parses/validates input file and creates Quiz object.
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
        if len(line)>=len(COMMENT) and line[0:len(COMMENT)]==COMMENT:
            continue
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
    if remove_blanks(q_lines, space_is_blank=False)==[]:
        random_blank_lines() # ends termination

    NEWLINE = ">>>"
    Progress.parse_update()
    question = q_lines[0].replace(NEWLINE, "\n")
    if question[0]!="#":
        error(f"Input file must begin with '#' (for a question) or '{COMMENT}' (for a comment).") # called on first question only
    
    q_lines = [l.replace(NEWLINE, "\n") for l in q_lines[1:]]
    split_q = split_on_blank(q_lines, space_is_blank=False)
    desc_arr = split_q[0] # [desc_line1, desc_line2, ...] or []

    answers = shrink_answers(split_q[1])
    feedback = None
    try:
        if answers[-1][0:2] in FBACK_BULLETS:
            feedback = answers[-1]
            answers = answers[0:-1]
    except IndexError:
        pass

    verify_answers(answers) # ensures answers are of plausable format
    q_class = find_q_class(answers)
    parsed_answers = q_class.parse_answers(answers)

    if feedback:
        desc_arr.append(parse_feedback(feedback))

    q = q_class(answers=parsed_answers, question=get_line_content(question))
    # warn about FIB mistake
    if q.type!=Question.QType.CLOZE and Question.Cloze.BLANK_MARKER in q.question:
        warning(f"{Question.QType.CLOZE.value} blank marker '{Question.Cloze.BLANK_MARKER}' found in {q.type.value} question. Is this a mistake?")
    
    # description
    if len(desc_arr)>=1:
        desc = ""
        # format multiline description
        for l in desc_arr:
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
            random_blank_lines() # ends termination
            # error(f"Blank line found in answers/description. Add a space to include in output or '{COMMENT}' to hide in output.\nInclude --add_numbers flag to find erroneous question, check start/end of file for extra newlines.")
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

    is_match = len(answers)>0 # if answers==[], is_match=False
    for a in answers:
        if not Question.Match.SPLITTER in a:
            is_match = False
            break
    
    if is_match:
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
            # no space in answer
            not_enough_spaces(a) # ends termination   
        bullet = a.split(" ")[0]
        for p in patterns[:]:
            if not re.fullmatch(p, bullet):
                patterns.remove(p)
            if patterns==[]:
                # answer doesn't start with number or bullet
                not_enough_spaces(a) # ends termination
            if patterns==[num_pat] and bullet.split(".")[0]!=str(a_i+1):
                # answer starts with number but in the wrong order
                error(msg.format(a)+"\n(Numbers not sequential and starting from 1.)")

# parses feedback specified with utils.FEEDBACK_BULLETS
# input: ++ good job\n-- try again
# output: <<correctfeedback:good job; incorrectfeedback: try again>>
def parse_feedback(feedback):
    output = ""
    for fb in feedback.split("\n"):
        try:
            bullet = fb[0:2]
            if not bullet in FBACK_BULLETS:
                error(f"Feedback is poorly formatted: '{fb}'\nEach feedback item cannot be across multiple lines.")
            content = fb[2:].strip() # space not required between bullet and content
        except IndexError:
            error(f"Feedback is too short: {fb}.\nNote each feedback item cannot be across multiple lines.")
        
        output += f"{FBACK_BULLETS[bullet]}:{content};"
    return f"<<{output}>>"
