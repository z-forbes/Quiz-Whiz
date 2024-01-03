import xml.etree.ElementTree as ET
import main # TODO comment out
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
        # TODO question properties
        root.append(question_root)

    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0) # TODO what does this do
    tree.write(fpath, encoding="utf-8")

###############
## EXPORTERS ##
###############
# each exporter exports 1 Question q
    
def MC_exporter(q):
    q_root = init_question(q, "multichoice")
    for a in q.answers:
        q_root.append(init_answer(a.body, 100*a.correct)) # 100*True=100, 100*False=0
    return q_root

def TF_exporter(q):
    q_root = init_question(q, "truefalse")
    answer = q.get_correct_as()[0].body
    q_root.append(init_answer(str(answer).lower(), 100)) # correct
    q_root.append(init_answer(str(not answer).lower(), 0)) # incorrect
    return q_root

def NUM_exporter(q):
    q_root = init_question(q, "numerical")
    ans = init_answer(q.get_answer(), 100) # only one answer so frac=100
    
    # TODO is tolerance in text?
    # ans.append(text_inside("tolerance", q.get_tolerance()))

    tol = ET.SubElement(ans, "tolerance")
    tol.text = str(q.get_tolerance())
    
    q_root.append(ans)
    return q_root

def ESSAY_exporter(q):
    q_root = init_question(q, "essay")
    q_root.append(init_answer(" ", 0 )) # TODO defaults for essays?
    return q_root

def MATCH_exporter(q):
    q_root = init_question(q, "matching")
    for pair in q.answers:
        sub_q = text_inside("subquestion", pair[0])
        sub_q.append(text_inside("answer", pair[1]))
        q_root.append(sub_q)
    return q_root

def CLOZE_exporter(q):
    q_root = init_question(q, "cloze")
    # TODO https://docs.moodle.org/403/en/Embedded_Answers_(Cloze)_question_type#Format

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
def init_answer(ans_text, fraction, feedback=None):
    output = text_inside("answer", ans_text)
    output.set("fraction", str(fraction))
    # if feedback:
    #     output.append(text_inside("feedback", feedback))
    return output


# creates element: <e_name><text>content</text></e_name>
def text_inside(e_name, content):
    output = ET.Element(e_name)
    se = ET.SubElement(output, "text")
    se.text = str(content)
    return output


###########
## UTILS ##
###########

# returns method in this file to use to export question
def get_exporter(qtype):
    return eval(str(qtype).split(".")[1]+"_exporter")