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
        output += export_f(question)+"\n\\\n\n"
    Progress.reset()    
    f = safe_open(fpath, "w", encoding="utf-8")
    f.write(output)
    f.close()

def mk_no_correct(fpath):
    f = safe_open(fpath, "r")
    contents = f.read()
    f.close()
    
    new_fpath = os.path.join(TMP_DIR(), "no_correct"+os.path.basename(fpath))
    f = safe_open(new_fpath, "w")
    f.write(re.sub(mk_correct("(.|\n)*?"),"", contents))
    f.close()
    return new_fpath


############### 
## EXPORTERS ## 
############### 
# each exporter exports 1 Question q

def MC_exporter(q):
    output = mk_title_desc(q)
    correct = []
    for i, a in enumerate(q.answers):
        output += f"\n{i+1}. {a.body}"
        if a.correct:
            correct.append(i+1)

    if correct==[]:
        correct="_None_"
    return output + mk_correct(str(correct)[1:-1])


def TF_exporter(q):
    correct = q.get_correct_as()
    if len(correct)!=1:
        error("not 1 correct answer in TF question")
    return mk_title_desc(q) + "\n1. True\n2. False\n" + mk_correct(correct[0].body)

def NUM_exporter(q):
    return mk_title_desc(q) + mk_correct(f"{q.get_answer()} ± {q.get_tolerance()}")

def ESSAY_exporter(q):
    return mk_title_desc(q) + "\n"

def MATCH_exporter(q):
    # no input validation. 
    # headers: [a,b], contents: [[a,b],[c,d],...,[e,f]]
    def mk_table(contents, headers=["Group 1", "Group 2"]):
        rows = [headers] + [["---", "---"]] + contents
        output = ""
        for r in rows:
            output += f"| {r[0]} | {r[1]} |\n"
        return "\n"+output
    
    # shuffles second elements (numbers here) in array [[a,1],[c,2],...,[e,3]]
    def shuffle_answers(ans):
        group_2 = [p[1] for p in ans]
        shuffle(group_2)
        return [[p[0], group_2[i]] for i, p in enumerate(ans)]


    output = mk_title_desc(q) + "\n"
    output += "Match each item in the first group to one in the second group:\n" + mk_table(shuffle_answers(q.answers))
    output += mk_correct("\n" + mk_table(q.answers))
    return output

def CLOZE_exporter(q):
    q.verify() # check number of blanks is same as number of answers
    
    # title and descripton
    question_old = q.question
    q.question = q.question.replace("[]", f"[{'&nbsp;'*5}]")
    output = mk_title_desc(q)
    q.question = question_old
    
    # options
    if len(q.answers)>1:
        output += "\n\nOptions:\n\n"
        as_copy = q.answers[:]
        shuffle(as_copy)
        for a in as_copy:
            output += f"- {a}\n"
    
    # correct
    correct = q.question
    for a in q.answers:
        correct = correct.replace("[]", f"**[{a}]**", 1)
    return output + mk_correct(correct)



###########
## UTILS ##
###########
# returns method in this file to use to export question
def get_exporter(qtype):
    return eval(str(qtype).split(".")[1]+"_exporter")
    

def mk_title_desc(question):
    output = f"### {question.question}"
    if question.description:
        output += f"\n{question.description}"

    return output

def mk_correct(answer):
    return f"\n\n<!-- correct start -->\nCorrect: {answer}\n<!-- correct end -->\n"