from program.input_parser import parse_input
import program.learn_exporter as learn_exporter
import program.moodle_exporter as moodle_exporter
from os import listdir
from program.utils import *

def shrink_answers(answers):
    if answers == None or len(answers)==0:
        return answers
    output = []
    current = ""
    for a in answers:
        if a[0]=="-" or type(force_type(a[0]))==int: # starts with - or int
            if current != "":
                current = current[:-1]
                output.append(current)
                current = ""
        current += a + "\n"

    current = current[:-1]
    output.append(current)
    return output

a = ["a\n\nb", "b\n\n\nc"]
a = shrink_answers(a)
print([e.replace("\n", "$") for e in a])