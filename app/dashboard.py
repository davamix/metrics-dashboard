from flask import Flask, jsonify, request

from views.board_view import BoardView
from views.figure_view import FigureView
from controllers.board_controller import BoardController


app = Flask(__name__)

app.add_url_rule('/board', view_func=BoardView.as_view('board', controller=BoardController()))
app.add_url_rule('/figure', view_func=FigureView.as_view('figure'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)