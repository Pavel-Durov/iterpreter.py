from src.kimchi_object import Object

class ReturnValue(Object):
    def __init__(self, value):
        self.value = value

    def type(self):
        return Object.RETURN_VALUE_OBJ

    def inspect(self):
        return self.value.inspect()
