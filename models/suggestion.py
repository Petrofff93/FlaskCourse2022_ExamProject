from sqlalchemy import func

from db import db
from models.enums import State


class SuggestionModel(db.Model):
    """
    This model represents the suggestions and assessments of the university users.
    In order to evaluate the university or to give a suggestion for improvement,
    they should add title, content of the suggestion, they should rate the university,
    and a mandatory rule is that they upload at least one certificate to prove that they are students.
    """
    __tablename__ = "suggestion"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # The assessment is important for the business in order to check overall opinion.
    assessment_rate = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, server_default=func.now())
    status = db.Column(db.Enum(State), default=State.pending, nullable=False)
    course_certificate_url = db.Column(db.String(255), nullable=False)

    suggester_id = db.Column(db.Integer, db.ForeignKey("suggester.id"), nullable=False)
    suggester = db.relationship("SuggesterModel")
