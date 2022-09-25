
from src.kimchi_object import Object

class Builtin(Object):
    def __init__(self, fn):
        self.fn = fn

    def type(self):
        return Object.BUILTIN_OBJ

    def inspect(self):
        return "builtin function"

    def __str__(self):
        return self.inspect()
