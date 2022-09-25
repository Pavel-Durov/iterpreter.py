from src.kimchi_object import Object, HashKey, HashableObject
from src.kimchi_object.kimchi_hash import kimchi_hash



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
        return HashKey(Object.HASH_OBJ, kimchi_hash(self.pairs))
