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
    phone_number = f"+359{str(randint(100000, 200000))}"
    role = UserType.base_user
