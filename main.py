from input_parser import parse_input
import learn_exporter, moodle_exporter


def learn_test():
    quiz = parse_input("input/2nd_marker_example.md")
    learn_exporter.export(quiz, "output/learn_import.txt")
    return quiz
    

def moodle_test():
    quiz = parse_input("input/match_only.md")
    moodle_exporter.export(quiz, "output/moodle_import.xml")

q = learn_test()
# moodle_test()

mcq = q.questions[0]
num = q.questions[7]
match = q.questions[4]

print(num.answers)
print(num.get_answer(), num.get_tolerance())

print("finished")