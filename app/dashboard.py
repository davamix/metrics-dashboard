from flask import Flask, jsonify, request
from flask_restful import Resource, Api

from views.board_view import BoardView
from controllers.board_controller import BoardController


app = Flask(__name__)
api = Api(app)

api.add_resource(BoardView, "/board", resource_class_kwargs={'controller': BoardController()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)