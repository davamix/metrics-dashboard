import base64
from io import BytesIO
from flask.views import MethodView
from matplotlib.figure import Figure

class BoardController(MethodView):
    def __init__(self, model):
        self.model = model

    def get(self):
        fig = Figure()
        ax = fig.subplots()
        ax.plot(self.model.get_all())

        buf = BytesIO()
        fig.savefig(buf, format="png")

        data = base64.b64encode(buf.getbuffer()).decode("ascii")

        return f"<img src='data:image/png;base64, {data}' />"
