from input_parser import parse_input
import learn_exporter, moodle_exporter
from os import listdir

def get_single_file(dirpath):
    fs = [f for f in listdir(dirpath) if ("." in f)]
    if len(fs)==1:
        return dirpath + fs[0]
    return None

def learn_test(man_file="2nd_marker_example.md"):
    # choose file
    dpath = "input/"
    fpath = get_single_file(dpath)
    if not fpath:
        fpath = dpath+man_file

    # main
    quiz = parse_input(fpath)
    learn_exporter.export(quiz, "output/learn_import.txt")
    return quiz
    
def moodle_test(man_file="match_only.md"):
    # choose file
    dpath = "input/"
    fpath = get_single_file(dpath)
    if not fpath:
        fpath = dpath+man_file

    # main
    quiz = parse_input(fpath)
    moodle_exporter.export(quiz, "output/moodle_import.xml")
    return quiz

moodle_test()

print("finished")