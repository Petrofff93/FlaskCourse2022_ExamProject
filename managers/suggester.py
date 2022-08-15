from werkzeug.security import generate_password_hash

from db import db
from models import SuggesterModel


class SuggesterManager:
    @staticmethod
    def register(suggester_data):
        suggester_data["password"] = generate_password_hash(suggester_data["password"])
        user = SuggesterModel(**suggester_data)
        db.session.add(user)
        db.session.commit()
