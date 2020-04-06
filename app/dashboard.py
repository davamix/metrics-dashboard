import os
from flask import Flask
from flask_socketio import SocketIO

from controllers.board_controller import BoardController
# from models.metrics.metric import Metric

templates_path = os.path.join(os.getcwd(), "templates")

app = Flask(__name__, template_folder=templates_path)
socketio = SocketIO(app)

# metric_model = Metric()
metrics = [] # Array of Metric
merged_metrics = {} # {"metric_name": metric_names[]}

app.add_url_rule("/board", view_func=BoardController.as_view("board", metrics = metrics, merged = merged_metrics, socket = socketio))

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True)