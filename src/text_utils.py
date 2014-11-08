import xml.etree.ElementTree as ET
import nltk.data
import itertools

from paths import stop_path

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
        stopwords = load_dictionary(stop_path)
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
