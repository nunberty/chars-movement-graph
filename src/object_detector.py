import sys
import nltk.data
import xml.etree.ElementTree as ET
import itertools

class NamedObject(object):
    def __init__(self):
        self.names = []

    def is_disjoint(self, another):
        pass

    def add(self, name):
        self.names.append(name)

class Person(NamedObject):
    def __init__(self):
        NamedObject.__init__(self)

    def __str__(self):
        print("Person: ".join(str(self.names)))

class Location(NamedObject):
    def __init__(self):
        NamedObject.__init__(self)

    def __str__(self):
        print("Location: ".join(str(self.names)))

def load_dictionary(filename):
    with open(filename) as dict_src:
        data = dict_src.read()

    ret = set(data.splitlines())
    return ret

def parse_fb2(source):
    return ET.parse(source)

def get_enumerate_sents(tree):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sents = []
    for body in tree.find('body'):
        for p in body.findall('p'):
            if p.text:
                sents.extend(sent_detector.tokenize(p.text.strip()))

    return enumerate(sents)

def find_proper(sents):

    def find_capitalize_words(tokens):
        ret = []
        for t in tokens:
            for k, g in itertools.groupby(tokens,key = lambda s : s[0].isupper()):
                if k:
                    ret.append(tuple(g))
        return ret;

    propers = []
    for i, sent in sents:
        tokens = nltk.word_tokenize(sent)
        propers.extend(find_capitalize_words(tokens[1:]))
    return list(set(propers))

def analyze_propers(propers):
    return 1, 3

def gether_statistic(data, propers):
    pass

# Will be script parameter
filename = "../datasets/1/1.fb2"

tree = parse_fb2(filename)
sents = get_enumerate_sents(tree)

places_dictionary = load_dictionary("../dictionaries/places.txt")
personality_dictionary = load_dictionary("../dictionaries/professions.txt")

propers = sorted(find_proper(sents), key = lambda x : -1 * len(x))

persons, locations = analyze_propers(propers)
print("\n".join(str(y) for y in propers))
