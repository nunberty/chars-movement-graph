import sys
import paths
import text_utils

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
        return "NamedObject: {}, {}".format(str(self.names), str(self.coordinates))

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
        return "Person: {}, {}".format(str(self.names), str(self.coordinates))

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
        return "Location: {},{}".format(str(self.names), str(self.coordinates))

    def __str__(self):
        return self.__repr__()

def find_propers(sents):
    propers = [NamedObject(x, i) for i, x in sorted(text_utils.find_proper(sents), key=lambda x:-len(x))]
    result = []

    while propers:
        named_object = propers.pop()
        for another in propers[1:]:
            if named_object.intersects(another):
                named_object.union(another)
                propers.remove(another)
        result.append(named_object)
    return result

def analyze(sents, dictionaries):

    places_dictionary = text_utils.load_dictionary(dictionaries[0])
    personality_dictionary = text_utils.load_dictionary(dictionaries[1])
    directionprep_dictionary = text_utils.load_dictionary(dictionaries[2])

    named_objects = find_propers(sents)

    ret = []
    for named_object in named_objects:
        words_set = {x.lower() for x in named_object.words_set()}
        things = []
        if words_set.intersection(personality_dictionary):
            things.append(Person())
        if words_set.intersection(places_dictionary):
            things.append(Location())

        for thing in things:
            thing.names.update(named_object.names)
            thing.coordinates.update(named_object.coordinates)
            ret.append(thing)
            named_objects.remove(named_object)

    print("\n".join(str(x) for x in ret))

    return named_objects

def gether_statistic(data, propers):
    pass

if __name__ == "__main__":
    dictionaries = [paths.places_path, paths.profs_path, paths.preps_path]
    filename = paths.ds1

    tree = text_utils.parse_fb2(filename)
    sents = text_utils.get_enumerate_sents(tree)

    named_objects =  analyze(sents, dictionaries)
