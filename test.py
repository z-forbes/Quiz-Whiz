from difflib import SequenceMatcher

def most_similar(original, comps, threshold=0.7):
    # input verification
    if comps==[]:
        return None
    
    # remove extensions
    original = original.split(".")[:-1][0] if "." in original else original
    
    # do comparisons
    ratios = [(SequenceMatcher(None, original, c.split(".")[:-1][0] if "." in c else c).ratio(), c) for c in comps] # [(ratio, comp_file)]
    print(ratios)
    m = max(ratios, key=lambda r: r[0])
    return m[1] if m[0]>=threshold else None


o = "appel.txt"
cs = ["papell.txt", "orange", "banana.txt"] 
print(most_similar(o, cs))