from program.input_parser import parse_input
import program.learn_exporter as learn_exporter
import program.moodle_exporter as moodle_exporter
import os
from program.utils import *
from program.Question import QType

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

count_lines()