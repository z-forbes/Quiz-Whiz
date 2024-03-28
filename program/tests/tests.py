import os
from os.path import join, exists
from time import time
from shutil import rmtree
import csv


def mk_file(t, n):
    with open(join(tests_dir, f"mcq_{t}.md"), "r") as f:
        q = f.read().strip()

    output = ""
    for _ in range(n):
        output += q + "\n\n"
    
    outpath = join(tests_dir, "tmp.md")
    with open(outpath, "w") as f:
        f.write(output.strip())
    
    return outpath


tests_dir = "program/tests"

for vle in ["learn", "moodle"]:
    print(vle)
    output = [["qcount", "basic time", "complex time"]]
    for qcount in range(1, 100, 2):
        print(qcount)
        row = [qcount]
        for t in ["basic", "complex"]:
            if exists("output"): rmtree("output") # remove all current files for fairness
            if exists("program/__pycache__"): rmtree("program/__pycache__") # remove all current files for fairness

            cmd = f"python3 main.py {mk_file(t, qcount)} --{vle} -q"
            s = time()
            os.system(cmd)
            dur = time() - s
            row.append(str(dur))
        output.append(row)

    with open(f"{vle}_timing_results.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(output)