from utils import *

class Answer:
    def __str__(self):
        c_marker = "✗"
        if self.correct:
            c_marker = "✓"
        
        return "({}) {}\nproperties: {}\n".format(c_marker, self.body, self.properties)
        

    def __init__(self, body, correct, properties):
        self.body = body        # string
        self.correct = correct  # boolean
        self.properties = properties  # ???
