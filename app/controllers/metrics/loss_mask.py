import base64
from io import BytesIO
from flask import request
from flask.views import MethodView
from flask_socketio import emit
from matplotlib.figure import Figure

class LossMaskController(MethodView):
    def __init__(self, model, socket):
        self.socket = socket
        self.model = model

    def create_figure(self, data):
        fig = Figure()
        ax = fig.subplots()
        ax.plot(data)

        buf = BytesIO()
        fig.savefig(buf, format="png")

        return base64.b64encode(buf.getbuffer()).decode("ascii")

    # def get(self):
        # return f"{self.model.get_all()}"

    def post(self):
        data = request.get_json()

        if data:
            self.model.add(data)

            figure = self.create_figure(self.model.get_all())
            self.socket.emit("loss_mask", figure)            

        return "No data added", 204