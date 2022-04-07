from flask import request
from flask_restful import Resource

from user import services
from user.schemas import UserSchema


class UserCreate(Resource):

    def post(self):
        user = services.register_user(
            first_name=request.json.get('first_name'),
            last_name=request.json.get('last_name'),
            email=request.json.get('email'),
            password=request.json.get('password'),
            repeat_password=request.json.get('repeat_password'),
        )
        return UserSchema().dump(user), 201
