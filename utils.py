from markdown import markdown
import re
import base64
import pypandoc
import os
from shutil import rmtree

def error(msg):
    raise Exception(msg)

def is_blank(s):
    return s==None or s.strip()==""

# input: array
# output: array with null/blank/whitespace-only elements removed
def remove_blanks(arr):
    output = []
    for x in arr:
        if not is_blank(x):
            output.append(x)
    return output

# input: array
# output: [array, array]
# explaination: splits on the first blank element in arr. if no blank found, returns None
def split_on_blank(arr):
    fst = []
    snd = []
    blank_found = False
    for x in arr:
        if is_blank(x) and not blank_found:
            blank_found = True
            continue # do not add first blank to any output
        
        if blank_found:
            snd.append(x)
        else:
            fst.append(x)
    return [fst, snd]

# input: string
# output: Bool/int/string where appropriate
def force_type(s):
    if s.lower() == "true":    
        return True
    if s.lower() == "false":
        return False
    
    try:
        return int(s)
    except:
        pass

    try:
        return float(s)
    except:
        return s
    

# removes a bullet/number from a string
def get_line_content(s):
    if not " " in s:
        print("utils.remove_bullet called with no space in string")
        return s
    content = s.split(" ")
    output = ""
    for x in content[1:]:
        output += x + " "
    output = output[:-1] # remove extra space at the
    return output


def file_str(x):
    if x!=None:
        return str(x)
    else:
        return ""
    
def md_to_html(md_str):
    def md_to_html_pandoc(md_str):
        # write tmp_md file
        dname = "tmp_files_for_pandoc_convert" 
        if not os.path.exists(dname):
            os.mkdir(dname)
        md_fpath = dname+"/tmp.md"
        f = open(md_fpath, "w")
        f.write(md_str)
        f.close()

        # use pandoc to create tmp html file
        html_fpath = dname+"/tmp.html"
        pypandoc.convert_file(md_fpath, 'html', format='md', outputfile=html_fpath)

        # read html file contents
        f = open(html_fpath, "r", encoding="utf-8")
        html = f.read()
        f.close()

        # delete tmp directory
        rmtree(dname)

        return html

    def img_to_b64(fpath):
        with open(fpath, "rb") as f:
            data = str(base64.b64encode(f.read()))
            return "data:image/;base64, {}".format(data.replace("'", "")[1:])
        
    # convert to HTML. pandoc deals with newlines weirdly.
    html = ""
    for line in md_str.split("\n"):
        html += md_to_html_pandoc(line)

    html = html.replace("\n", " ") # learn automatically includes newlines beacuse of seperate <p> tags

    # deal with images
    srcs = re.findall("src=\".*?\"", html)
    for src in srcs:
        if len(re.findall("https*?://", src))==0:
            # images are local
            im_path = re.findall("\".*\"", src)[0].replace("\"", "")
            html = html.replace(src, "src=\"{}\"".format(img_to_b64(im_path)))
    html = re.sub("<figcaption.*?<\/figcaption>", " ", html) # remove figcaption tag
    return html


CLEANR = re.compile('<.*?>') 
def remove_tags(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext