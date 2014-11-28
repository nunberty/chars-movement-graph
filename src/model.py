class NamedObject(object):
    def __init__(self, coordinates, names):
        self.coordinates = frozenset(coordinates)
        self.names = frozenset(names)

    def __repr__(self):
        return "NamedObject: {}, {}".format(str(self.coordinates), str(self.names))

    def __str__(self):
        return self.__repr__()

    def _create_set(self):
        ret = set()
        for l in self.names:
            ret.update(l)
        return ret

    def __hash__(self):
        return hash((self.coordinates, self.names))

    def __eq__(self, other):
        return other.coordinates == self.coordinates and other.names == self.names

class Person(NamedObject):
    def __repr__(self):
        return "Person: {}, {}".format(str(self.coordinates), str(self.names))

    def __str__(self):
        return self.__repr__()

class Location(NamedObject):
    def __repr__(self):
        return "Location: {},{}".format(str(self.coordinates), str(self.names))

    def __str__(self):
        return self.__repr__()
