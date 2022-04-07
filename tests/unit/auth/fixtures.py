from flask_jwt_extended import create_access_token

from user.models import User


def get_auth_headers(user_or_token):
    if isinstance(user_or_token, User):
        token = create_access_token(user_or_token)
    elif isinstance(user_or_token, str):
        token = user_or_token
    else:
        raise ValueError('User instance or token expected')

    return {
        'Authorization': f'Bearer {token}',
    }
