from db import db
from models.enums import UserType


class BaseUserModel(db.Model):
    __abstract__ = True

    # Using 'PK' instead of 'ID' in order to avoid name shadowing
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)


class AdministratorModel(BaseUserModel):
    __tablename__ = "administrator"

    role = db.Column(db.Enum(UserType), default=UserType.admin, nullable=False)


class SuggesterModel(BaseUserModel):
    __tablename__ = "suggester"

    suggestions = db.relationship(
        "SuggestionModel", backref="suggestion", lazy="dynamic"
    )
    role = db.Column(db.Enum(UserType), default=UserType.base_user, nullable=False)
