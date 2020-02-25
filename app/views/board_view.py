from flask import jsonify, request
from flask.views import MethodView

# from controllers.board_controller import BoardController

class BoardView(MethodView):
    def __init__(self, controller):
        self.controller = controller

    def get(self):
        # return jsonify({"message":"This is a board"})
        #return self.controller.get_total()
        value = self.controller.get_total()
        return f"{value}"

    def post(self):
        data = request.get_json() 

        self.controller.add_value(data["value"])
        
        # Do something with the data

        return self.controller.get_total(), 201