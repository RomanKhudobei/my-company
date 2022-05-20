from flask_jwt_extended import create_access_token, create_refresh_token

from auth.exceptions import AuthenticationFailed
from auth.schemas import UserLoginSchema
from user.models import User


def authenticate(email, password):
    user = User.query.filter_by(email=email).one_or_none()

    if (not user) or (user and user.password != password):
        raise AuthenticationFailed('Invalid email or password')

    return user


def login(email, password):
    validated_data = UserLoginSchema().load({
        'email': email,
        'password': password,
    })

    user = authenticate(
        validated_data.get('email'),
        validated_data.get('password'),
    )

    return {
        'access_token': create_access_token(user),
        'refresh_token': create_refresh_token(user),
    }


def refresh_token(user):
    return {
        'access_token': create_access_token(user),
    }
