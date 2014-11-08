import sys
import paths
import itertools
import text_utils
import model

def find_propers(sents):
    propers = [model.NamedObject(x, i) for i, x in sorted(text_utils.find_proper(sents), key=lambda x:-len(x))]
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
            things.append(model.Person())
        if words_set.intersection(places_dictionary):
            things.append(model.Location())

        for thing in things:
            thing.names.update(named_object.names)
            thing.coordinates.update(named_object.coordinates)
            ret.append(thing)
            named_objects.remove(named_object)

    for named_object in named_objects:
        print("CO")
        print(named_object.coordinates)
        sentences = [s for s in sents if s[0] in named_object.coordinates]
        print(" ".join(str(x) for x in sentences))
        for i, s in sentences:
            for name in named_object.names:
                if text_utils.get_word_before(s, " ".join(x for x in name)) in directionprep_dictionary:
                    thing = Location()
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
    sents = text_utils.get_sents(tree)

    named_objects = analyze(sents, dictionaries)
