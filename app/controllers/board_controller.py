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

    def create_figure(self, metrics):
        fig = Figure(figsize=(7,3))
        ax = fig.subplots()

        # Figure title
        figure_name = " & ".join(metrics)
        ax.set_title(figure_name)

        # Plot metrics
        for m in metrics:
            ax.plot(self.model.get(m), label=m)

        ax.legend()

        buf = BytesIO()
        fig.savefig(buf, format="png")

        return figure_name, base64.b64encode(buf.getbuffer()).decode("ascii")
            
    def get(self):
        return render_template('dashboard.html', title="Metrics")

    def post(self):
        data = request.get_json()

        if data:
            for metric in data:
                self.model.add(metric, data[metric])

            name, figure = self.create_figure(data.keys())

            self.socket.emit("metrics", {"name":name, "value":figure})

        return "", 204