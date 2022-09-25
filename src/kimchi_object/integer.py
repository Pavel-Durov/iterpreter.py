from src.kimchi_object import HashableObject, Object
from .hash_key import HashKey

class Integer(HashableObject):
    def __init__(self, value):
        self.value = value

    def type(self):
        return Object.INTEGER_OBJ

    def inspect(self):
        return str(self.value)

    def __str__(self):
        return self.inspect()

    def hash_key(self):
        return HashKey(self.type(), self.value)
