from flask import Blueprint
from flask_restful import Api

from user.resources import UserCreate, UserRetrieve, UserUpdate, ChangePassword

bp = Blueprint('user', __name__)
api = Api(bp)

api.add_resource(UserCreate, '/users/', endpoint='create')
api.add_resource(UserRetrieve, '/users/me/', endpoint='retrieve')
api.add_resource(UserUpdate, '/users/me/', endpoint='update')
api.add_resource(ChangePassword, '/users/me/change-password/', endpoint='change_password')
