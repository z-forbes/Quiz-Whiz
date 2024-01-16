import argparse
import os.path as path

from program.utils import *

from program.input_parser import parse_input
from program.learn_exporter import export as learn
from program.moodle_exporter import export as moodle

# TODO option to not conver to HTML to speed things up?


############
## PARSER ##
############
parser = argparse.ArgumentParser(description='Markdown to Moodle/Learn Ultlra converter!\nDocumentation: https://github.com/lewisforbes/ug5-project/blob/main/readme.md')

# required
parser.add_argument('input', type=str,
                    help='Path of input file/directory')

# optional
parser.add_argument('--output', '-o', type=str,
                    help='Path of output directory.')


# optional args to select output(s)
parser.add_argument('--moodle', '-m', action='store_true',
                    help='Produce Moodle output.')
parser.add_argument('--learn', '-l', action='store_true',
                    help='Produce Mearn output.')

# output modes
parser.add_argument('--debug', '-d', action='store_true',
                    help='Show detailed error messages.')

parser.add_argument('--no_colour', '-nc', action='store_true',
                    help='Do not output colour to terminal.')


args = parser.parse_args()

# ensure output format is specified
if not (args.learn or args.moodle):
    print(Fore.YELLOW)
    parser.error('No output format specified - include --moodle and/or --learn')

# output dirname validation
if args.output and (os.path.abspath("program") in os.path.abspath(args.output)):
    error("Cannot write output within program directory.")


########
# MAIN #
########
def main(args):
    # input
    if path.isdir(args.input):
        inputs = [path.join(args.input,f) for f in os.listdir(args.input) if ("." in f)]
    else:
        inputs = [args.input]
    quizzes = [parse_input(i) for i in inputs]

    # set all Quiz.input_file
    assert len(quizzes)==len(inputs)
    for i,q in enumerate(quizzes):
        q.input_file = path.basename(inputs[i])

    # display parse summary
    print("Parsed question totals:")
    for q in quizzes:
        print(f"'{q.input_file}': {len(q.questions)}")
    
    # output
    output_dir = "output"
    if args.output:
        output_dir = args.output
    if not path.isdir(output_dir):
        try:
            os.mkdir(output_dir)
        except:
            error(f"Unable to create directory '{output_dir}'")
        
    print() # newline in terminal
    for quiz in quizzes:
        print(f"Exporting {quiz.input_file}...")
        bname = path.basename(quiz.input_file)
        if args.learn:
            learn(quiz, path.join(output_dir, f"LEARN_{change_ftype(bname, 'txt')}"))
        if args.moodle:
            moodle(quiz, path.join(output_dir, f"MOODLE_{change_ftype(bname, 'xml')}"))

    print(f"{Fore.GREEN}Success!{Fore.RESET}")


## EXCECUTION STARTS HERE ##
if args.no_colour:
    Fore.YELLOW = ""
    Fore.RED = ""
    Fore.BLUE = ""
    Fore.GREEN = ""
    Fore.RESET = ""

# normal
if not args.debug:
    try:
        main(args)
    except SystemExit:
        pass # known error already displayed
    except:
        error("An unexpected error occured. Rerun with --debug flag for details.", show_progress=False)

# debug
if args.debug:
    success = False
    try:
        main(args)
        success = True
    except SystemExit:
        success = True # known error occured
    except:
        # print Utils.Progress details
        if Progress.current_action=="":
            print(f"{Fore.YELLOW}No progress update since start of excecution or since Utils.Progress reset.{Fore.RESET}\n")
        else:
            print(f"{Fore.YELLOW}Error occured when{Progress.current_action}.{Fore.RESET}\n")
    if not success:
        main(args) # show error in full