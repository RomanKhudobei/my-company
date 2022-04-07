from flask import request
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource

from auth import services


class Login(Resource):

    def post(self):
        auth_credentials = services.login(
            email=request.json.get('email'),
            password=request.json.get('password'),
        )

        return auth_credentials, 200


class RefreshToken(Resource):

    @jwt_required(refresh=True)
    def post(self):
        auth_credentials = services.refresh_token(current_user)
        return auth_credentials, 200
