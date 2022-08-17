from marshmallow import fields
from models.enums import State
from marshmallow_enum import EnumField

from schemas.base_suggestion import BaseSuggestionSchema


class SuggestionResponseSchema(BaseSuggestionSchema):
    id = fields.Int(required=True)
    status = EnumField(State, by_value=True)
    created_on = fields.DateTime(required=True)
    