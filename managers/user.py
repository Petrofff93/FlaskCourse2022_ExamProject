from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth import AuthManager
from models import SuggesterModel


class SuggesterManager:
    @staticmethod
    def register(suggester_data):
        suggester_data["password"] = generate_password_hash(
            suggester_data["password"], method="sha256"
        )
        suggester = SuggesterModel(**suggester_data)
        try:
            db.session.add(suggester)
            db.session.flush()
            return AuthManager.encode_token(suggester)
        except Exception as error:
            raise BadRequest(str(error))

    @staticmethod
    def login(data):
        try:
            suggester = SuggesterModel.query.filter_by(email=data["email"]).first()
            if suggester and check_password_hash(suggester.password, data["password"]):
                return AuthManager.encode_token(suggester)
            raise Exception
        except Exception:
            raise BadRequest("The username and/or password are not valid!")
