class Metric():
    def __init__(self):
        self.values = {}

    def add(self, name, value):
        if name in self.values:
            self.values[name].append(value)
        else:
            self.values[name] = []
            self.values[name].append(value)

    def get(self, name):
        if name in self.values:
            return self.values[name]