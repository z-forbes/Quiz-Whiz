import re
def add_new_lines(md_str): # this function is wild (derogatory)
    new_lines = re.finditer("\n", md_str)
    to_dupe_is = []
    for nl in new_lines:
        dupe = True
        for c in re.finditer("```.*?```", md_str, re.DOTALL): # for some reason you have to do this every loop 
            if nl.start()>=c.start() and nl.start()<c.end(): # if newline is within code
                dupe = False
                break
        if dupe:
            to_dupe_is.append(nl.start())
        
    to_dupe_is.sort(reverse=True)
    for i in to_dupe_is:
        pre = md_str[0:i]
        post = md_str[i:]
        md_str = pre + "\n" + post

    return md_str


# a = re.finditer("\n", "bgkhg\nsgkhfsbgfdhg\ngjdsbds ```lhfdgvkfdb lfdjhbvfdlj vdj \n lhbf \n ``` fljf  \n ```vljv\n```jg")
# for sas in a:
#     print(sas.start())