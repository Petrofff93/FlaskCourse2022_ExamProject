from marshmallow import Schema, fields, validate


class BaseSuggestionSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    importance_rate = fields.Int(required=True, validate=validate.Range(min=1, max=10))
    course_certificate_url = fields.Str(required=True)
