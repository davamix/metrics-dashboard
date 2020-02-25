class BoardController():
    def __init__(self):
        self.losses = []

    def add_loss(self, loss):
        self.losses.append(loss)

    def get_losses(self):
        return self.losses
