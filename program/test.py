# `python3 program/test.py` to check warnings work as expected
import subprocess
from shutil import rmtree
import os
from sys import exit

if os.path.basename(os.getcwd())=="program":
    input("This file should be ran from the base directory.\nPress enter to exit.")
    exit()

def check_warnings(f, w, vle="l"):
    B = f"python3 main.py -{vle} -q -o test_inputs/warnings/tmp_outputs test_inputs/warnings/"
    w = w if w>0 else "no"
    if not f"Finished with {w} warning" in str(subprocess.run(B+f, capture_output=True).stdout):
        subprocess.run(f"{B}{f}".replace("-q", ""))
        input(f"Failed for w={w}: {B+f}")
    else:
        print("Test passed.")

check_warnings("bad_prop.md", 2, vle="m")
check_warnings("bad_prop.md", 0, vle="l")
check_warnings("bad_prop.md", 0, vle="f html")
check_warnings("match_mc.md", 2)
check_warnings("cloze_choice.md", 1, vle="m")
check_warnings("cloze_choice.md", 0, vle="l")
check_warnings("cloze_choice.md", 0, vle="f html")
check_warnings("fib_as_f.md", 3)
check_warnings("cloze.md", 2)
check_warnings("accidental_essay.md", 2)
check_warnings("MC1A.md", 2, vle="l")
check_warnings("MC1A.md", 0, vle="m")
check_warnings("MC1A.md", 0, vle="f html")



rmtree("test_inputs/warnings/tmp_outputs")