import base64
from io import BytesIO
from flask import render_template
from flask.views import MethodView
from matplotlib.figure import Figure
from flask import request
from flask_socketio import emit

class BoardController(MethodView):
    def __init__(self, model, socket):
        self.model = model
        self.socket = socket

    def create_figure(self, name, values):
        fig = Figure()
        ax = fig.subplots()
        ax.set_title(name)
        ax.plot(values)

        buf = BytesIO()
        fig.savefig(buf, format="png")

        return base64.b64encode(buf.getbuffer()).decode("ascii")
            
    def get(self):
        return render_template('dashboard.html', title="Metrics")

    def post(self):
        data = request.get_json()

        if data:
            self.model.add(data[0], data[1])

            figure = self.create_figure(data[0], self.model.get(data[0]))

            self.socket.emit("metrics", {"name":data[0], "value":figure})

        return "", 204