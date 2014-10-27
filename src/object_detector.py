import nltk.data
import xml.etree.ElementTree as ET
import itertools
import sys

class NamedObject(object):
    def __init__(self, name, coordinate):
        self.coordinates = set((coordinate,))
        self.names = set((name,))

    def union(self, another):
        self.names = self.names.union(another.names)
        self.coordinates = self.coordinates.union(another.coordinates)

    def intersects(self, another):
        return len(self._create_set().intersection(another._create_set())) > 0

    def words_set(self):
        return self._create_set()

    def __repr__(self):
        return "NamedObject: " + str(self.names)  + str(self.coordinates)

    def __str__(self):
        return self.__repr__()

    def _create_set(self):
        ret = set()
        for l in self.names:
            ret.update(l)
        return ret

class Person(NamedObject):
    def __init__(self, name=None, coordinate=None):
        self.coordinates = set()
        if coordinate:
            self.coordinates.update((coordinate,))
        self.names = set()
        if name:
            self.names.add((name,))

    def __repr__(self):
        return "Person: " + str(self.names) + str(self.coordinates)

    def __str__(self):
        return self.__repr__()

class Location(NamedObject):
    def __init__(self, name=None, coordinate=None):
        self.coordinates = set()
        if coordinate:
            self.coordinates.update((coordinate,))
        self.names = set()
        if name:
            self.names.add((name,))

    def __repr__(self):
        return "Location: " + str(self.names) + str(self.coordinates)

    def __str__(self):
        return self.__repr__()

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

def find_propers(sents, stopwords):

    def find_proper(sents):

        def find_capitalize_words(tokens):
            ret = []
            for k, g in itertools.groupby(tokens,key=lambda s:s[0].isupper()):
                if k:
                    group = tuple(g)
                    if not any(word.lower() in stopwords for word in group):
                        ret.append((i, group))
            return ret

        propers = []
        for i, sent in sents:
            tokens = nltk.word_tokenize(sent)
            propers.extend(find_capitalize_words(tokens[1:]))
        return set(propers)

    propers = [NamedObject(x, i) for i, x in sorted(find_proper(sents), key=lambda x:-len(x))]
    result = []

    while len(propers) > 0:
        named_object = propers.pop()
        for another in propers[1:]:
            if named_object.intersects(another):
                named_object.union(another)
                propers.remove(another)
        result.append(named_object)
    return result

def analyze(sents, dictionaries):

    places_dictionary = load_dictionary(dictionaries[0])
    personality_dictionary = load_dictionary(dictionaries[1])
    directionprep_dictionary = load_dictionary(dictionaries[2])
    stopwords = load_dictionary(dictionaries[3])

    named_objects = find_propers(sents, stopwords)

    print("\n".join(str(x) for x in named_objects))

    ret = []
    for named_object in named_objects:
        words_set = set(x.lower() for x in named_object.words_set())
        if len(words_set.intersection(personality_dictionary)) > 0:
            person = Person()
            person.names.update(named_object.names)
            person.coordinates.update(named_object.coordinates)
            ret.append(person)
            named_objects.remove(named_object)

        if len(words_set.intersection(places_dictionary)) > 0:
            location = Location()
            location.names.update(named_object.names)
            location.coordinates.update(named_object.coordinates)
            ret.append(location)
            named_objects.remove(named_object)

    return named_objects

def gether_statistic(data, propers):
    pass

if __name__ == "__main__":
    with open("paths") as params_file:
        params = params_file.read().splitlines()

    i = 1
    datasets = []
    while params[i]:
        datasets.append(params[i])
        i += 1
    i += 1

    dictionaries = []
    while params[i] or i == len(params):
        dictionaries.append(params[i].strip())
        i += 1

    filename = datasets[int(sys.argv[1])]

    tree = parse_fb2(filename)
    sents = get_enumerate_sents(tree)

    named_objects =  analyze(sents, dictionaries)

    print("\n".join(str(no) for no in named_objects))
