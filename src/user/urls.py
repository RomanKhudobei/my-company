from flask import Blueprint
from flask_restful import Api

from user.resources import UserCreate, UserRetrieve

bp = Blueprint('user', __name__)
api = Api(bp)

api.add_resource(UserCreate, '/user/', endpoint='create')
api.add_resource(UserRetrieve, '/user/<int:user_id>/', endpoint='retrieve')
