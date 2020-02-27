from flask import request
from flask.views import MethodView

class TotalLossController(MethodView):
    def __init__(self, model):
        self.model = model
    
    def get(self):
        return f"{self.model.get()}"

    def post(self):
        data = request.get_json()

        if data:
            self.model.add(data)
            return f"{data} added", 201

        return "No data added", 204