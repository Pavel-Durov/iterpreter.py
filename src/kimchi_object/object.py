class Object():
    INTEGER_OBJ = "INTEGER"
    BOOLEAN_OBJ = "BOOLEAN"
    NULL_OBJ = "NULL"
    RETURN_VALUE_OBJ = "RETURN_VALUE"
    ERROR_OBJ = "ERROR"
    FUNCTION_OBJ = "FUNCTION"
    STRING_OBJECT = "STRING"
    BUILTIN_OBJ = "BUILTIN"
    ARRAY_OBJ = "ARRAY"

    def type():
        pass

    def inspect():
        pass


class Integer(Object):
    def __init__(self, value):
        self.value = value

    def type(self):
        return Object.INTEGER_OBJ

    def inspect(self):
        return str(self.value)

    def __str__(self):
        return self.inspect()


class Boolean(Object):
    def __init__(self, value):
        self.value = value

    def type(self):
        return Object.BOOLEAN_OBJ

    def inspect(self):
        return str(self.value)

    def __str__(self):
        return self.inspect()


class Null(Object):
    def __init__(self):
        pass

    def type(self):
        return Object.NULL_OBJ

    def inspect(self):
        return "null"

    def __str__(self):
        return self.inspect()


class ReturnValue(Object):
    def __init__(self, value):
        self.value = value

    def type(self):
        return Object.RETURN_VALUE_OBJ

    def inspect(self):
        return self.value.inspect()


class Error(Object):
    def __init__(self, message):
        self.message = message

    def type(self):
        return Object.ERROR_OBJ

    def inspect(self):
        return "ERROR: " + self.message

    def __str__(self):
        return self.inspect()


class Function(Object):
    def __init__(self, parameters, body, env):
        self.parameters = parameters
        self.body = body
        self.env = env

    def type(self):
        return Object.FUNCTION_OBJ

    def inspect(self):
        out = "fn("
        out += ", ".join(self.parameters)
        out += ") {\n"
        out += str(self.body)
        out += "\n}"
        return out


class String(Object):
    def __init__(self, value):
        self.value = value

    def type(self):
        return Object.STRING_OBJ

    def inspect(self):
        return self.value

    def __str__(self):
        return self.inspect()


class Builtin(Object):
    def __init__(self, fn):
        self.fn = fn

    def type(self):
        return Object.BUILTIN_OBJ

    def inspect(self):
        return "builtin function"

    def __str__(self):
        return self.inspect()


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
