from app.db import db
from user.models import User
from user.schemas import UserCreateSchema, UserSchema


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


def update_user(user, updated_data):
    validated_data = UserSchema().load(updated_data)

    for field, value in validated_data.items():
        setattr(user, field, value)

    db.session.commit()
