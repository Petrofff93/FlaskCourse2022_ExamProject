from db import db
from models import SuggesterModel, State

from models.suggestion import SuggestionModel


class SuggestionManager:
    @staticmethod
    def get_all_user_suggestions(user):
        if isinstance(user, SuggesterModel):
            return SuggestionModel.query.filter_by(suggester_pk=user.pk).all()
        return SuggestionModel.query.all()

    @staticmethod
    def create(data, suggester_pk):
        data["suggester_pk"] = suggester_pk
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
