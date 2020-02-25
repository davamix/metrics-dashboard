import base64
from io import BytesIO

from flask import Flask
from flask.views import View
from matplotlib.figure import Figure

class FigureView(View):
    def dispatch_request(self):
        fig = Figure()
        ax = fig.subplots()
        ax.plot([1, 2])

        buf = BytesIO()
        fig.savefig(buf, format="png")

        data = base64.b64encode(buf.getbuffer()).decode("ascii")

        return f"<img src='data:image/png;base64, {data}' />"