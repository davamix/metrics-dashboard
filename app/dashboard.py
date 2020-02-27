from flask import Flask

from controllers.board_controller import BoardController
from controllers.metrics.total_loss import TotalLossController
from models.metrics.total_loss import TotalLoss


app = Flask(__name__)

total_loss_model = TotalLoss()

app.add_url_rule('/metrics/loss', view_func=TotalLossController.as_view('metrics_loss', model=total_loss_model))
app.add_url_rule('/board', view_func=BoardController.as_view('board', model=total_loss_model))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)