from program.input_parser import parse_input
import program.learn_exporter as learn_exporter
import program.moodle_exporter as moodle_exporter
from os import listdir
from program.utils import *

def verify_answers(answers):
    msg = "Incorrect title/answer format: {}"
    patterns = ["-", "[0-9]+\."]
    for a in answers:
        if not " " in a:
            error(msg.format(a))
        bullet = a.split(" ")[0]
        for p in patterns:
            if not re.match(p, bullet):
                patterns.remove(p)
            if patterns==[]:
                error(msg.format(a))


a = ["10. fjns dkjgnf", "2. geldfjgnfd", "3. dfjgndfgs", "4. glj dgdlg"]
verify_answers(a)