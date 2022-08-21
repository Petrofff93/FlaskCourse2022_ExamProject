import phonenumbers
from marshmallow import ValidationError
from password_strength import PasswordPolicy

# The additional validation for strong password used in Schemas
from phonenumbers import NumberParseException

from models import SuggesterModel, AdministratorModel

policy = PasswordPolicy.from_names(
    uppercase=1,
    numbers=1,
    special=1,
    nonletters=1
)


# Custom validation for the password using external library 'password_strength'
def validate_password(password):
    errors = policy.test(password)
    if errors:
        raise ValidationError("Password does not meet requirements!")


# Custom validation for the phone number using external library 'phonenumbers'
def validate_phone_number(phone_number):
    number = f"{phone_number}"
    try:
        current = phonenumbers.parse(number)
        phonenumbers.is_valid_number(current)
    except NumberParseException:
        raise ValidationError("Please enter a valid phone number!")


# Custom validation for already existing email
def validate_email_already_exists(email):
    current_mail_suggester = SuggesterModel.query.filter_by(email=email).first()
    current_mail_admin = AdministratorModel.query.filter_by(email=email).first()
    if current_mail_suggester or current_mail_admin:
        raise ValidationError("Email already exists!")


# Custom validation for already used phone numbers(you should not use one number for more than one reg)
def validate_phone_number_already_exists(phone_number):
    current_phone_number_suggester = SuggesterModel.query.filter_by(phone_number=phone_number).first()
    current_phone_number_admin = AdministratorModel.query.filter_by(phone_number=phone_number).first()
    if current_phone_number_admin or current_phone_number_suggester:
        raise ValidationError("User with that phone number already exists!")
