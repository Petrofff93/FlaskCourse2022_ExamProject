from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import Unauthorized

from models import SuggesterModel, AdministratorModel


class AuthManager:
    """
    Authentication manager which is responsible to encode/decode and validate tokens
    """
    @staticmethod
    def encode_token(user):
        payload = {
            "sub": user.id,
            "exp": datetime.utcnow() + timedelta(days=4),
            "type": type(user).__name__,
        }
        return jwt.encode(payload, key=config("JWT_SECRET_KEY"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(
                token, key=config("JWT_SECRET_KEY"), algorithms=["HS256"]
            )
            return payload["sub"], payload["type"]
        except Exception as error:
            raise error


authentication = HTTPTokenAuth(scheme="Bearer")


@authentication.verify_token
def verify_token(token):
    """
    a verification func which takes care to verify if the user is regular or admin or does not exist
    """
    try:
        user_id = AuthManager.decode_token(token)
        if user_id[1] == 'SuggesterModel':
            return SuggesterModel.query.filter_by(id=user_id[0]).first()
        if user_id[1] == 'AdministratorModel':
            return AdministratorModel.query.filter_by(id=user_id[0]).first()
    except Exception:
        raise Unauthorized("Token is invalid or missing!")
