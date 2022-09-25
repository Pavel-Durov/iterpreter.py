from src.kimchi_object.object import Object


class Array(Object):
    def __init__(self, elements):
        self.elements = elements

    def type(self):
        return Object.ARRAY_OBJ

    def inspect(self):
        out = "["
        out += ", ".join([str(e) for e in self.elements])
        out += "]"
        return out

    def __str__(self):
        return self.inspect()
