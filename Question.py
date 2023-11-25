from enum import Enum
from utils import error
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
        if not self.answers:
            error("Basic.get_type() called while Basic.answers==None")

        # check if type is ESSAY
        if not self.answers:
            return QType.ESSAY
        
        # check if type is TF
        is_TF = True
        for x in self.answers:
            if type(x)!=bool:
                is_TF=False
                break
        if is_TF:
            return QType.TF
        
        # type is either MC or NUM
        if False in [type(x)==int or type(x)==float for x in self.answers]:
            return QType.MC
        else:
            return QType.NUM

    # static method
    def parse_answer(lines):
        print("here")

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

class Match:
    def __init__(self):
        super.__init__()
        self.type = QType.MATCH
        self.pairs = None

    def set_pairs(self, pairs):
        self.pairs = pairs

