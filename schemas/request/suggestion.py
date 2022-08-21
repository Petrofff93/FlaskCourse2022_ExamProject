from marshmallow import fields

from schemas.base_suggestion import BaseSuggestionSchema


class RequestSuggestionSchema(BaseSuggestionSchema):
    certificate = fields.Str(required=True)
    certificate_extension = fields.Str(required=True)

