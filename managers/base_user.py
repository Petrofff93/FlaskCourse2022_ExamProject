from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth import AuthManager
from models import SuggesterModel


class SuggesterManager:
    """
    A class manager which takes care for registration and login of the base users(suggesters)
    """

    @staticmethod
    def register(suggester_data):
        suggester_data["password"] = generate_password_hash(
            suggester_data["password"], method="sha256"
        )

        suggester = SuggesterModel(**suggester_data)
        try:
            db.session.add(suggester)
            return AuthManager.encode_token(suggester)
        except Exception as error:
            # raises a Bad request and as a text uses the exception made as string
            raise BadRequest(str(error))

    @staticmethod
    def login(signin_data):
        suggester = SuggesterModel.query.filter_by(email=signin_data["email"]).first()
        if not suggester:
            raise BadRequest("There is no such email! Please Signup")

        if check_password_hash(suggester.password, signin_data["password"]):
            return AuthManager.encode_token(suggester)
        raise BadRequest("Incorrect password!")
