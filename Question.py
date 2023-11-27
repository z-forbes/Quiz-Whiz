from enum import Enum
from utils import *
from abc import ABC, abstractmethod

class QType(Enum):
    MC = 1
    TF = 2
    NUM = 3
    ESSAY = 4
    CLOZE = 5
    MATCH = 6

# abstract superclass
class Question(ABC):
    def __init__(self):
        self.question = None
        self.desc     = None
        self.type     = None

    def set_question(self, s):
        self.question = s
    
    def set_desc(self, s):
        self.desc = s

    # parses answers/pairs/blanks
    @abstractmethod
    def parse_answer(lines):
        pass

class Basic(Question):
    def __init__(self):
        super().__init__()
        self.answers = None

    def set_answers(self, answers):
        self.answers = answers
        self.type = self.get_type()

    def get_type(self):
        # check if type is ESSAY
        if not self.answers:
            return QType.ESSAY
        
        # check if type is TF
        if self.answers==[True, False] or self.answers==[False, True]:
            return QType.TF
        
        # type is either MC or NUM
        if False in [type(x)==int or type(x)==float for x in self.answers]:
            return QType.MC
        
        return QType.NUM

    # static method
    def parse_answer(lines):
        lines = remove_blanks(lines)
        if len(lines)==0:
            return None
        
        lines = [force_type(l[2:]) for l in lines]
        is_num = True
        for l in lines:
            if type(l)!=int or type(l)!=float:
                is_num=False
                break
        
        if is_num:
            return lines
        
        if lines == [True, False] or lines == [False, True]:
            return lines
        
        return [str(l) for l in lines]




        

class Cloze:
    def __init__(self):
        super.__init__()
        self.type   = QType.CLOZE
        self.blanks = None

    def set_blanks(self, blanks):
        self.blanks = blanks

    def verify(self):
        if not self.blanks or not self.question:
            error("Cloze.verify() called before Close.blanks and/or Cloze.question set") 

        if len(self.blanks) != len(self.question.count("[]")):
            error("Cloze poorly formatted")

    # static method
    def parse_answer(lines):
        lines = remove_blanks(lines)
        splitter = "///"
        pairs = []
        for l in lines:
            current = l.split(splitter)
            if len(current)!=2:
                error("cloze answers poorly formatted")
            pairs.append(current)
        return pairs


class Match:
    def __init__(self):
        super.__init__()
        self.type = QType.MATCH
        self.pairs = None

    def set_pairs(self, pairs):
        self.pairs = pairs

    # static method
    def parse_answer(lines):
        lines = remove_blanks(lines)
        splitter = "///"
        pairs = []
        for l in lines:
            current = l.split(splitter)
            if len(current)!=2:
                error("match answers poorly formatted")
            pairs.append(current)
        return pairs


