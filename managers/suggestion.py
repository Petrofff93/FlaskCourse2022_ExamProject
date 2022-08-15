from db import db

from models.suggestion import SuggestionModel


class SuggestionManager:
    @staticmethod
    def get_all_user_suggestions(user):
        if isinstance(user, SuggestionModel):
            return SuggestionModel.query.filter_by(suggester_pk=user.pk).all()
        return SuggestionModel.query.all()

    @staticmethod
    def create(data, suggester_pk):
        data["suggester_pk"] = suggester_pk
        sugg = SuggestionModel(**data)
        db.session.add(sugg)
        db.session.flush()
        return sugg
