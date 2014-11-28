import sys
import itertools
import collections

import nltk

from . import config

NamedThingBase = collections.namedtuple('BaseNamedThing', ['tokens', 'context'])

class NamedThing(NamedThingBase):
    def is_person(self):
        return classifier.has_person_words(self.tokens)

    def is_location(self):
        prep = _get_word_before(self.context, " ".join(self.tokens))

        return (classifier.has_locarion_words(self.tokens) or
                classifier.is_directional_preposition(prep))

class Entity(object):
    def __init__(self, name, position):
        self._names = [name]
        self._positions = [position]

    def is_same_thing(self, thing):
        thing_words = set(thing.tokens)
        my_words = {x for t in self._names for x in t.tokens}
        return bool(thing_words & my_words)

    def add_thing(self, thing, position):
        assert self.is_same_thing(thing)
        self._names.append(thing)
        self._positions.append(position)

    @property
    def is_person(self):
        return any(name.is_person() for name in self._names)

    @property
    def is_location(self):
        return any(name.is_location() for name in self._names)

    @property
    def canonical_name(self):
        return " ".join(max(self._names, key=lambda n: len(n.tokens)).tokens)

    def __str__(self):
        return self.canonical_name


def analyze(sents):
    named_things = [(n_s, thing)
        for n_s, sentence in enumerate(sents)
        for thing in _find_named_things(sentence)
    ]
    entities = _find_entities(named_things)
    return entities

def _find_entities(named_things):
    entities = set()
    for position, thing in named_things:
        for e in entities:
            if e.is_same_thing(thing):
                e.add_thing(thing, position)
                break
        else:
            entities.add(Entity(thing, position))
    return entities

def _find_named_things(sentence):
    tokens = nltk.word_tokenize(sentence)
    def is_cap(s): return s[0].isupper()
    for is_capital, g in itertools.groupby(tokens[1:], key=is_cap):
        if is_capital:
            group = tuple(g)
            if not classifier.has_stop_words(group):
                yield NamedThing(group, sentence)

def _get_word_before(string, substring):
    if substring in string:
        index = string.find(substring)
        if not index:
            return ""
        string = string[0:index].strip()
        return string.split()[-1]
    else:
        return ""

def _load_dictionary(dictionary_name):
    path = config.DICTIONARIES_DIR / "{}.txt".format(dictionary_name)
    with path.open() as f:
        return set(f.read().split())

class WordClassifier(object):
    def __init__(self):
        self._locations = _load_dictionary('locations')
        self._persons = _load_dictionary('persons')
        self._directionprep = _load_dictionary('directionprep')
        self._stop_words = _load_dictionary('stopwords')

    def is_person_word(self, word):
        return word.lower() in self._persons

    def has_person_words(self, words):
        return any(self.is_person_word(w) for w in words)

    def is_location_word(self, word):
        return word.lower() in self._locations

    def has_locarion_words(self, words):
        return any(self.is_location_word(w) for w in words)

    def is_stop_word(self, word):
        return word.lower() in self._stop_words

    def has_stop_words(self, words):
        return any(self.is_stop_word(w) for w in words)

    def is_directional_preposition(self, word):
        return word.lower() in self._directionprep

classifier = WordClassifier()
