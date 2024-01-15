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
                    help='Produce moodle output.')
parser.add_argument('--learn', '-l', action='store_true',
                    help='Produce learn output.')

parser.add_argument('--debug', '-d', action='store_true',
                    help='Show detailed error messages.')

# parser.add_argument('--clear-output', action='store_true', 
#                     help='Clear output folder before creating new output') 
args = parser.parse_args()

# ensure output format is specified
if not (args.learn or args.moodle):
    print(Fore.YELLOW)
    parser.error('No output format specified - include --moodle and/or --learn')


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
    # output dirname validation
    
    if args.output and path.basename(args.output)=="program":
        error("Output directory cannot be the same as program directory")
    if args.output:
        output_dir = args.output
    if not path.isdir(output_dir):
        try:
            os.mkdir(output_dir)
        except:
            error(f"Unable to create directory '{output_dir}'")


    # if args.clear_output:
    #     old_dir = path.join(output_dir, "old_outputs")
    #     if not path.exists(old_dir):
    #         os.mkdir(old_dir)
    #     old_fpaths = [path.join(output_dir,f) for f in os.listdir(output_dir) if not path.isdir(path.join(output_dir,f))] # paths of files in current output dir
        
    print()
    for quiz in quizzes:
        print(f"Exporting {quiz.input_file}...")
        if args.learn:
            learn(quiz, path.join(output_dir, f"LEARN_{path.basename(quiz.input_file)}"))
        if args.moodle:
            moodle(quiz, path.join(output_dir, f"MOODLE_{path.basename(quiz.input_file)}"))

    print(f"{Fore.GREEN}Success!{Fore.RESET}")


## EXCECUTION STARTS HERE ##
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
        if Progress.for_error()=="":
            print(f"{Fore.YELLOW}No progress update since start of excecution or since Utils.Progress reset.{Fore.RESET}\n")
        else:
            print(f"{Fore.YELLOW}Error occured when{Progress.for_error()}.{Fore.RESET}\n")
    if not success:
        main(args) # show error in full