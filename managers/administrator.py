from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash

from managers.auth import AuthManager
from models import AdministratorModel


class AdminManager:
    """
    Manager which takes care that only the admins could log into the admin panel.
    """

    @staticmethod
    def login(login_data):
        admin = AdministratorModel.query.filter_by(email=login_data["email"]).first()
        if not admin:
            raise BadRequest("There is no such email! Please Signup")

        if not admin.password == login_data["password"]:
            raise BadRequest("Password is incorrect!")

        return AuthManager.encode_token(admin)
