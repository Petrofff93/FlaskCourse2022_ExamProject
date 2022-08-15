import enum


class UserType(enum.Enum):
    admin = "admin"
    base_user = "user"


class State(enum.Enum):
    pending = "Waiting for an overview"
    accepted = "Post accepted"
    rejected = "Post rejected"
