from flask import Blueprint
from flask_restful import Api

from user.resources import UserCreate, UserRetrieve, UserUpdate, ChangePassword

bp = Blueprint('user', __name__)
api = Api(bp)

api.add_resource(UserCreate, '/user/', endpoint='create')
api.add_resource(UserRetrieve, '/user/<int:user_id>/', endpoint='retrieve')
api.add_resource(UserUpdate, '/user/<int:user_id>/', endpoint='update')
api.add_resource(ChangePassword, '/user/change-password/', endpoint='change_password')
