"""
This file contains assorted general utility functions used by other
modules in the PyAIML package.
"""


def sentences(s):
    """Split the string s into a list of sentences."""
    if not isinstance(s, str):
        raise TypeError("s must be a string")
    pos = 0
    sentenceList = []
    l = len(s)
    while pos < l:
        try:
            p = s.index('.', pos)
        except ValueError:
            p = l + 1
        try:
            q = s.index('?', pos)
        except ValueError:
            q = l + 1
        try:
            e = s.index('!', pos)
        except ValueError:
            e = l + 1
        end = min(p, q, e)
        sentenceList.append(s[pos:end].strip())
        pos = end+1
    # If no sentences were found, return a one-item list containing
    # the entire input string.
    if len(sentenceList) == 0:
        sentenceList.append(s)
    return sentenceList

# Self test
if __name__ == "__main__":
    # sentences
    results = sentences("First.  Second, still?  Third and Final!  Well, not really")
    assert(len(results) == 4)
