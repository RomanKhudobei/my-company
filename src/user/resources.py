from flask import request
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource, abort

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


class UserRetrieve(Resource):

    @jwt_required()
    def get(self, user_id):
        user = services.get_user_by_id(user_id)

        if not user:
            abort(404)

        requesting_self_information = (current_user.id == user.id)
        if not requesting_self_information:
            abort(403)

        response_data = {}

        if user:
            response_data = UserSchema().dump(user)

        return response_data, 200


class UserUpdate(Resource):

    @jwt_required()
    def put(self, user_id):
        user = services.get_user_by_id(user_id)

        if not user:
            abort(404)

        requesting_self_information = (current_user.id == user.id)
        if not requesting_self_information:
            abort(403)

        services.update_user(user, request.json)
        return UserSchema().dump(user), 200


class ChangePassword(Resource):

    @jwt_required()
    def post(self):
        services.change_password(
            current_user,
            old_password=request.json.get('old_password'),
            new_password=request.json.get('new_password'),
            repeat_password=request.json.get('repeat_password'),
        )
        return 200
