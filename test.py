import re
from utils import *

class Cloze:
    def __init__(self):
        self.answers = ["a", "b", "c"]
        self.question = "word1 [] word2 [] word3 [] word4."

    def verify(self):
        return True
    
    BLANK_MARKER = "[]"


def mk_questiontext(q):
    assert q.verify() # ensure len(q.answers) == blanks in question

    brackets = [] # brackets is final {}s in questiontext
    for q_blank_i in range(len(q.answers)):  # there is probs a better way to do this
        bracket = "{1:MCS:" # MCS to shuffle answers
        for ans_i, a in enumerate(q.answers):
            if q_blank_i==ans_i: # correct answer
                bracket+="=" 
            bracket += a + "~"
        bracket = bracket[:-1] + "}"
        brackets.append(bracket)

    split_q = q.question.split(Cloze.BLANK_MARKER)
    # len(split_q) == len(brackets)+1
    output = ""
    for i in range(len(brackets)):
        output += split_q[i] + brackets[i]

    return output + split_q[-1] 




    



print(mk_questiontext(Cloze()))