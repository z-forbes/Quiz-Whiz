from program.input_parser import parse_input
import program.learn_exporter as learn_exporter
import program.moodle_exporter as moodle_exporter
import os
from program.utils import *
from program.Question import QType
import markdown2, markdown
from timeit import default_timer as timer

def count_lines():
    files = ["main.py"]
    for f in os.listdir("program/"):
        if not "pycache" in f:
            files.append(os.path.join("program/", f))

    total = 0 
    for p in files:
        with open(p, "r") as f:
            total += len(f.readlines())
    print(total)

# count_lines()
    
def md_to_html_pandoc(md_str):
    # (over)write tmp_md file
    mk_tmp_dir() 
    md_fpath = TMP_DIR()+"/md_tmp.md"
    f = open(md_fpath, "w")
    f.write(md_str)
    f.close()

    # use pandoc to create tmp html file
    html_fpath = TMP_DIR()+"/html_tmp.html"
    pypandoc.convert_file(md_fpath, 'html', format='md', outputfile=html_fpath)

    # read html file contents
    f = open(html_fpath, "r", encoding="utf-8")
    html = f.read()
    f.close()

    return html

def pandoc_fr(md_str):
    return pypandoc.convert_text(md_str, "html", format='md')



md = '''
normal text 
code:
```python
def sum(a,b):
    return a+b
```
local image: ![alt text](inputs/images/dot.png)
web image: ![alt text](https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSai5tNIi1MsKHbPiTwr6-fM4eyCUWwJMZGB7xnQbAy3KNGmxnt){width=100px}
**bold text** *italic test*
'''
# with open("delete.html", "w") as f:
#     f.write(md_to_html_pandoc(md))
#     # f.write(markdown.markdown(md))
#     # f.wr_te(markdown2.markdown(md))

start = timer()
for _ in range(1000):
    markdown.markdown(md)
print(timer() - start)


start = timer()
for _ in range(1000):
    markdown2.markdown(md)
print(timer() - start)


start = timer()
for _ in range(1000):
    md_to_html_pandoc(md)
print(timer() - start)

start = timer()
for _ in range(1000):
    pandoc_fr(md)
print(timer() - start)
