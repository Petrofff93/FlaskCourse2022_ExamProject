from flask import request
from flask_api import status
from flask_restful import Resource

from managers.user import SuggesterManager
from schemas.request.user import RequestRegisterUserSchema, RequestLoginUserSchema
from utils.decorators import validate_schema


class RegisterSuggesterResource(Resource):
    @validate_schema(RequestRegisterUserSchema)
    def post(self):
        data = request.get_json()
        token = SuggesterManager.register(data)
        return {"token": token}, status.HTTP_201_CREATED


class LoginSuggesterResource(Resource):
    @validate_schema(RequestLoginUserSchema)
    def post(self):
        data = request.get_json()
        token = SuggesterManager.login(data)
        return {"token": token, "role": "suggester"}, status.HTTP_200_OK
