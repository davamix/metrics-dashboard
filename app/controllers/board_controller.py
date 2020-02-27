import base64
from io import BytesIO
from flask.views import MethodView
from matplotlib.figure import Figure

class BoardController(MethodView):
    def __init__(self, total_loss_model, loss_mask_model):
        self.total_loss_model = total_loss_model
        self.loss_mask_model = loss_mask_model

    def get(self):
        fig = Figure()
        ax = fig.subplots(1,2)
        ax[0].plot(self.total_loss_model.get_all())
        ax[1].plot(self.loss_mask_model.get_all())

        buf = BytesIO()
        fig.savefig(buf, format="png")

        data = base64.b64encode(buf.getbuffer()).decode("ascii")


        # TODO: Create the figure for loss mask

        return f"<img src='data:image/png;base64, {data}' />"

