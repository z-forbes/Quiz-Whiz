from program.input_parser import parse_input
import program.learn_exporter as learn_exporter
import program.moodle_exporter as moodle_exporter
import os
from program.utils import *
from program.Question import QType
import markdown2, markdown
from timeit import default_timer as timer

def count_lines():
    files = ["main.py"]
    for f in os.listdir("program/"):
        if not "pycache" in f:
            files.append(os.path.join("program/", f))

    total = 0 
    for p in files:
        with open(p, "r") as f:
            total += len(f.readlines())
    print(total)

# count_lines()
    


# os.system("pandoc --version")
# subprocess.run('pandoc --version', check=True, shell=True)
# subprocess.run('freespace', check=True)

# parses feedback specified with utils.FEEDBACK_BULLETS
# input: ++ good job\n-- try again
# output: <<correctfeedback:good job; incorrectfeedback: try again>>
def parse_feedback(feedback):
    output = ""
    for fb in feedback.split("\n"):
        try:
            bullet = fb[0:2]
            if not bullet in FBACK_BULLETS:
                error(f"Feedback is poorly formatted: '{fb}'\nEach feedback item cannot be across multiple lines.")
            content = fb[2:].strip() # space not required between bullet and content
        except IndexError:
            error(f"Feedback is too short: {fb}.\nnote Each feedback item cannot be across multiple lines.")
        
        output += f"{FBACK_BULLETS[bullet]}:{content};"
    return f"<<{output}>>"


print(parse_feedback("++ good job\n-- try again"))