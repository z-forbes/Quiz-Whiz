from program.input_parser import parse_input
import program.learn_exporter as learn_exporter
import program.moodle_exporter as moodle_exporter
from os import listdir
from program.utils import *


banned = "program"
user = "C:\\Users\\lewis\\Downloads\\ug5-project-main\\program\\results"
print(os.path.abspath(banned))
print(os.path.abspath(user))
print(os.path.abspath(banned) in os.path.abspath(user))