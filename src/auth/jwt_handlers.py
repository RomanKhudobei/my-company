from user.models import User


def user_identity_lookup(user):
    return user.id


def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()
