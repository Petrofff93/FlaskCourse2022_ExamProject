import os
import uuid

from constants import TEMP_FILE_DIR
from db import db
from models import SuggesterModel, State

from models.suggestion import SuggestionModel
from services.s3 import S3Service
from utils.helpers import decode_photo

s3 = S3Service()


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
        This method returns all the accepted suggestions no matter who wants to see them (admin, user, unregistered).
        In that case everybody can take a look of the overall assessment.
        """
        return SuggestionModel.query.filter_by(status="accepted").all()

    @staticmethod
    def create(data, suggester_id):
        data["suggester_id"] = suggester_id
        extension = data.pop("certificate_extension")
        certificate = data.pop("certificate")
        file_name = f"{str(uuid.uuid4())}.{extension}"
        path = os.path.join(TEMP_FILE_DIR, file_name)
        decode_photo(path, certificate)
        url = s3.upload_cert(path, file_name, extension)
        data["course_certificate_url"] = url
        os.remove(path)

        suggestion = SuggestionModel(**data)
        db.session.add(suggestion)
        # The flush method makes the changes in the DB, but they are not permanent until commit() method is called.
        db.session.flush()
        return suggestion

    @staticmethod
    def upload_suggestion(id_):
        SuggestionModel.query.filter_by(id=id_).update({"status": State.accepted})

    @staticmethod
    def reject_upload(id_):
        SuggestionModel.query.filter_by(id=id_).update({"status": State.rejected})
