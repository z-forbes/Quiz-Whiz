import re

def error(msg):
    raise Exception(msg)

def is_blank(s):
    s = s.strip()
    return s==None or s=="" or re.search("  *", s)==None

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