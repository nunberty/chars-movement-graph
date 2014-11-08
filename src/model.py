class NamedObject(object):
    def __init__(self, name=None, coordinate=None):
        self.coordinates = set()
        self.names = set()
        if name:
            self.names.update((name,))
        if coordinate:
            self.coordinates.update((coordinate,))

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
    def __repr__(self):
        return "Person: {}, {}".format(str(self.names), str(self.coordinates))

    def __str__(self):
        return self.__repr__()

class Location(NamedObject):
    def __repr__(self):
        return "Location: {},{}".format(str(self.names), str(self.coordinates))

    def __str__(self):
        return self.__repr__()
