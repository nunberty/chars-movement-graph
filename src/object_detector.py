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

    def dict_index(self):
        return 1

class Location(NamedObject):
    def __init__(self):
        NamedObject.__init__(self)

    def __str__(self):
        print("Location: ".join(str(self.names)))

    def dict_index(self):
        return 0

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
        for k, g in itertools.groupby(tokens,key = lambda s : s[0].isupper()):
            if k:
                ret.append(tuple(g))
        return ret

    propers = []
    for i, sent in sents:
        tokens = nltk.word_tokenize(sent)
        propers.extend(find_capitalize_words(tokens[1:]))
    return list(set(propers))

def analyze_propers(propers):
    return 1, 3

def gether_statistic(data, propers):
    pass

if __name__ == "__main__":
    with open("paths") as params_file:
        params = params_file.read().splitlines()

    i = 1
    datasets = []
    while(params[i]):
        datasets.append(params[i])
        i += 1
    i += 1

    dictionaries = []
    while(params[i] or i == len(params)):
        dictionaries.append(params[i].strip())
        i += 1

    filename = datasets[0]

    tree = parse_fb2(filename)
    sents = get_enumerate_sents(tree)

    places_dictionary = load_dictionary(dictionaries[0])
    personality_dictionary = load_dictionary(dictionaries[1])
    directionprep_dictionary = load_dictionary(dictionaries[2])

    propers = sorted(find_proper(sents), key = lambda x : -len(x))
    propers = [NamedObject(x) for x in propers]

    persons, locations = analyze_propers(propers)
    print("\n".join(str(y) for y in propers))
