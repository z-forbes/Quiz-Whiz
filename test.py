from utils import *
# import main
import re

# q = main.learn_test()
# print([a.properties for a in q.questions[0].answers])


props_pattern = "<<(.*?)>>"
a = "- ^question!! <<a:1;b:fjhsljkngsljfn ldjfhsd;>>"
props = get_props(a)
print(props==None)
for k in props:
    print(k, props[k])