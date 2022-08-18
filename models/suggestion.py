from sqlalchemy import func

from db import db
from models.enums import State


class SuggestionModel(db.Model):
    __tablename__ = "suggestion"

    # Here also we will use 'pk' instead of 'id'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # The importance rate will be value which the user provide in order to point the urgency
    importance_rate = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, server_default=func.now())
    status = db.Column(db.Enum(State), default=State.pending, nullable=False)
    course_certificate_url = db.Column(db.String(255), nullable=False)

    suggester_id = db.Column(db.Integer, db.ForeignKey("suggester.id"), nullable=False)
    suggester = db.relationship("SuggesterModel")
