class Object():
    INTEGER_OBJ = "INTEGER"
    BOOLEAN_OBJ = "BOOLEAN"
    NULL_OBJ = "NULL"
    RETURN_VALUE_OBJ = "RETURN_VALUE"
    ERROR_OBJ = "ERROR"
    FUNCTION_OBJ = "FUNCTION"
    STRING_OBJ = "STRING"
    BUILTIN_OBJ = "BUILTIN"
    ARRAY_OBJ = "ARRAY"
    HASH_OBJ = "HASH"

    def type():
        pass

    def inspect():
        pass


class HashableObject(Object):
    def hash_key():
        pass


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


class Boolean(HashableObject):
    def __init__(self, value):
        self.value = value

    def type(self):
        return Object.BOOLEAN_OBJ

    def inspect(self):
        return str(self.value)

    def __str__(self):
        return self.inspect()

    def hash_key(self):
        if self.value:
            return HashKey(self.type(), 1)
        else:
            return HashKey(self.type(), 0)


class String(HashableObject):
    def __init__(self, value):
        self.value = value

    def type(self):
        return Object.STRING_OBJ

    def inspect(self):
        return self.value

    def __str__(self):
        return self.inspect()

    def hash_key(self):
        return HashKey(self.type(), hash(self.value))


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


class HashKey(Object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __eq__(self, other):
        if self.type != other.type:
            return False
        if self.type == Object.INTEGER_OBJ:
            return self.value == other.value
        if self.type == Object.STRING_OBJ:
            return self.value == other.value
        if self.type == Object.BOOLEAN_OBJ:
            return self.value == other.value
        raise Exception("uncomparable type: " + self.type)

    def __hash__(self):
        if self.type == Object.INTEGER_OBJ or self.type == Object.BOOLEAN_OBJ or self.type == Object.STRING_OBJ:
            return hash(self.value)
        raise Exception("unhashable type: " + self.type)

    def __str__(self):
        return str(self.value)


class HashPair(Object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return str(self.key) + ": " + str(self.value)


class Hash(Object):
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
        return HashKey(self.type(), hash(self.pairs))
