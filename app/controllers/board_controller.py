class BoardController():
    def __init__(self):
        self.total = 0

    def add_value(self, value):
        self.total += value

        return self.total

    def get_total(self):
        return self.total
