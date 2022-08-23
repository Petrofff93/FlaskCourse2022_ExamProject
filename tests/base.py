from managers.auth import AuthManager


def generate_token(user):
    return AuthManager.encode_token(user)


def mock_uuid():
    return "666666"
