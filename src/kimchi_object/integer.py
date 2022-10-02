# from enum import Enum
from src.kimchi_object import HashableObject, Object
from .hash_key import HashKey


class IntegerBuilder():
    def __init__(self, use_class=True):
        self.use_class = use_class

    def build(self, value):
        if self.use_class:
            return Integer(value)
        else:
            return IntegerBuilder.__construct(value)
    
    @staticmethod
    def __construct(value):
        return { "type": 1, "value": value, "hash": value }
    

    @staticmethod
    def is_int(obj):
        if isinstance(obj, Integer):
            return True
        return type(obj) == dict and "type" in obj and obj["type"] == 1
    
    @staticmethod
    def set_value(obj, value):
        if isinstance(obj, Integer):
            obj.value = value
        obj["value"] = value
          


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
    

    