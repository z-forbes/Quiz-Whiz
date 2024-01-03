from markdown import markdown
import re
import base64
import pypandoc
import os
from shutil import rmtree

#############
## STRINGS ##
#############

# input: string
# output: True iff input is None/blank/whitespace-only
def is_blank(s):
    return s==None or s.strip()==""

# removes HTML tags 
def remove_tags(raw_html):
  return re.sub("<.*?>", "", raw_html)

# removes first 'word' from string
# generally removes - / x. / #
def get_line_content(s):
    if not " " in s:
        print("utils.remove_bullet called with no space in string")
        return s
    content = s.split(" ")
    output = ""
    for x in content[1:]:
        output += x + " "
    output = output[:-1] # remove extra space at the end
    return output

# input: string
# output: output ready to be written to file
def file_str(x):
    if x:
        return str(x)
    else:
        return ""
    
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
        return s # returns string
    
# converts a markdown string to an HTML string
def md_to_html(md_str):
    # input: markdown string
    # output: raw pandoc conversion to html of input
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

    # input: filepath of local image
    # output: string of image encoded in base64
    def img_to_b64(fpath):
        with open(fpath, "rb") as f:
            data = str(base64.b64encode(f.read()))
            return "data:image/;base64, {}".format(data.replace("'", "")[1:])
    
    # input: html generated by pandoc
    # output: html with <br> instead of \n in code blocks
    def format_code(html):
        PATTERN = '<div class="sourceCode"(.|\n)*?<\/div>'
        match = re.search(PATTERN, html)
        while match and ("\n" in match.group(0)):
            match_str = re.sub("<\/span>\n<span", "</span><br><span", match.group(0)) # add code newlines
            match_str = re.sub("<pre\n", "<pre ", match_str) # remove newline in pre tag

            html = sub_range(html, match_str, match.start(), match.end())
            match = re.search(PATTERN, html)
        return html
    
    # input: raw markdown
    # output: markdown with newlines outside of code blocks duplicated 
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
    
    md_str = format_not_code(md_str)
    html = md_to_html_pandoc(md_str)
    html = format_code(html)
    html = html.replace("\n", " ") # all remaining newlines redundant

    ## Images ##
    srcs = re.findall("src=\".*?\"", html)
    for src in srcs:
        if len(re.findall("https*?://", src))==0:
            # images are local
            im_path = re.findall("\".*\"", src)[0].replace("\"", "")
            html = html.replace(src, "src=\"{}\"".format(img_to_b64(im_path)))
    html = re.sub("<figcaption.*?<\/figcaption>", " ", html) # remove figcaption tag

    return html

# replaces provided range in old_str with sub
def sub_range(old_str, sub_str, start, end):
    if end<start or start<0 or end>len(old_str):
        error("utils.sub_range() not being used as intended.") 
    start_str = old_str[0:start]
    end_str = old_str[end:]
    return start_str + sub_str + end_str


############
## ARRAYS ##
############

# input: array
# output: array with blank elements removed
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


############
## ERRORS ##
############

# throws an error (used for future flexibility)
def error(msg):
    raise Exception(msg)


###########
## FILES ##
###########
def TMP_DIR():
    return "temporary_directory_which_will_be_deleted!!!!!!!!/"

# creates directory TMP_DIR() if it doesn't exist
def mk_tmp_dir():
    if not os.path.exists(TMP_DIR()):
        os.mkdir(TMP_DIR())

def del_tmp_dir():
    rmtree(TMP_DIR())
