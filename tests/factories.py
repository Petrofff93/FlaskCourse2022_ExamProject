from random import randint

import factory

from db import db
from models import SuggestionModel
from models.enums import UserType, State
from models.user import SuggesterModel, AdministratorModel


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        obj = super().create(**kwargs)
        db.session.add(obj)
        db.session.flush()
        return obj


class SuggesterFactory(BaseFactory):
    class Meta:
        model = SuggesterModel

    id = factory.Sequence(lambda x: x)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    phone_number = f"+359{str(randint(1000000, 2000000))}"
    role = UserType.base_user


class SuggesterEmailFactory(SuggesterFactory):
    id = factory.Sequence(lambda x: x)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = "test@test.com"
    password = factory.Faker("password")
    phone_number = f"+359{str(randint(1000000, 2000000))}"
    role = UserType.base_user


class SuggesterPhoneFactory(SuggesterFactory):
    id = factory.Sequence(lambda x: x)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    phone_number = "+359876870777"
    role = UserType.base_user


class SuggesterFactoryLoginUser(SuggesterFactory):
    id = factory.Sequence(lambda x: x)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = "test@test.com"
    password = "Password123!"
    phone_number = "+359876870777"
    role = UserType.base_user


class SuggestionFactory(BaseFactory):
    class Meta:
        model = SuggestionModel

    title = factory.Faker("first_name")
    content = factory.Faker("last_name")
    assessment_rate = str(randint(1, 10))
    status = State.pending
    course_certificate_url = "some.s3.random.url"
    suggester_id = 1


class AdminFactory(SuggesterFactory):
    class Meta:
        model = AdministratorModel

    id = 2
    role = UserType.admin
    phone_number = "+359876870777"


class SuggesterUploadFactory(SuggesterFactory):
    id = 1
