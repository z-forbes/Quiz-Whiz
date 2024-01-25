# Creates file to import to Learn from Quiz object
import program.Question
from program.utils import *
from random import shuffle
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
        Progress.export_update("Markdown")
        export_f = get_exporter(question.type)
        output += export_f(question)+"\n"
    Progress.reset()    
    f = safe_open(fpath, "w", encoding="utf-8")
    f.write(output)
    f.close()
    del_tmp_dir()

############### 
## EXPORTERS ## 
############### 
# each exporter exports 1 Question q

def MC_exporter(q):
    output = mk_title_desc(q)
    for i, a in enumerate(q.answers):
        output += f"\n{i+1}. {a.body}"
    correct = [(i+1) for i,a in enumerate(q.answers) if a.correct]
    if correct==[]:
        correct="None"
    else:
        correct=str(correct)[1:-1]
    output+= "\n" + correct_line(correct)
    return output


def TF_exporter(q):
    correct = q.get_correct_as()
    if len(correct)!=1:
        error("not 1 correct answer in TF question")
    return mk_title_desc(q) + "\n1. True\n2. False\n" + correct_line(correct[0].body)

def NUM_exporter(q):
    return mk_title_desc(q) + correct_line(f"{q.get_answer()} ± {q.get_tolerance()}")

def ESSAY_exporter(q):
    return mk_title_desc(q)

def MATCH_exporter(q):
    # no input validation. 
    # headers: [a,b], contents: [[a,b],[c,d],...,[e,f]]
    def mk_table(contents, headers=["Group 1", "Group 2"], correct=False):
        rows = [headers] + [["---", "---"]] + contents
        output = ""
        for r in rows:
            if correct:
                output += correct_marker() + " "
            output += f"| {r[0]} | {r[1]} |\n"
        return "\n"+output
    
    # shuffles second elements (numbers here) in array [[a,1],[c,2],...,[e,3]]
    def shuffle_answers(ans):
        group_2 = [p[1] for p in ans]
        shuffle(group_2)
        return [[p[0], group_2[i]] for i, p in enumerate(ans)]


    output = mk_title_desc(q) + "\n"
    output += "Match each item in the first group to one in the second group:\n" + mk_table(shuffle_answers(q.answers))
    output += correct_line("\n" + mk_table(q.answers, correct=True))
    return output


def CLOZE_exporter(q):
    q.verify() # check number of blanks is same as number of answers
    # TODO
    pass



###########
## UTILS ##
###########
# returns method in this file to use to export question
def get_exporter(qtype):
    return eval(str(qtype).split(".")[1]+"_exporter")
    

def mk_title_desc(question):
    output = f"### {question.question}"
    if question.description:
        output += f"\n{question.description}\n"
    return output

def correct_line(correct):
    return f"\n{correct_marker()}Correct: {correct}\n"

def correct_marker():
    return "<!---- correct! --->"