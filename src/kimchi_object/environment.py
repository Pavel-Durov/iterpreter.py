class Environment():
    def __init__(self, outer=None):
        self.store = {}
        self.outer = outer

    def get(self, name):
        if name in self.store:
            return self.store[name]
        elif self.outer is not None:
            return self.outer.get(name)
        return None

    def set(self, name, value):
        self.store[name] = value
        return value
