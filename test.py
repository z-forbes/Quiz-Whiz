# checks every answer starts with bullet or every answer starts with list index (X.) 
# answers: raw, shrunk answers
# throws error/not_enough_spaces() if bad, does nothing if good
def verify_answers(answers):
    msg = 'Answer poorly formatted: "{}"'
    
    # check bullet/space
    good = True
    for a in answers:
        # check answer starts with - or X.
        if not (re.match(NUM_PAT, a) or re.match(f"\{BULLET}", a)):
            error(msg.format(a) + f"\nAnswer must start with '{BULLET}' or '{PRETTY_NUM_PAT} '")
            
        # check there's a space after bullet
        if not (re.match(NUM_PAT+" ", a) or re.match(f"\{BULLET} ", a)):
            not_enough_spaces(a) # ends termination
        
        if a.split(" ")[0]!=BULLET:
            good = False
            break
    if good: return # every answer is well-formatted bullet

    # check number format/space
    for a_i, a in enumerate(answers):
        # check answer starts with - or X.
        if not (re.match(NUM_PAT, a) or re.match(f"\{BULLET}", a)):
            error(msg.format(a) + f"\nAnswer must start with '{BULLET}' or '{PRETTY_NUM_PAT} '")
            
        # check there's a space after bullet
        if not (re.match(NUM_PAT+" ", a) or re.match(f"\{BULLET} ", a)):
            not_enough_spaces(a) # ends termination

        bullet = a.split(" ")[0]
        if bullet!=f"{a_i+1}.": # NUM_PATTERN should probs be used
            # format invalid - find out how and inform
            if bullet==BULLET:
                error(f"A mix of bullet types has been used. Use all {BULLET} or {PRETTY_NUM_PAT}")
            else:
                error(msg.format(a)+f"\nNumbers must be sequential and starting from 1 - was expecting '{a_i+1}.' here.")  