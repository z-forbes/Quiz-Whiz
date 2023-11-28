import Question
from utils import *

def arr_to_line(arr, s="\t"):
    output  = ""
    for e in arr:
        output += file_str(e)+s
    return output[:-len(s)]


def get_exporter(qtype):
    return eval(str(qtype).split(".")[1]+"_exporter")

def export(quiz, fpath):
    output = ""
    for question in quiz.questions:
        export_f = get_exporter(question.type)
        output += export_f(question)+"\n"
    
    f = open(fpath, "w")
    f.write(output)
    f.close()

def MC_exporter(q):
    CORRECT = "correct"
    INCORRECT = "incorrect"

    line = []
    if len(q.get_correct_as())==1:
        line.append("MC")
    else:
        line.append("MA") # TODO MA if 0 are correct??

    line.append(q.question) # TODO what to do with q.description?
    for a in q.answers:
        line.append(a.body)
        if a.correct:
            line.append(CORRECT)
        else:
            line.append(INCORRECT)

    return arr_to_line(line)

def TF_exporter(q):
    correct = q.get_correct_as()
    if len(correct)!=1:
        error("not 1 correct answer in TF question")
    return arr_to_line(["TF", q.question, correct[0].body])


def NUM_exporter(q): # TODO why is there no 'correct' in export file??
    if q.get_correct_as()!=[]:
        return MC_exporter(q)
    
    return arr_to_line(["NUM", q.question] + [a.body for a in q.answers])

def ESSAY_exporter(q):
    return arr_to_line(["ESS", q.question, q.description]) # TODO placeholder=q.description?

def MATCH_exporter(q):
    line = ["MAT", q.question]
    for pair in q.answers:
        line += pair
    return arr_to_line(line)

def CLOZE_exporter(q):
    q.verify() # check number of blanks is same as number of answers
    if len(q.answers)==1:
        return mk_FIB(q)
    else:
        return mk_FIB_PLUS(q)
    

def mk_FIB(q):
    return arr_to_line(["FIB", q.question.replace(Question.Cloze.BLANK_MARKER, "___"), q.answers[0]])

def mk_FIB_PLUS(q):
    if len(q.answers)>26:
        error("too many answers in fill in blanks question") # TODO can you get more than 26?

    ALPH = "abcdefghijklmnopqrstuvwxyz"
    BM = Question.Cloze.BLANK_MARKER
    new_q = q.question
    answers = []
    for i in range(new_q.count(BM)):
        BM_i = new_q.find(BM)
        pre_BM = new_q[0:BM_i]
        post_BM = new_q[BM_i+len(BM):]
        new_q = pre_BM + "[{}]".format(ALPH[i]) + post_BM
        answers += [ALPH[i], q.answers[i]]
    
    return arr_to_line(["FIB_PLUS", new_q] + answers)