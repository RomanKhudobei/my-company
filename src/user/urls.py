from flask import Blueprint
from flask_restful import Api

from user.resources import UserCreate

bp = Blueprint('user', __name__)
api = Api(bp)

api.add_resource(UserCreate, '/user/', endpoint='create')
