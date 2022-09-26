from rpython.rlib.jit import purefunction, hint


class Environment():
    def __init__(self, outer=None):
        self.store = {}
        self.outer = outer

    def get(self, name):
        if name in self.store:
            return self.store[name]
        elif self.outer is not None:
            return self.outer.get(name)
        return None

    def set(self, name, value):
        self.store[name] = value
        return value


class SelfLikeMap(object):
    def __init__(self):
        self.attribute_indexes = {}
        self.other_maps = {}

    @purefunction
    def get_index(self, name):
        return self.attribute_indexes.get(name, -1)

    @purefunction
    def new_map_with_additional_attribute(self, name):
        if name not in self.other_maps:
            newmap = SelfLikeMap()
            newmap.attribute_indexes.update(self.attribute_indexes)
            newmap.attribute_indexes[name] = len(self.attribute_indexes)
            self.other_maps[name] = newmap
        return self.other_maps[name]


EMPTY_MAP = SelfLikeMap()


class SelfLikeObjEnvironment(Environment):
    def __init__(self, outer=None):
        self.outer = outer
        self.map = EMPTY_MAP
        self.storage = []

    def get(self, name):
        map = hint(self.map, promote=True)
        index = map.get_index(name)
        if index != -1:
            return self.storage[index]
        elif self.outer is not None:
            return self.outer.get(name)
        return None

    def set(self, name, value):
        map = hint(self.map, promote=True)
        index = map.get_index(name)
        if index != -1:
            self.storage[index] = value
            return
        self.map = map.new_map_with_additional_attribute(name)
        self.storage.append(value)

