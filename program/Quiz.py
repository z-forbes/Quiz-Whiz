# Quiz object created by parser and used by exporters.
class Quiz:
    def __init__(self):
        self.questions = []
        self.input_file = None

    def add_q(self, q):
        self.questions.append(q)

