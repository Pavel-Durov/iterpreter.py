class Environment():
    def __init__(self):
        self.store = {}

    def get(self, name):
        if name in self.store:
            return self.store[name]
        return None

    def set(self, name, value):
        self.store[name] = value
        return value
