from utils import *
from input_parser import parse_input

quiz = parse_input("input/example.md")

for q in quiz.questions:
    print(q)

