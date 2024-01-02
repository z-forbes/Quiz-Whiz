import re
from utils import *

def format_code(html):
    PATTERN = '<div class="sourceCode"(.|\n)*?<\/div>'
    match = re.search(PATTERN, html)
    while match and ("\n" in match.group(0)):
        match_str = re.sub("<\/span>\n<span", "<\/span><br><span", match.group(0)) # add code newlines
        match_str = re.sub("<pre\n", "<pre ", match_str) # remove newline in pre tag

        html = sub_range(html, match_str, match.start(), match.end())
        match = re.search(PATTERN, html)

    return html

def format_not_code(md_str):
    code_is = [(m.start(), m.end()) for m in re.finditer("```(.|\n)*?```", md_str)]
    nl_to_dupe = []
    for nl_i in [m.start() for m in re.finditer("\n", md_str)]:
        dupe = True
        for code_i in code_is:
            if nl_i>=code_i[0] and nl_i<code_i[1]: # if nl_i within code block
                dupe = False
                break
        # nl_i is not within code block
        if dupe:
            nl_to_dupe.append(nl_i)
    for nl_i in sorted(nl_to_dupe, reverse=True):
        md_str = sub_range(md_str, "\n\n", nl_i, nl_i+1)
    return md_str



f = open("output/learn_import.txt")
md = f.read()
f.close()

mk_tmp_dir()
f = open(TMP_DIR()+"md.txt", "w")
f.write(format_not_code(md))
f.close()