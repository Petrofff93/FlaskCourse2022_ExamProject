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
    """
    Resource class which is responsible for retrieving(reading) the data for a specific user,
    creating (posting a suggestion and assessment) from the specific user.
    """

    # In order to retrieve a resource - the user should be existing and logged in.
    @authentication.login_required
    def get(self):
        user = authentication.current_user()
        suggestions = SuggestionManager.get_all_user_suggestions(user)
        return SuggestionResponseSchema().dump(suggestions, many=True)

    # In order to create(post) a resource - the user should be logged in and should be base user.
    @authentication.login_required
    @permission_required(UserType.base_user)
    @validate_schema(RequestSuggestionSchema)
    def post(self):
        suggester = authentication.current_user()
        data = request.get_json()
        suggestion = SuggestionManager.create(data, suggester.id)
        return SuggestionResponseSchema().dump(suggestion)


class SuggestionListGetAllResource(Resource):
    """
    Resource class which is responsible for retrieving all the approved (accepted by admins) data
    and made it visible for anyone who wants to check (admins, base users, non registered)
    """

    def get(self):
        suggestions = SuggestionManager.get_all_suggestions()
        return SuggestionResponseSchema().dump(suggestions, many=True)


class UploadSuggestionResource(Resource):
    """
    Resource class which gives the admins the option to check and upload(approve) the pending suggestion.
    """

    @authentication.login_required
    @permission_required(UserType.admin)
    def put(self, id):
        SuggestionManager.upload_suggestion(id)
        return status.HTTP_204_NO_CONTENT


class RejectSuggestionResource(Resource):
    """
    Resource class which gives the admins the option to check and download/delete (reject) the pending suggestion.
    """

    @authentication.login_required
    @permission_required(UserType.admin)
    def put(self, id):
        SuggestionManager.reject_upload(id)
        return status.HTTP_204_NO_CONTENT
