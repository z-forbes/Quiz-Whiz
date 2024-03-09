[← ← ←](../../../#full-usage)
# Advanced Formatting
## Images
Images can be included in most questions, although Learn will reject images placed in certain locations. 
They can be either local or from the web. If local, images will be encoded in base 64 to be uploaded.

They are included as follows `![alt text](path_to_image){width=_px}`. Size information inside `{}` is optional, see the [Pandoc documentation](https://pandoc.org/MANUAL.html#extension-link_attributes) for details. 

## Comments
Comments are included by starting a line with `:`.

## Newlines
Where permitted, newlines are copied from markdown file to output. Newlines can also be added using `>>>`, useful when adding newlines to titles.

The following are equivalent:
```
# Question Title
Description line 1
Description line 2
```
```
# Question Title
Description line 1>>>Description line 2
```

A blank line can only be inclded between questions or before answers start. To include more blank lines in answers, add a space or use `>>>`.

## Code
Code is included with the following syntax:
````
```python
def sum(a,b):
  return a+b
```
````

## Properties
Properties can be included in quesions or answers when exporting to the Moodle format. Including properties will have no effect when exporting to the Learn format.

Properties are included by adding `<<prop1:value; prop2;value>>` in title, description, or answer. This software performs very limited error checking on properties. See the [Moodle documentation](https://docs.moodle.org/403/en/Moodle_XML_format) for more information on valid properties.

As an example, below is an example multiple choice question from the Moodle documentation, followed by how it would be created using this software:

```   
<question type="multichoice">
  <name format="html">
    <text>Name of question</text>
  </name>
  <questiontext format="html">
    <text>What is the answer to this question?</text>
  </questiontext>
  <answer format="html" fraction="100">
    <text>The correct answer </text>
    <feedback>
      <text>Correct!</text>
    </feedback>
  </answer>
  <answer format="html" fraction="0">
    <text>A distractor </text>
    <feedback>
      <text>Ooops!</text>
    </feedback>
  </answer>
  <answer format="html" fraction="0">
    <text>Another distractor </text>
    <feedback>
      <text>Ooops!</text>
    </feedback>
  </answer>
  <shuffleanswers>1</shuffleanswers>
  <single>true</single>
  <answernumbering>abc</answernumbering>
</question>
```

```
# Name of question
What is the answer to this question?
<<shuffleanswers:1; single:true; answernumbering:abc>>

- ^The correct answer <<fraction:100; feedback:Correct!>>
- A distractor <<fraction:0; feedback:Ooops!>>
- Another distractor <<fraction:0; feedback:Ooops!>>
```
