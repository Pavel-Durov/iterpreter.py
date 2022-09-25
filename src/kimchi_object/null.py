from src.kimchi_object import Object


class Null(Object):
    def __init__(self):
        pass

    def type(self):
        return Object.NULL_OBJ

    def inspect(self):
        return "null"

    def __str__(self):
        return self.inspect()
