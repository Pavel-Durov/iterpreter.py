from src.kimchi_object import Object


class Function(Object):
    def __init__(self, parameters, body, env):
        self.parameters = parameters
        self.body = body
        self.env = env

    def type(self):
        return Object.FUNCTION_OBJ

    def inspect(self):
        out = "fn("
        for p in self.parameters:
            if p is not None:
                out += ", " + str(p)
        out += ") {\n"
        if self.body is not None:
            out += str(self.body)
        out += "\n}"
        return out
