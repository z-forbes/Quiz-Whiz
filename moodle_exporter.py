import xml.etree.ElementTree as ET
import Question

# TODO images
# TODO <text><![CDATA[ md_to_html(content) ]]><text>

##########
## MAIN ##
#####h####

# quiz: imported Quiz
# fpath: file path to export .xml file to
def export(quiz, fpath):
    root = ET.Element("quiz")
    for question in quiz.questions:
        export_f = get_exporter(question.type)
        question_root = export_f(question)
        question_root = add_properties(question_root, question.properties)
        root.append(question_root)

    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0) # makes file readable
    tree.write(fpath, encoding="utf-8")

###############
## EXPORTERS ##
###############
# each exporter exports 1 Question q
    
def MC_exporter(q):
    q_root = init_question(q, "multichoice")
    for a in q.answers:
        q_root.append(init_answer(a.body, 100*a.correct, a.properties)) # 100*True=100, 100*False=0
    return q_root

def TF_exporter(q):
    q_root = init_question(q, "truefalse")
    for a in q.answers:
        q_root.append(init_answer(str(a.body).lower(), 100*a.correct, a.properties))
    return q_root

# TODO properties
def NUM_exporter(q):
    q_root = init_question(q, "numerical")
    q_root.append(init_answer(q.get_answer(), 100, None)) # only one answer so frac=100

    q_root = add_properties(q_root, {"tolerance":q.get_tolerance})
    return q_root

def ESSAY_exporter(q):
    q_root = init_question(q, "essay")
    q_root.append(init_answer(" ", 0, None)) # TODO defaults for essays?
    return q_root

def MATCH_exporter(q):
    q_root = init_question(q, "matching")
    for pair in q.answers:
        sub_q = text_inside("subquestion", pair[0])
        sub_q.append(text_inside("answer", pair[1]))
        q_root.append(sub_q)
    return q_root

# TODO plan how Cloze questions will work
def CLOZE_exporter(q):
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

        split_q = q.question.split(Question.Cloze.BLANK_MARKER)
        # note: len(split_q) == len(brackets)+1
        output = ""
        for i in range(len(brackets)):
            output += split_q[i] + brackets[i]

        return output + split_q[-1] 
        
    q_root = ET.Element("question")
    q_root.set("type", "cloze")
    q_root.append(text_inside("name", "Cloze Question"))
    q_root.append(text_inside("questiontext", mk_questiontext(q)))
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
def init_answer(ans_text, fraction, properties):
    output = text_inside("answer", ans_text)
    if properties:
        if "fraction" in properties.keys():
            fraction = properties[fraction] # overwrite fraction default
        output = add_properties(output, properties)
    
    output.set("fraction", str(fraction))
    return output

# creates element: <e_name><text>content</text></e_name>
def text_inside(e_name, content):
    output = ET.Element(e_name)
    output.append(e_with_txt("text", content))
    return output

# returns new element with given tag and text
def e_with_txt(tag, text):
    output = ET.Element(tag)
    output.text = str(text)
    return output

# adds given properties to question/answer root and returns root
def add_properties(root, props):
    if not props:
        return root
    for pname, pval in props.items():
        if "feedback" in pname: # TODO verify heuristic
            root.append(text_inside(pname, pval))
        else:
            root.append(e_with_txt(pname, pval))
    return root



###########
## UTILS ##
###########

# returns method in this file to use to export question
def get_exporter(qtype):
    return eval(str(qtype).split(".")[1]+"_exporter")