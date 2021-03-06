import sys
import itertools
import collections
import nltk
from nltk.metrics.distance import edit_distance

from . import config

def compare_names(first, second):
    return edit_distance(first, second) / min(len(first), len(second)) < 0.3

NamedThingBase = collections.namedtuple('BaseNamedThing', ['tokens', 'context'])

class NamedThing(NamedThingBase):
    def is_person(self):
        return classifier.has_person_words(self.tokens)

    def is_location(self):
        prep = _get_word_before(self.context, " ".join(self.tokens))

        return (classifier.has_location_words(self.tokens) or
                classifier.is_directional_preposition(prep) and
                not classifier.has_person_words(self.tokens))

class Entity(object):
    def __init__(self, name, position):
        self._names = [name]
        self._positions = [position]
        self._canonical_name = None
        self._is_person = False

    def is_same_thing(self, thing):
        def meaningful(x): return len(x) > 2
        thing_words = {x for x in thing.tokens if meaningful(x)}
        my_words = {x for t in self._names for x in t.tokens if meaningful(x)}
        return any(compare_names(a, b) for a in thing_words for b in my_words)

    def has_same_name(self, name):
        ret = any(compare_names(name, ' '.join(n.tokens))
            for n in self._names)
        if ret:
            self._canonical_name = name
            self._is_person = ret
        return ret

    def add_thing(self, thing, position):
        assert self.is_same_thing(thing)
        self._names.append(thing)
        self._positions.append(position)

    @property
    def is_person(self):
        return self._is_person or any(name.is_person() for name in self._names)

    @property
    def is_location(self):
        return any(name.is_location() for name in self._names)

    @property
    def canonical_name(self):
        if self._canonical_name:
            return self._canonical_name
        return " ".join(max(self._names, key=lambda n: len(n.tokens)).tokens)

    def __str__(self):
        return self.canonical_name

class Base():
    def __init__(self, entity):
        self._entity = entity

    def __str__(self):
        return self._entity.canonical_name

    @property
    def positions(self):
        return self._entity._positions

class Person(Base):
    pass

class Location(Base):
    pass

def analyze(names, sents):
    named_things = [(n_s, thing)
        for n_s, sentence in enumerate(sents)
        for thing in _find_named_things(sentence)
    ]
    entities = _find_entities(named_things)
    return _classify(names, entities)

def _classify_entity(names, entity):
    """ Returns tuple of persons and location lists """
    def is_person(entity):
        return any(entity.has_same_name(name) for name in names)
    is_person = is_person(entity)
    is_location = entity.is_location
    if is_person:
        return Person(entity)
    elif is_location:
        return Location(entity)
    else:
        return None

def _classify(names, entities):
    locations = []
    persons = []
    for e in entities:
        classified_entity = _classify_entity(names, e)
        if classified_entity:
            add_to = persons if isinstance(classified_entity, Person) else locations
            add_to.append(classified_entity)
    return persons, locations

def _find_entities(named_things):
    entities = []
    for position, thing in named_things:
        for e in entities:
            if e.is_same_thing(thing):
                e.add_thing(thing, position)
                break
        else:
            entities.append(Entity(thing, position))
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

    def has_location_words(self, words):
        return any(self.is_location_word(w) for w in words)

    def is_stop_word(self, word):
        return word.lower() in self._stop_words

    def has_stop_words(self, words):
        return any(self.is_stop_word(w) for w in words)

    def is_directional_preposition(self, word):
        return word.lower() in self._directionprep

classifier = WordClassifier()

def generate_schema(persons, locations):
    coordinates = []
    for p in persons:
        for l in locations:
            for i in set(p.positions) & set(l.positions):
                coordinates.append((i, l, p))

    return coordinates
