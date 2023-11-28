from enum import Enum
from utils import *
from abc import ABC, abstractmethod
from Answer import Answer
import re

class QType(Enum):
    MC = 1
    TF = 2
    NUM = 3
    ESSAY = 4
    CLOZE = 5
    MATCH = 6

# abstract superclass
class Question(ABC):
    def __str__(self):
        t = self.type
        if t:
            t = str(t).split(".")[1]
        s = "Question type: {}".format(t)
        s += "\nQ: {}\nD: {}".format(self.question, self.description)

        if self.answers:
            a_len = len(self.answers)
        else:
            a_len = None

        a_term = "answers"
        if self.type == QType.CLOZE:
            a_term = "blanks"
        elif self.type == QType.MATCH:
            a_term = "pairs"
        return s + "\nNumber of {}: {}\n".format(a_term, a_len)

    def __init__(self, question=None, description=None, answers=None, type=None):
        self.question    = question
        self.description = description
        self.answers     = answers
        self.type        = type

    def set_question(self, s):
        self.question = s
        return self
    
    def set_description(self, s):
        self.description = s
        return self
    
    def set_answers(self, a):
        self.answers = a
        return self

    def set_type(self, t):
        self.type = t
        return self

    # parses answers
    @abstractmethod
    def parse_answers(lines):
        pass

class Basic(Question):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "type" in kwargs.keys():
            error("why was type passed into Question.Basic?")

        if "answers" in kwargs.keys():
            self.type = self.get_type()
        

    def set_answers(self, answers):
        super().set_answers(answers)
        self.type = self.get_type()

    def get_type(self):
        # check if type is ESSAY
        if not self.answers:
            return QType.ESSAY
        
        bodies = [a.body for a in self.answers]
        
        # check if type is TF
        if bodies==[True, False] or bodies==[False, True]:
            return QType.TF
        
        # type is either MC or NUM
        if False in [type(x)==int or type(x)==float for x in bodies]:
            return QType.MC
        
        return QType.NUM

    def get_correct_as(self):
        return [a for a in self.answers if a.correct]

    # static method
    def parse_answers(lines):
        def parse_answer(raw_answer):
            raw_answer = get_line_content(raw_answer)

            props_pattern = "<<(.*?)>>"
            props = re.findall(props_pattern, raw_answer)
            if len(props)==0:
                props = None
            else:
                props = remove_blanks(props[-1].split(" "))

            raw_answer = re.sub(props_pattern, "", raw_answer).strip()
            varname = re.findall("\*\*(.*)\*\*", raw_answer) # TODO what to call this var lol
            if len(varname)==0:
                correct = False
                body = raw_answer
            else:
                correct = True
                body = varname[0]

            return Answer(force_type(body), correct, props)

        if len(lines)==0:
            return None
        
        return [parse_answer(l) for l in lines]



class Cloze(Question):
    BLANK_MARKER = "[]"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type   = QType.CLOZE
        if "question" in kwargs.keys():
            self.question = re.sub("\[.*?\]", Cloze.BLANK_MARKER, self.question) # standardises all blanks

    def verify(self):
        if not self.answers or not self.question:
            error("Cloze.verify() called before Close.answers and/or Cloze.question set") 

        if len(self.answers) != self.question.count(Cloze.BLANK_MARKER):
            print(self.question)
            error("Cloze poorly formatted")

    # static method
    def parse_answers(lines):
        return [(get_line_content(l)) for l in lines]
    

class Match(Question):
    SPLITTER = "///"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = QType.MATCH

    # static method
    def parse_answers(lines):
        lines = [get_line_content(l) for l in lines]
        
        pairs = []
        for l in lines:
            current = l.split(Match.SPLITTER)
            if len(current)!=2:
                error("match answers poorly formatted")
            pairs.append(current)
        
        return pairs