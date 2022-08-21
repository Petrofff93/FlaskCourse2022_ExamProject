from marshmallow import Schema, fields, validate


class BaseSuggestionSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    # The base user is framed between 1 and 10 for his assessment rate.
    assessment_rate = fields.Int(required=True, validate=validate.Range(min=1, max=10))


