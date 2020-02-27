class LossMask():
    def __init__(self):
        self.values = []

    def add(self, value):
        self.values.append(value)

    def get_all(self):
        return self.values

    def get(self, index):
        if index >= 0 and index < len(self.values):
            return self.values[index]