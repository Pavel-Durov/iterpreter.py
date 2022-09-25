from src.kimchi_object import Object, HashKey, HashableObject


class Hash(HashableObject):
    def __init__(self, pairs):
        self.pairs = pairs

    def type(self):
        return Object.HASH_OBJ

    def inspect(self):
        out = "{"
        out += ", ".join([str(self.pairs[p].key) + " : " + str(self.pairs[p].value) for p in self.pairs])
        out += "}"
        return out

    def __str__(self):
        return self.inspect()

    def hash_key(self):
        # TODO: add hash of pairs
        # return HashKey(Object.HASH_OBJ, str(self.pairs))
        return HashKey(Object.HASH_OBJ, 1)
