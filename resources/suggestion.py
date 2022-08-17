from flask import request
from flask_api import status
from flask_restful import Resource

from managers.auth import authentication
from managers.suggestion import SuggestionManager
from models import UserType
from schemas.request.suggestion import RequestSuggestionSchema
from schemas.response.suggestion import SuggestionResponseSchema
from utils.decorators import validate_schema, permission_required


class SuggestionListCreateResource(Resource):
    @authentication.login_required
    @validate_schema(RequestSuggestionSchema)
    def get(self):
        user = authentication.current_user()
        suggestions = SuggestionManager.get_all_user_suggestions(user)
        return SuggestionResponseSchema().dump(suggestions, many=True)

    @authentication.login_required
    @permission_required(UserType.base_user)
    @validate_schema(RequestSuggestionSchema)
    def post(self):
        suggester = authentication.current_user()
        data = request.get_json()
        suggestion = SuggestionManager.create(data, suggester.id)
        return SuggestionResponseSchema().dump(suggestion)


class UploadSuggestion(Resource):
    @authentication.login_required
    @permission_required(UserType.admin)
    def put(self, id_):
        SuggestionManager.upload_suggestion(id_)
        return status.HTTP_200_OK


class RejectSuggestion(Resource):
    @authentication.login_required
    @permission_required
    def put(self, id_):
        SuggestionManager.reject_upload(id_)
        return status.HTTP_200_OK
