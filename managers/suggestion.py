import os
import uuid

from decouple import config

from constants import TEMP_FILE_DIR
from db import db
from models import SuggesterModel, State
from models.suggestion import SuggestionModel
from services.s3 import S3Service
from services.ses import SESService
from utils.helpers import decode_photo

s3 = S3Service()
email_service = SESService()


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
        # A method which is responsible for storing the suggestion and uploading the certificates to AWS cloud.
        data["suggester_id"] = suggester_id
        extension = data.pop("certificate_extension")
        certificate = data.pop("certificate")
        # In order to track user uploads in bucket, we add user id for each certificate.
        file_name = f"{str(uuid.uuid4())}userid{suggester_id}.{extension}"
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
        # Method which accepts the user's suggestion and sending them a confirmation email
        body = "Greetings!\nYour post is uploaded. Thanks for helping us improve!\n Stay safe!"
        SuggestionModel.query.filter_by(id=id_).update({"status": State.accepted})
        email_service.send_mail(
            "Uploaded post",
            [config("AWS_RECIPIENT")],
            body
        )

    @staticmethod
    def reject_upload(id_):
        # After admin check, this method rejects the user's upload and also notifies the user via email service.
        body = "Greetings!\nWe are sorry to inform you that due to violations your post was rejected.\n Stay safe!"
        SuggestionModel.query.filter_by(id=id_).update({"status": State.rejected})
        email_service.send_mail(
            "Rejected post",
            [config("AWS_RECIPIENT")],
            body
        )

    @staticmethod
    def delete_rejected():
        # A method used only by admins in order to delete rejected posts from db over time.
        SuggestionModel.query.filter_by(status=State.rejected).delete(
            synchronize_session=False
        )
