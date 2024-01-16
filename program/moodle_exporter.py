import xml.etree.ElementTree as ET
import program.Question
from program.utils import *

##########
## MAIN ##
#####h####

# quiz: imported Quiz
# fpath: file path to export .xml file to
def export(quiz, fpath):
    root = ET.Element("quiz")
    Progress.reset()
    for question in quiz.questions:
        Progress.export_update("Moodle")
        export_f = get_exporter(question.type)
        question_root = export_f(question)
        question_root = add_properties(question_root, question.properties)
        if question_root:
            root.append(question_root)

    Progress.reset()
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0) # makes file readable
    try: # can't use safe_open() since tree.write() required
        tree.write(fpath, encoding="utf-8")
    except:
        error("Could not write Moodle output.")

    # sub unnecessary escape characters
    f = safe_open(fpath, "r", encoding="utf-8")
    contents = f.read()
    f.close()
    f = safe_open(fpath, "w", encoding="utf-8")
    f.write(contents.replace("&lt;", "<").replace("&gt;", ">"))
    f.close()

    del_tmp_dir()


###############
## EXPORTERS ##
###############
# each exporter exports 1 Question q
    
def MC_exporter(q):
    q_root = init_question(q, "multichoice")
    for a in q.answers:
        q_root.append(init_answer(a.body, 100*a.correct, a.properties)) # 100*True=100, 100*False=0
    if len(q.get_correct_as())!=1:
        q_root = add_properties(q_root, {"single":"false"})
    return q_root

def TF_exporter(q):
    q_root = init_question(q, "truefalse")
    for a in q.answers:
        q_root.append(init_answer(str(a.body).lower(), 100*a.correct, a.properties, to_html=False))
    return q_root

def NUM_exporter(q):
    q_root = init_question(q, "numerical")
    q_root.append(init_answer(q.get_answer(), 100, None, to_html=False)) # only one answer so frac=100

    q_root = add_properties(q_root, {"tolerance":q.get_tolerance()})
    return q_root

def ESSAY_exporter(q):
    q_root = init_question(q, "essay")
    q_root.append(init_answer("", 0, None, to_html=False)) # TODO defaults for essays?

    return q_root

def MATCH_exporter(q):
    q_root = init_question(q, "matching")
    for pair in q.answers:
        sub_q = text_inside("subquestion", pair[0])
        sub_q.append(text_inside("answer", pair[1]))
        q_root.append(sub_q)
    return q_root

def CLOZE_exporter(q):
    if len(q.answers)==1:
        warning("Must have at least two choices in a cloze question. Skipping question.")
        return None
    # makes the question text (there's probs a better way to do this)
    def mk_questiontext(q):
        q.verify() # ensure len(q.answers) == blanks in question

        brackets = [] # brackets is final {}s in questiontext
        for q_blank_i in range(len(q.answers)): 
            bracket = "{1:MCS:" # MCS to shuffle answers
            for ans_i, a in enumerate(q.answers):
                if q_blank_i==ans_i: # correct answer
                    bracket+="=" 
                bracket += a + "~"
            bracket = bracket[:-1] + "}"
            brackets.append(bracket)

        split_q = q.question.split(program.Question.Cloze.BLANK_MARKER)
        # note: len(split_q) == len(brackets)+1
        output = ""
        for i in range(len(brackets)):
            output += split_q[i] + brackets[i]

        return output + split_q[-1] 
        
    q_root = ET.Element("question")
    q_root.set("type", "cloze")
    q_root.append(text_inside("name", "Cloze Question"))
    q_root.append(text_inside("questiontext", mk_questiontext(q), to_html=False))
    q_root.append(e_with_txt("shuffleanswers", 1)) # so answers aren't given in order
    return q_root


#################
## XML HEPLERS ##
#################

# creates question element with name/description
def init_question(q, type):
    output = ET.Element("question")
    output.set("type", type)
    output.append(text_inside("name", q.question))
    if q.description:
        output.append(text_inside("questiontext", q.description))
    return output

# creates answer with given answer text and fraction TODO and feedback if provided
def init_answer(ans_text, fraction, properties, to_html=True):
    output = text_inside("answer", ans_text, to_html)
    if properties:
        if "fraction" in properties.keys():
            fraction = properties[fraction] # overwrite fraction default
        output = add_properties(output, properties)
    
    output.set("fraction", str(fraction))
    return output

# to_html=True:  <e_name format="html"><text>md_to_html(content)</text></e_name>
# to_html=False: <e_name><text>content</text></e_name>
def text_inside(e_name, content, to_html=True):
    attrib = {}
    if to_html:
        content = "<![CDATA["+md_to_html(str(content))+"]]>"
        attrib["format"]="html"
    output = ET.Element(e_name, attrib=attrib)
    output.append(e_with_txt("text", content))
    return output

# returns new element with given tag and text
def e_with_txt(tag, text):
    output = ET.Element(tag)
    output.text = str(text)
    return output

# adds given properties to question/answer root and returns root
def add_properties(root, props):
    if not props or not root:
        return root
    for pname, pval in props.items():
        if "feedback" in pname: # TODO verify heuristic
            root.append(text_inside(pname, pval, to_html=False))
        else:
            root.append(e_with_txt(pname, pval))
    return root



###########
## UTILS ##
###########

# returns method in this file to use to export question
def get_exporter(qtype):
    return eval(str(qtype).split(".")[1]+"_exporter")