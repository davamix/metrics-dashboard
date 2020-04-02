import os
from flask import Flask
from flask_socketio import SocketIO

from controllers.board_controller import BoardController
from controllers.metrics.total_loss import TotalLossController
from controllers.metrics.loss_mask import LossMaskController

# Models
from models.metrics.total_loss import TotalLoss
from models.metrics.loss_mask import LossMask

templates_path = os.path.join(os.getcwd(), "templates")

app = Flask(__name__, template_folder=templates_path)
socketio = SocketIO(app)

total_loss_model = TotalLoss()
loss_mask_model = LossMask()

app.add_url_rule('/metrics/loss', view_func=TotalLossController.as_view('metrics_loss', model = total_loss_model, socket = socketio))
app.add_url_rule('/metrics/mask', view_func=LossMaskController.as_view('metrics_mask', model = loss_mask_model, socket = socketio))
app.add_url_rule('/board', view_func=BoardController.as_view('board', total_loss_model = total_loss_model, loss_mask_model = loss_mask_model))

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True)