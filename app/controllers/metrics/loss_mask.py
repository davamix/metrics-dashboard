from flask import request
from flask.views import MethodView
from flask_socketio import emit

class LossMaskController(MethodView):
    def __init__(self, model, socket):
        self.socket = socket
        self.model = model
    
    def get(self):
        return f"{self.model.get_all()}"

    def post(self):
        data = request.get_json()

        if data:
            self.model.add(data)

            self.socket.emit("loss_mask", data)
            

        return "No data added", 204