# Gets arguments from user, runs program.
# Test user has required modules installed. Prompt them to install if not.
def init_new_modules():
    import tabulate
    import pypandoc
    import colorama

try:
    init_new_modules()
except ModuleNotFoundError:
    from sys import exit
    from os import system
    packages = ["tabulate", "pypandoc", "colorama"]
    yes = ["(y)es", "y", "yes"]
    no = ["(n)o", "n", "no"]
    while True:
        print("Missing required package(s).")
        user_in = input(f"Install following: {str(packages)[1:-1]}?\n[{yes[0]}/{no[0]}] > ")
        if user_in.lower() in yes:
            break
        if user_in.lower() in no:
            print("Exiting.")
            exit()
        print("Invalid input.")
    for p in packages:
        system(f"pip install {p}")
    print("Finished setup.")

# Begin normal excecution
import argparse
import os.path as path
import os

from program.utils import *

from program.input_parser import parse_input
from program.learn_exporter import export as learn
from program.moodle_exporter import export as moodle

from tabulate import tabulate

############
## PARSER ##
############
parser = argparse.ArgumentParser(description='Markdown to Moodle/Learn Ultlra converter!\nDocumentation: https://github.com/lewisforbes/ug5-project/blob/main/readme.md',
                                 epilog="Note: at least one of --moodle, --learn required.", formatter_class=argparse.RawDescriptionHelpFormatter)

# required
parser.add_argument('input', type=str,
                    help='path of input file/directory')

# optional
parser.add_argument('--output', '-o', type=str,
                    help='path of output directory (default "output/")')

# optional args to select output(s)
outputs = parser.add_argument_group()
outputs.add_argument('--moodle', '-m', action='store_true',
                    help='produce Moodle output')
outputs.add_argument('--learn', '-l', action='store_true',
                    help='produce Mearn output')

# output modes
parser.add_argument('--debug', '-d', action='store_true',
                    help='show detailed error messages')

parser.add_argument('--no_colour', '-nc', action='store_true',
                    help="doesn't output colour to terminal")

parser.add_argument('--quiet', '-q', action='store_true',
                    help='suppresses all non-error outputs')

# question numbers
nums = parser.add_mutually_exclusive_group()
nums.add_argument('--add_nums', '-an', action='store_true',
                    help='adds question numbers to input file(s)')

nums.add_argument('--remove_nums', '-rn', action='store_true',
                    help='undos action of --add_nums')


args = parser.parse_args()

# ensure output format is specified
if not (args.learn or args.moodle):
    print(Fore.YELLOW)
    parser.error('No output format specified - include --moodle and/or --learn')

# output dirname validation
if args.output and (os.path.abspath("program") in os.path.abspath(args.output)):
    error("Cannot write output within program directory.")

if args.quiet:
    Progress.quiet = True

########
# MAIN #
########
def main(args):
    # deals with --add_nums and --remove_nums
    def nums_flags(args, inputs):
        assert not (args.add_nums and args.remove_nums)
        qnum = comment() + " Question {} //\n"
        if args.add_nums:
            for fpath in inputs:
                q_i = 0
                new_lines = []
                f = safe_open(fpath, 'r')
                qnum_present = False
                for line in f:
                    if line[0]=="#":
                        q_i+=1
                        if not qnum_present:
                            new_lines.append(qnum.format(q_i))
                    new_lines.append(line)
                    qnum_present = line==qnum.format(q_i+1)

                f.close()
                f = safe_open(fpath, 'w')
                f.writelines(new_lines)
                f.close()
        if args.remove_nums:
            for fpath in inputs:
                new_lines = []
                f = safe_open(fpath, 'r')
                for line in f:
                    if re.match(qnum.format("[0-9]+"), line):
                        continue
                    new_lines.append(line)
                f.close()
                f = safe_open(fpath, 'w')
                f.writelines(new_lines)
                f.close()
   
    # input
    if path.isdir(args.input):
        inputs = [path.join(args.input,f) for f in os.listdir(args.input) if ("." in f)]
    else:
        inputs = [args.input]
    
    nums_flags(args, inputs)
    quizzes = []
    my_print("Parsing input(s)...", end=" ")
    for i in inputs:
        Progress.import_file = path.basename(i)
        quizzes.append(parse_input(i))
    Progress.import_file = None
    my_print("finished!")

    # set all Quiz.input_file
    assert len(quizzes)==len(inputs)
    for i,q in enumerate(quizzes):
        q.input_file = path.basename(inputs[i])

    # display parse summary
    my_print(make_parse_table(quizzes), end="")

    # output
    output_dir = "output"
    if args.output:
        output_dir = args.output
    if not path.isdir(output_dir):
        try:
            os.mkdir(output_dir)
        except:
            error(f"Unable to create directory '{output_dir}'")
        
    my_print() # newline in terminal
    for quiz in quizzes:
        my_print(f"\nExporting {quiz.input_file}...")
        bname = path.basename(quiz.input_file)
        if args.learn:
            learn(quiz, path.join(output_dir, f"LEARN_{change_ftype(bname, 'txt')}"))
        if args.moodle:
            moodle(quiz, path.join(output_dir, f"MOODLE_{change_ftype(bname, 'xml')}"))

    with_warnings = ""
    if Progress.warn_count!=0:
        s="s"
        if Progress.warn_count==1:
            s = ""
        with_warnings = f" with {Progress.warn_count} warning{s}"
    my_print()
    print(f"{Fore.GREEN}Finished{with_warnings}.{Fore.RESET}")


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
            my_print(f"{Fore.YELLOW}No progress update since start of excecution or since Utils.Progress reset.{Fore.RESET}\n")
        else:
            my_print(f"{Fore.YELLOW}Error occured when{Progress.current_action}.{Fore.RESET}\n")
    if not success:
        Progress.quiet = True # don't reshow program output
        main(args) # show error in full