from input_parser import parse_input
import learn_exporter

quiz = parse_input("input/learn_example.md")
learn_exporter.export(quiz, "output/learn_test.txt")

