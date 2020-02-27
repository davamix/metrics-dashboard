import base64
from io import BytesIO
from multiprocessing import Pool
from flask import render_template
from flask.views import MethodView
from matplotlib.figure import Figure

class BoardController(MethodView):
    def __init__(self, total_loss_model, loss_mask_model):
        self.total_loss_model = total_loss_model
        self.loss_mask_model = loss_mask_model

    def create_figure(self, data):
        fig = Figure()
        ax = fig.subplots()
        ax.plot(data)

        buf = BytesIO()
        fig.savefig(buf, format="png")

        return base64.b64encode(buf.getbuffer()).decode("ascii")

    def get(self):
        figures = []
        
        with Pool() as p:
            figures = p.map(self.create_figure, [self.total_loss_model.get_all(), self.loss_mask_model.get_all()])

        return render_template('dashboard.html', title="Yeee", figures = figures)