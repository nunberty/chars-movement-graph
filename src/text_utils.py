import xml.etree.ElementTree as ET
import nltk.data
import itertools

from paths import stop_path, english_pickle

def load_dictionary(filename):
    with open(filename) as dict_src:
        data = dict_src.read()

    ret = set(data.splitlines())
    return ret

def parse_fb2(source):
    return ET.parse(source)

def get_sents(tree):
    sent_detector = nltk.data.load(english_pickle)
    sents = []
    for body in tree.find('body'):
        for p in body.findall('p'):
            if p.text:
                sents.extend(sent_detector.tokenize(p.text.strip()))
    return sents

def find_capitalize_words(tokens):
    stopwords = load_dictionary(stop_path)
    ret = []
    for k, g in itertools.groupby(tokens,key=lambda s:s[0].isupper()):
        if k:
            group = tuple(g)
            if not any(word.lower() in stopwords for word in group):
                ret.append(group)
    return ret

def find_proper(sents):
    propers = []
    for i, sent in enumerate(sents):
        tokens = nltk.word_tokenize(sent)
        for p in find_capitalize_words(tokens[1:]):
            propers.append((i, p))
    return set(propers)

def get_word_before(string, substring):
    if substring in string:
        index = string.find(substring)
        if not index:
            return ""
        string = string[0:index].strip()
        return string.split()[-1]
    else:
        return ""

if __name__ == '__main__':
    sent = 'London is the capital of Great Britain.'
    word = get_word_before(sent, 'the UK')
