import xml.etree.ElementTree as ET

def get_exporter(qtype):
    return eval(str(qtype).split(".")[1]+"_exporter")

# creates element: <e_name><text>content</text></e_name>
def text_inside(e_name, content):
    output = ET.Element(e_name)
    se = ET.SubElement(output, "text")
    se.text = content
    return output

# creates question element with name/description
def init_question(q, type):
    output = ET.Element("question")
    output.set("type", type)
    output.append(text_inside("name", q.question))
    if q.description:
        output.append(text_inside("questiontext", q.description))
    return output


def export(quiz, fpath):
    root = ET.Element("quiz")
    for question in quiz.questions:
        export_f = get_exporter(question.type)
        root.append(export_f(question))

    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    tree.write(fpath, encoding="utf-8")


def MATCH_exporter(q):
    q_root = init_question(q, "matching")

    for pair in q.answers:
        sub_q = text_inside("subquestion", pair[0])
        sub_q.append(text_inside("answer", pair[1]))
        q_root.append(sub_q)
    
    return q_root
