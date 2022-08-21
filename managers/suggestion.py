from db import db
from models import SuggesterModel, State

from models.suggestion import SuggestionModel


class SuggestionManager:
    """
    A manager class which is responsible for retrieving, creating, updating or deleting the concrete suggestion
    """
    @staticmethod
    def get_all_user_suggestions(user):
        # This method returns only the suggestions of the current user (accepted or rejected)
        if isinstance(user, SuggesterModel):
            return SuggestionModel.query.filter_by(suggester_id=user.id).all()

    @staticmethod
    def get_all_suggestions():
        """
        This method returns all the accepted suggestions no matter who wants to see them (admin, user, unregistered)
        """
        return SuggestionModel.query.filter_by(status="accepted").all()

    @staticmethod
    def create(data, suggester_id):
        data["suggester_id"] = suggester_id
        sugg = SuggestionModel(**data)
        db.session.add(sugg)
        db.session.flush()
        return sugg

    @staticmethod
    def upload_suggestion(id_):
        SuggestionModel.query.filter_by(id=id_).update({"status": State.accepted})

    @staticmethod
    def reject_upload(id_):
        SuggestionModel.query.filter_by(id=id_).update({"status": State.rejected})
