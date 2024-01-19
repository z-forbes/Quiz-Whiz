# Quiz object created by parser and used by exporters.
class Quiz:
    def __init__(self):
        self.questions = []
        self.input_file = None

    def add_q(self, q):
        self.questions.append(q)

    # returns summary of questions: {QType:count}
    def question_summary(self):
        output = {}
        for q in self.questions:
            if q.type.value in output:
                output[q.type.value]+=1
            else:
                output[q.type.value]=1
        return output