from input_parser import parse_input
import learn_exporter, moodle_exporter


def learn_test():
    quiz = parse_input("input/2nd_marker_example.md")
    learn_exporter.export(quiz, "output/learn_import.txt")
    

def moodle_test():
    quiz = parse_input("input/match_only.md")
    moodle_exporter.export(quiz, "output/moodle_import.xml")

learn_test()
moodle_test()

print("finished")