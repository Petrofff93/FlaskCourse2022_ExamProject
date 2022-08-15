from flask import request
from flask_restful import Resource


from managers.suggester import SuggesterManager


class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        SuggesterManager.register(data)
        return 201
