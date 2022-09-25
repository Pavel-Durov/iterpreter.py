from src.kimchi_object import Object
from .kimchi_hash import kimchi_hash


class HashKey(Object):
    def __init__(self, type, value):
        self.t = type
        self.value = value

    def __eq__(self, other):
        if self.t == Object.INTEGER_OBJ or self.t == Object.BOOLEAN_OBJ or self.t == Object.STRING_OBJ:
            return self.value == other.value
        if self.t != other.type:
            return False

    def __hash__(self):
        if self.t == Object.INTEGER_OBJ or self.t == Object.BOOLEAN_OBJ or self.t == Object.STRING_OBJ:
            return kimchi_hash(str(self.value))
        raise Exception("unhashable type: " + self.t)

    def __str__(self):
        return str(self.value)

    def type(self):
        return self.t
