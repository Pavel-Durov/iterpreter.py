from src.kimchi_object import Object

class Error(Object):
    def __init__(self, message):
        self.message = message

    def type(self):
        return Object.ERROR_OBJ

    def inspect(self):
        return "ERROR: " + self.message

    def __str__(self):
        return self.inspect()
