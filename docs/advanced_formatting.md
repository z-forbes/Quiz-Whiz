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
#  Question Title
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
