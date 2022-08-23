from db import db
from random import randint

import factory

from models.enums import UserType
from models.user import SuggesterModel


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
