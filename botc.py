import re

def clean(s: str):
    return re.sub("[-' ]", "", s.lower())