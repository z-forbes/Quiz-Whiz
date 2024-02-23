# Creates file to import to Learn from Quiz object
import program.Question
from program.utils import *
# could make a copy of quiz and convert everything to html
# TODO can't import MC/MA questions with only one answer


##########
## MAIN ##
##########
# quiz: Quiz object
# fpath: output filepath
def export(quiz, fpath):
    Progress.reset()
    output = ""
    for question in quiz.questions:
        Progress.export_update("Learn")
        export_f = get_exporter(question.type)
        q_to_add = export_f(question)
        if q_to_add: # skip question if none 
            output += q_to_add +"\n"
    Progress.reset()    
    with safe_open(fpath, "w", encoding="utf-8") as f:
        f.write(output)
    del_tmp_dir()


############### 
## EXPORTERS ## 
############### 
# each exporter exports 1 Question q

def MC_exporter(q):
    if len(q.answers)==1:
        warning(f"Learn does not accept {program.Question.QType.MC.value} questions with one answer only.\n{Fore.RED}Skipping question.")
        return None
    CORRECT = "correct"
    INCORRECT = "incorrect"

    line = []
    if len(q.get_correct_as())==1:
        line.append("MC")
    else:
        line.append("MA") # TODO MA if 0 are correct??

    line.append(mk_qtext(q)) 
    for a in q.answers:
        line.append(md_to_html(a.body))
        if a.correct:
            line.append(CORRECT)
        else:
            line.append(INCORRECT)

    return arr_to_line(line)

def TF_exporter(q):
    correct = q.get_correct_as()
    if len(correct)!=1:
        raise Exception("Not 1 correct answer in TF question")
    return arr_to_line(["TF", mk_qtext(q), str(correct[0].body).lower()])

def NUM_exporter(q):
    return arr_to_line(["NUM", mk_qtext(q)] + [q.get_answer(), q.get_tolerance()])

def ESSAY_exporter(q):
    if q.description:
        placeholder = [md_to_html(q.description)]
    else:
        placeholder = []

    return arr_to_line(["ESS", md_to_html(q.question)] + placeholder)

def MATCH_exporter(q):
    answers = []
    for pair in q.answers:
        answers += pair
    return arr_to_line(["MAT", mk_qtext(q)] + [md_to_html(e) for e in answers])

def CLOZE_exporter(q):
    q.verify() # check number of blanks is same as number of answers
    joined_answers = str(q.answers)[1:-1] # slice removes brackets
    if ("\\n" in joined_answers) or has_formatting(joined_answers): # both True: "\\n" in str(["\n"]), not "\n" in str(["\n"])
        warning(f"Non-plaintext (or newline) found in {program.Question.QType.CLOZE.value} answers.\nLearn does not accept HTML here so check results are as expected.")

    if len(q.answers)==1:
        return mk_FIB(q)
    else:
        return mk_FIB_PLUS(q)

# Cloze Helpers #
# used for questions with one blank
def mk_FIB(q):
    old_q = q.question
    q.question = q.question.replace(program.Question.Cloze.BLANK_MARKER, "___")
    output = arr_to_line(["FIB"]+[mk_qtext(q), q.answers[0].replace("\n", " ")])
    q.question = old_q
    return output

# used for questions with multiple blanks
def mk_FIB_PLUS(q):
    if len(q.answers)>26:
        error("Too many answers in fill in blanks question, Learn accepts a max of 26.") # TODO can you get more than 26?

    ALPH = "abcdefghijklmnopqrstuvwxyz"
    BM = program.Question.Cloze.BLANK_MARKER
    new_q = mk_qtext(q)
    answers = []
    for i in range(new_q.count(BM)):
        BM_i = new_q.find(BM)
        pre_BM = new_q[0:BM_i]
        post_BM = new_q[BM_i+len(BM):]
        new_q = pre_BM + f"[{ALPH[i]}]" + post_BM
        answers += [ALPH[i], q.answers[i].replace("\n", " "), None] # None adds extra tab

    return arr_to_line(["FIB_PLUS", new_q] + answers)



###########
## UTILS ##
###########
# example input: arr=["a", 2, "c"], s="*"
# example output: "a*2*c"
def arr_to_line(arr, s="\t"):
    output  = ""
    for e in arr:
        output += file_str(e)+s # file_str(None)->""
    return output[:-len(s)] # removes trailing s

# returns method in this file to use to export question
def get_exporter(qtype):
    return eval(str(qtype).split(".")[1]+"_exporter")

# combines question title and description to be exported
# q: Question
def mk_qtext(q):
    output = q.question
    if q.description:
        output += "\n"+q.description
    return md_to_html(output)
    