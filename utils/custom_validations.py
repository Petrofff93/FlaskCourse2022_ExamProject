from marshmallow import ValidationError
from password_strength import PasswordPolicy

# The additional validation for strong password used in Schemas
policy = PasswordPolicy.from_names(
    uppercase=1,
    numbers=1,
    special=1,
    nonletters=1
)


def validate_password(password):
    errors = policy.test(password)
    if errors:
        raise ValidationError("Password does not meet requirements!")
