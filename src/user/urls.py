from flask import Blueprint
from flask_restful import Api

from user.resources import UserCreate, UserRetrieve, UserUpdate, ChangePassword

bp = Blueprint('user', __name__)
api = Api(bp)

api.add_resource(UserCreate, '/users/', endpoint='create')
api.add_resource(UserRetrieve, '/users/<int:user_id>/', endpoint='retrieve')
api.add_resource(UserUpdate, '/users/<int:user_id>/', endpoint='update')
api.add_resource(ChangePassword, '/users/change-password/', endpoint='change_password')
