from input_parser import parse_input
import learn_exporter, moodle_exporter


def learn_test():
    quiz = parse_input("input/learn_example.md")
    learn_exporter.export(quiz, "output/learn_test.txt")

def moodle_test():
    quiz = parse_input("input/match_only.md")
    moodle_exporter.export(quiz, "delete.xml")

moodle_test()