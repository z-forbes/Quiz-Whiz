# https://python-patterns.guide/gang-of-four/singleton/
from os.path import exists
from datetime import datetime
import re

class Logger(object):
    _instance = None
    output = None
    logging = False

    FULL = "console_full.html"
    RECENT = "console_recent.html"

    def __new__(cls, heading=None, content=None):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls.logging = True
        if heading:
            cls.add_heading(cls, no_col(heading))
        if content:
            cls.add_content(cls, no_col(content))
        return cls._instance

    def add_heading(cls, h):
        if not cls.output:
            cls.output = f"## {h}"
        else:
            cls.output += f"\n\n## {h}"

    def add_content(cls, c):
        if c!="\n":
            c = c.replace("\n", "\\\n")
        cls.output += f"\n{c}"
    
    def export(cls):
        from pypandoc import convert_text
        cls.output = cls.output.replace("\n\\", "\n").replace("|\\", "|").replace("- - - - - - - \\", "- - - - - - -") # lazy but it works
        html = convert_text(cls.output, "html", "md")
        with open(cls.RECENT, "w") as f:
            f.write(html)
        
        old = ""
        if exists(cls.FULL):
            with open(cls.FULL, "r", encoding='utf-8') as f:
                old = f.read()
        with open(cls.FULL, "w", encoding='utf-8') as f:
            f.write(f"<h1>Timestamp: {datetime.now()}</h1>\n\n"+html + old)
        print(f"Log files {cls.FULL} and {cls.RECENT} updated.")


## HELPER ##
# removes any Fore.COLOUR info from string
def no_col(s):
        return re.sub('\x1B\[[0-?]*[ -/]*[@-~]', '' , s)