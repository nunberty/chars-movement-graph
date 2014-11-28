import sys
import paths
import itertools
import text_utils
import model

def reduce_propers(propers):
    copy = propers[:]
    result = set()

    while propers:
        named_object = propers.pop()
        for another in copy:
            if named_object.names.intersect(another.n):
                named_object.union(another)
        result.add(named_object)
    return list(result)

def find_propers(sents):
    propers = sorted(text_utils.find_proper(sents), key=lambda x:-len(x[1]))
    return [model.NamedObject({x[0]}, {x[1]}) for x in propers]

def analyze(sents, dictionaries):

    places_dictionary = text_utils.load_dictionary(dictionaries[0])
    personality_dictionary = text_utils.load_dictionary(dictionaries[1])
    directionprep_dictionary = text_utils.load_dictionary(dictionaries[2])

    named_objects = find_propers(sents)
    named_objects_copy = named_objects[:]

    ret = []
    for named_object in named_objects:
        words_set = {x.lower() for x in named_object.words_set()}
        things = []
        if words_set.intersection(personality_dictionary):
            things.append(model.Person())
        if words_set.intersection(places_dictionary):
            things.append(model.Location())

        for thing in things:
            thing.names.update(named_object.names)
            thing.coordinates.update(named_object.coordinates)
            ret.append(thing)
            named_objects.remove(named_object)

    for named_object in named_objects:
        sentences = [s for s in enumerate(sents) if s[0] in named_object.coordinates]
        for i, s in sentences:
            for name in named_object.names:
                if text_utils.get_word_before(s, " ".join(x for x in name)) in directionprep_dictionary:
                    thing = model.Location()
                    thing.names.update(named_object.names)
                    thing.coordinates.update(named_object.coordinates)
                    ret.append(thing)

    print("\n".join(str(x) for x in ret))

    return named_objects

def gether_statistic(data, propers):
    pass

if __name__ == "__main__":
    dictionaries = [paths.places_path, paths.profs_path, paths.preps_path]
    filename = paths.ds1

    tree = text_utils.parse_fb2(filename)
    sents = text_utils.get_sents(tree)

    named_objects = analyze(sents, dictionaries)
