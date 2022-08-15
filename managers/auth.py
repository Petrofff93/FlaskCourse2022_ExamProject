from datetime import datetime, timedelta
from decouple import config

import jwt
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import Unauthorized


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {"sub": user.id, "exp": datetime.utcnow() + timedelta(days=4), "type": type(user).__name__}
        return jwt.encode(payload, key=config("SECRET_KEY"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        try:
            info_data = jwt.decode(jwt=token, key=config("SECRET_KEY"), algorithms=["HS256"])
            return info_data["sub"], info_data["type"]
        except Exception as error:
            raise error


authentication = HTTPTokenAuth(scheme="Bearer")


@authentication.verify_token
def verify_token(token):
    try:
        user_id, user_type = AuthManager.decode_token(token)
        return eval(f"{user_type}.query.filter_by(id={user_id}).first()")
    except Exception as error:
        raise Unauthorized("Token is invalid or missing!")
