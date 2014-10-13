import sys
import xml.etree.ElementTree as ET

def load_dictionary(filename):
    with open(filename) as dict_src:
        data = dict_src.read()

    ret = set(data.splitlines())
    return ret

tree = ET.parse("../datasets/1/1.fb2")

# I dislike this code
sents = []
for body in tree.find('body'):
    for p in body.findall('p'):
        if p.text:
            for s in p.text.split("."):
                for l in s.split("?"):
                    for k in l.split("!"):
                        sents.append(k.strip())

sents = enumerate(sents)

places = load_dictionary("../dictionaries/places.txt")
professions = load_dictionary("../dictionaries/professions.txt")

names = set()
points = set()
for s in sents:

    def is_proper(word):
        return word[0].isupper()

    words = s[1].split()
    if len(words) > 1:
        for pair in zip(words[1:], words[2:]):
            a = pair[0].strip(",-.':")
            b = pair[1].strip(",-.':")
            if len(a) > 1 and len(b) > 1:

                print(" ".join(t for t in [a, b]))
                if is_proper(a) and is_proper(b) and 'I' not in (a, b):

                    if a.lower() in places or b.lower() in places:
                        points.add((a, b))
                    else:

                        names.add((a, b))
                        names.add((a))
                        names.add((b))

#print(" ".join(str(t) for t in names))
#print(" ".join(str(p) for p in points))
