from flask import request
from flask_restful import Resource


from managers.user import SuggesterManager


class RegisterSuggesterResource(Resource):
    def post(self):
        data = request.get_json()
        SuggesterManager.register(data)
        return 201


class LoginSuggesterResource(Resource):
    def post(self):
        data = request.get_json()
        SuggesterManager.login(data)
        return 200
