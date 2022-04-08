from app.db import db
from user.models import User
from user.schemas import UserCreateSchema


def register_user(first_name, last_name, email, password, repeat_password):
    validated_user_data = UserCreateSchema().load({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'repeat_password': repeat_password,
    })
    validated_user_data.pop('repeat_password')

    user = User(**validated_user_data)
    db.session.add(user)

    db.session.commit()
    return user


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).one_or_none()
