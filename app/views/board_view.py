from flask import jsonify, request
from flask.views import MethodView
import base64
from io import BytesIO
from matplotlib.figure import Figure
from flask import redirect, url_for

# from controllers.board_controller import BoardController

class BoardView(MethodView):
    def __init__(self, controller):
        self.controller = controller

    def get(self):
        # return jsonify({"message":"This is a board"})
        #return self.controller.get_total()
        # value = self.controller.get_losses()
        # return f"{value}"
        fig = Figure()
        ax = fig.subplots()
        ax.plot(self.controller.get_losses())

        buf = BytesIO()
        fig.savefig(buf, format="png")

        data = base64.b64encode(buf.getbuffer()).decode("ascii")

        return f"<img src='data:image/png;base64, {data}' />"

    def post(self):
        data = request.get_json() 
        
        if data:
            self.controller.add_loss(data["loss"])
        
        # Do something with the data

        return f"{self.controller.get_losses()}", 201
        #return redirect(url_for('board'))